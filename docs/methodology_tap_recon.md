# Methodology: International Roaming Reconciliation
## Strategy: MSC Event Logs vs TAP3 Outbound

The methodology focuses on the **Mediation & Rating** stage of the roaming lifecycle, where raw network events are transformed into billable settlement records.



### 1. Data Source Definition
* **MSC/SGSN Logs (Source A)**: The "Ground Truth" captured at the switch level. It records the IMSI (International Mobile Subscriber Identity) and actual usage volume.
* **TAP3 Outbound (Source B)**: The industry-standard file format used to exchange billing information between Roaming Partners (VPMN and HPMN).

### 2. The SDR Financial Framework
International roaming is settled in **SDR (Special Drawing Rights)**. Our methodology includes a validation layer that:
* Standardizes usage into SDR units.
* Applies a simulated daily exchange rate to estimate the local currency (IDR) impact.
* Maps MCC-MNC codes to specific partner tax regimes (e.g., VAT in Europe vs. Tax-free zones).

### 3. Reconciliation Logic (Left-Join Audit)
We perform a high-precision join on the `event_id`. 
* **The Match**: Validates that the rated amount in the TAP file matches the expected amount based on the MSC volume.
* **The Gap**: Any MSC event without a corresponding TAP record is flagged as **Technical Leakage** (likely a failure in the Mediation/Encoding process).

### 4. Root Cause Analysis (RCA)
Data is segmented to identify if leaks are:
* **Partner-Specific**: Indicating a configuration error in the TAP delivery to a specific MCC-MNC.
* **Service-Specific**: Identifying if Data sessions (SGSN) are leaking more than Voice (MSC).