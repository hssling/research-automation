#!/usr/bin/env python3
"""
India Antibiotic Consumption Dashboard Launcher
==========================================

This script launches the Streamlit dashboard for the antibiotic consumption
meta-analysis project.

Usage:
    python run_dashboard.py
    or
    streamlit run dashboard/dashboard.py

Requirements:
    pip install -r dashboard/requirements.txt

Author: Dr. Siddalingaiah H. S.
Created: October 2025
"""

import subprocess
import sys
import os
import platform

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'pandas', 'plotly']

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n📦 Install with:")
        print("   pip install -r dashboard/requirements.txt")
        return False

    return True

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.py")

    if not os.path.exists(dashboard_path):
        print(f"❌ Dashboard file not found: {dashboard_path}")
        return False

    try:
        print("🚀 Launching India Antibiotic Consumption Dashboard...")
        print("📊 Opening in web browser...")

        if platform.system() == "Windows":
            # Windows
            cmd = [sys.executable, "-m", "streamlit", "run", dashboard_path]
        else:
            # Unix/Linux/Mac
            cmd = ["streamlit", "run", dashboard_path]

        print(f"💻 Running command: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=os.path.dirname(dashboard_path))

        return True

    except KeyboardInterrupt:
        print("\n⏹️  Dashboard stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("💊 INDIA ANTIBIOTIC CONSUMPTION DASHBOARD")
    print("   WHO ATC/DDD Meta-Analysis Dashboard")
    print("=" * 60)

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Launch dashboard
    if not launch_dashboard():
        sys.exit(1)

    print("\n👋 Dashboard closed. Thanks for using the India Antibiotic Consumption Dashboard!")

if __name__ == "__main__":
    main()
