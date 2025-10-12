#!/usr/bin/env python3
"""
Simple PubMed search for fibromyalgia microbiome studies
Uses NCBI Entrez API to get real literature search results
"""

import xml.etree.ElementTree as ET
import requests
import pandas as pd
from datetime import datetime

def search_pubmed(query, max_results=50):
    """Search PubMed using Entrez API"""
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

    # Search for PMIDs
    search_url = f'{base_url}esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&sort=relevance&retmode=json'
    search_response = requests.get(search_url)

    if search_response.status_code != 200:
        print(f"Error: API request failed with status {search_response.status_code}")
        return []

    search_data = search_response.json()

    pmids = search_data.get('esearchresult', {}).get('idlist', [])
    print(f'Found {len(pmids)} studies for query: {query}')

    if pmids:
        # Fetch details for PMIDs
        pmids_str = ','.join(pmids)
        fetch_url = f'{base_url}efetch.fcgi?db=pubmed&id={pmids_str}&retmode=xml'
        fetch_response = requests.get(fetch_url)

        if fetch_response.status_code != 200:
            print(f"Error: Fetch request failed with status {fetch_response.status_code}")
            return []

        # Parse XML and extract basic info
        results = []
        try:
            root = ET.fromstring(fetch_response.text)

            for article in root.findall('.//PubmedArticle'):
                title = article.findtext('.//ArticleTitle', '')
                authors = []
                for author in article.findall('.//Author'):
                    lastname = author.findtext('.//LastName', '')
                    firstname = author.findtext('.//ForeName', '')
                    if lastname or firstname:
                        authors.append(f'{firstname} {lastname}'.strip())

                year = article.findtext('.//PubDate/Year', '')
                journal = article.findtext('.//Journal/Title', '')
                # Fix DOI extraction - find ArticleId with type doi
                doi_elem = article.find('.//ArticleId[@IdType="doi"]')
                doi = doi_elem.text if doi_elem is not None else ''

                results.append({
                    'pmid': article.findtext('.//PMID', ''),
                    'title': title,
                    'authors': '; '.join(authors),
                    'year': year,
                    'journal': journal,
                    'doi': doi,
                    'query': query,
                    'search_date': datetime.now().isoformat()
                })
        except ET.ParseError as e:
            print(f"XML parsing error: {e}")
            return []

        return results
    return []

def main():
    """Main search execution"""
    print("🔬 Searching PubMed for fibromyalgia microbiome studies...")
    print("=" * 70)

    # Search for fibromyalgia microbiome studies
    query = 'fibromyalgia[TIAB] AND (microbiome[TIAB] OR microbiota[TIAB])'
    results = search_pubmed(query, 20)

    if results:
        df = pd.DataFrame(results)
        df.to_csv('fibromyalgia_real_search_results.csv', index=False)
        print(f"\n✅ Successfully saved {len(results)} real PubMed search results!")
        print("📋 File saved: fibromyalgia_real_search_results.csv")

        print("\n📄 Sample Results:")
        print("-" * 50)
        for i, row in df.head(5).iterrows():
            title_short = row.title[:80] + "..." if len(row.title) > 80 else row.title
            print(f"{i+1}. {row.pmid} ({row.year})")
            print(f"   {title_short}")
            print(f"   Authors: {row.authors[:50]}..." if len(str(row.authors)) > 50 else f"   Authors: {row.authors}")
            print(f"   Journal: {row.journal}")
            print()

        print("📊 SUMMARY:")
        print(f"   Total studies found: {len(results)}")
        print(f"   Search query: {query}")
        print(f"   Generated CSV file: fibromyalgia_real_search_results.csv")

        return results
    else:
        print("❌ No results found - check internet connection and API")
        return []

if __name__ == "__main__":
    main()
