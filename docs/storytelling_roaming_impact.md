# Data Storytelling: Roaming Settlement Insights
## Bridging the Gap Between Network Usage and Global Revenue

This narrative explains how to interpret the Roaming Assurance Dashboard to drive financial recovery.

### 1. The "Invisible" Loss: Integrity Score
The dashboard reveals the percentage of roaming traffic that successfully bypassed the mediation layer to become a TAP file. A **95% Integrity Score** in roaming is more dangerous than in domestic retail because of the high unit cost of roaming services.

### 2. High-Value Target: Roaming Partner Analysis
**Insight**: "Our analysis shows that while traffic from **Singtel (Singapore)** is high, the leakage rate is minimal. However, traffic from **Vodafone (Netherlands)** shows a 10% leakage."
**Action**: This suggests a mismatch in the TAP3 version compatibility or a tax-rounding error specific to European VAT configurations. We prioritize fixing the Vodafone pipeline to recover high-value Euro-pegged revenue.

### 3. The SDR-to-IDR Exposure
**Insight**: By visualizing potential loss in IDR, we translate technical "missing records" into "lost cash flow."
**Story**: Because Roaming is settled in SDR, a leak that happens during a period of IDR depreciation is doubly painful. This dashboard helps the Treasury department understand the "Currency Risk" associated with unbilled roaming traffic.

### 4. Hourly Trends & Batch Failures
**Insight**: We notice spikes in leakage during specific UTC windows. 
**Story**: In the Roaming world, files are often sent in batches. A spike in the trend line usually indicates a **Clearinghouse Timeout**—where our system tried to send TAP files, but the international gate was closed for maintenance.

### Conclusion
This project moves the Roaming Team from "Calculating Bills" to "Protecting Margins." It ensures that XL Axiata (or any simulated carrier) doesn't just provide a world-class network for tourists, but also gets paid for every bit of it.