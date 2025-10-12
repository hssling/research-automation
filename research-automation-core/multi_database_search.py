"""
Multi-Database Literature Search Integration
Automated search across PubMed, Cochrane, Embase, and other databases
"""

import requests
import pandas as pd
import time
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import re
from pathlib import Path
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse
import xml.etree.ElementTree as ET

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Configuration for different literature databases"""

    DATABASES = {
        'pubmed': {
            'name': 'PubMed',
            'base_url': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils',
            'search_endpoint': 'esearch.fcgi',
            'fetch_endpoint': 'efetch.fcgi',
            'max_results': 10000,
            'batch_size': 1000,
            'rate_limit': 3,  # requests per second
        },
        'cochrane': {
            'name': 'Cochrane Central Register of Controlled Trials',
            'base_url': 'https://www.cochranelibrary.com',
            'search_endpoint': 'advanced-search',
            'requires_api_key': False,
            'max_results': 1000,
            'rate_limit': 2,
        },
        'embase': {
            'name': 'Embase',
            'base_url': 'https://embase.com',
            'requires_subscription': True,
            'rate_limit': 1,
        },
        'web_of_science': {
            'name': 'Web of Science',
            'base_url': 'https://clarivate.com/webofscience',
            'requires_subscription': True,
            'rate_limit': 1,
        },
        'scopus': {
            'name': 'Scopus',
            'base_url': 'https://www.scopus.com',
            'requires_subscription': True,
            'rate_limit': 2,
        }
    }

    @classmethod
    def get_database_config(cls, database_name: str) -> Dict[str, Any]:
        """Get configuration for a specific database"""
        return cls.DATABASES.get(database_name.lower(), {})


class LiteratureSearchQuery:
    """Represents a search query across multiple databases"""

    def __init__(self, query: str, databases: List[str] = None,
                 date_from: str = None, date_to: str = None,
                 max_results: int = 1000, language: str = 'en'):
        self.query = query
        self.databases = databases or ['pubmed']
        self.date_from = date_from
        self.date_to = date_to or datetime.now().strftime('%Y/%m/%d')
        self.max_results = max_results
        self.language = language
        self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert query to dictionary"""
        return {
            'query': self.query,
            'databases': self.databases,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'max_results': self.max_results,
            'language': self.language,
            'created_at': self.created_at.isoformat()
        }

    def get_pubmed_query(self) -> str:
        """Convert to PubMed query format"""
        query_parts = []

        # Add main query
        query_parts.append(f"({self.query})")

        # Add language filter
        if self.language == 'en':
            query_parts.append('"english"[Language]')

        # Add date filter
        if self.date_from:
            date_from_iso = self.date_from.replace('/', '').replace('-', '')
            date_to_iso = self.date_to.replace('/', '').replace('-', '')
            query_parts.append(f"({date_from_iso}:{date_to_iso}[Date - Publication])")

        return ' AND '.join(query_parts)

    def get_cochrane_query(self) -> str:
        """Convert to Cochrane query format"""
        # Cochrane uses a different syntax
        return self.query

    def validate_query(self) -> List[str]:
        """Validate the search query"""
        errors = []

        if not self.query or len(self.query.strip()) < 3:
            errors.append("Query must be at least 3 characters long")

        for db in self.databases:
            if db.lower() not in DatabaseConfig.DATABASES:
                errors.append(f"Unsupported database: {db}")

        if self.date_from and self.date_to:
            try:
                from_date = datetime.strptime(self.date_from.replace('/', '-'), '%Y-%m-%d')
                to_date = datetime.strptime(self.date_to.replace('/', '-'), '%Y-%m-%d')
                if from_date > to_date:
                    errors.append("From date cannot be after to date")
            except ValueError:
                errors.append("Invalid date format. Use YYYY/MM/DD")

        return errors


class PubMedSearch:
    """PubMed search implementation"""

    def __init__(self, email: str = "research@example.com", api_key: str = None):
        self.email = email
        self.api_key = api_key
        self.config = DatabaseConfig.get_database_config('pubmed')
        self.session = requests.Session()

        # Set up proper headers
        self.session.headers.update({
            'User-Agent': f'Python-requests/2.25.1 ({email})',
            'Accept': 'application/xml'
        })

    def search(self, query: LiteratureSearchQuery) -> pd.DataFrame:
        """Search PubMed using the Entrez API"""
        logger.info(f"Searching PubMed: {query.query}")

        pubmed_query = query.get_pubmed_query()
        logger.info(f"PubMed query: {pubmed_query}")

        # Initial search to get IDs
        search_params = {
            'db': 'pubmed',
            'term': pubmed_query,
            'retmax': min(query.max_results, self.config['max_results']),
            'usehistory': 'y',
            'datetype': 'pdat',
            'mindate': query.date_from or '1900',
            'maxdate': query.date_to[:4],  # Year only for PubMed
        }

        if self.api_key:
            search_params['api_key'] = self.api_key

        try:
            response = self.session.get(f"{self.config['base_url']}/{self.config['search_endpoint']}",
                                      params=search_params, timeout=30)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.content)

            # Extract IDs from either WebEnv history or direct results
            webenv = root.find('.//WebEnv')
            query_key = root.find('.//QueryKey')
            count = int(root.find('.//Count').text)

            if count == 0:
                logger.info("No results found")
                return pd.DataFrame()

            logger.info(f"Found {count} results")

            # Fetch results in batches
            all_results = []
            batch_size = self.config['batch_size']

            for start in range(0, min(count, query.max_results), batch_size):
                batch_results = self._fetch_results_batch(webenv.text if webenv is not None else None,
                                                        query_key.text if query_key is not None else None,
                                                        start, min(batch_size, min(count, query.max_results) - start))
                all_results.extend(batch_results)

                # Rate limiting
                time.sleep(1 / self.config['rate_limit'])

            df = pd.DataFrame(all_results)
            logger.info(f"Retrieved {len(df)} records from PubMed")
            return df

        except Exception as e:
            logger.error(f"PubMed search failed: {e}")
            raise

    def _fetch_results_batch(self, webenv: str, query_key: str, start: int, retmax: int) -> List[Dict[str, Any]]:
        """Fetch a batch of results by ID or WebEnv"""

        if webenv and query_key:
            # Use history
            fetch_params = {
                'db': 'pubmed',
                'WebEnv': webenv,
                'query_key': query_key,
                'retstart': start,
                'retmax': retmax,
                'rettype': 'medline',
                'retmode': 'xml'
            }
        else:
            # Direct fetch by IDs (not implemented here for simplicity)
            return []

        if self.api_key:
            fetch_params['api_key'] = self.api_key

        response = self.session.get(f"{self.config['base_url']}/{self.config['fetch_endpoint']}",
                                  params=fetch_params, timeout=30)
        response.raise_for_status()

        # Parse XML and extract data
        return self._parse_medline_xml(response.content)


    def _parse_medline_xml(self, xml_content: bytes) -> List[Dict[str, Any]]:
        """Parse PubMed Medline XML format"""
        root = ET.fromstring(xml_content)
        results = []

        for article in root.findall('.//MedlineCitation'):
            try:
                # Extract basic information
                pmid = article.find('.//PMID').text
                title_element = article.find('.//ArticleTitle')
                title = title_element.text if title_element is not None else ""

                # Extract abstract
                abstract_element = article.find('.//AbstractText')
                abstract = ''
                if abstract_element is not None:
                    if abstract_element.text:
                        abstract = abstract_element.text
                    elif list(abstract_element):  # Check for structured abstract
                        abstract_parts = []
                        for part in abstract_element:
                            if part.text:
                                abstract_parts.append(part.text)
                        abstract = ' '.join(abstract_parts)

                # Extract authors
                authors = []
                author_list = article.findall('.//Author')
                for author in author_list:
                    last_name = author.find('.//LastName')
                    fore_name = author.find('.//ForeName')
                    if last_name is not None and fore_name is not None:
                        authors.append(f"{last_name.text}, {fore_name.text}")

                # Extract journal info
                journal_element = article.find('.//Journal/Title')
                journal = journal_element.text if journal_element is not None else ""

                # Extract publication date
                year_element = article.find('.//PubDate/Year')
                year = year_element.text if year_element is not None else ""

                result = {
                    'pmid': pmid,
                    'title': title,
                    'abstract': abstract,
                    'authors': '; '.join(authors),
                    'journal': journal,
                    'year': year,
                    'database': 'pubmed',
                    'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                }

                results.append(result)

            except Exception as e:
                logger.error(f"Error parsing article: {e}")
                continue

        return results


class CochraneSearch:
    """Cochrane Library search implementation"""

    def __init__(self):
        self.config = DatabaseConfig.get_database_config('cochrane')
        self.session = requests.Session()

    def search(self, query: LiteratureSearchQuery) -> pd.DataFrame:
        """Search Cochrane Library"""
        logger.info(f"Searching Cochrane: {query.query}")

        # Cochrane search is more complex and may require different approach
        # This is a simplified implementation

        search_url = f"{self.config['base_url']}/search"
        params = {
            'searchText': query.query,
            'rowsPerPage': min(query.max_results, 100),
            'page': 1
        }

        try:
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()

            # Parse response - this would need to be adapted based on actual API
            # For now, return empty DataFrame as Cochrane API is complex
            logger.warning("Cochrane search not fully implemented - requires API access")
            return pd.DataFrame()

        except Exception as e:
            logger.error(f"Cochrane search failed: {e}")
            return pd.DataFrame()


class MultiDatabaseSearch:
    """
    Unified search across multiple literature databases
"""

    def __init__(self, email: str = "research@example.com", pubmed_api_key: str = None):
        self.email = email
        self.pubmed_api_key = pubmed_api_key
        self.search_engines = {
            'pubmed': PubMedSearch(email, pubmed_api_key),
            'cochrane': CochraneSearch()
        }

    def search(self, query: LiteratureSearchQuery, parallel: bool = True) -> pd.DataFrame:
        """
        Search across multiple databases

        Args:
            query: Search query object
            parallel: Whether to search databases in parallel

        Returns:
            Combined DataFrame of all results
        """
        logger.info(f"Starting multi-database search: {query.query}")
        logger.info(f"Databases: {', '.join(query.databases)}")

        # Validate query
        errors = query.validate_query()
        if errors:
            raise ValueError("Query validation failed: " + "; ".join(errors))

        all_results = []

        if parallel and len(query.databases) > 1:
            # Parallel search
            with ThreadPoolExecutor(max_workers=len(query.databases)) as executor:
                future_to_db = {
                    executor.submit(self._search_single_database, db, query): db
                    for db in query.databases
                }

                for future in as_completed(future_to_db):
                    db = future_to_db[future]
                    try:
                        results = future.result()
                        all_results.append(results)
                        logger.info(f"{db}: found {len(results)} results")
                    except Exception as e:
                        logger.error(f"{db} search failed: {e}")
        else:
            # Sequential search
            for db in query.databases:
                try:
                    results = self._search_single_database(db, query)
                    all_results.append(results)
                    logger.info(f"{db}: found {len(results)} results")

                    # Rate limiting between databases
                    time.sleep(0.5)
                except Exception as e:
                    logger.error(f"{db} search failed: {e}")

        # Combine results
        if all_results:
            combined_df = pd.concat(all_results, ignore_index=True)

            # Remove duplicates based on title similarity
            combined_df = self._deduplicate_results(combined_df)

            logger.info(f"Total unique results: {len(combined_df)}")
            return combined_df
        else:
            return pd.DataFrame()

    def _search_single_database(self, database: str, query: LiteratureSearchQuery) -> pd.DataFrame:
        """Search a single database"""
        if database in self.search_engines:
            engine = self.search_engines[database]
            return engine.search(query)
        else:
            logger.warning(f"No search engine available for {database}")
            return pd.DataFrame()

    def _deduplicate_results(self, df: pd.DataFrame, similarity_threshold: float = 0.85) -> pd.DataFrame:
        """
        Remove duplicate results based on title similarity

        Args:
            df: DataFrame with results
            similarity_threshold: Threshold for considering titles similar

        Returns:
            Deduplicated DataFrame
        """

        def titles_similar(title1: str, title2: str) -> bool:
            """Simple title similarity check"""
            if not title1 or not title2:
                return False

            # Normalize titles
            t1 = re.sub(r'[^\w\s]', '', title1.lower())
            t2 = re.sub(r'[^\w\s]', '', title2.lower())

            # Simple word overlap check
            words1 = set(t1.split())
            words2 = set(t2.split())

            if not words1 or not words2:
                return False

            overlap = len(words1.intersection(words2))
            max_words = max(len(words1), len(words2))

            return (overlap / max_words) > similarity_threshold

        # Simple deduplication - keep first occurrence
        unique_indices = []
        titles = df['title'].fillna('').tolist()

        for i, title1 in enumerate(titles):
            is_duplicate = False
            for j in unique_indices:
                title2 = titles[j]
                if titles_similar(title1, title2):
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_indices.append(i)

        logger.info(f"Deduplication: {len(df)} -> {len(unique_indices)}")
        return df.iloc[unique_indices].copy()

    def save_results(self, results: pd.DataFrame, output_path: str,
                    format: str = 'csv') -> str:
        """Save search results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"literature_search_{timestamp}.{format}"

        if not output_path:
            output_path = filename
        else:
            Path(output_path).mkdir(parents=True, exist_ok=True)
            output_path = str(Path(output_path) / filename)

        if format == 'csv':
            results.to_csv(output_path, index=False)
        elif format == 'json':
            results.to_json(output_path, orient='records', indent=2)
        elif format == 'xlsx':
            results.to_excel(output_path, index=False)

        logger.info(f"Results saved to: {output_path}")
        return output_path

    def generate_search_report(self, query: LiteratureSearchQuery,
                             results: pd.DataFrame) -> Dict[str, Any]:
        """Generate a search report"""

        report = {
            'search_query': query.to_dict(),
            'total_results': len(results),
            'database_breakdown': results['database'].value_counts().to_dict() if 'database' in results.columns else {},
            'date_range': {
                'from': query.date_from,
                'to': query.date_to
            },
            'generated_at': datetime.now().isoformat(),
            'summary_stats': {}
        }

        if len(results) > 0:
            # Basic statistics
            report['summary_stats'] = {
                'avg_title_length': results['title'].fillna('').str.len().mean(),
                'avg_abstract_length': results.get('abstract', pd.Series([''] * len(results))).fillna('').str.len().mean(),
                'unique_journals': results.get('journal', pd.Series([''] * len(results))).fillna('').nunique(),
                'year_distribution': results.get('year', pd.Series([''] * len(results))).value_counts().head(10).to_dict()
            }

        return report


def create_search_query_from_picos(pico: Dict[str, str],
                                 additional_terms: List[str] = None) -> LiteratureSearchQuery:
    """
    Create a search query from PICO framework components

    Args:
        pico: Dictionary with PICO components (Population, Intervention, Comparison, Outcome)
        additional_terms: Additional search terms to include

    Returns:
        LiteratureSearchQuery object
    """

    pico_terms = []

    if 'population' in pico and pico['population']:
        pico_terms.append(f"({pico['population']})")

    if 'intervention' in pico and pico['intervention']:
        pico_terms.append(f"({pico['intervention']})")

    if 'comparison' in pico and pico['comparison']:
        pico_terms.append(f"({pico['comparison']})")

    if 'outcome' in pico and pico['outcome']:
        pico_terms.append(f"({pico['outcome']})")

    # Combine PICO terms
    if pico_terms:
        query = ' AND '.join(pico_terms)
    else:
        query = ""

    # Add additional terms
    if additional_terms:
        additional_query = ' OR '.join(f"({term})" for term in additional_terms)
        if query:
            query = f"({query}) AND ({additional_query})"
        else:
            query = additional_query

    return LiteratureSearchQuery(
        query=query,
        databases=['pubmed', 'cochrane']
    )


# Command-line interface
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Multi-Database Literature Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--databases", nargs='+', default=['pubmed'],
                       help="Databases to search (pubmed, cochrane)")
    parser.add_argument("--from-date", help="Start date (YYYY/MM/DD)")
    parser.add_argument("--to-date", help="End date (YYYY/MM/DD)")
    parser.add_argument("--max-results", type=int, default=1000,
                       help="Maximum results per database")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--format", choices=['csv', 'json', 'xlsx'], default='csv',
                       help="Output format")
    parser.add_argument("--email", default="research@example.com",
                       help="Email for PubMed API")
    parser.add_argument("--pubmed-api-key", help="PubMed API key")
    parser.add_argument("--parallel", action='store_true',
                       help="Search databases in parallel")

    args = parser.parse_args()

    # Create search query
    search_query = LiteratureSearchQuery(
        query=args.query,
        databases=args.databases,
        date_from=args.from_date,
        date_to=args.to_date,
        max_results=args.max_results
    )

    # Initialize search engine
    search_engine = MultiDatabaseSearch(args.email, args.pubmed_api_key)

    # Execute search
    results = search_engine.search(search_query, args.parallel)

    # Save results
    if results.empty:
        print("No results found")
        return

    output_path = search_engine.save_results(results, args.output, args.format)

    # Generate report
    report = search_engine.generate_search_report(search_query, results)

    print("Search completed:")
    print(f"- Total results: {len(results)}")
    print(f"- Results saved to: {output_path}")
    print(f"- Database breakdown: {report['database_breakdown']}")


if __name__ == "__main__":
    main()
