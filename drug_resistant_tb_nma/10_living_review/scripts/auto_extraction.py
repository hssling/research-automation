#!/usr/bin/env python3
"""
Automated Data Extraction for Drug-Resistant TB Living Review
Extracts structured data from new studies for analysis updates
"""

import json
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
import re
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))


class DataExtractor:
    """Automated data extraction system for MDR-TB studies"""

    def __init__(self, config_path="../living_review_config.json"):
        """Initialize the extraction system"""
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.extracted_data = []

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
            filename=log_config.get('file', 'data_extraction.log'),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def load_new_studies(self):
        """Load new studies from the search results"""
        search_dir = Path("01_literature_search/new_studies")

        if not search_dir.exists():
            self.logger.info("No new studies directory found")
            return []

        # Find the most recent CSV file
        csv_files = list(search_dir.glob("new_studies_*.csv"))

        if not csv_files:
            self.logger.info("No new studies CSV files found")
            return []

        # Get the most recent file
        latest_file = max(csv_files, key=lambda f: f.stat().st_mtime)

        try:
            df = pd.read_csv(latest_file)
            self.logger.info(f"Loaded {len(df)} studies from {latest_file}")
            return df.to_dict('records')
        except Exception as e:
            self.logger.error(f"Failed to load studies: {e}")
            return []

    def extract_study_metadata(self, study: Dict[str, Any]) -> Dict[str, Any]:
        """Extract basic study metadata"""
        metadata = {
            'study_id': self.generate_study_id(study),
            'title': study.get('title', ''),
            'source': study.get('source', ''),
            'pmid': study.get('pmid', ''),
            'nct_id': study.get('nct_id', ''),
            'doi': study.get('doi', ''),
            'journal': study.get('journal', ''),
            'publication_year': self.extract_year(study.get('publication_date', '')),
            'search_date': study.get('search_date', ''),
            'extraction_date': datetime.now().isoformat()
        }

        return metadata

    def generate_study_id(self, study: Dict[str, Any]) -> str:
        """Generate unique study identifier"""
        pmid = study.get('pmid', '')
        nct_id = study.get('nct_id', '')

        if pmid:
            return f"PMID{pmid}"
        elif nct_id:
            return f"NCT{nct_id}"
        else:
            # Generate hash-based ID from title
            title = study.get('title', '')
            title_hash = hash(title) % 10000
            return f"STUDY{abs(title_hash):04d}"

    def extract_year(self, date_string: str) -> Optional[int]:
        """Extract year from date string"""
        if not date_string:
            return None

        # Try different date formats
        patterns = [
            r'\b(20\d{2})\b',  # YYYY format
            r'(\d{4})',        # Any 4-digit year
        ]

        for pattern in patterns:
            match = re.search(pattern, date_string)
            if match:
                year = match.group(1)
                # Validate year range
                year_int = int(year)
                if 1900 <= year_int <= datetime.now().year + 1:
                    return year_int

        return None

    def extract_population_data(self, study: Dict[str, Any]) -> Dict[str, Any]:
        """Extract population characteristics"""
        # This would typically involve NLP analysis of abstracts/full text
        # For now, we'll use rule-based extraction from available fields

        population = {
            'sample_size_total': 0,
            'sample_size_per_arm': {},
            'age_mean': None,
            'age_range': None,
            'sex_distribution': {},
            'hiv_prevalence': None,
            'resistance_patterns': [],
            'country': self.extract_country(study)
        }

        # Extract sample size from enrollment or abstract
        enrollment = study.get('enrollment', 0)
        if enrollment > 0:
            population['sample_size_total'] = enrollment

        # Extract country information
        country_patterns = [
            r'\b(India|China|South Africa|Brazil|Russia|Indonesia)\b',
            r'\b(USA|United States|US)\b',
            r'\b(UK|United Kingdom)\b'
        ]

        abstract = study.get('abstract', '').lower()
        for pattern in country_patterns:
            match = re.search(pattern, abstract)
            if match:
                population['country'] = match.group(1)
                break

        return population

    def extract_country(self, study: Dict[str, Any]) -> Optional[str]:
        """Extract country information from study"""
        # Try different sources of country information
        sources = [
            study.get('conditions', []),
            study.get('abstract', ''),
            study.get('title', '')
        ]

        all_text = ' '.join(str(s) for s in sources).lower()

        # Common country mentions in TB research
        countries = {
            'india': 'India',
            'china': 'China',
            'south africa': 'South Africa',
            'brazil': 'Brazil',
            'russia': 'Russia',
            'indonesia': 'Indonesia',
            'pakistan': 'Pakistan',
            'nigeria': 'Nigeria',
            'bangladesh': 'Bangladesh',
            'philippines': 'Philippines'
        }

        for key, value in countries.items():
            if key in all_text:
                return value

        return None

    def extract_intervention_data(self, study: Dict[str, Any]) -> Dict[str, Any]:
        """Extract intervention details"""
        interventions = {
            'treatment_arms': [],
            'control_arms': [],
            'regimens_identified': [],
            'duration_weeks': None,
            'drugs_identified': []
        }

        # Extract from interventions field (ClinicalTrials.gov)
        study_interventions = study.get('interventions', [])
        if study_interventions:
            interventions['treatment_arms'] = study_interventions

        # Extract from abstract using pattern matching
        abstract = study.get('abstract', '').lower()

        # Look for TB drug names
        tb_drugs = [
            'bedaquiline', 'pretomanid', 'linezolid', 'moxifloxacin',
            'levofloxacin', 'delamanid', 'clofazimine', 'cycloserine',
            'terizidone', 'ethionamide', 'prothionamide', 'para-aminosalicylic acid',
            'streptomycin', 'kanamycin', 'amikacin', 'capreomycin'
        ]

        found_drugs = []
        for drug in tb_drugs:
            if drug in abstract:
                found_drugs.append(drug)

        interventions['drugs_identified'] = found_drugs

        # Look for regimen patterns
        regimen_patterns = [
            r'bpalm?\b',  # BPaL or BPaLM
            r'short.course',  # Short course regimen
            r'individualized',  # Individualized regimen
            r'conventional',  # Conventional regimen
        ]

        found_regimens = []
        for pattern in regimen_patterns:
            if re.search(pattern, abstract):
                found_regimens.append(pattern)

        interventions['regimens_identified'] = found_regimens

        return interventions

    def extract_outcome_data(self, study: Dict[str, Any]) -> Dict[str, Any]:
        """Extract outcome data"""
        outcomes = {
            'treatment_success': {'numerator': None, 'denominator': None, 'percentage': None},
            'relapse': {'numerator': None, 'denominator': None, 'percentage': None},
            'mortality': {'numerator': None, 'denominator': None, 'percentage': None},
            'adverse_events': {'total': None, 'severe': None},
            'culture_conversion': {'numerator': None, 'denominator': None, 'percentage': None}
        }

        abstract = study.get('abstract', '').lower()

        # Look for success rates
        success_patterns = [
            r'(\d+(?:\.\d+)?)%?\s*(?:treatment\s*)?success',
            r'success.*(\d+(?:\.\d+)?)%',
            r'cured?\s*(\d+(?:\.\d+)?)%',
        ]

        for pattern in success_patterns:
            match = re.search(pattern, abstract)
            if match:
                try:
                    percentage = float(match.group(1))
                    if 0 <= percentage <= 100:
                        outcomes['treatment_success']['percentage'] = percentage
                        break
                except ValueError:
                    continue

        # Look for sample sizes in success rates
        sample_patterns = [
            r'(\d+)/(\d+)\s*(?:patients?|participants?)',
            r'(\d+)\s*of\s*(\d+)\s*(?:patients?|participants?)',
        ]

        for pattern in sample_patterns:
            match = re.search(pattern, abstract)
            if match:
                try:
                    num = int(match.group(1))
                    den = int(match.group(2))
                    if 0 < num <= den:
                        outcomes['treatment_success']['numerator'] = num
                        outcomes['treatment_success']['denominator'] = den
                        break
                except (ValueError, IndexError):
                    continue

        return outcomes

    def assess_study_quality(self, study: Dict[str, Any]) -> Dict[str, Any]:
        """Assess study quality indicators"""
        quality = {
            'risk_of_bias': 'unclear',
            'funding_source': 'not_reported',
            'blinding': 'not_reported',
            'randomization': 'not_reported',
            'sample_size_adequate': False,
            'follow_up_complete': 'unclear',
            'itt_analysis': 'unclear'
        }

        abstract = study.get('abstract', '').lower()

        # Check for randomization
        if re.search(r'randomi[sz]ed|randomly?\s*assigned', abstract):
            quality['randomization'] = 'reported'

        # Check for blinding
        if re.search(r'blind|mask', abstract):
            quality['blinding'] = 'reported'

        # Check for intention-to-treat
        if re.search(r'intention.to.treat|itt', abstract):
            quality['itt_analysis'] = 'yes'

        # Check for funding
        if re.search(r'funded?|sponsored?|grant', abstract):
            quality['funding_source'] = 'reported'

        # Assess sample size adequacy
        sample_size = study.get('enrollment', 0) or study.get('sample_size', 0)
        if sample_size >= 50:
            quality['sample_size_adequate'] = True

        return quality

    def extract_data_from_study(self, study: Dict[str, Any]) -> Dict[str, Any]:
        """Extract all data from a single study"""
        try:
            extracted_study = {
                'metadata': self.extract_study_metadata(study),
                'population': self.extract_population_data(study),
                'interventions': self.extract_intervention_data(study),
                'outcomes': self.extract_outcome_data(study),
                'quality': self.assess_study_quality(study),
                'extraction_confidence': self.assess_extraction_confidence(study)
            }

            return extracted_study

        except Exception as e:
            self.logger.error(f"Failed to extract data from study {study.get('title', 'Unknown')}: {e}")
            return None

    def assess_extraction_confidence(self, study: Dict[str, Any]) -> Dict[str, float]:
        """Assess confidence in extracted data"""
        confidence = {
            'overall': 0.0,
            'metadata': 0.0,
            'population': 0.0,
            'interventions': 0.0,
            'outcomes': 0.0,
            'quality': 0.0
        }

        # Metadata confidence
        if study.get('title'):
            confidence['metadata'] += 0.3
        if study.get('pmid') or study.get('nct_id'):
            confidence['metadata'] += 0.3
        if study.get('doi'):
            confidence['metadata'] += 0.2
        if study.get('journal'):
            confidence['metadata'] += 0.2

        # Population confidence
        if study.get('enrollment', 0) > 0:
            confidence['population'] += 0.5
        if self.extract_country(study):
            confidence['population'] += 0.3
        if study.get('abstract'):
            confidence['population'] += 0.2

        # Interventions confidence
        interventions = study.get('interventions', [])
        if interventions:
            confidence['interventions'] += 0.6
        if study.get('abstract'):
            confidence['interventions'] += 0.4

        # Outcomes confidence
        abstract = study.get('abstract', '')
        if re.search(r'\d+%', abstract):
            confidence['outcomes'] += 0.5
        if re.search(r'\d+/\d+', abstract):
            confidence['outcomes'] += 0.3
        if study.get('abstract'):
            confidence['outcomes'] += 0.2

        # Overall confidence
        confidence['overall'] = np.mean([
            confidence['metadata'],
            confidence['population'],
            confidence['interventions'],
            confidence['outcomes']
        ])

        return confidence

    def save_extracted_data(self, extracted_studies: List[Dict[str, Any]]):
        """Save extracted data to files"""
        if not extracted_studies:
            self.logger.info("No extracted data to save")
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create output directory
        output_dir = Path("02_data_extraction/incremental")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save detailed extraction results
        json_file = output_dir / f"extracted_data_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_studies, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Saved detailed extraction to {json_file}")

        # Create summary CSV
        summary_data = []
        for study in extracted_studies:
            if study:
                summary_row = {
                    'study_id': study['metadata'].get('study_id', ''),
                    'title': study['metadata'].get('title', ''),
                    'source': study['metadata'].get('source', ''),
                    'sample_size': study['population'].get('sample_size_total', 0),
                    'success_rate': study['outcomes'].get('treatment_success', {}).get('percentage'),
                    'confidence': study['extraction_confidence'].get('overall', 0),
                    'drugs_identified': ', '.join(study['interventions'].get('drugs_identified', [])),
                    'country': study['population'].get('country', ''),
                    'extraction_date': study['metadata'].get('extraction_date', '')
                }
                summary_data.append(summary_row)

        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            csv_file = output_dir / f"extraction_summary_{timestamp}.csv"
            summary_df.to_csv(csv_file, index=False)
            self.logger.info(f"Saved summary to {csv_file}")

            # Update master extraction file
            master_file = output_dir / "all_extracted_data.csv"
            if master_file.exists():
                existing_df = pd.read_csv(master_file)
                combined_df = pd.concat([existing_df, summary_df], ignore_index=True)
                combined_df.to_csv(master_file, index=False)
            else:
                summary_df.to_csv(master_file, index=False)

    def run_extraction(self):
        """Run the complete extraction process"""
        self.logger.info("Starting automated data extraction...")

        # Load new studies
        new_studies = self.load_new_studies()

        if not new_studies:
            self.logger.info("No new studies to process")
            return 0

        # Extract data from each study
        extracted_studies = []
        for study in new_studies:
            extracted = self.extract_data_from_study(study)
            if extracted:
                extracted_studies.append(extracted)

        # Save extracted data
        if extracted_studies:
            self.save_extracted_data(extracted_studies)

        self.logger.info(f"Data extraction completed. Processed {len(extracted_studies)} studies")
        return len(extracted_studies)


def main():
    """Main function to run data extraction"""
    extractor = DataExtractor()
    extracted_count = extractor.run_extraction()

    print(f"Data extraction completed. Processed {extracted_count} studies.")

    if extracted_count > 0:
        print("Extracted data saved to: 02_data_extraction/incremental/")
        return 0
    else:
        print("No data extracted.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
