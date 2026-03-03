# Roaming Business Logic & Industry Standards
## Understanding the Mechanics of International Settlement

This document explains the underlying business rules and telecommunication standards implemented in this project's logic.

---

## 1. The GSMA TAP3 Standard
International roaming is governed by the **GSMA (Global System for Mobile Communications Association)**. The primary protocol used for billing between operators is **TAP3 (Transferred Account Procedure version 3)**.

* **Logic in Project**: Our `traffic_generator.py` and `tap_encoder.py` (simulated) follow the TAP3 requirement where raw MSC logs must be converted into formatted records containing IMSI, MCC-MNC, and UTC Time Offsets before being sent to the partner.

---

## 2. SDR (Special Drawing Rights) Pricing
Unlike domestic retail billing, international roaming prices are not set in local currencies (IDR, USD, etc.). They are set in **SDR**, a basket of currencies maintained by the IMF.

* **The Problem**: SDR rates are stable, but local currency exchange rates (IDR) fluctuate daily.
* **The Logic**: Our `validator.py` applies a triple-conversion logic: `Usage Unit` -> `SDR Rate` -> `USD` -> `IDR`. This allows the Finance team to see the actual revenue impact in the company's reporting currency.


## 3. Inbound vs. Outbound Roaming
This project specifically focuses on **Inbound Roaming Assurance**:
* **Definition**: Foreign subscribers (e.g., a Singtel user) using the XL Axiata network in Indonesia.
* **Revenue Flow**: XL Axiata provides the service -> Generates TAP files -> Sends to Singtel -> Singtel pays XL Axiata.
* **Risk**: If we fail to generate a TAP file for a Singtel user, XL Axiata provides the service for "free" (Revenue Leakage).

---

## 4. Taxes and Regulatory Compliance
Every country has different tax treatments for wholesale roaming services:
* **Inter-Operator Tariff (IOT)**: The base price agreed between two operators.
* **VAT/GST**: Some regions (like Europe/EU) require Value Added Tax to be explicitly calculated in the TAP file, while others (like Hong Kong) are tax-free zones.
* **Logic in Project**: Our `validator.py` uses a `tax_map` based on MCC-MNC codes to ensure the `total_invoice_idr` reflects these regional tax differences.

---

## 5. The Role of the Clearinghouse
In a real-world scenario, operators don't send files directly to 500+ global partners. They use a **Data Clearinghouse (DCH)** like Syniverse or Comfone.

* **Project Context**: Our reconciliation engine acts as the "Pre-DCH Audit." It ensures that before we send data to the Clearinghouse, we have already verified that 100% of the network usage has been captured. This prevents disputes and "rejected files" later in the settlement cycle.



---