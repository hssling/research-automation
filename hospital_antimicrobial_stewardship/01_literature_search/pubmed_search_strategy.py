#!/usr/bin/env python3
"""
PubMed Literature Search for Hospital Antimicrobial Stewardship
Network Meta-Analysis

This script conducts a comprehensive literature search on PubMed for studies
related to hospital antimicrobial stewardship interventions.

Author: Research Team
Date: October 13, 2025
"""

import requests
import json
import time
from datetime import datetime
import pandas as pd
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

class PubMedSearcher:
    """Class to handle PubMed literature searches for antimicrobial stewardship studies."""

    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.email = "research@hospital-stewardship.org"  # Replace with actual email

    def _search_pubmed(self, query: str, max_results: int = 1000) -> List[str]:
        """
        Search PubMed and return list of PMIDs.

        Args:
            query: PubMed search query
            max_results: Maximum number of results to retrieve

        Returns:
            List of PMIDs
        """
        search_url = f"{self.base_url}esearch.fcgi"

        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': min(max_results, 10000),  # PubMed limit is 10,000
            'retmode': 'xml',
            'email': self.email
        }

        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.content)
            pmid_list = []

            for pmid in root.findall('.//Id'):
                pmid_list.append(pmid.text)

            return pmid_list

        except requests.exceptions.RequestException as e:
            print(f"Error searching PubMed: {e}")
            return []

    def _fetch_article_details(self, pmids: List[str]) -> List[Dict]:
        """
        Fetch detailed information for articles given PMIDs.

        Args:
            pmids: List of PubMed IDs

        Returns:
            List of article dictionaries
        """
        if not pmids:
            return []

        fetch_url = f"{self.base_url}efetch.fcgi"

        # Process in batches to avoid overwhelming the API
        batch_size = 100
        all_articles = []

        for i in range(0, len(pmids), batch_size):
            batch_pmids = pmids[i:i + batch_size]
            pmid_string = ','.join(batch_pmids)

            params = {
                'db': 'pubmed',
                'id': pmid_string,
                'retmode': 'xml',
                'email': self.email
            }

            try:
                response = requests.get(fetch_url, params=params)
                response.raise_for_status()

                # Parse article details
                articles = self._parse_article_xml(response.content)
                all_articles.extend(articles)

                # Be respectful to the API
                time.sleep(0.5)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching articles: {e}")
                continue

        return all_articles

    def _parse_article_xml(self, xml_content: bytes) -> List[Dict]:
        """Parse PubMed XML response for article details."""
        articles = []

        try:
            root = ET.fromstring(xml_content)

            for article in root.findall('.//PubmedArticle'):
                article_data = {}

                # Extract PMID
                pmid_elem = article.find('.//PMID')
                article_data['pmid'] = pmid_elem.text if pmid_elem is not None else ''

                # Extract title
                title_elem = article.find('.//ArticleTitle')
                article_data['title'] = title_elem.text if title_elem is not None else ''

                # Extract abstract
                abstract_elem = article.find('.//AbstractText')
                article_data['abstract'] = abstract_elem.text if abstract_elem is not None else ''

                # Extract journal
                journal_elem = article.find('.//Journal/Title')
                article_data['journal'] = journal_elem.text if journal_elem is not None else ''

                # Extract year
                year_elem = article.find('.//PubDate/Year')
                article_data['year'] = year_elem.text if year_elem is not None else ''

                # Extract authors
                authors = []
                for author in article.findall('.//Author'):
                    last_name = author.find('LastName')
                    first_name = author.find('ForeName')
                    if last_name is not None:
                        authors.append(f"{first_name.text if first_name is not None else ''} {last_name.text}".strip())
                article_data['authors'] = '; '.join(authors)

                # Extract MeSH terms for relevance filtering
                mesh_terms = []
                for mesh in article.findall('.//MeshHeading/DescriptorName'):
                    mesh_terms.append(mesh.text if mesh is not None else '')
                article_data['mesh_terms'] = mesh_terms

                # Extract keywords
                keywords = []
                for keyword in article.findall('.//Keyword'):
                    keywords.append(keyword.text if keyword is not None else '')
                article_data['keywords'] = keywords

                articles.append(article_data)

        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")

        return articles

    def search_stewardship_studies(self, max_results: int = 1000) -> pd.DataFrame:
        """
        Conduct comprehensive search for antimicrobial stewardship studies.

        Args:
            max_results: Maximum number of results to retrieve

        Returns:
            DataFrame with search results
        """

        # Primary search strategy based on protocol
        search_queries = [
            # Main stewardship interventions search
            '("antimicrobial stewardship" OR "antibiotic stewardship") AND (hospital OR "acute care" OR inpatient OR ICU) AND (RCT OR "randomized controlled trial" OR "cluster randomized" OR "interrupted time series" OR "controlled before-after")',

            # Specific interventions
            '("preauthorization" OR "prior authorization" OR "pre-approval") AND (antibiotic OR antimicrobial) AND (hospital OR inpatient) AND (RCT OR randomized OR trial)',

            '("prospective audit" OR "audit and feedback") AND (antibiotic OR antimicrobial) AND (hospital OR inpatient) AND (RCT OR randomized OR trial)',

            '("rapid diagnostic" OR "rapid testing" OR MALDI-TOF OR PCR) AND (antibiotic OR antimicrobial) AND stewardship AND (hospital OR inpatient)',

            '(CDSS OR "computerized decision support" OR "e-prescribing" OR "electronic prescribing") AND (antibiotic OR antimicrobial) AND (hospital OR inpatient)',

            # Outcomes focused search
            '(antibiotic OR antimicrobial) AND stewardship AND (mortality OR "CDI" OR "Clostridium difficile" OR "MDRO" OR "multidrug resistant" OR "antibiotic consumption" OR DOT OR DDD) AND (hospital OR inpatient) AND (RCT OR randomized OR trial)',

            # Setting-specific searches
            'antimicrobial stewardship AND ICU AND (RCT OR randomized OR trial)',
            'antimicrobial stewardship AND ward AND (RCT OR randomized OR trial)'
        ]

        all_pmids = set()
        all_articles = []

        print(f"Starting literature search across {len(search_queries)} search strategies...")

        for i, query in enumerate(search_queries, 1):
            print(f"Search {i}/{len(search_queries)}: {query[:80]}...")

            # Search for PMIDs
            pmids = self._search_pubmed(query, max_results=500)

            # Remove duplicates
            new_pmids = [pmid for pmid in pmids if pmid not in all_pmids]
            all_pmids.update(new_pmids)

            print(f"  Found {len(new_pmids)} new articles (total: {len(all_pmids)})")

            if new_pmids:
                # Fetch article details
                articles = self._fetch_article_details(new_pmids)
                all_articles.extend(articles)

                print(f"  Retrieved details for {len(articles)} articles")

        # Convert to DataFrame
        df = pd.DataFrame(all_articles)

        # Remove duplicates based on PMID
        if not df.empty:
            df = df.drop_duplicates(subset=['pmid'], keep='first')

        print(f"\nSearch completed. Total unique articles: {len(df)}")

        return df

    def filter_relevant_studies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter studies based on relevance criteria.

        Args:
            df: DataFrame with all search results

        Returns:
            Filtered DataFrame with relevant studies
        """

        if df.empty:
            return df

        # Define relevance keywords
        relevance_keywords = [
            'stewardship', 'antimicrobial', 'antibiotic', 'resistance',
            'mortality', 'CDI', 'clostridium difficile', 'MDRO',
            'multidrug resistant', 'consumption', 'DOT', 'DDD',
            'pre-authorization', 'prior authorization', 'audit and feedback',
            'prospective audit', 'rapid diagnostic', 'CDSS', 'e-prescribing'
        ]

        # Filter based on title and abstract content
        def is_relevant(text):
            if pd.isna(text):
                return False
            text_lower = text.lower()
            return any(keyword in text_lower for keyword in relevance_keywords)

        # Apply relevance filter
        relevant_mask = (
            df['title'].apply(is_relevant) |
            df['abstract'].apply(is_relevant) |
            df['keywords'].apply(lambda x: any(keyword in str(x).lower() for keyword in relevance_keywords))
        )

        filtered_df = df[relevant_mask].copy()
        filtered_df['relevance_score'] = filtered_df.apply(
            lambda row: sum(1 for keyword in relevance_keywords if keyword in str(row['title']).lower() or keyword in str(row['abstract']).lower()),
            axis=1
        )

        # Sort by relevance score
        filtered_df = filtered_df.sort_values('relevance_score', ascending=False)

        print(f"Filtered to {len(filtered_df)} relevant studies")

        return filtered_df

def main():
    """Main function to run the literature search."""

    print("Hospital Antimicrobial Stewardship Literature Search")
    print("=" * 55)

    # Initialize searcher
    searcher = PubMedSearcher()

    # Conduct search
    print("Conducting comprehensive literature search...")
    results_df = searcher.search_stewardship_studies(max_results=1000)

    if results_df.empty:
        print("No articles found. Please check search strategy.")
        return

    # Filter for relevance
    print("\nFiltering for relevance...")
    relevant_df = searcher.filter_relevant_studies(results_df)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save all results
    all_results_file = f"hospital_antimicrobial_stewardship/01_literature_search/pubmed_search_results_{timestamp}.csv"
    results_df.to_csv(all_results_file, index=False)
    print(f"\nAll search results saved to: {all_results_file}")

    # Save relevant results
    relevant_results_file = f"hospital_antimicrobial_stewardship/01_literature_search/pubmed_relevant_studies_{timestamp}.csv"
    relevant_df.to_csv(relevant_results_file, index=False)
    print(f"Relevant studies saved to: {relevant_results_file}")

    # Generate summary report
    summary_file = f"hospital_antimicrobial_stewardship/01_literature_search/search_summary_{timestamp}.txt"

    with open(summary_file, 'w') as f:
        f.write("Hospital Antimicrobial Stewardship Literature Search Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Search conducted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total articles found: {len(results_df)}\n")
        f.write(f"Relevant articles: {len(relevant_df)}\n")
        f.write(f"Relevance rate: {len(relevant_df)/len(results_df)*100:.1f}%\n\n")

        f.write("Top 10 most relevant studies:\n")
        f.write("-" * 30 + "\n")

        for i, (_, row) in enumerate(relevant_df.head(10).iterrows(), 1):
            f.write(f"{i}. {row.get('title', 'No title')[:100]}...")
            if row.get('year'):
                f.write(f" ({row['year']})")
            f.write(f" [PMID: {row.get('pmid', 'Unknown')}]\n")

    print(f"Summary report saved to: {summary_file}")

    print("\nSearch completed successfully!")
    print(f"Found {len(relevant_df)} potentially relevant studies for full-text review.")

if __name__ == "__main__":
    main()
