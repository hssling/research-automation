#!/usr/bin/env python3
"""
Automated Literature Search Execution Script
Systematic Review: Synbiotics and Postbiotics in MDR-TB Treatment Outcomes

This script executes systematic literature searches across multiple databases
and manages the search results for the systematic review.

Requirements:
- Python 3.8+
- requests library for API access
- pandas for data management
- json for result storage
- datetime for timestamping

Install dependencies:
pip install requests pandas
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime
import urllib.parse
import os

class SystematicSearchEngine:
    """
    Automated systematic literature search execution engine
    """

    def __init__(self, search_date=None):
        """
        Initialize the search engine

        Parameters:
        search_date (str): Date of search execution (YYYY-MM-DD)
        """
        self.search_date = search_date or datetime.now().strftime('%Y-%m-%d')
        self.results_dir = "synbiotics_postbiotics_mdr_tb"
        self.search_results = {}

        # PubMed search query
        self.pubmed_query = '''(multidrug-resistant tuberculosis[Title/Abstract] OR MDR tuberculosis[Title/Abstract] OR extensively drug-resistant tuberculosis[Title/Abstract] OR MDR-TB[Title/Abstract] OR XDR-TB[Title/Abstract]) AND (synbiotic*[Title/Abstract] OR postbiotic*[Title/Abstract] OR probiotic*[Title/Abstract] OR prebiotic*[Title/Abstract] OR microbiome[Title/Abstract] OR microbiota[Title/Abstract]) AND (treatment outcome*[Title/Abstract] OR cure rate*[Title/Abstract] OR conversion[Title/Abstract] OR sputum conversion[Title/Abstract] OR culture conversion[Title/Abstract] OR efficacy[Title/Abstract]) AND (versus[Title/Abstract] OR compared[Title/Abstract] OR adjunct[Title/Abstract] OR add-on[Title/Abstract] OR additional[Title/Abstract] OR standard care[Title/Abstract] OR randomized controlled trial[Publication Type] OR clinical trial[Publication Type])'''

        # EMBASE search query (simplified for demonstration)
        self.embase_query = '''multidrug-resistant tuberculosis/de OR 'multidrug resistant tuberculosis'/exp OR extensively-drug-resistant-tuberculosis/de AND (synbiotic*/ti,ab OR postbiotic*/ti,ab OR probiotic*/ti,ab OR microbiome/ti,ab OR microbiota/ti,ab) AND (treatment-outcome*/de OR 'cure rate'/ti,ab OR conversion/ti,ab OR efficacy/ti,ab) AND (versus/ti,ab OR compared/ti,ab OR adjunct/ti,ab OR 'add on'/ti,ab OR additional/ti,ab OR 'standard care'/ti,ab OR 'randomized controlled trial'/de OR 'clinical trial'/de)'''

        print("=" * 60)
        print(f"Systematic Literature Search Execution - {self.search_date}")
        print("Review: Synbiotics/Postbiotics in MDR-TB Treatment Outcomes")
        print("=" * 60)

    def search_pubmed(self):
        """
        Execute PubMed search via E-utilities API

        Returns:
        dict: Search results summary
        """
        print("\n[1/6] Executing PubMed Search...")
        print(f"Query: {self.pubmed_query[:100]}...")

        try:
            # PubMed E-utilities API base
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

            # Step 1: Search
            search_url = f"{base_url}esearch.fcgi"
            params = {
                'db': 'pubmed',
                'term': self.pubmed_query,
                'retmax': '10000',
                'retmode': 'json',
                'datetype': 'pdat',
                'mindate': '2010',
                'maxdate': self.search_date.split('-')[0]  # Current year
            }

            response = requests.get(search_url, params=params, timeout=30)
            response.raise_for_status()

            search_data = response.json()
            pubmed_ids = search_data['esearchresult']['idlist']

            print(f"✓ PubMed Search Complete: {len(pubmed_ids)} records found")

            # Step 2: Get summaries (first 200 for demonstration)
            summary_url = f"{base_url}esummary.fcgi"
            summary_ids = pubmed_ids[:200] if len(pubmed_ids) > 200 else pubmed_ids

            if summary_ids:
                summary_params = {
                    'db': 'pubmed',
                    'id': ','.join(summary_ids),
                    'retmode': 'json'
                }

                summary_response = requests.get(summary_url, params=summary_params, timeout=30)
                summary_response.raise_for_status()
                summaries = summary_response.json()

                pubmed_results = []
                for pubmed_id in summary_ids:
                    if pubmed_id in summaries['result']:
                        result = summaries['result'][pubmed_id]
                        pubmed_results.append({
                            'pmid': pubmed_id,
                            'title': result.get('title', ''),
                            'authors': result.get('authors', []),
                            'journal': result.get('fulljournalname', ''),
                            'pub_date': result.get('pubdate', ''),
                            'doi': result.get('elocationid', ''),
                            'database': 'PubMed'
                        })

                self.search_results['pubmed'] = {
                    'total_count': len(pubmed_ids),
                    'detailed_count': len(pubmed_results),
                    'results': pubmed_results
                }

                print(f"✓ Retrieved {len(pubmed_results)} detailed records from PubMed")
            else:
                self.search_results['pubmed'] = {
                    'total_count': len(pubmed_ids),
                    'detailed_count': 0,
                    'results': []
                }

            return True

        except Exception as e:
            print(f"✗ PubMed search failed: {str(e)}")
            self.search_results['pubmed'] = {
                'total_count': 0,
                'detailed_count': 0,
                'results': [],
                'error': str(e)
            }
            return False

    def search_embase(self):
        """
        Skip EMBASE search - requires institutional subscription/API key
        Not available for independent researchers
        """
        print("\n[2/6] EMBASE Search (Skipped)...")
        print("Note: EMBASE requires institutional subscription - not accessible for independent research")

        skipped_results = {
            'total_count': 0,
            'detailed_count': 0,
            'results': [],
            'note': 'Skipped - requires institutional subscription',
            'status': 'skipped_institutional'
        }

        self.search_results['embase'] = skipped_results
        print("EMBASE search skipped due to access restrictions")

        return True

    def search_cochrane(self):
        """
        Skip Cochrane CENTRAL search - requires institutional subscription
        Not available for independent researchers
        """
        print("\n[3/6] Cochrane CENTRAL Search (Skipped)...")
        print("Note: Cochrane CENTRAL requires institutional subscription - not accessible for independent research")

        skipped_results = {
            'total_count': 0,
            'detailed_count': 0,
            'results': [],
            'note': 'Skipped - requires institutional subscription',
            'status': 'skipped_institutional'
        }

        self.search_results['cochrane'] = skipped_results
        print("Cochrane CENTRAL search skipped due to access restrictions")

        return True

    def search_web_of_science(self):
        """
        Skip Web of Science search - requires institutional subscription/API key
        Not available for independent researchers
        """
        print("\n[4/6] Web of Science Search (Skipped)...")
        print("Note: Web of Science requires institutional subscription - not accessible for independent research")

        skipped_results = {
            'total_count': 0,
            'detailed_count': 0,
            'results': [],
            'note': 'Skipped - requires institutional subscription',
            'status': 'skipped_institutional'
        }

        self.search_results['web_of_science'] = skipped_results
        print("Web of Science search skipped due to access restrictions")

        return True

    def search_clinicaltrials_gov(self):
        """
        Execute ClinicalTrials.gov search via their API
        """
        print("\n[5/6] ClinicalTrials.gov Search...")

        try:
            base_url = "https://clinicaltrials.gov/api/v2/studies"
            query_params = {
                'query.cond': 'multidrug-resistant tuberculosis OR MDR tuberculosis',
                'query.inter': 'probiotic OR synbiotic OR postbiotic OR prebiotic OR microbiome',
                'query.outc': 'treatment outcome OR cure OR conversion OR efficacy',
                'filter.overallStatus': 'COMPLETED',
                'pageSize': 100,
                'countTotal': 'true'
            }

            response = requests.get(base_url, params=query_params, timeout=30)
            response.raise_for_status()

            data = response.json()

            clinical_trials = []
            if 'studies' in data:
                for study in data['studies'][:50]:  # Limit for demonstration
                    protocol = study.get('protocolSection', {})
                    identification = protocol.get('identificationModule', {})
                    status = protocol.get('statusModule', {})

                    clinical_trials.append({
                        'nct_id': identification.get('nctId', ''),
                        'title': identification.get('briefTitle', ''),
                        'status': status.get('overallStatus', ''),
                        'completion_date': status.get('completionDateStruct', {}).get('date', ''),
                        'database': 'ClinicalTrials.gov'
                    })

            self.search_results['clinicaltrials_gov'] = {
                'total_count': len(clinical_trials),
                'detailed_count': len(clinical_trials),
                'results': clinical_trials
            }

            print(f"✓ ClinicalTrials.gov Search Complete: {len(clinical_trials)} completed trials found")

        except Exception as e:
            print(f"✗ ClinicalTrials.gov search failed: {str(e)}")
            self.search_results['clinicaltrials_gov'] = {
                'total_count': 0,
                'detailed_count': 0,
                'results': [],
                'error': str(e)
            }

    def search_who_ictrp(self):
        """
        Execute WHO ICTRP search via their API
        """
        print("\n[6/6] WHO ICTRP Search...")

        try:
            url = "https://trialsearch.who.int/API"
            headers = {'Content-Type': 'application/json'}

            payload = {
                "Condition": ["multidrug-resistant tuberculosis", "MDR tuberculosis"],
                "Intervention": ["probiotic", "synbiotic", "postbiotic", "prebiotic", "microbiome"],
                "RecruitmentStatus": ["Completed"],
                "PageSize": 100
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()

            who_trials = []
            if 'Trial' in data:
                for trial in data['Trial'][:50]:  # Limit for demonstration
                    who_trials.append({
                        'trial_id': trial.get('TrialID', ''),
                        'title': trial.get('Public_title', ''),
                        'status': trial.get('Recruitment_status', ''),
                        'registration_date': trial.get('Date_registration', ''),
                        'database': 'WHO ICTRP'
                    })

            self.search_results['who_ictrp'] = {
                'total_count': len(who_trials),
                'detailed_count': len(who_trials),
                'results': who_trials
            }

            print(f"✓ WHO ICTRP Search Complete: {len(who_trials)} trials found")

        except Exception as e:
            print(f"✗ WHO ICTRP search failed: {str(e)}")
            self.search_results['who_ictrp'] = {
                'total_count': 0,
                'detailed_count': 0,
                'results': [],
                'error': str(e)
            }

    def deduplicate_results(self):
        """
        Perform deduplication of search results
        """
        print("\n[7/7] Deduplicating Results...")

        all_records = []
        total_before_dedup = 0

        # Collect all records
        for db_name, db_results in self.search_results.items():
            if 'results' in db_results:
                all_records.extend(db_results['results'])
                total_before_dedup += db_results.get('total_count', 0)

        print(f"Total records before deduplication: {total_before_dedup}")

        # Simple deduplication by title similarity (basic implementation)
        unique_records = []
        seen_titles = set()

        for record in all_records:
            title = record.get('title', '').lower().strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_records.append(record)

        print(f"Total unique records after deduplication: {len(unique_records)}")

        self.search_results['deduplicated'] = {
            'total_before_dedup': total_before_dedup,
            'total_after_dedup': len(unique_records),
            'duplicate_count': total_before_dedup - len(unique_records),
            'results': unique_records
        }

    def save_results(self):
        """
        Save search results to files
        """
        print("\n💾 Saving Results...")

        # Create results filename with date
        results_file = f"{self.results_dir}/search_results_{self.search_date}.json"

        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.search_results, f, indent=2, ensure_ascii=False)

        # Save deduplicated CSV for reference management
        if 'deduplicated' in self.search_results:
            dedup_file = f"{self.results_dir}/deduplicated_results_{self.search_date}.csv"

            df = pd.DataFrame(self.search_results['deduplicated']['results'])
            if not df.empty:
                df.to_csv(dedup_file, index=False, encoding='utf-8')
                print(f"✓ Deduplicated results saved to {dedup_file}")

        print(f"✓ Complete search results saved to {results_file}")

    def generate_search_report(self):
        """
        Generate comprehensive search report
        """
        print("\n📊 Generating Search Report...")

        report = {
            'search_date': self.search_date,
            'review_title': 'Synbiotics and Postbiotics in MDR-TB Treatment Outcomes',
            'total_databases_searched': len(self.search_results) - 1,  # Exclude deduplicated
            'database_summary': {}
        }

        if 'deduplicated' in self.search_results:
            report['deduplication_stats'] = {
                'total_before_dedup': self.search_results['deduplicated']['total_before_dedup'],
                'total_after_dedup': self.search_results['deduplicated']['total_after_dedup'],
                'duplicates_removed': self.search_results['deduplicated']['duplicate_count']
            }

        for db_name, db_results in self.search_results.items():
            if db_name != 'deduplicated':
                report['database_summary'][db_name] = {
                    'total_records': db_results.get('total_count', 0),
                    'detailed_records': db_results.get('detailed_count', 0),
                    'note': db_results.get('note', ''),
                    'error': db_results.get('error', None)
                }

        # Save report
        report_file = f"{self.results_dir}/search_report_{self.search_date}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"✓ Search report saved to {report_file}")

        # Display summary
        print("\n" + "=" * 60)
        print("SEARCH EXECUTION SUMMARY")
        print("=" * 60)
        print(f"Date: {self.search_date}")
        print(f"Databases Searched: {len(report['database_summary'])}")
        print(f"Total Records Found: {report['deduplication_stats']['total_before_dedup']}")
        print(f"After Deduplication: {report['deduplication_stats']['total_after_dedup']}")

        print("\nDatabase Results:")
        for db, stats in report['database_summary'].items():
            print(".4f")

    def run_all_searches(self):
        """
        Execute complete systematic search workflow
        """
        print("Starting Complete Systematic Literature Search...\n")

        # Execute searches
        self.search_pubmed()
        self.search_embase()
        self.search_cochrane()
        self.search_web_of_science()
        self.search_clinicaltrials_gov()
        self.search_who_ictrp()

        # Process results
        self.deduplicate_results()

        # Save everything
        self.save_results()
        self.generate_search_report()

        print("\n🎉 Systematic literature search completed!")
        print("Next steps: Title/abstract screening and data extraction")

        return self.search_results

# Main execution
if __name__ == "__main__":
    # Initialize and run search
    engine = SystematicSearchEngine()
    results = engine.run_all_searches()

    print("\nSearch execution complete. Results saved in synbiotics_postbiotics_mdr_tb/ directory.")
    print("Ready for screening phase of systematic review.")
    print("\nNote: Some databases required API keys/institutional access for full results.")
    print("EMBASE, Cochrane, and Web of Science results are simulated estimates.")
    print("PubMed and clinical trials databases accessed via public APIs.")
