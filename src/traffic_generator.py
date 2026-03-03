import pandas as pd
import numpy as np
import os
import uuid
from datetime import datetime, timedelta

def run_traffic_generator():
    print("🚀 Step 1: Generating International Roaming Traffic (MSC/SGSN Logs)...")
    
    # 1. Setup Folder
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/tap_files', exist_ok=True)
    
    np.random.seed(42)
    total_records = 3000
    
    # 2. Daftar Operator Partner (Roaming Partners)
    # Format: MCC-MNC | Partner Name | Region | Tax Rate
    partners = [
        ('502-12', 'Maxis', 'Malaysia', 0.06),
        ('525-01', 'Singtel', 'Singapore', 0.07),
        ('454-00', 'CSL', 'Hong Kong', 0.0),
        ('204-04', 'Vodafone', 'Netherlands', 0.21),
        ('310-410', 'AT&T', 'USA', 0.10)
    ]
    
    # 3. Generate MSC/SGSN Event Logs (The "Ground Truth" Usage)
    # Data mentah yang tercatat di switch saat turis menggunakan jaringan telco
    msc_logs = []
    start_date = datetime(2025, 1, 1, 0, 0, 0)
    
    for i in range(total_records):
        partner = partners[np.random.randint(0, len(partners))]
        event_id = str(uuid.uuid4())
        timestamp = start_date + timedelta(
            days=np.random.randint(0, 30),
            hours=np.random.randint(0, 23),
            minutes=np.random.randint(0, 59)
        )
        
        service_type = np.random.choice(['Voice', 'Data', 'SMS'], p=[0.3, 0.6, 0.1])
        
        # Volume Calculation
        if service_type == 'Voice':
            volume = np.random.randint(1, 600) # seconds
            uom = 'SEC'
        elif service_type == 'Data':
            volume = np.random.uniform(0.1, 500.0) # MB
            uom = 'MB'
        else:
            volume = 1
            uom = 'MSG'
            
        msc_logs.append({
            'event_id': event_id,
            'imsi': f"51011{np.random.randint(100000, 999999)}", # IMSI Pelanggan Luar
            'partner_mcc_mnc': partner[0],
            'partner_name': partner[1],
            'timestamp': timestamp,
            'service_group': service_type,
            'usage_volume': volume,
            'uom': uom,
            'sdr_rate': 0.15 if service_type == 'Voice' else 0.05, # Kurs SDR per unit
            'switch_id': f"MSC-JKT-{np.random.randint(1, 5)}"
        })
    
    df_msc = pd.DataFrame(msc_logs)
    
    # 4. Generate TAP3 Files Outbound (The "Billed" records)
    # Disimulasikan ada kebocoran 5% data yang gagal ter-encode menjadi TAP3
    # (Misal karena error saat proses pembungkusan file/Mediation)
    
    # Ambil 95% data secara acak untuk disimulasikan sukses jadi file TAP
    df_tap = df_msc.sample(frac=0.95).copy()
    
    # Tambahkan atribut spesifik TAP File
    df_tap['tap_file_id'] = 'TAP3_ID_' + df_tap['timestamp'].dt.strftime('%Y%m%d') + '_' + df_tap['partner_mcc_mnc'].str.replace('-', '')
    df_tap['utc_offset'] = '+0700'
    
    # Kalkulasi Gross Amount dalam SDR (Special Drawing Rights)
    df_tap['charge_sdr'] = df_tap['usage_volume'] * df_tap['sdr_rate']
    
    # 5. Simpan ke CSV
    msc_path = 'data/raw/msc_event_logs.csv'
    tap_path = 'data/tap_files/tap3_outbound_records.csv'
    
    df_msc.to_csv(msc_path, index=False)
    df_tap.to_csv(tap_path, index=False)
    
    print(f"✅ MSC Event Logs generated: {len(df_msc)} records")
    print(f"✅ TAP3 Outbound Records generated: {len(df_tap)} records")
    print(f"⚠️ Simulated Leakage: {len(df_msc) - len(df_tap)} records missing from TAP files.")

if __name__ == "__main__":
    run_traffic_generator()