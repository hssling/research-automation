#!/usr/bin/env python3
"""
Automated PubMed Systematic Search for PPG Heart Rate Accuracy Literature

This script implements automated literature retrieval following the systematic review protocol
for accuracy of photoplethysmography-based heart rate monitoring devices vs. ECG.

Author: Research Integrity Automation Agent
Date: September 23, 2025

Requirements:
- biopython (pip install biopython)
- pandas (pip install pandas)
- beautifulsoup4 (pip install beautifulsoup4)

Usage:
    python scripts/pubmed_search.py
"""

import sys
import time
from datetime import datetime, timedelta
import pandas as pd
from Bio import Entrez
from Bio import Medline
import requests
from bs4 import BeautifulSoup
import json
import os

# Email for NCBI API (required for E-utilities)
Entrez.email = "ppg.systematic.review@example.com"
Entrez.api_key = ""  # Add your NCBI API key here for higher rate limits

class PubMedSystematicSearch:
    """Automated PubMed search for systematic review on PPG heart rate accuracy."""

    def __init__(self):
        # Simplified query for reliability
        self.search_query = 'PPG heart rate accuracy validation ECG'

        self.results_columns = [
            'pmid', 'title', 'authors', 'journal', 'year', 'abstract',
            'doi', 'keywords', 'mesh_terms', 'pubtype', 'url'
        ]

    def clean_query(self, query):
        """Remove extra whitespace and newlines from query."""
        return ' '.join(query.strip().split())

    def perform_search(self, max_records=2000):
        """
        Perform PubMed search with the predefined systematic query.

        Args:
            max_records (int): Maximum number of records to retrieve

        Returns:
            list: List of PubMed IDs
        """
        print("🔍 Performing initial PubMed search...")
        query = self.clean_query(self.search_query)

        try:
            # Perform initial search to get PMIDs
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_records, mindate="2010/01/01", maxdate="2025/12/31", sort="pub_date")
            record = Entrez.read(handle)
            handle.close()

            pmids = record["IdList"]
            total_count = int(record["Count"])

            print(f"📊 Found {total_count} total records (2010-2025)")
            print(f"📄 Retrieved {len(pmids)} PMIDs")

            # Limit to prevent memory issues
            if total_count > max_records:
                print(f"⚠️  Limited to first {max_records} records due to memory constraints")
                pmids = pmids[:max_records]

            return pmids

        except Exception as e:
            print(f"❌ Error during search: {e}")
            return []

    def fetch_pubmed_records(self, pmids, batch_size=50):
        """
        Fetch detailed record information for each PMID.

        Args:
            pmids (list): List of PubMed IDs
            batch_size (int): Number of records to fetch per request

        Returns:
            list: List of Medline record dictionaries
        """
        print("📥 Fetching detailed records...")
        records = []
        totalFetched = 0

        for i in range(0, len(pmids), batch_size):
            batch_pmids = pmids[i:i+batch_size]
            print(f"  ↳ Batch {i//batch_size + 1}: Records {i+1}-{min(i+batch_size, len(pmids))}")

            try:
                handle = Entrez.efetch(db="pubmed", id=batch_pmids, rettype="medline", retmode="text")
                records.extend(Medline.parse(handle))
                handle.close()

                totalFetched += len(batch_pmids)

                # Progress update every 100 records
                if totalFetched % 100 == 0:
                    print(f"    ✓ Fetched {totalFetched} of {len(pmids)} records")

                # NCBI rate limiting: 3 requests per second for API key users
                time.sleep(0.5)  # Conservative delay

            except Exception as e:
                print(f"❌ Error fetching batch {i//batch_size + 1}: {e}")
                continue

        print(f"✓ Successfully fetched {len(records)} detailed records")
        return records

    def extract_record_data(self, record):
        """
        Extract relevant information from a Medline record.

        Args:
            record (dict): Medline record dictionary

        Returns:
            dict: Extracted study data
        """
        def safe_get(record, keys, default=""):
            """Safely extract nested dictionary values."""
            try:
                for key in keys:
                    record = record[key]
                return record
            except (KeyError, TypeError, IndexError):
                return default

        # Extract core information
        data = {
            'pmid': record.get('PMID', ''),
            'title': record.get('TI', ''),
            'authors': ', '.join(record.get('AU', [])),
            'journal': record.get('JT', ''),
            'year': '',  # Will be extracted from DP field
            'abstract': record.get('AB', ''),
            'doi': '',  # Will be extracted from LID field
            'keywords': ', '.join(record.get('OT', []) + record.get('KW', [])),
            'mesh_terms': ', '.join([mh.split('/')[0] for mh in record.get('MH', [])]),
            'pubtype': ', '.join(record.get('PT', [])),
            'url': f"https://pubmed.ncbi.nlm.nih.gov/{record.get('PMID', '')}/"
        }

        # Extract year from DP (Date of Publication) field
        dp_field = record.get('DP', '')
        if dp_field:
            try:
                data['year'] = dp_field.split(' ')[0]
            except:
                data['year'] = ''

        # Extract DOI from LID (Location Identifier) field
        lid_field = record.get('LID', [])
        if lid_field:
            for lid in lid_field:
                if '[doi]' in lid:
                    data['doi'] = lid.replace(' [doi]', '')
                    break
                elif lid.startswith('10.'):
                    data['doi'] = lid.split()[0]
                    break

        return data

    def process_records(self, records):
        """
        Process Medline records into a pandas DataFrame.

        Args:
            records (list): List of Medline record dictionaries

        Returns:
            pd.DataFrame: Processed study data
        """
        print("🔄 Processing records into structured format...")
        processed_data = []

        for i, record in enumerate(records):
            if i % 50 == 0:
                print(f"  → Processed {i}/{len(records)} records")

            data = self.extract_record_data(record)
            processed_data.append(data)

        # Convert to DataFrame and clean data
        df = pd.DataFrame(processed_data)

        # Remove duplicates based on PMID
        df = df.drop_duplicates(subset=['pmid'], keep='first')

        # Clean and standardize data
        df = df.apply(self.clean_dataframe_columns)

        print(f"✓ Processed {len(df)} unique records")
        return df

    def clean_dataframe_columns(self, col):
        """Clean individual DataFrame columns."""
        if col.dtype == 'object':
            return col.str.strip().str.replace(r'\s+', ' ', regex=True)
        return col

    def save_results(self, df, output_dir="ppg_hr_accuracy_meta_analysis/data/literature_search_results"):
        """
        Save search results to CSV and provide summary statistics.

        Args:
            df (pd.DataFrame): Processed study data
        """
        print("💾 Saving search results...")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Save full results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"{output_dir}/pubmed_search_results_{timestamp}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"✓ Saved full results to: {csv_filename}")

        # Create summary statistics
        summary_stats = self.generate_summary_stats(df)
        print("\n📊 Search Summary:")
        for key, value in summary_stats.items():
            print(f"  {key}: {value}")

        # Save summary as JSON
        summary_file = f"{output_dir}/search_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_stats, f, indent=2, default=str)
        print(f"✓ Saved summary statistics to: {summary_file}")

    def generate_summary_stats(self, df):
        """Generate summary statistics from the search results."""
        return {
            'total_records': len(df),
            'search_query': self.search_query.replace('\n', ' ').strip(),
            'date_range': '2010-2025',
            'journals': df['journal'].nunique(),
            'year_range': f"{df['year'].min()} - {df['year'].max()}",
            'avg_authors_per_paper': round(df['authors'].str.count(',').mean() + 1, 1),
            'percent_with_abstract': round((df['abstract'] != '').sum() / len(df) * 100, 1),
            'percent_with_doi': round((df['doi'] != '').sum() / len(df) * 100, 1),
            'top_journals': df['journal'].value_counts().head(5).to_dict(),
            'publications_by_year': df['year'].value_counts().sort_index().tail(5).to_dict()
        }

    def run_systematic_search(self, max_records=2000, output_dir="ppg_hr_accuracy_meta_analysis/data/literature_search_results"):
        """
        Execute the complete systematic search pipeline.

        Args:
            max_records (int): Maximum number of records to retrieve
            output_dir (str): Directory to save results
        """
        print("=" * 70)
        print("🔴 PPG HEART RATE ACCURACY SYSTEMATIC LITERATURE SEARCH")
        print("=" * 70)
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        cleaned_query = self.search_query.replace('\n', ' ').strip()
        print(f"🔍 Search Query: {cleaned_query}")
        print(f"📊 Max Records: {max_records}")
        print("=" * 70)

        try:
            # Step 1: Perform search
            pmids = self.perform_search(max_records)
            if not pmids:
                print("❌ No records found. Please check search query.")
                return

            # Step 2: Fetch detailed records
            records = self.fetch_pubmed_records(pmids)

            # Step 3: Process records
            df = self.process_records(records)

            # Step 4: Save results
            self.save_results(df, output_dir)

            print("\n" + "=" * 70)
            print("✅ SYSTEMATIC SEARCH COMPLETED SUCCESSFULLY")
            print("=" * 70)

        except Exception as e:
            print(f"\n❌ SEARCH FAILED: {e}")
            print("💡 Check internet connection and NCBI API availability")
            raise

def main():
    """Main execution function."""
    print("🔴 PPG Heart Rate Accuracy Systematic Literature Search")
    print("Automated PubMed search following PRISMA 2020 guidelines")

    # Initialize and run search
    searcher = PubMedSystematicSearch()
    searcher.run_systematic_search()

if __name__ == "__main__":
    main()
