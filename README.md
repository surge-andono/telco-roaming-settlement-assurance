# Roaming Settlement Assurance: Revenue Leakage Detection
## (Reconciliation MSC Logs vs TAP3 Files)
### 🌍 International Roaming Financial Integrity Pipeline (Standard GSMA Simulation)

## 📌 Overview
This repository contains an end-to-end automated audit pipeline designed for **International Roaming Revenue Assurance**. In the telco industry, roaming involves complex data exchanges between global operators. Any failure in converting network usage (MSC Logs) into settlement files (TAP3) results in "unbilled" revenue that is difficult to recover.

This project simulates the reconciliation of inbound roaming traffic—where foreign subscribers use the local network—ensuring every byte and second is correctly billed to the partner operator in **SDR (Special Drawing Rights)** and **IDR**.

## 🚀 Technical Highlights
* **Domain Expertise**: Implements GSMA-standard logic for TAP (Transferred Account Procedure) validation.
* **Multi-Currency Engine**: Automated conversion between SDR, USD, and IDR.
* **Leakage RCA**: Identifies unbilled roaming sessions by partner, country (MCC-MNC), and service type.
* **Automated Pipeline**: Modular Python scripts covering Generation -> Validation -> Reconciliation -> Visualization.

## 💼 Business Impact
* **Foreign Exchange Protection**: Ensures billing accuracy amid fluctuating SDR-to-IDR exchange rates.
* **Settlement Acceleration**: Identifies missing TAP files within 24 hours, reducing the weighted average days to collect.
* **Partner Compliance**: Provides data-driven evidence for dispute management with international roaming partners.

## 🛠️ Usage
1. Install requirements: `pip install -r requirements.txt`
2. Run the pipeline: `python src/main.py`
3. View the results: `data/output/roaming_dashboard.html` or screenshot : `data/output/Roaming_Assurance_Dashboard.pdf`
