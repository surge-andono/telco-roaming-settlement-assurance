import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.traffic_generator import run_traffic_generator
from src.validator import run_validator
from src.reconciler import run_reconciler
from src.dashboard import run_dashboard

def main():
    print("🔔 Starting International Roaming Settlement Assurance Pipeline...")
    print("-" * 60)
    
    run_traffic_generator()
    run_validator()
    run_reconciler()
    run_dashboard()
    
    print("-" * 60)
    print("🏁 Pipeline Completed. All results are in 'data/' folder.")

if __name__ == "__main__":
    main()
