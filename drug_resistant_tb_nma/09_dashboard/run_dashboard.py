#!/usr/bin/env python3
"""
Helper script to run the Streamlit dashboard from the correct directory
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Run the dashboard from the correct directory"""

    # Get the current working directory
    current_dir = Path.cwd()

    # Check if we're in the drug_resistant_tb_nma directory
    if current_dir.name == 'drug_resistant_tb_nma':
        print("✅ Running dashboard from correct directory")
        dashboard_path = current_dir / '09_dashboard' / 'dashboard.py'
    else:
        # Try to find the drug_resistant_tb_nma directory
        potential_path = current_dir / 'drug_resistant_tb_nma' / '09_dashboard' / 'dashboard.py'

        if potential_path.exists():
            print(f"✅ Found dashboard at: {potential_path}")
            dashboard_path = potential_path
        else:
            print("❌ Error: Cannot find the dashboard file")
            print("Please ensure you are running this script from the drug_resistant_tb_nma directory")
            print("or from a parent directory that contains the drug_resistant_tb_nma folder")
            return False

    # Check if required files exist
    required_files = [
        dashboard_path.parent.parent / '02_data_extraction' / 'extracted_data.csv',
        dashboard_path.parent.parent / '04_results' / 'treatment_effects_summary.csv',
        dashboard_path.parent.parent / '04_results' / 'component_effects_summary.csv'
    ]

    missing_files = []
    for file_path in required_files:
        if not file_path.exists():
            missing_files.append(file_path.name)

    if missing_files:
        print(f"❌ Missing required data files: {', '.join(missing_files)}")
        print("Please ensure all CSV files are present in the correct directories")
        return False

    # Run the dashboard
    print(f"🚀 Starting Streamlit dashboard...")
    print(f"📂 Dashboard file: {dashboard_path}")
    print(f"🌐 The dashboard will open in your web browser")
    print(f"🔄 Press Ctrl+C to stop the dashboard")

    try:
        # Run streamlit
        result = subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', str(dashboard_path)
        ], cwd=dashboard_path.parent.parent)

        return result.returncode == 0

    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
