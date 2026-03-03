import pandas as pd
import numpy as np
import os

def run_reconciler():
    print("🔍 Step 3: Performing Roaming Reconciliation (MSC vs TAP3)...")
    
    # 1. Load Validated Data
    try:
        df_msc = pd.read_csv('data/processed/msc_validated.csv')
        df_tap = pd.read_csv('data/processed/tap_validated.csv')
    except FileNotFoundError:
        print("❌ Error: Validated data not found. Run validator first.")
        return

    # 2. Master Join (Left Join to find unbilled events)
    # Kita bandingkan data Network (MSC) sebagai master dengan data Billing (TAP)
    recon_df = pd.merge(
        df_msc, 
        df_tap[['event_id', 'tap_file_id', 'billed_revenue_idr', 'total_invoice_idr']], 
        on='event_id', 
        how='left'
    )

    # 3. Leakage Identification Logic
    # Jika billed_revenue_idr kosong (NaN), berarti trafik ada tapi tidak ditagihkan
    recon_df['status'] = np.where(
        recon_df['billed_revenue_idr'].isna(), 
        'LEAKAGE (Unbilled)', 
        'BILLED'
    )

    # 4. Calculate Revenue Leakage (The Financial Impact)
    recon_df['leakage_amount_idr'] = np.where(
        recon_df['status'] == 'LEAKAGE (Unbilled)',
        recon_df['estimated_revenue_idr'],
        0
    )

    # 5. Detail Analysis: Leakage by Partner & Service
    summary_partner = recon_df.groupby('partner_name').agg({
        'event_id': 'count',
        'estimated_revenue_idr': 'sum',
        'leakage_amount_idr': 'sum'
    }).reset_index()
    
    summary_partner['leakage_percentage'] = (summary_partner['leakage_amount_idr'] / summary_partner['estimated_revenue_idr']) * 100

    # 6. Save Results
    os.makedirs('data/results', exist_ok=True)
    recon_df.to_csv('data/results/master_reconciliation.csv', index=False)
    summary_partner.to_csv('data/results/leakage_summary_by_partner.csv', index=False)

    total_leakage = recon_df['leakage_amount_idr'].sum()
    leakage_count = len(recon_df[recon_df['status'] == 'LEAKAGE (Unbilled)'])
    
    print(f"✅ Reconciliation Complete.")
    print(f"💰 Total Potential Loss Detected: Rp {total_leakage:,.2f}")
    print(f"📊 Total Unbilled Events: {leakage_count} records")

if __name__ == "__main__":
    run_reconciler()