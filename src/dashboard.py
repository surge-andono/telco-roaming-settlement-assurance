import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def run_dashboard():
    print("📊 Step 4: Generating Unified Roaming Executive Dashboard...")
    
    # 1. Load Results
    try:
        df = pd.read_csv('data/results/master_reconciliation.csv')
        summary = pd.read_csv('data/results/leakage_summary_by_partner.csv')
    except FileNotFoundError:
        print("❌ Error: Reconciliation results not found. Run reconciler first.")
        return

    # --- KONTEN GRAFIK ---

    # A. Grafik Batang: Revenue vs Leakage per Partner
    fig_partner = px.bar(
        summary, 
        x='partner_name', 
        y=['estimated_revenue_idr', 'leakage_amount_idr'],
        title='Financial Impact: Revenue vs Leakage by Partner',
        labels={'value': 'Amount (IDR)', 'partner_name': 'Roaming Partner'},
        barmode='group',
        color_discrete_map={
            'estimated_revenue_idr': '#2ecc71', # Hijau untuk Revenue
            'leakage_amount_idr': '#e74c3c'    # Merah untuk Leakage
        },
        template='plotly_white'
    )

    # B. Grafik Pie: Distribusi Kebocoran per Layanan
    service_leak = df[df['status'] == 'LEAKAGE (Unbilled)'].groupby('service_group')['leakage_amount_idr'].sum().reset_index()
    fig_service = px.pie(
        service_leak, 
        values='leakage_amount_idr', 
        names='service_group',
        title='Leakage Source by Service Type',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # C. Grafik Garis: Tren Kebocoran Harian
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    trend = df.resample('D', on='timestamp')['leakage_amount_idr'].sum().reset_index()
    fig_trend = px.line(
        trend, 
        x='timestamp', 
        y='leakage_amount_idr',
        title='Daily Leakage Trend (Root Cause Analysis)',
        labels={'leakage_amount_idr': 'Potential Loss (IDR)'},
        line_shape='spline',
        markers=True
    )
    fig_trend.update_traces(line_color='#f39c12')

    # --- PENYUSUNAN LAYOUT DASHBOARD (SINGLE HTML) ---

    os.makedirs('data/output', exist_ok=True)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Roaming Assurance Executive Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; }}
            .container {{ max-width: 1200px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }}
            .header h1 {{ color: #2c3e50; margin: 0; }}
            .header p {{ color: #7f8c8d; }}
            .summary-cards {{ display: flex; justify-content: space-around; margin-bottom: 30px; }}
            .card {{ background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; width: 30%; border-left: 5px solid #3498db; }}
            .card h3 {{ margin: 0; color: #7f8c8d; font-size: 14px; }}
            .card p {{ font-size: 20px; font-weight: bold; color: #2c3e50; margin: 10px 0 0 0; }}
            .chart-row {{ display: flex; flex-wrap: wrap; gap: 20px; }}
            .chart-full {{ width: 100%; margin-bottom: 30px; }}
            .chart-half {{ width: calc(50% - 10px); background: #fff; border: 1px solid #eee; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌍 International Roaming Settlement Dashboard</h1>
                <p>Automated Reconciliation Audit: MSC Logs vs TAP3 Outbound</p>
            </div>

            <div class="summary-cards">
                <div class="card">
                    <h3>TOTAL POTENTIAL REVENUE</h3>
                    <p>Rp {df['estimated_revenue_idr'].sum():,.0f}</p>
                </div>
                <div class="card" style="border-left-color: #e74c3c;">
                    <h3>TOTAL LEAKAGE DETECTED</h3>
                    <p>Rp {df['leakage_amount_idr'].sum():,.0f}</p>
                </div>
                <div class="card" style="border-left-color: #27ae60;">
                    <h3>DATA INTEGRITY SCORE</h3>
                    <p>{(1 - (df['leakage_amount_idr'].sum() / df['estimated_revenue_idr'].sum()))*100:.2f}%</p>
                </div>
            </div>

            <div class="chart-full">
                {fig_partner.to_html(full_html=False, include_plotlyjs=False)}
            </div>

            <div class="chart-row">
                <div class="chart-half">
                    {fig_service.to_html(full_html=False, include_plotlyjs=False)}
                </div>
                <div class="chart-half">
                    {fig_trend.to_html(full_html=False, include_plotlyjs=False)}
                </div>
            </div>
            
            <p style="text-align: center; color: #bdc3c7; font-size: 12px; margin-top: 50px;">
                Generated by Roaming Assurance Pipeline &copy; 2025
            </p>
        </div>
    </body>
    </html>
    """

    with open('data/output/roaming_dashboard.html', 'w') as f:
        f.write(html_content)

    print(f"✅ Unified Dashboard generated at: data/output/roaming_dashboard.html")

if __name__ == "__main__":
    run_dashboard()
