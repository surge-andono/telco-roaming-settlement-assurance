import pandas as pd
import numpy as np
import os

def run_validator():
    print("💱 Step 2: Validating Roaming Rates & Currency Conversion (SDR to IDR)...")
    
    # 1. Load Data
    try:
        df_msc = pd.read_csv('data/raw/msc_event_logs.csv')
        df_tap = pd.read_csv('data/tap_files/tap3_outbound_records.csv')
    except FileNotFoundError:
        print("❌ Error: Raw data files not found. Run traffic_generator first.")
        return

    # 2. Simulasi Kurs Mata Uang (Reference Rates)
    # Dalam realita, ini bisa diambil dari API IMF atau Bank Sentral
    # 1 SDR biasanya berkisar di angka 1.3 - 1.4 USD
    SDR_TO_USD = 1.34
    USD_TO_IDR = 15850  # Kurs simulasi 2026
    SDR_TO_IDR = SDR_TO_USD * USD_TO_IDR

    print(f"ℹ️ Current Exchange Rate: 1 SDR = Rp {SDR_TO_IDR:,.2f}")

    # 3. Data Cleaning & Normalization
    # Pastikan format IMSI dan Event ID bersih
    df_msc['event_id'] = df_msc['event_id'].astype(str)
    df_tap['event_id'] = df_tap['event_id'].astype(str)

    # 4. Currency Conversion (Kalkulasi Nilai Rupiah)
    # Kita hitung nilai IDR untuk data MSC (Ground Truth) dan data TAP (Billed)
    df_msc['estimated_revenue_idr'] = df_msc['usage_volume'] * df_msc['sdr_rate'] * SDR_TO_IDR
    df_tap['billed_revenue_idr'] = df_tap['charge_sdr'] * SDR_TO_IDR

    # 5. International Tax Calculation
    # Aturan pajak roaming berbeda tiap negara (simulasi tax_rate dari traffic_generator)
    # Kita asumsikan partner memiliki tax_rate yang tersimpan di database
    tax_map = {
        '502-12': 0.06,   # Malaysia
        '525-01': 0.07,   # Singapore
        '454-00': 0.0,    # Hong Kong (Tax Free)
        '204-04': 0.21,   # Netherlands (VAT)
        '310-410': 0.10   # USA
    }

    df_tap['tax_amount_idr'] = df_tap.apply(
        lambda x: x['billed_revenue_idr'] * tax_map.get(x['partner_mcc_mnc'], 0.1), axis=1
    )
    df_tap['total_invoice_idr'] = df_tap['billed_revenue_idr'] + df_tap['tax_amount_idr']

    # 6. Save Validated Data
    os.makedirs('data/processed', exist_ok=True)
    df_msc.to_csv('data/processed/msc_validated.csv', index=False)
    df_tap.to_csv('data/processed/tap_validated.csv', index=False)

    print(f"✅ Validation Complete. IDR Conversion applied to {len(df_tap)} TAP records.")

if __name__ == "__main__":
    run_validator()