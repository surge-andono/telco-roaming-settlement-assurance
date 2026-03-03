import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def run_dashboard():
    print("📊 Step 4: Generating Roaming Settlement Executive Dashboard...")
    
    # 1. Load Results
    try:
        df = pd.read_csv('data/results/master_reconciliation.csv')
        summary = pd.read_csv('data/results/leakage_summary_by_partner.csv')
    except FileNotFoundError:
        print("❌ Error: Reconciliation results not found. Run reconciler first.")
        return

    # 2. Create Visualization: Revenue vs Leakage by Partner
    fig_partner = px.bar(
        summary, 
        x='partner_name', 
        y=['estimated_revenue_idr', 'leakage_amount_idr'],
        title='Revenue vs Potential Leakage by Roaming Partner (IDR)',
        labels={'value': 'Amount (IDR)', 'partner_name': 'Partner'},
        barmode='group',
        color_discrete_map={
            'estimated_revenue_idr': '#3498db',
            'leakage_amount_idr': '#e74c3c'
        }
    )

    # 3. Create Visualization: Leakage by Service Type
    service_leak = df[df['status'] == 'LEAKAGE (Unbilled)'].groupby('service_group')['leakage_amount_idr'].sum().reset_index()
    fig_service = px.pie(
        service_leak, 
        values='leakage_amount_idr', 
        names='service_group',
        title='Leakage Distribution by Service Group',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    # 4. Create Visualization: Leakage Trend (Temporal Analysis)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    trend = df.resample('D', on='timestamp')['leakage_amount_idr'].sum().reset_index()
    fig_trend = px.line(
        trend, 
        x='timestamp', 
        y='leakage_amount_idr',
        title='Daily Revenue Leakage Trend',
        labels={'leakage_amount_idr': 'Leakage (IDR)'},
        line_shape='spline'
    )

    # 5. Build Final Dashboard Layout
    os.makedirs('data/output', exist_ok=True)
    
    # Simpan dashboard ke file HTML mandiri
    with open('data/output/roaming_dashboard.html', 'w') as f:
        f.write("<html><head><title>Roaming Assurance Dashboard</title>")
        f.write("<style>body { font-family: Arial, sans-serif; background-color: #f4f7f6; padding: 20px; }</style></head><body>")
        f.write("<h1 style='text-align: center; color: #2c3e50;'>🌍 Roaming Settlement & Leakage Dashboard</h1>")
        f.write("<p style='text-align: center;'>Status: Automated Reconciliation Usage vs Billing</p>")
        f.write(fig_partner.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write("<div style='display: flex;'>")
        f.write("<div style='width: 50%;'>" + fig_service.to_html(full_html=False, include_plotlyjs='cdn') + "</div>")
        f.write("<div style='width: 50%;'>" + fig_trend.to_html(full_html=False, include_plotlyjs='cdn') + "</div>")
        f.write("</div>")
        f.write("</body></html>")

    print(f"✅ Dashboard generated successfully at: data/output/roaming_dashboard.html")

if __name__ == "__main__":
    run_dashboard()