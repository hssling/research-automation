#!/usr/bin/env python3
"""
Automated Literature Search for Drug-Resistant TB Living Review
Searches bibliographic databases for new studies on MDR/RR-TB treatments
"""

import json
import logging
import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))


class LiteratureSearch:
    """Automated literature search system for MDR-TB studies"""

    def __init__(self, config_path="living_review_config.json"):
        """Initialize the search system with configuration"""
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.search_results = []

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Configuration file not found: {config_path}")
            return None
        except json.JSONDecodeError:
            print(f"Invalid JSON in configuration file: {config_path}")
            return None

    def setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        logging.basicConfig(
            level=getattr(logging, log_config.get('level', 'INFO')),
            filename=log_config.get('file', 'literature_search.log'),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def search_pubmed(self, search_terms, date_range="last_week"):
        """Search PubMed for relevant studies"""
        self.logger.info("Searching PubMed...")

        # Calculate date range
        if date_range == "last_week":
            to_date = datetime.now()
            from_date = to_date - timedelta(days=7)
        else:
            from_date = datetime.strptime(date_range['from'], '%Y/%m/%d')
            to_date = datetime.strptime(date_range['to'], '%Y/%m/%d')

        # Build search query
        query_parts = []

        # Add primary search terms
        primary_terms = search_terms.get('primary', [])
        if primary_terms:
            primary_query = ' OR '.join([f'"{term}"' for term in primary_terms])
            query_parts.append(f'({primary_query})')

        # Add intervention terms
        intervention_terms = search_terms.get('interventions', [])
        if intervention_terms:
            intervention_query = ' OR '.join([f'"{term}"' for term in intervention_terms])
            query_parts.append(f'({intervention_query})')

        # Add outcome terms
        outcome_terms = search_terms.get('outcomes', [])
        if outcome_terms:
            outcome_query = ' OR '.join([f'"{term}"' for term in outcome_terms])
            query_parts.append(f'({outcome_query})')

        full_query = ' AND '.join(query_parts)

        # PubMed API parameters
        params = {
            'db': 'pubmed',
            'term': full_query,
            'mindate': from_date.strftime('%Y/%m/%d'),
            'maxdate': to_date.strftime('%Y/%m/%d'),
            'retmax': 1000,
            'retmode': 'json'
        }

        try:
            # PubMed E-utilities API
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'esearchresult' in data:
                pmids = data['esearchresult'].get('idlist', [])
                self.logger.info(f"Found {len(pmids)} studies in PubMed")

                # Get detailed information for each PMID
                for pmid in pmids[:100]:  # Limit to first 100 for efficiency
                    details = self.get_pubmed_details(pmid)
                    if details:
                        self.search_results.append(details)

            return len(pmids)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"PubMed search failed: {e}")
            return 0

    def get_pubmed_details(self, pmid):
        """Get detailed information for a specific PMID"""
        try:
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            params = {
                'db': 'pubmed',
                'id': pmid,
                'retmode': 'json'
            }

            response = requests.get(base_url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()

            if 'result' in data and pmid in data['result']:
                article = data['result'][pmid]

                return {
                    'source': 'PubMed',
                    'pmid': pmid,
                    'doi': article.get('doi', ''),
                    'title': article.get('title', ''),
                    'authors': [author.get('name', '') for author in article.get('authors', [])],
                    'journal': article.get('source', ''),
                    'publication_date': article.get('pubdate', ''),
                    'abstract': article.get('abstract', '')[:1000],  # Truncate long abstracts
                    'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    'search_date': datetime.now().isoformat()
                }

        except Exception as e:
            self.logger.error(f"Failed to get details for PMID {pmid}: {e}")

        return None

    def search_clinicaltrials_gov(self, search_terms):
        """Search ClinicalTrials.gov for relevant trials"""
        self.logger.info("Searching ClinicalTrials.gov...")

        # Build search query
        query_parts = []

        primary_terms = search_terms.get('primary', [])
        if primary_terms:
            primary_query = ' OR '.join(primary_terms)
            query_parts.append(f'({primary_query})')

        intervention_terms = search_terms.get('interventions', [])
        if intervention_terms:
            intervention_query = ' OR '.join(intervention_terms)
            query_parts.append(f'({intervention_query})')

        full_query = ' AND '.join(query_parts)

        try:
            # ClinicalTrials.gov API v2
            base_url = "https://clinicaltrials.gov/api/v2/studies"
            params = {
                'query.term': full_query,
                'pageSize': 1000,
                'format': 'json'
            }

            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            studies = data.get('studies', [])
            self.logger.info(f"Found {len(studies)} trials in ClinicalTrials.gov")

            for study in studies:
                protocol = study.get('protocolSection', {})
                identification = protocol.get('identificationModule', {})

                study_info = {
                    'source': 'ClinicalTrials.gov',
                    'nct_id': identification.get('nctId', ''),
                    'title': identification.get('officialTitle', ''),
                    'status': identification.get('overallStatus', ''),
                    'start_date': identification.get('startDateStruct', {}).get('date', ''),
                    'completion_date': identification.get('completionDateStruct', {}).get('date', ''),
                    'enrollment': protocol.get('designModule', {}).get('enrollmentInfo', {}).get('count', 0),
                    'conditions': [cond.get('term', '') for cond in identification.get('conditionsModule', {}).get('conditions', [])],
                    'interventions': [intervention.get('name', '') for intervention in protocol.get('armsInterventionsModule', {}).get('interventions', [])],
                    'url': f"https://clinicaltrials.gov/study/{identification.get('nctId', '')}",
                    'search_date': datetime.now().isoformat()
                }

                self.search_results.append(study_info)

            return len(studies)

        except Exception as e:
            self.logger.error(f"ClinicalTrials.gov search failed: {e}")
            return 0

    def apply_eligibility_criteria(self, study):
        """Apply eligibility criteria to filter studies"""
        criteria = self.config.get('eligibility_criteria', {})

        # Check population criteria
        population = criteria.get('population', {})

        # Check if study involves eligible conditions
        conditions = [cond.lower() for cond in study.get('conditions', [])]
        eligible_conditions = [cond.lower() for cond in population.get('conditions', [])]

        has_eligible_condition = any(
            cond in ' '.join(conditions) for cond in eligible_conditions
        )

        if not has_eligible_condition:
            return False

        # Check study design
        eligible_designs = criteria.get('study_designs', [])
        study_design = study.get('study_design', '').lower()

        if eligible_designs and not any(
            design.lower() in study_design for design in eligible_designs
        ):
            return False

        # Check sample size
        sample_size_min = self.config.get('search', {}).get('filters', {}).get('sample_size_min', 10)
        sample_size = study.get('sample_size', 0)

        if sample_size < sample_size_min:
            return False

        return True

    def remove_duplicates(self):
        """Remove duplicate studies based on title similarity and DOI"""
        if not self.search_results:
            return

        unique_studies = []
        seen_titles = set()
        seen_dois = set()

        for study in self.search_results:
            title = study.get('title', '').lower()
            doi = study.get('doi', '')

            # Check for duplicates
            is_duplicate = False

            # Title similarity check (simple approach)
            for seen_title in seen_titles:
                if self.calculate_similarity(title, seen_title) > 0.9:
                    is_duplicate = True
                    break

            # DOI check
            if doi and doi in seen_dois:
                is_duplicate = True

            if not is_duplicate:
                unique_studies.append(study)
                seen_titles.add(title)
                if doi:
                    seen_dois.add(doi)

        self.search_results = unique_studies
        self.logger.info(f"Removed duplicates, {len(unique_studies)} unique studies remain")

    def calculate_similarity(self, text1, text2):
        """Calculate simple text similarity (Jaccard similarity)"""
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0

    def save_results(self):
        """Save search results to CSV and JSON files"""
        if not self.search_results:
            self.logger.info("No results to save")
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create output directories if they don't exist
        output_dir = Path("01_literature_search/new_studies")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save as CSV
        csv_file = output_dir / f"new_studies_{timestamp}.csv"
        df = pd.DataFrame(self.search_results)
        df.to_csv(csv_file, index=False)
        self.logger.info(f"Saved {len(self.search_results)} studies to {csv_file}")

        # Save as JSON
        json_file = output_dir / f"new_studies_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.search_results, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Saved studies to {json_file}")

        # Update master file
        master_file = output_dir / "all_new_studies.csv"
        if master_file.exists():
            existing_df = pd.read_csv(master_file)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df.to_csv(master_file, index=False)
        else:
            df.to_csv(master_file, index=False)

        self.logger.info(f"Updated master file with {len(df)} new studies")

    def run_search(self):
        """Run the complete search process"""
        self.logger.info("Starting automated literature search...")

        search_config = self.config.get('search', {})
        search_terms = search_config.get('search_terms', {})

        # Search PubMed
        pubmed_count = self.search_pubmed(search_terms)

        # Search ClinicalTrials.gov
        trials_count = self.search_clinicaltrials_gov(search_terms)

        # Remove duplicates
        self.remove_duplicates()

        # Apply eligibility criteria
        eligible_studies = []
        for study in self.search_results:
            if self.apply_eligibility_criteria(study):
                eligible_studies.append(study)

        self.search_results = eligible_studies
        self.logger.info(f"After eligibility filtering: {len(eligible_studies)} studies")

        # Save results
        if self.search_results:
            self.save_results()

        total_studies = len(self.search_results)
        self.logger.info(f"Literature search completed. Found {total_studies} eligible new studies")

        return total_studies

def main():
    """Main function to run the literature search"""
    search_system = LiteratureSearch()
    new_studies_count = search_system.run_search()

    print(f"Literature search completed. Found {new_studies_count} new eligible studies.")

    if new_studies_count > 0:
        print("New studies saved to: 01_literature_search/new_studies/")
        return 0
    else:
        print("No new eligible studies found.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
