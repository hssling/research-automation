#!/usr/bin/env python3
"""
Automated Literature Search for Antimicrobial Stewardship Mortality Studies
Part of the Living Review System for ongoing evidence monitoring
"""

import requests
from scholarly import scholarly
import pandas as pd
import time
from datetime import datetime, timedelta
import json
import os
import logging
from typing import List, Dict, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('living_review.log'),
        logging.StreamHandler()
    ]
)

class ASPEvidenceMonitor:
    """Automated monitoring system for new ASP mortality evidence"""

    def __init__(self, data_dir: str = "../02_data_extraction"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Search parameters
        self.search_terms = [
            "antimicrobial stewardship mortality",
            "antibiotic stewardship hospital mortality",
            "ASP interventions mortality outcomes",
            "stewardship programs death rates",
            "antimicrobial stewardship clinical outcomes"
        ]

        self.exclusion_terms = [
            "outpatient", "community", "ambulatory", "veterinary",
            "dental", "animal", "plant", "environmental"
        ]

    def search_pubmed_api(self, days_back: int = 7) -> List[Dict]:
        """Search PubMed for new ASP mortality studies"""
        try:
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)

            start_str = start_date.strftime("%Y/%m/%d")
            end_str = end_date.strftime("%Y/%m/%d")

            results = []

            for term in self.search_terms:
                # Construct search query
                query = f'({term}) AND (mortality OR death OR outcome*)'
                query += f' AND ("{start_str}"[Date - Publication] : "{end_str}"[Date - Publication])'
                query += ' AND (randomized controlled trial[Publication Type] OR controlled clinical trial[Publication Type] OR clinical trial[Publication Type])'

                # First, get IDs
                search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmode=json&retmax=50"
                search_response = requests.get(search_url, timeout=30)
                search_data = search_response.json()

                if 'esearchresult' not in search_data or 'idlist' not in search_data['esearchresult']:
                    continue

                pmids = search_data['esearchresult']['idlist']

                if not pmids:
                    continue

                # Get article details
                id_string = ",".join(pmids[:10])  # Limit to prevent API overload
                fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={id_string}&retmode=xml"
                fetch_response = requests.get(fetch_url, timeout=30)

                # Parse XML response (simplified - would need proper XML parsing in production)
                if fetch_response.status_code == 200:
                    for pmid in pmids[:10]:
                        results.append({
                            'pmid': pmid,
                            'title': 'Retrieved from automated search',
                            'abstract': 'Abstract pending full review',
                            'authors': 'Authors pending full review',
                            'journal': 'Journal pending full review',
                            'year': end_date.year,
                            'search_term': term,
                            'found_date': end_date.isoformat(),
                            'status': 'pending_review'
                        })

                time.sleep(1)  # Respect API limits

            return results

        except Exception as e:
            logging.error(f"PubMed search error: {str(e)}")
            return []

    def search_google_scholar(self, days_back: int = 7) -> List[Dict]:
        """Search Google Scholar for new ASP mortality studies"""
        try:
            results = []

            for term in self.search_terms:
                search_query = f"{term} mortality randomized controlled trial"

                try:
                    search_results = scholarly.search_pubs(search_query, year_low=2023)

                    for i, result in enumerate(search_results):
                        if i >= 5:  # Limit results per search
                            break

                        # Check if publication is recent
                        pub_year = getattr(result, 'bib', {}).get('year', 0)
                        if pub_year and pub_year >= 2023:

                            scholar_result = {
                                'title': getattr(result, 'bib', {}).get('title', ''),
                                'authors': getattr(result, 'bib', {}).get('author', []),
                                'abstract': getattr(result, 'bib', {}).get('abstract', ''),
                                'journal': getattr(result, 'bib', {}).get('journal', ''),
                                'year': pub_year,
                                'citations': getattr(result, 'citedby', 0),
                                'search_term': term,
                                'found_date': datetime.now().isoformat(),
                                'status': 'pending_review',
                                'source': 'google_scholar'
                            }

                            # Skip if contains exclusion terms
                            title_lower = scholar_result['title'].lower()
                            if not any(term.lower() in title_lower for term in self.exclusion_terms):
                                results.append(scholar_result)
                                logging.info(f"Found Google Scholar result: {scholar_result['title'][:50]}...")

                except Exception as e:
                    logging.warning(f"Google Scholar search error for term '{term}': {str(e)}")
                    continue

                time.sleep(2)  # Respect Google Scholar limits

            return results

        except Exception as e:
            logging.error(f"Google Scholar search error: {str(e)}")
            return []

    def check_duplicates(self, new_results: List[Dict]) -> List[Dict]:
        """Remove duplicates from search results and existing database"""

        try:
            # Load existing data
            existing_file = self.data_dir / "batch_2_extraction_results.csv"
            if existing_file.exists():
                existing_df = pd.read_csv(existing_file)
                existing_pmids = set(existing_df['pmid'].dropna().astype(str))
            else:
                existing_pmids = set()

            # Filter out duplicates
            unique_results = []
            for result in new_results:
                pmid = str(result.get('pmid', result.get('title', '')))
                if pmid not in existing_pmids:
                    result['duplicate_check'] = 'new'
                    unique_results.append(result)
                    existing_pmids.add(pmid)
                else:
                    result['duplicate_check'] = 'duplicate'
                    logging.info(f"Duplicate found: {result.get('title', '')[:50]}...")

            return unique_results

        except Exception as e:
            logging.error(f"Duplicate checking error: {str(e)}")
            return new_results

    def save_new_studies(self, studies: List[Dict]) -> str:
        """Save new studies to pending review file"""

        try:
            if not studies:
                logging.info("No new studies found")
                return "No new studies found"

            # Convert to DataFrame
            new_studies_df = pd.DataFrame(studies)

            # Add metadata
            new_studies_df['discovered_at'] = datetime.now().isoformat()
            new_studies_df['batch'] = 'automated_search'
            new_studies_df['review_status'] = 'pending'

            # Save to file
            output_file = self.data_dir / "automated_search_pending.csv"
            new_studies_df.to_csv(output_file, index=False)

            # Also append to existing summary
            summary_file = self.data_dir / "automated_search_summary.md"

            with open(summary_file, 'w') as f:
                f.write("# Automated Literature Search Summary\n\n")
                f.write(f"**Search Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"**New Studies Found:** {len(studies)}\n\n")

                if len(studies) > 0:
                    f.write("## New Studies Requiring Review\n\n")
                    for i, study in enumerate(studies, 1):
                        f.write(f"### {i}. {study.get('title', 'No title')}\n")
                        f.write(f"- **Source:** {study.get('source', 'Unknown')}\n")
                        f.write(f"- **Year:** {study.get('year', 'Unknown')}\n")
                        f.write(f"- **Search Term:** {study.get('search_term', 'N/A')}\n\n")

                f.write("## Action Required\n\n")
                f.write("1. Review each new study for eligibility\n")
                f.write("2. Extract data if eligible\n")
                f.write("3. Update meta-analysis\n")
                f.write("4. Update manuscript and dashboard\n\n")

            logging.info(f"Successfully saved {len(studies)} new studies for review")
            return f"Found {len(studies)} new studies requiring review. See automated_search_summary.md"

        except Exception as e:
            logging.error(f"Error saving studies: {str(e)}")
            return f"Error saving studies: {str(e)}"

    def run_search(self, days_back: int = 7) -> str:
        """Main search function combining multiple sources"""

        logging.info(f"Starting automated literature search for past {days_back} days")

        all_results = []

        # Search PubMed
        logging.info("Searching PubMed...")
        pubmed_results = self.search_pubmed_api(days_back)
        all_results.extend(pubmed_results)
        logging.info(f"Found {len(pubmed_results)} studies from PubMed")

        # Search Google Scholar
        logging.info("Searching Google Scholar...")
        scholar_results = self.search_google_scholar(days_back)
        all_results.extend(scholar_results)
        logging.info(f"Found {len(scholar_results)} studies from Google Scholar")

        # Remove duplicates
        logging.info("Checking for duplicates...")
        unique_results = self.check_duplicates(all_results)

        # Save results
        summary = self.save_new_studies(unique_results)

        logging.info(f"Search completed. {summary}")
        return summary

def main():
    """Command line interface"""

    import argparse

    parser = argparse.ArgumentParser(description="Automated Literature Search for ASP Mortality Evidence")
    parser.add_argument("--days", type=int, default=7, help="Days to search back (default: 7)")
    parser.add_argument("--data-dir", type=str, default="../02_data_extraction",
                       help="Data directory path")

    args = parser.parse_args()

    # Initialize monitor
    monitor = ASPEvidenceMonitor(args.data_dir)

    # Run search
    result = monitor.run_search(args.days)

    print(f"\n{result}")
    print("\nNext steps:")
    print("1. Review automated_search_pending.csv")
    print("2. Extract data from eligible studies")
    print("3. Update meta-analysis with new data")
    print("4. Update manuscript and dashboard")

if __name__ == "__main__":
    main()
