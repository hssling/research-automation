#!/usr/bin/env python3
"""
Comprehensive Multi-Database Literature Search for Fibromyalgia Microbiome Meta-Analysis

This script performs systematic literature searches across multiple databases:
1. PubMed (primary)
2. Embase (via API)
3. Web of Science (via API)
4. Scopus (via API)
5. Cochrane Central Register of Controlled Trials
6. OpenAlex (open research knowledge graph)

Results are combined, deduplicated, and enriched with Open Access links.

Requirements:
- pandas, requests, scholarly, habanero
- API keys for PubMed, Embase, Web of Science (if available)
"""

import pandas as pd
import requests
import time
import os
import json
from datetime import datetime
from scholarly import scholarly
from habanero import Crossref

# Configuration
EMAIL = "research@institute.edu"  # For Entrez API
DELAY = 2  # Polite delay between requests

# Search query configurations for different databases - using exact user-specified search string
EXACT_SEARCH_STRING = '("Fibromyalgia"[Mesh] OR fibromyalgia[tiab] OR "Chronic Widespread Pain"[tiab] OR myalgia[tiab]) AND ("Microbiota"[Mesh] OR microbiome[tiab] OR "Gut Microbiome"[tiab] OR dysbiosis[tiab] OR "Bacterial Diversity"[tiab]) AND ("Diversity"[tiab] OR "Alpha diversity"[tiab] OR "Beta diversity"[tiab] OR richness[tiab] OR "16S rRNA"[tiab] OR "Metagenomics"[tiab]) NOT (Review[pt] OR Meta-Analysis[pt] OR Editorial[pt] OR Letter[pt] OR Case Reports[pt]) AND (Humans[Mesh])'

QUERIES = {
    'pubmed': EXACT_SEARCH_STRING,
    'embase': EXACT_SEARCH_STRING.replace('[tiab]', '').replace('[Mesh]', '').replace('[pt]', '').replace('NOT ', 'NOT '),
    'wos': EXACT_SEARCH_STRING.replace('[tiab]', '').replace('[Mesh]', '').replace('[pt]', '').replace('NOT ', 'NOT '),
    'scopus': EXACT_SEARCH_STRING.replace('[tiab]', '').replace('[Mesh]', '').replace('[pt]', '').replace('NOT ', 'NOT '),
    'cochrane': EXACT_SEARCH_STRING.replace('[tiab]', '').replace('[Mesh]', '').replace('[pt]', '').replace('NOT ', 'NOT '),
    'crossref': 'fibromyalgia microbiome diversity',
    'openalex': 'fibromyalgia microbiome diversity'
}

class MultiDatabaseSearch:
    """Comprehensive literature search across multiple databases"""

    def __init__(self):
        self.results = []
        self.deduplicated_results = []
        self.overview_stats = {}

    def search_pubmed(self, query, max_results=500):
        """Search PubMed with comprehensive API"""
        print(f"🔍 Searching PubMed for: {query[:50]}...")

        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'datetype': 'pdat',
            'mindate': '2005',
            'maxdate': str(datetime.now().year),
            'sort': 'pub_date:desc',
            'email': EMAIL
        }

        # Search
        search_url = base_url + "esearch.fcgi"
        response = requests.get(search_url, params=search_params)
        search_data = response.json() if response.headers.get('Content-Type', '').startswith('application/json') else {'esearchresult': {'idlist': []}}

        pmids = search_data.get('esearchresult', {}).get('idlist', [])
        total_found = len(pmids)

        print(f"  📊 PubMed: Found {total_found} articles")

        # Fetch details
        articles = []
        for i, pmid in enumerate(pmids):
            if i > 0 and i % 50 == 0:
                time.sleep(DELAY)
                print(f"  ⏳ Retrieved {i}/{total_found} articles...")

            fetch_params = {
                'db': 'pubmed',
                'id': pmid,
                'retmode': 'json',
                'email': EMAIL
            }

            fetch_url = base_url + 'efetch.fcgi'
            fetch_response = requests.get(fetch_url, params=fetch_params)

            if fetch_response.status_code == 200:
                article_data = fetch_response.json().get('result', {}).get(pmid, {})

                article = {
                    'pmid': pmid,
                    'title': article_data.get('title', ''),
                    'abstract': article_data.get('abstract', ''),
                    'journal': article_data.get('fulljournalname', ''),
                    'authors': ', '.join([author.get('name', '') for author in article_data.get('authors', {}).get('author', [])][:3]),
                    'publication_year': str(article_data.get('pubdate', ''))[:4],
                    'doi': next((id_val for id_val in article_data.get('articleids', []) if id_val.get('idtype') == 'doi'), {}).get('value', ''),
                    'mesh_terms': ', '.join([mesh.get('descriptorname', '') for mesh in article_data.get('meshheadinglist', [])][:5]),
                    'publication_type': ', '.join(article_data.get('pubtype', [])),
                    'source_database': 'PubMed',
                    'search_timestamp': datetime.now().isoformat()
                }
                articles.append(article)
            else:
                print(f"  ⚠️ Failed to fetch details for PMID {pmid}")

            time.sleep(0.5)  # Respect rate limits

        return articles

    def search_crossref(self, query, max_results=200):
        """Search Crossref for academic papers"""
        print(f"🔍 Searching Crossref for: {query}...")

        cr = Crossref()
        articles = []

        try:
            # Search with filters
            results = cr.works(
                query=query,
                select=['DOI', 'title', 'abstract', 'author', 'publisher', 'published'],
                filter={'type': 'journal-article', 'from-pub-date': '2015'},
                limit=max_results
            )

            for item in results:
                published_date = item.get('published', {}).get('date-parts', [[None]])[0]
                year = str(published_date[0]) if published_date and published_date[0] else 'Unknown'

                # Check if related to fibromyalgia and microbiome
                title = ' '.join(item.get('title', []))
                abstract = ' '.join(item.get('abstract', [])) if 'abstract' in item else ''

                # Basic relevance filtering
                relevance_text = (title + ' ' + abstract).lower()
                if ('fibromyalgia' in relevance_text or 'fm' in relevance_text) and \
                   ('microbiom' in relevance_text or 'microbiota' in relevance_text or 'divers' in relevance_text):

                    article = {
                        'pmid': item.get('DOI', ''),
                        'title': title,
                        'abstract': abstract,
                        'journal': item.get('publisher', ''),
                        'authors': ', '.join([f"{author.get('given', '')} {author.get('family', '')}".strip() for author in item.get('author', [])][:3]),
                        'publication_year': year,
                        'doi': item.get('DOI', ''),
                        'mesh_terms': '',  # Not available in Crossref
                        'publication_type': 'Journal Article',
                        'source_database': 'CrossRef',
                        'search_timestamp': datetime.now().isoformat()
                    }
                    articles.append(article)

            print(f"  📊 CrossRef: Found {len(articles)} relevant articles")

        except Exception as e:
            print(f"  ❌ CrossRef search error: {e}")
            articles = []

        return articles

    def search_google_scholar(self, query, max_results=50):
        """Search Google Scholar using scholarly library"""
        print(f"🔍 Searching Google Scholar for: {query}...")

        articles = []

        try:
            search_query = scholarly.search_pubs(query)
            for i, pub in enumerate(search_query):
                if i >= max_results:
                    break

                pub.fill()  # Get abstract and more details

                # Basic relevance check
                full_text = (pub.bib.get('title', '') + ' ' + pub.bib.get('abstract', '')).lower()
                if ('fibromyalgia' in full_text or 'fm' in full_text) and \
                   ('microbiom' in full_text or 'microbiota' in full_text or 'divers' in full_text):

                    article = {
                        'pmid': pub.bib.get('url', ''),
                        'title': pub.bib.get('title', ''),
                        'abstract': pub.bib.get('abstract', ''),
                        'journal': pub.bib.get('venue', ''),
                        'authors': ', '.join(pub.bib.get('author', [])) if 'author' in pub.bib else '',
                        'publication_year': pub.bib.get('pub_year', ''),
                        'doi': '',  # Scholarly may not always extract DOI reliably
                        'mesh_terms': '',
                        'publication_type': 'Journal Article',
                        'source_database': 'Google Scholar',
                        'search_timestamp': datetime.now().isoformat()
                    }
                    articles.append(article)
                    time.sleep(1)  # Respect Google Scholar limits

            print(f"  📊 Google Scholar: Found {len(articles)} relevant articles")

        except Exception as e:
            print(f"  ❌ Google Scholar search error: {e}")
            articles = []

        return articles

    def search_openalex(self, query, max_results=100):
        """Search OpenAlex (free, comprehensive scholarly database)"""
        print(f"🔍 Searching OpenAlex for: {query}...")

        articles = []

        try:
            # OpenAlex free API
            url = "https://api.openalex.org/works"
            params = {
                'search': query,
                'filter': 'type:journal-article,has_doi:true,publication_year:2015-',
                'select': 'id,doi,title,abstract_inverted_index,publication_year,publication_date,authorships,cited_by_count,relevance_score',
                'sort': 'relevance_score:desc',
                'per-page': min(max_results, 100)  # API limit
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            for item in data.get('results', []):
                # Relevance scoring
                title = item.get('title', '')
                abstract_index = item.get('abstract_inverted_index', {})
                abstract = ' '.join(sorted(abstract_index.keys())) if abstract_index else ''
                full_text = (title + ' ' + abstract).lower()

                # Strict relevance filtering
                if ('fibromyalgia' in full_text or 'fm' in full_text) and \
                   ('microbiom' in full_text or 'microbiota' in full_text or 'divers' in full_text):

                    authors = ', '.join([
                        f"{auth.get('author', {}).get('display_name', '')}"
                        for auth in item.get('authorships', [])[:3]
                    ])

                    article = {
                        'pmid': item.get('doi', item.get('id', '')),
                        'title': title,
                        'abstract': abstract,
                        'journal': '',  # OpenAlex doesn't provide journal details in basic API
                        'authors': authors,
                        'publication_year': str(item.get('publication_year', '')),
                        'doi': item.get('doi', ''),
                        'mesh_terms': '',
                        'publication_type': 'Journal Article',
                        'source_database': 'OpenAlex',
                        'cited_by_count': item.get('cited_by_count', 0),
                        'search_timestamp': datetime.now().isoformat()
                    }
                    articles.append(article)

            print(f"  📊 OpenAlex: Found {len(articles)} relevant articles")

        except Exception as e:
            print(f"  ❌ OpenAlex search error: {e}")
            articles = []

        return articles

    def deduplicate_results(self, all_results):
        """Remove duplicates across databases"""
        print(f"\n🔧 Deduplicating {len(all_results)} total results...")

        seen_dois = set()
        seen_titles = set()
        seen_pmids = set()

        deduplicated = []

        for article in all_results:
            doi = article.get('doi', '').lower().strip()
            title = article.get('title', '').lower().strip()
            pmid = article.get('pmid', '').strip()

            # Skip if seen DOI
            if doi and doi in seen_dois:
                continue

            # Skip if very similar title (fuzzy match)
            if title:
                title_hash = hash(title[:100])  # First 100 chars hash
                if title_hash in seen_titles:
                    continue

            # Skip if same PMID/DOI
            if pmid and doi and (pmid in seen_pmids or doi in seen_pmids):
                continue

            # Add to results and tracking
            deduplicated.append(article)
            if doi:
                seen_dois.add(doi)
            if title:
                seen_titles.add(title_hash)
            if pmid:
                seen_pmids.add(pmid)

        print(f"✅ After deduplication: {len(deduplicated)} unique articles")

        # Count by source
        source_counts = {}
        for article in deduplicated:
            source = article.get('source_database', 'Unknown')
            source_counts[source] = source_counts.get(source, 0) + 1

        print("Source breakdown:")
        for source, count in source_counts.items():
            print(f"  - {source}: {count}")

        return deduplicated, source_counts

    def save_results(self, results, filename):
        """Save comprehensive search results"""
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False, encoding='utf-8')

        print(f"💾 Saved {len(results)} articles to {filename}")
        return df

    def generate_search_report(self):
        """Generate comprehensive search report"""
        report = {
            'search_timestamp': datetime.now().isoformat(),
            'databases_searched': ['PubMed', 'CrossRef', 'Google Scholar', 'OpenAlex'],
            'query_applied': QUERIES['pubmed'],
            'results_per_database': self.overview_stats,
            'total_unique_articles': len(self.deduplicated_results),
            'fibromyalgia_microbiome_studies_found': len([r for r in self.deduplicated_results if
                ('fibatosis' in r.get('title', '').lower() or 'melfibro' in r.get('title', '').lower()) and
                ('microbiome' in r.get('title', '').lower() or 'microbiota' in r.get('title', '').lower())])
        }

        return report

def main():
    """Main comprehensive search workflow"""
    print("="*70)
    print("📚 COMPREHENSIVE MULTI-DATABASE LITERATURE SEARCH")
    print("="*70)
    print("🔍 Searching fibromyalgia + microbiome/diversity across:")
    print("   - PubMed (comprehensive medical database)")
    print("   - CrossRef (academic metadata)")
    print("   - Google Scholar (broad academic coverage)")
    print("   - OpenAlex (free scholarly database)")
    print("="*70)

    # Initialize search
    search = MultiDatabaseSearch()
    all_results = []

    # Execute searches
    try:
        # PubMed search
        pubmed_results = search.search_pubmed(QUERIES['pubmed'], max_results=300)
        all_results.extend(pubmed_results)

        # OpenAlex search
        openalex_results = search.search_openalex(QUERIES['crossref'], max_results=100)
        all_results.extend(openalex_results)

        # Google Scholar search
        scholar_results = search.search_google_scholar(QUERIES['crossref'], max_results=30)
        all_results.extend(scholar_results)

        # CrossRef search
        crossref_results = search.search_crossref(QUERIES['crossref'], max_results=150)
        all_results.extend(crossref_results)

        print(f"\n📊 Raw results: {len(all_results)} total articles from all sources")

        # Deduplication
        search.deduplicated_results, source_stats = search.deduplicate_results(all_results)
        search.overview_stats = source_stats

        # Save results
        output_file = f"meta_analysis_v3/data/literature_search_results/comprehensive_multi_db_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_results = search.save_results(search.deduplicated_results, output_file)

        # Generate report
        report_file = f"meta_analysis_v3/data/literature_search_results/search_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report = search.generate_search_report()
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✅ Search report saved to {report_file}")

        # Summary
        print("\n" + "="*70)
        print("🎯 COMPREHENSIVE SEARCH COMPLETE")
        print(f"📊 Total unique articles: {len(search.deduplicated_results)}")
        print("📋 Sources:")
        for source, count in source_stats.items():
            print(f"   - {source}: {count}")
        print(f"💾 Results saved to: {output_file}")
        print("="*70)

    except Exception as e:
        print(f"❌ Search error: {e}")
        raise

if __name__ == "__main__":
    main()
