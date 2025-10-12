#!/usr/bin/env python3
"""
FAERS Data Fetcher
Download latest FAERS ASCII datasets from FDA website
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

def download_faers_data(year_quarter="2024q1"):
    """
    Download and extract FAERS data for specified year/quarter from FDA

    Args:
        year_quarter (str): Year and quarter (e.g., "2024q1")

    Returns:
        str: Path to extracted data directory
    """
    setup_logging()
    output_dir = "raw_faers"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # FAERS ASCII data URL
    url = f"https://fis.fda.gov/content/Exports/faers_ascii_{year_quarter}.zip"

    try:
        print(f"📥 Downloading FAERS data for {year_quarter}...")
        logging.info(f"Starting download from: {url}")

        # Download the zip file
        r = requests.get(url)
        r.raise_for_status()

        logging.info(f"Download completed: {len(r.content)} bytes")

        # Extract the zip file
        print("📦 Extracting FAERS data...")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(output_dir)

        # List extracted files
        extracted_files = z.namelist()
        print(f"✅ Extracted {len(extracted_files)} files to {output_dir}")

        # Log key files
        key_files = [f for f in extracted_files if any(k in f.upper() for k in ['DRUG', 'REAC', 'DEMO', 'OUTC', 'THER'])]
        logging.info(f"Key FAERS files extracted: {key_files}")

        print(f"💾 FAERS data ready for processing in {output_dir}")
        return output_dir

    except requests.RequestException as e:
        error_msg = f"❌ Failed to download FAERS data: {e}"
        print(error_msg)
        logging.error(error_msg)
        raise
    except zipfile.BadZipFile as e:
        error_msg = f"❌ Failed to extract FAERS data: {e}"
        print(error_msg)
        logging.error(error_msg)
        raise

def main():
    """Main function"""
    print("🚀 FAERS Data Fetcher")
    print("====================")

    # Download latest quarterly data
    year_quarter = "2024q1"  # Latest available

    try:
        download_faers_data(year_quarter)
        print("✅ FAERS data download completed successfully")

    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()
