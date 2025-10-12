#!/usr/bin/env python3
"""
FAERS Data Fetcher
Automatically download and extract FAERS database files from FDA
"""

import requests
import zipfile
import io
import os
from datetime import datetime
import logging

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        filename='../results/pharmacovigilance/fetch_faers.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def download_faers_data(year_quarter="2024q1", output_dir="raw_faers"):
    """
    Download and extract FAERS data for specified year/quarter

    Args:
        year_quarter (str): Year and quarter (e.g., "2024q1")
        output_dir (str): Output directory for extracted files
    """
    setup_logging()

    # FAERS ASCII data URL (quarterly updates)
    url = f"https://fis.fda.gov/content/Exports/faers_ascii_{year_quarter}.zip"

    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        print(f"📥 Downloading FAERS data: {year_quarter}")
        logging.info(f"Starting download from: {url}")

        # Download the zip file
        r = requests.get(url)
        r.raise_for_status()

        logging.info(f"Download completed: {len(r.content)} bytes")

        # Extract the zip file
        print("📦 Extracting FAERS data...")
        z = zipfile.ZipFile(io.BytesIO(r.content))

        # Extract all files
        z.extractall(output_dir)

        # List extracted files
        extracted_files = z.namelist()
        print(f"✅ Extracted {len(extracted_files)} files to {output_dir}")

        # Log key files
        key_files = [f for f in extracted_files if any(k in f.upper() for k in ['DRUG', 'REAC', 'DEMO', 'OUTC', 'THER'])]
        logging.info(f"Key FAERS files extracted: {key_files}")

        return extracted_files

    except requests.RequestException as e:
        error_msg = f"Failed to download FAERS data: {e}"
        print(f"❌ {error_msg}")
        logging.error(error_msg)
        raise
    except zipfile.BadZipFile as e:
        error_msg = f"Failed to extract FAERS data: {e}"
        print(f"❌ {error_msg}")
        logging.error(error_msg)
        raise

def main():
    """Main function"""
    print("🚀 FAERS Data Fetcher")
    print("=====================")

    # You can modify year_quarter for different quarters
    year_quarter = "2024q1"  # Latest available quarter
    output_dir = "raw_faers"

    try:
        files = download_faers_data(year_quarter, output_dir)

        # Summary
        print("\n📊 Summary:")
        print(f"   FAERS Quarter: {year_quarter}")
        print(f"   Output Directory: {output_dir}")
        print(f"   Files Downloaded: {len(files)}")
        print("   ✅ FAERS data download completed successfully")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()
