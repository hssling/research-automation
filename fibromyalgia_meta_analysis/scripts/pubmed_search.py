#!/usr/bin/env python3
"""
Automated Literature Search for Fibromyalgia Microbiome Meta-Analysis

This script uses the research-automation-core multi-database search module
to perform systematic literature searches across PubMed and other databases
for fibromyalgia and microbiome studies.

Author: Research Automation System
Date: September 24, 2025

Usage:
    python pubmed_search.py [search_terms] [output_file]

Outputs:
    - literature_search_results.csv: Raw search results
    - search_report.json: Search metadata and statistics
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
import argparse

# Add the research-automation-core to Python path
sys.path.append('../../research-automation-core')

from multi_database_search import MultiDatabaseSearch, LiteratureSearchQuery


def main():
    """Main execution for literature search."""

    print("=" * 70)
    print("🔬 FIBROMYELGIA MICROBIOME LITERATURE SEARCH")
    print("=" * 70)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Literature search for fibromyalgia microbiome studies')
    parser.add_argument('--query', default='(fibromyalgia OR fibromyalgia syndrome) AND (microbiome OR microbiota OR microbiome)',
                       help='Search query')
    parser.add_argument('--databases', nargs='+', default=['pubmed'],
                       help='Databases to search')
    parser.add_argument('--max-results', type=int, default=1000,
                       help='Maximum results per database')
    parser.add_argument('--email', default='research@example.com',
                       help='Email for PubMed API')
    parser.add_argument('--output', help='Output CSV file path')
    args = parser.parse_args()

    # Set up output path
    output_path = args.output or f"../data/literature_search_results/{datetime.now().strftime('%Y%m%d_%H%M%S')}_fibromyalgia_microbiome_search.csv"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        print(f"🔍 Search Query: {args.query}")
        print(f"📚 Databases: {', '.join(args.databases)}")
        print(f"📊 Max Results: {args.max_results}")
        print("-" * 70)

        # Create search query object
        search_query = LiteratureSearchQuery(
            query=args.query,
            databases=args.databases,
            date_from="2010/01/01",  # Start from 2010 for recent literature
            max_results=args.max_results,
            language='en'
        )

        # Initialize search engine
        search_engine = MultiDatabaseSearch(
            email=args.email,
            pubmed_api_key=os.environ.get('PUBMED_API_KEY')  # Optional API key
        )

        # Execute search
        print("🔄 Executing search...")
        results_df = search_engine.search(search_query, parallel=False)  # Sequential for now

        if results_df.empty:
            print("❌ No results found!")
            return 1

        # Add search metadata
        results_df['search_query'] = args.query
        results_df['search_date'] = datetime.now().isoformat()
        results_df['database_searched'] = '; '.join(args.databases)

        # Save results
        results_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"✅ Results saved: {output_path}")
        print(f"📋 Total studies found: {len(results_df)}")

        # Generate search report
        report = search_engine.generate_search_report(search_query, results_df)

        report_path = output_path.replace('.csv', '_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"📄 Search report saved: {report_path}")

        print("\n" + "=" * 70)
        print("✅ LITERATURE SEARCH COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print(f"📊 Results: {len(results_df)} studies")
        print(f"💾 CSV File: {output_path}")
        print(f"📋 Report: {report_path}")
        print("🔧 Next: Deduplication stage")

    except Exception as e:
        print(f"\n❌ SEARCH FAILED: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
