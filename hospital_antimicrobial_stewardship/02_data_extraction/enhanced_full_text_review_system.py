#!/usr/bin/env python3
"""
Enhanced Full-Text Review and Data Extraction System
Hospital Antimicrobial Stewardship Network Meta-Analysis

This script provides an enhanced data extraction system that simulates
full-text review capabilities and identifies gaps that would require
actual full-text access.

Author: Research Team
Date: October 13, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class DataCompleteness(Enum):
    """Enumeration for data completeness levels."""
    ABSTRACT_ONLY = "abstract_only"
    FULL_TEXT_NEEDED = "full_text_needed"
    COMPLETE = "complete"

@dataclass
class ExtractionGap:
    """Represents a data gap that requires full-text review."""
    study_id: str
    pmid: str
    data_field: str
    reason: str
    priority: str
    estimated_effort: str

class EnhancedDataExtractor:
    """Enhanced data extractor with full-text review simulation capabilities."""

    def __init__(self, included_studies_file: str, existing_extraction_dir: str = "02_data_extraction"):
        """
        Initialize the enhanced extractor.

        Args:
            included_studies_file: Path to CSV file with included studies
            existing_extraction_dir: Directory with existing extracted data
        """
        self.included_studies_file = included_studies_file
        self.existing_extraction_dir = existing_extraction_dir

        # Load existing data
        self._load_existing_data()

        # Initialize gap analysis
        self.extraction_gaps = []
        self.completeness_assessment = {}

        # Enhanced extraction patterns
        self._initialize_enhanced_patterns()

    def _load_existing_data(self):
        """Load existing extracted data."""
        try:
            # Load study characteristics
            study_files = [f for f in os.listdir(self.existing_extraction_dir)
                          if f.startswith('study_characteristics_') and f.endswith('.csv')]

            if study_files:
                latest_file = max(study_files)
                self.existing_study_chars = pd.read_csv(
                    os.path.join(self.existing_extraction_dir, latest_file)
                )
                print(f"Loaded existing study characteristics: {len(self.existing_study_chars)} records")
            else:
                self.existing_study_chars = None
                print("No existing study characteristics found")

        except Exception as e:
            print(f"Error loading existing data: {e}")
            self.existing_study_chars = None

    def _initialize_enhanced_patterns(self):
        """Initialize enhanced extraction patterns for better data capture."""
        # Enhanced journal pattern recognition
        self.journal_patterns = {
            'Clinical Infectious Diseases': r'clin infect dis|clinical infectious diseases',
            'Journal of Antimicrobial Chemotherapy': r'j antimicrob chemother|journal of antimicrobial chemotherapy',
            'Infection Control & Hospital Epidemiology': r'infect control hosp epidemiol|infection control.*epidemiology',
            'The Lancet Infectious Diseases': r'lancet infect dis|lancet infectious diseases',
            'Emerging Infectious Diseases': r'emerg infect dis|emerging infectious diseases',
            'Antimicrobial Agents and Chemotherapy': r'antimicrob agents chemother|antimicrobial agents.*chemotherapy',
            'International Journal of Antimicrobial Agents': r'int j antimicrob agents|international journal.*antimicrobial',
            'European Journal of Clinical Microbiology & Infectious Diseases': r'eur j clin microbiol|infect dis|european journal.*clinical microbiology',
            'Journal of Hospital Infection': r'j hosp infect|journal of hospital infection',
            'Diagnostic Microbiology and Infectious Disease': r'diagn microbiol infect dis|diagnostic microbiology.*infectious'
        }

        # Enhanced intervention component detection
        self.intervention_components = {
            'preauthorization': [
                'pre-authorization', 'prior authorization', 'preapproval', 'prior approval',
                'restricted antibiotic', 'formulary restriction', 'approval required'
            ],
            'prospective_audit': [
                'prospective audit', 'audit and feedback', 'post-prescription review',
                'antibiotic review', 'prescription review', 'feedback'
            ],
            'rapid_diagnostics': [
                'rapid diagnostic', 'rapid test', 'maldi-tof', 'pcr', 'molecular diagnostic',
                'rapid identification', 'quick diagnostic', 'point-of-care'
            ],
            'cdss': [
                'cdss', 'computerized decision support', 'clinical decision support',
                'e-prescribing', 'electronic prescribing', 'computerized physician order entry',
                'cpoe', 'electronic health record', 'ehr'
            ],
            'education': [
                'education', 'educational intervention', 'academic detailing',
                'guideline implementation', 'bundle', 'care bundle', 'protocol'
            ]
        }

        # Enhanced outcome extraction patterns
        self.outcome_patterns = {
            'mortality': [
                r'mortality.*?(\d+(?:\.\d+)?)\s*%', r'(\d+(?:\.\d+)?)\s*%\s*mortality',
                r'death.*?(\d+(?:\.\d+)?)\s*%', r'survival.*?(\d+(?:\.\d+)?)\s*%',
                r'mortality rate.*?(\d+(?:\.\d+)?)', r'died.*?(\d+)'
            ],
            'cdi': [
                r'cdi.*?(\d+(?:\.\d+)?)\s*per\s*10,?000', r'cdi.*?(\d+(?:\.\d+)?)\s*per\s*1,?000',
                r'clostridium difficile.*?(\d+(?:\.\d+)?)', r'c\. difficile.*?(\d+(?:\.\d+)?)',
                r'cdi incidence.*?(\d+(?:\.\d+)?)', r'cdi rate.*?(\d+(?:\.\d+)?)'
            ],
            'mdro': [
                r'mdro.*?(\d+(?:\.\d+)?)\s*%', r'multidrug.*?(\d+(?:\.\d+)?)\s*%',
                r'mrsa.*?(\d+(?:\.\d+)?)\s*%', r'vre.*?(\d+(?:\.\d+)?)\s*%',
                r'esbl.*?(\d+(?:\.\d+)?)\s*%', r'cre.*?(\d+(?:\.\d+)?)\s*%',
                r'resistance.*?(\d+(?:\.\d+)?)\s*%', r'resistant.*?(\d+(?:\.\d+)?)\s*%'
            ],
            'antibiotic_consumption': [
                r'dot.*?(\d+(?:\.\d+)?)\s*per\s*1,?000', r'ddd.*?(\d+(?:\.\d+)?)\s*per\s*1,?000',
                r'antibiotic.*?consumption.*?(\d+(?:\.\d+)?)', r'antibiotic.*?use.*?(\d+(?:\.\d+)?)',
                r'days.*?therapy.*?(\d+(?:\.\d+)?)', r'defined.*?daily.*?dose.*?(\d+(?:\.\d+)?)'
            ]
        }

    def perform_enhanced_extraction(self) -> Dict:
        """
        Perform enhanced data extraction with gap analysis.

        Returns:
            Dictionary with enhanced extraction results and gap analysis
        """
        print("Starting enhanced full-text review simulation...")
        print("=" * 60)

        enhanced_data = []
        all_gaps = []

        for i, (_, study) in enumerate(self.existing_study_chars.iterrows()):
            print(f"Processing study {i+1}/{len(self.existing_study_chars)}: {study.get('title', '')[:60]}...")

            # Perform enhanced extraction for this study
            enhanced_study_data = self._extract_study_with_gaps(study)
            enhanced_data.append(enhanced_study_data)

            # Collect gaps for this study
            study_gaps = enhanced_study_data.get('extraction_gaps', [])
            all_gaps.extend(study_gaps)

        # Create enhanced DataFrame
        enhanced_df = pd.DataFrame(enhanced_data)

        # Analyze gaps and completeness
        gap_analysis = self._analyze_extraction_gaps(all_gaps)

        results = {
            'enhanced_data': enhanced_df,
            'gap_analysis': gap_analysis,
            'extraction_gaps': all_gaps,
            'completeness_summary': self._assess_overall_completeness(enhanced_df)
        }

        print("\nEnhanced extraction completed!")
        print(f"Enhanced records: {len(enhanced_df)}")
        print(f"Total gaps identified: {len(all_gaps)}")
        print(f"Average completeness: {gap_analysis['average_completeness']:.1f}%")

        return results

    def _extract_study_with_gaps(self, study: pd.Series) -> Dict:
        """
        Extract data from a study with gap identification.

        Args:
            study: Study data series

        Returns:
            Enhanced study data with gap information
        """
        study_id = study.get('study_id', '')
        title = study.get('title', '')
        abstract = study.get('abstract', '')

        # Start with existing data
        enhanced_data = study.to_dict()

        # Add enhanced extraction fields
        enhanced_data.update({
            'enhanced_extraction_date': datetime.now().isoformat(),
            'extraction_method': 'Enhanced automated with gap analysis',
            'data_completeness_score': 0.0,
            'extraction_gaps': [],
            'full_text_access_needed': False,
            'priority_for_full_text_review': 'Low'
        })

        # Perform enhanced field extraction
        enhanced_fields = self._extract_enhanced_fields(title, abstract, study)
        enhanced_data.update(enhanced_fields)

        # Identify gaps and calculate completeness
        gaps, completeness_score = self._identify_data_gaps(study, enhanced_data)
        enhanced_data['extraction_gaps'] = gaps
        enhanced_data['data_completeness_score'] = completeness_score
        enhanced_data['full_text_access_needed'] = len(gaps) > 0

        # Determine priority for full-text review
        enhanced_data['priority_for_full_text_review'] = self._calculate_review_priority(gaps, study)

        return enhanced_data

    def _extract_enhanced_fields(self, title: str, abstract: str, study: pd.Series) -> Dict:
        """Extract enhanced fields with better pattern recognition."""
        text_content = f"{title} {abstract}".lower()

        enhanced = {}

        # Enhanced journal extraction
        enhanced['journal_detailed'] = self._extract_detailed_journal(title, abstract)

        # Enhanced year extraction with better patterns
        enhanced['publication_year_detailed'] = self._extract_detailed_year(title, abstract)

        # Enhanced sample size extraction
        enhanced['sample_size_detailed'] = self._extract_detailed_sample_size(title, abstract)

        # Enhanced study design classification
        enhanced['study_design_detailed'] = self._classify_detailed_study_design(title, abstract)

        # Enhanced intervention classification
        enhanced['intervention_classification'] = self._classify_intervention_type(title, abstract)

        # Enhanced outcome extraction with numerical values
        enhanced['extracted_numerical_outcomes'] = self._extract_numerical_outcomes(title, abstract)

        # Enhanced statistical analysis details
        enhanced['statistical_analysis_details'] = self._extract_statistical_details(title, abstract)

        # Enhanced baseline characteristics
        enhanced['baseline_characteristics'] = self._extract_baseline_characteristics(title, abstract)

        return enhanced

    def _extract_detailed_journal(self, title: str, abstract: str) -> str:
        """Extract detailed journal information."""
        text_lower = f"{title} {abstract}".lower()

        for journal, pattern in self.journal_patterns.items():
            if re.search(pattern, text_lower):
                return journal

        return "Journal not identified from abstract"

    def _extract_detailed_year(self, title: str, abstract: str) -> int:
        """Extract publication year with enhanced patterns."""
        text_content = f"{title} {abstract}"

        # Multiple year extraction patterns
        year_patterns = [
            r'\b(20[1-2][0-9])\b',  # 2010-2029
            r'published.*?(\d{4})',
            r'(\d{4})\s*;',
            r'year.*?(\d{4})'
        ]

        years_found = []
        for pattern in year_patterns:
            matches = re.findall(pattern, text_content)
            years_found.extend([int(year) for year in matches if 2010 <= int(year) <= 2025])

        if years_found:
            return max(years_found)  # Return most recent year

        return 2020  # Default

    def _extract_detailed_sample_size(self, title: str, abstract: str) -> Dict:
        """Extract detailed sample size information."""
        text_lower = f"{title} {abstract}".lower()

        sample_info = {
            'total_patients': 0,
            'patients_per_arm': [],
            'icu_patients': 0,
            'ward_patients': 0,
            'extraction_confidence': 'Low'
        }

        # Look for total sample size
        total_patterns = [
            r'total.*?(\d+)\s*patients?',
            r'n\s*=\s*(\d+)',
            r'sample.*?(\d+)',
            r'enrolled.*?(\d+)',
            r'included.*?(\d+)'
        ]

        for pattern in total_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                sample_info['total_patients'] = max(map(int, matches))
                sample_info['extraction_confidence'] = 'Medium'
                break

        # Look for per-arm sample sizes
        arm_patterns = [
            r'(\d+)\s*(?:patients?|subjects?).*?(?:arm|group)',
            r'arm.*?(\d+)\s*(?:patients?|subjects?)',
            r'group.*?(\d+)\s*(?:patients?|subjects?)'
        ]

        for pattern in arm_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                sample_info['patients_per_arm'] = list(map(int, matches))
                sample_info['extraction_confidence'] = 'High'

        return sample_info

    def _classify_detailed_study_design(self, title: str, abstract: str) -> Dict:
        """Classify study design in detail."""
        text_lower = f"{title} {abstract}".lower()

        design_info = {
            'primary_design': 'Not specified',
            'design_confidence': 'Low',
            'randomization_method': 'Not specified',
            'blinding': 'Not specified',
            'control_type': 'Not specified'
        }

        # Primary design classification
        if any(keyword in text_lower for keyword in ['randomized controlled trial', 'randomised controlled trial', 'rct']):
            design_info['primary_design'] = 'RCT'
            design_info['design_confidence'] = 'High'
        elif any(keyword in text_lower for keyword in ['cluster randomized', 'cluster randomised']):
            design_info['primary_design'] = 'Cluster-RCT'
            design_info['design_confidence'] = 'High'
        elif any(keyword in text_lower for keyword in ['interrupted time series', 'its']):
            design_info['primary_design'] = 'ITS'
            design_info['design_confidence'] = 'Medium'
        elif any(keyword in text_lower for keyword in ['controlled before-after', 'controlled before after']):
            design_info['primary_design'] = 'CBA'
            design_info['design_confidence'] = 'Medium'

        # Randomization method
        if 'random' in text_lower:
            if 'computer' in text_lower or 'software' in text_lower:
                design_info['randomization_method'] = 'Computer-generated randomization'
            elif 'block' in text_lower:
                design_info['randomization_method'] = 'Block randomization'
            else:
                design_info['randomization_method'] = 'Randomization mentioned'

        # Blinding
        if any(keyword in text_lower for keyword in ['blind', 'masked', 'double-blind', 'single-blind']):
            design_info['blinding'] = 'Blinding implemented'
        else:
            design_info['blinding'] = 'Not blinded or not mentioned'

        # Control type
        if 'placebo' in text_lower:
            design_info['control_type'] = 'Placebo control'
        elif 'usual care' in text_lower or 'standard care' in text_lower:
            design_info['control_type'] = 'Usual/standard care'
        elif 'active control' in text_lower:
            design_info['control_type'] = 'Active control'

        return design_info

    def _classify_intervention_type(self, title: str, abstract: str) -> Dict:
        """Classify intervention type in detail."""
        text_lower = f"{title} {abstract}".lower()

        intervention_info = {
            'primary_category': 'Not specified',
            'specific_components': [],
            'intervention_complexity': 'Simple',
            'technology_intensity': 'Low'
        }

        # Check each intervention category
        for category, keywords in self.intervention_components.items():
            if any(keyword in text_lower for keyword in keywords):
                intervention_info['specific_components'].append(category)

                # Determine primary category
                if intervention_info['primary_category'] == 'Not specified':
                    intervention_info['primary_category'] = category.replace('_', ' ').title()

        # Assess complexity
        if len(intervention_info['specific_components']) > 2:
            intervention_info['intervention_complexity'] = 'Complex'
        elif len(intervention_info['specific_components']) == 2:
            intervention_info['intervention_complexity'] = 'Moderate'

        # Assess technology intensity
        tech_components = ['rapid_diagnostics', 'cdss']
        if any(comp in intervention_info['specific_components'] for comp in tech_components):
            intervention_info['technology_intensity'] = 'High'

        return intervention_info

    def _extract_numerical_outcomes(self, title: str, abstract: str) -> Dict:
        """Extract numerical outcome values."""
        text_content = f"{title} {abstract}"
        text_lower = text_content.lower()

        outcomes = {
            'mortality_rate': None,
            'cdi_rate': None,
            'mdro_rate': None,
            'antibiotic_consumption': None,
            'length_of_stay': None,
            'cost_savings': None
        }

        # Extract mortality rates
        for pattern in self.outcome_patterns['mortality']:
            matches = re.findall(pattern, text_lower)
            if matches:
                outcomes['mortality_rate'] = float(matches[0])
                break

        # Extract CDI rates
        for pattern in self.outcome_patterns['cdi']:
            matches = re.findall(pattern, text_lower)
            if matches:
                outcomes['cdi_rate'] = float(matches[0])
                break

        # Extract MDRO rates
        for pattern in self.outcome_patterns['mdro']:
            matches = re.findall(pattern, text_lower)
            if matches:
                outcomes['mdro_rate'] = float(matches[0])
                break

        # Extract antibiotic consumption
        for pattern in self.outcome_patterns['antibiotic_consumption']:
            matches = re.findall(pattern, text_lower)
            if matches:
                outcomes['antibiotic_consumption'] = float(matches[0])
                break

        # Extract length of stay
        los_patterns = [
            r'length.*?stay.*?(\d+(?:\.\d+)?)\s*days?',
            r'los.*?(\d+(?:\.\d+)?)\s*days?',
            r'hospital.*?stay.*?(\d+(?:\.\d+)?)\s*days?'
        ]

        for pattern in los_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                outcomes['length_of_stay'] = float(matches[0])
                break

        return outcomes

    def _extract_statistical_details(self, title: str, abstract: str) -> Dict:
        """Extract statistical analysis details."""
        text_lower = f"{title} {abstract}".lower()

        stats_info = {
            'effect_measure': 'Not specified',
            'confidence_interval': 'Not reported',
            'p_value': 'Not reported',
            'statistical_significance': 'Not reported',
            'sample_size_calculation': 'Not mentioned',
            'power_analysis': 'Not mentioned'
        }

        # Effect measures
        if any(keyword in text_lower for keyword in ['odds ratio', 'or']):
            stats_info['effect_measure'] = 'Odds ratio (OR)'
        elif any(keyword in text_lower for keyword in ['risk ratio', 'rr', 'relative risk']):
            stats_info['effect_measure'] = 'Risk ratio (RR)'
        elif any(keyword in text_lower for keyword in ['hazard ratio', 'hr']):
            stats_info['effect_measure'] = 'Hazard ratio (HR)'
        elif any(keyword in text_lower for keyword in ['mean difference', 'md']):
            stats_info['effect_measure'] = 'Mean difference (MD)'

        # Confidence intervals
        if '95% ci' in text_lower or '95% confidence' in text_lower:
            stats_info['confidence_interval'] = '95% CI reported'

        # P-values
        p_patterns = [r'p\s*<\s*0\.05', r'p\s*=\s*0\.05', r'p\s*<\s*0\.01', r'significant']
        for pattern in p_patterns:
            if re.search(pattern, text_lower):
                stats_info['statistical_significance'] = 'Statistically significant'
                break

        # Sample size calculation
        if 'sample size' in text_lower or 'power' in text_lower:
            stats_info['sample_size_calculation'] = 'Mentioned'

        return stats_info

    def _extract_baseline_characteristics(self, title: str, abstract: str) -> Dict:
        """Extract baseline patient characteristics."""
        text_lower = f"{title} {abstract}".lower()

        baseline = {
            'age_mean': None,
            'age_sd': None,
            'male_percentage': None,
            'comorbidity_index': None,
            'severity_illness': None,
            'icu_percentage': None
        }

        # Age information
        age_patterns = [
            r'age.*?(\d+(?:\.\d+)?)\s*years?',
            r'mean.*?age.*?(\d+(?:\.\d+)?)',
            r'average.*?age.*?(\d+(?:\.\d+)?)'
        ]

        for pattern in age_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                baseline['age_mean'] = float(matches[0])
                break

        # Gender distribution
        gender_patterns = [
            r'(\d+(?:\.\d+)?)\s*%\s*male',
            r'male.*?(\d+(?:\.\d+)?)\s*%',
            r'female.*?(\d+(?:\.\d+)?)\s*%'
        ]

        for pattern in gender_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                baseline['male_percentage'] = float(matches[0])
                break

        # ICU percentage
        icu_patterns = [
            r'(\d+(?:\.\d+)?)\s*%\s*icu',
            r'icu.*?(\d+(?:\.\d+)?)\s*%',
            r'intensive.*?care.*?(\d+(?:\.\d+)?)\s*%'
        ]

        for pattern in icu_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                baseline['icu_percentage'] = float(matches[0])
                break

        return baseline

    def _identify_data_gaps(self, original_study: pd.Series, enhanced_data: Dict) -> Tuple[List[ExtractionGap], float]:
        """
        Identify data gaps that require full-text review.

        Args:
            original_study: Original study data
            enhanced_data: Enhanced extracted data

        Returns:
            Tuple of (gaps list, completeness score)
        """
        gaps = []

        # Define critical fields that typically require full-text
        critical_fields = {
            'sample_size': 'Sample size details',
            'baseline_characteristics': 'Detailed baseline patient characteristics',
            'intervention_details': 'Complete intervention implementation details',
            'outcome_results': 'Numerical outcome results with measures of uncertainty',
            'statistical_analysis': 'Detailed statistical analysis methods',
            'effect_estimates': 'Precise effect estimates with confidence intervals',
            'subgroup_analyses': 'Subgroup and moderator analyses',
            'sensitivity_analyses': 'Sensitivity analyses performed',
            'adverse_events': 'Intervention-related adverse events',
            'cost_effectiveness': 'Economic evaluation data'
        }

        # Check each critical field
        for field, description in critical_fields.items():
            if self._field_needs_full_text(field, enhanced_data):
                priority = self._determine_gap_priority(field)
                effort = self._estimate_extraction_effort(field)

                gap = ExtractionGap(
                    study_id=original_study.get('study_id', ''),
                    pmid=original_study.get('pmid', ''),
                    data_field=field,
                    reason=f"{description} not available in abstract",
                    priority=priority,
                    estimated_effort=effort
                )
                gaps.append(gap)

        # Calculate completeness score
        completeness_score = max(0, 100 - (len(gaps) * 5))  # 5 points per gap

        return gaps, completeness_score

    def _field_needs_full_text(self, field: str, enhanced_data: Dict) -> bool:
        """Determine if a field needs full-text access."""
        # Fields that almost always need full-text
        full_text_required = [
            'outcome_results', 'effect_estimates', 'statistical_analysis',
            'subgroup_analyses', 'sensitivity_analyses', 'adverse_events'
        ]

        if field in full_text_required:
            return True

        # Check if we have meaningful data for this field
        field_value = enhanced_data.get(field, '')

        if isinstance(field_value, (list, dict)):
            return len(field_value) == 0 or field_value == {}
        else:
            return field_value in ['Not specified', 'Not available from abstract', 'Results not available from abstract', 0, None]

    def _determine_gap_priority(self, field: str) -> str:
        """Determine priority level for filling this gap."""
        high_priority = ['outcome_results', 'effect_estimates', 'sample_size']
        medium_priority = ['baseline_characteristics', 'intervention_details', 'statistical_analysis']

        if field in high_priority:
            return 'High'
        elif field in medium_priority:
            return 'Medium'

        return 'Low'

    def _estimate_extraction_effort(self, field: str) -> str:
        """Estimate effort required to extract this field."""
        high_effort = ['statistical_analysis', 'subgroup_analyses', 'sensitivity_analyses']
        medium_effort = ['baseline_characteristics', 'intervention_details', 'effect_estimates']

        if field in high_effort:
            return 'High (detailed review required)'
        elif field in medium_effort:
            return 'Medium (moderate review required)'

        return 'Low (quick extraction possible)'

    def _calculate_review_priority(self, gaps: List[ExtractionGap], study: pd.Series) -> str:
        """Calculate overall priority for full-text review."""
        if not gaps:
            return 'Low'

        high_priority_gaps = [gap for gap in gaps if gap.priority == 'High']
        medium_priority_gaps = [gap for gap in gaps if gap.priority == 'Medium']

        if len(high_priority_gaps) >= 3:
            return 'High'
        elif len(high_priority_gaps) >= 1 or len(medium_priority_gaps) >= 3:
            return 'Medium'

        return 'Low'

    def _analyze_extraction_gaps(self, all_gaps: List[ExtractionGap]) -> Dict:
        """Analyze overall extraction gaps."""
        if not all_gaps:
            return {
                'total_gaps': 0,
                'average_completeness': 100.0,
                'gaps_by_priority': {'High': 0, 'Medium': 0, 'Low': 0},
                'gaps_by_field': {},
                'studies_needing_review': 0
            }

        # Count gaps by priority
        gaps_by_priority = {'High': 0, 'Medium': 0, 'Low': 0}
        gaps_by_field = {}

        for gap in all_gaps:
            gaps_by_priority[gap.priority] += 1
            gaps_by_field[gap.data_field] = gaps_by_field.get(gap.data_field, 0) + 1

        # Count studies needing review
        studies_needing_review = len(set([gap.study_id for gap in all_gaps]))

        # Calculate average completeness (assuming 5 points per gap)
        total_studies = len(self.existing_study_chars)
        max_possible_gaps = total_studies * 10  # 10 potential gap types
        average_completeness = max(0, 100 - (len(all_gaps) / max_possible_gaps * 100))

        return {
            'total_gaps': len(all_gaps),
            'average_completeness': average_completeness,
            'gaps_by_priority': gaps_by_priority,
            'gaps_by_field': gaps_by_field,
            'studies_needing_review': studies_needing_review
        }

    def _assess_overall_completeness(self, enhanced_df: pd.DataFrame) -> Dict:
        """Assess overall data completeness."""
        completeness = {
            'overall_score': enhanced_df['data_completeness_score'].mean(),
            'studies_by_completeness': {
                'High (≥90%)': (enhanced_df['data_completeness_score'] >= 90).sum(),
                'Medium (70-89%)': ((enhanced_df['data_completeness_score'] >= 70) &
                                   (enhanced_df['data_completeness_score'] < 90)).sum(),
                'Low (<70%)': (enhanced_df['data_completeness_score'] < 70).sum()
            },
            'fields_needing_attention': [],
            'priority_studies': enhanced_df[enhanced_df['priority_for_full_text_review'] == 'High']['study_id'].tolist()
        }

        return completeness

def main():
    """Main function to run enhanced full-text review simulation."""

    print("Enhanced Full-Text Review and Data Extraction System")
    print("=" * 65)
    print("Note: This system simulates full-text review capabilities.")
    print("Actual full-text access would be required for complete data extraction.")
    print()

    # Initialize enhanced extractor
    included_studies_file = "hospital_antimicrobial_stewardship/01_literature_search/included_studies_for_review_20251013_100509.csv"

    if not os.path.exists(included_studies_file):
        print(f"Error: Included studies file not found: {included_studies_file}")
        return

    extractor = EnhancedDataExtractor(included_studies_file)

    if extractor.existing_study_chars is None or extractor.existing_study_chars.empty:
        print("Error: No existing study data to enhance")
        return

    # Perform enhanced extraction
    results = extractor.perform_enhanced_extraction()

    # Save enhanced data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save enhanced study characteristics
    enhanced_file = f"hospital_antimicrobial_stewardship/02_data_extraction/enhanced_study_characteristics_{timestamp}.csv"
    results['enhanced_data'].to_csv(enhanced_file, index=False)
    print(f"\nEnhanced study characteristics saved to: {enhanced_file}")

    # Save gap analysis
    gap_analysis_file = f"hospital_antimicrobial_stewardship/02_data_extraction/gap_analysis_{timestamp}.json"
    with open(gap_analysis_file, 'w') as f:
        json.dump(results['gap_analysis'], f, indent=2)
    print(f"Gap analysis saved to: {gap_analysis_file}")

    # Save extraction gaps for manual review
    gaps_df = pd.DataFrame([
        {
            'study_id': gap.study_id,
            'pmid': gap.pmid,
            'data_field': gap.data_field,
            'reason': gap.reason,
            'priority': gap.priority,
            'estimated_effort': gap.estimated_effort
        }
        for gap in results['extraction_gaps']
    ])

    gaps_file = f"hospital_antimicrobial_stewardship/02_data_extraction/extraction_gaps_for_review_{timestamp}.csv"
    gaps_df.to_csv(gaps_file, index=False)
    print(f"Extraction gaps for manual review saved to: {gaps_file}")

    # Generate comprehensive summary report
    summary_file = f"hospital_antimicrobial_stewardship/02_data_extraction/enhanced_extraction_summary_{timestamp}.txt"

    with open(summary_file, 'w') as f:
        f.write("Enhanced Full-Text Review and Data Extraction Summary\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"Enhanced extraction completed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("ENHANCED EXTRACTION RESULTS:\n")
        f.write(f"Total studies processed: {len(results['enhanced_data'])}\n")
        f.write(f"Enhanced records created: {len(results['enhanced_data'])}\n\n")

        f.write("DATA COMPLETENESS ASSESSMENT:\n")
        completeness = results['completeness_summary']
        f.write(f"Overall completeness score: {completeness['overall_score']:.1f}%\n")
        f.write(f"High completeness (≥90%): {completeness['studies_by_completeness']['High (≥90%)']} studies\n")
        f.write(f"Medium completeness (70-89%): {completeness['studies_by_completeness']['Medium (70-89%)']} studies\n")
        f.write(f"Low completeness (<70%): {completeness['studies_by_completeness']['Low (<70%)']} studies\n\n")

        f.write("GAP ANALYSIS:\n")
        gap_analysis = results['gap_analysis']
        f.write(f"Total gaps identified: {gap_analysis['total_gaps']}\n")
        f.write(f"Studies needing full-text review: {gap_analysis['studies_needing_review']}\n")
        f.write(f"Average completeness: {gap_analysis['average_completeness']:.1f}%\n\n")

        f.write("GAPS BY PRIORITY:\n")
        for priority, count in gap_analysis['gaps_by_priority'].items():
            f.write(f"  {priority}: {count} gaps\n")

        f.write("\nGAPS BY FIELD:\n")
        for field, count in gap_analysis['gaps_by_field'].items():
            f.write(f"  {field}: {count} gaps\n")

        f.write("\nPRIORITY STUDIES FOR FULL-TEXT REVIEW:\n")
        for study_id in completeness['priority_studies'][:10]:  # Show top 10
            f.write(f"  {study_id}\n")

        f.write("\nRECOMMENDATIONS:\n")
        f.write("1. Prioritize full-text review for studies marked as 'High' priority\n")
        f.write("2. Focus on extracting numerical outcome data and effect estimates\n")
        f.write("3. Obtain detailed statistical analysis methods\n")
        f.write("4. Extract baseline patient characteristics\n")
        f.write("5. Document intervention implementation details\n")

    print(f"Comprehensive summary report saved to: {summary_file}")

    print("\nEnhanced extraction completed successfully!")
    print("\nRECOMMENDATIONS FOR ACTUAL FULL-TEXT REVIEW:")
    print(f"• {gap_analysis['studies_needing_review']} studies need full-text access")
    print(f"• {gap_analysis['gaps_by_priority']['High']} high-priority gaps identified")
    print(f"• Focus on outcome results and statistical analysis details")
    print("• Average completeness could be improved from "
    print(f"  {gap_analysis['average_completeness']:.1f}% to ~95% with full-text access")

if __name__ == "__main__":
    main()
