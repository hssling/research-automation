#!/usr/bin/env python3
"""
Batch Data Extraction Starter for Hospital Antimicrobial Stewardship
Network Meta-Analysis

This script provides a systematic batch extraction workflow, starting with
high-priority studies based on the prioritized review plan.

Author: Research Team
Date: October 13, 2025
"""

import pandas as pd
import json
import os
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple

class BatchExtractionManager:
    """Manages batch data extraction workflow."""

    def __init__(self, review_plan_file: str, included_studies_file: str):
        """
        Initialize batch extraction manager.

        Args:
            review_plan_file: Path to review plan JSON (may be None)
            included_studies_file: Path to included studies CSV
        """
        self.review_plan_file = review_plan_file
        self.included_studies_file = included_studies_file

        # Load data
        self.review_plan = self._load_review_plan()
        self.studies_df = pd.read_csv(included_studies_file)

    def _load_review_plan(self) -> Dict:
        """Load review plan from JSON file."""
        if self.review_plan_file and os.path.exists(self.review_plan_file):
            with open(self.review_plan_file, 'r') as f:
                return json.load(f)
        return None

    def select_initial_batch(self, batch_size: int = 10) -> Tuple[pd.DataFrame, Dict]:
        """
        Select initial batch of high-priority studies for extraction.

        Args:
            batch_size: Number of studies per batch

        Returns:
            Tuple of (batch_studies_df, batch_info_dict)
        """
        print("Selecting initial batch of high-priority studies...")

        # Get prioritized studies from review plan
        high_priority_studies = self.review_plan['studies_by_priority']['Medium'][:batch_size]
        # Note: High priority array was empty, so using Medium priority

        # Extract study IDs
        high_priority_ids = [study['study_id'] for study in high_priority_studies]

        # Filter studies dataframe
        batch_studies_df = self.studies_df[self.studies_df['study_id'].isin(high_priority_ids)].copy()

        # Add priority information
        priority_map = {study['study_id']: study for study in high_priority_studies}
        batch_studies_df['priority_level'] = 'Medium'
        batch_studies_df['estimated_time'] = batch_studies_df['study_id'].map(
            lambda x: priority_map[x]['estimated_time']
        )
        batch_studies_df['extraction_targets'] = batch_studies_df['study_id'].map(
            lambda x: priority_map[x]['key_targets']
        )

        # Create batch info
        batch_info = {
            'batch_number': 1,
            'batch_size': len(batch_studies_df),
            'priority_level': 'Medium (High priority array was empty)',
            'selection_criteria': f'Top {batch_size} Medium priority studies from review plan',
            'estimated_completion_time': f"{len(batch_studies_df) * 52} minutes (45-60 min per study)",
            'extraction_priorities': ['mortality', 'cdi', 'mdro', 'antibiotic_consumption']
        }

        print(f"Selected {len(batch_studies_df)} studies for initial batch")
        print(f"Priority level: {batch_info['priority_level']}")
        print(f"Estimated batch completion: {batch_info['estimated_completion_time']}")

        return batch_studies_df, batch_info

    def select_second_batch(self, batch_size: int = 10) -> Tuple[pd.DataFrame, Dict]:
        """
        Select batch from included studies based on mortality outcomes and complex interventions.
        If no review plan exists, use simple selection criteria.

        Args:
            batch_size: Number of studies per batch

        Returns:
            Tuple of (batch_studies_df, batch_info_dict)
        """
        print("Selecting high-impact studies for batch extraction...")

        if self.review_plan is None:
            # Simple selection when no review plan exists
            # Prioritize studies with mortality, stewardship, and complex interventions in titles
            print("Using simple selection criteria based on title keywords...")

            high_priority_keywords = ['mortality', 'death', 'survival', 'fatal']
            medium_priority_keywords = ['antimicrobial stewardship', 'antibiotic stewardship',
                                        'combination', 'multifaceted', 'bundle']

            # Score studies by keyword matches
            study_scores = []
            for _, study in self.studies_df.iterrows():
                title = str(study.get('title', '')).lower()
                score = 0

                # High priority: mortality related
                if any(kw in title for kw in high_priority_keywords):
                    score += 3

                # Medium priority: stewardship interventions
                if any(kw in title for kw in medium_priority_keywords):
                    score += 2

                # Complex interventions
                if any(kw in title for kw in ['combination', 'multifaceted', 'bundle', 'intensive', 'icu']):
                    score += 1

                study_scores.append((study['study_id'], score))

            # Sort by score and select top batch_size
            study_scores.sort(key=lambda x: x[1], reverse=True)
            selected_ids = [sid for sid, score in study_scores[:batch_size]]

            # Filter studies
            batch_studies_df = self.studies_df[self.studies_df['study_id'].isin(selected_ids)].copy()

            # Add basic priority info
            batch_studies_df['priority_level'] = 'High Impact (Title-based)'
            batch_studies_df['estimated_time'] = '50 minutes'
            # Create extraction targets as a list repeated for each study
            batch_studies_df['extraction_targets'] = [ ['mortality', 'cdi', 'mdro', 'antibiotic_consumption'] ] * len(batch_studies_df)

        else:
            # Original logic with review plan
            low_priority_studies = self.review_plan['studies_by_priority']['Low']

            # Prioritize studies with mortality outcomes and complex interventions
            high_impact_studies = []
            medium_impact_studies = []

            for study in low_priority_studies[:50]:  # Look at first 50 for high impact
                title = study['title'].lower()
                targets = study['key_targets']

                # High impact: mortality outcomes + complex interventions
                if ('mortality' in ' '.join(targets) or 'mortality' in title) and \
                   any(keyword in title for keyword in ['combination', 'multifaceted', 'bundle', 'intensive', 'icu']):
                    high_impact_studies.append(study)

                # Medium impact: just mortality outcomes
                elif 'mortality' in ' '.join(targets) or 'mortality' in title:
                    medium_impact_studies.append(study)

            # Select from high impact first, then medium impact
            selected_studies = []
            selected_studies.extend(high_impact_studies[:batch_size//2])  # Half from high impact
            remaining_needed = batch_size - len(selected_studies)
            selected_studies.extend(medium_impact_studies[:remaining_needed])

            # Extract study IDs
            selected_ids = [study['study_id'] for study in selected_studies]

            # Filter studies dataframe
            batch_studies_df = self.studies_df[self.studies_df['study_id'].isin(selected_ids)].copy()

            # Add priority information
            priority_map = {study['study_id']: study for study in selected_studies}
            batch_studies_df['priority_level'] = 'Low-High Impact'
            batch_studies_df['estimated_time'] = batch_studies_df['study_id'].map(
                lambda x: priority_map[x]['estimated_time']
            )
            batch_studies_df['extraction_targets'] = batch_studies_df['study_id'].map(
                lambda x: priority_map[x]['key_targets']
            )

        # Create batch info
        batch_info = {
            'batch_number': 1,  # Changed to 1 since it's Batch 1: Medium priority studies
            'batch_size': len(batch_studies_df),
            'priority_level': 'High Impact (Title-based selection)',
            'selection_criteria': 'Studies with mortality outcomes and complex antimicrobial stewardship interventions',
            'estimated_completion_time': f"{len(batch_studies_df) * 50} minutes (45-60 min per study)",
            'extraction_priorities': ['mortality', 'cdi', 'mdro', 'antibiotic_consumption']
        }

        print(f"Selected {len(batch_studies_df)} high-impact studies for batch extraction")
        print(f"Priority level: {batch_info['priority_level']}")
        print(f"Estimated batch completion: {batch_info['estimated_completion_time']}")

        return batch_studies_df, batch_info

    def prepare_extraction_forms(self, batch_studies_df: pd.DataFrame, batch_info: Dict) -> Dict:
        """
        Prepare extraction forms for the batch.

        Args:
            batch_studies_df: DataFrame with batch studies
            batch_info: Batch information dictionary

        Returns:
            Dictionary with extraction forms and templates
        """
        print("\nPreparing extraction forms...")

        # Initialize extraction forms
        extraction_forms = {
            'batch_info': batch_info,
            'study_characteristics_form': self._create_study_characteristics_form(batch_studies_df),
            'intervention_details_form': self._create_intervention_details_form(batch_studies_df),
            'outcome_data_form': self._create_outcome_data_form(batch_studies_df),
            'quality_assessment_form': self._create_quality_assessment_form(batch_studies_df),
            'extraction_checklist': self._create_extraction_checklist(),
            'validation_rules': self._create_validation_rules()
        }

        return extraction_forms

    def _create_study_characteristics_form(self, df: pd.DataFrame) -> Dict:
        """Create study characteristics extraction form."""
        form_template = {
            'columns': [
                'study_id', 'pmid', 'title', 'author', 'journal', 'year', 'doi',
                'study_design', 'unit_randomization', 'study_duration_months',
                'number_arms', 'sample_size_per_arm', 'inclusion_criteria',
                'exclusion_criteria', 'setting_type', 'hospital_beds',
                'geographic_region', 'country', 'funding_source',
                'ethical_approval', 'trial_registration', 'extractor_initials',
                'extraction_date', 'verification_status', 'verification_notes'
            ],
            'data_types': {
                'sample_size_per_arm': 'integer',
                'study_duration_months': 'float',
                'number_arms': 'integer',
                'hospital_beds': 'integer'
            },
            'required_fields': [
                'study_id', 'pmid', 'title', 'study_design', 'sample_size_per_arm',
                'setting_type', 'geographic_region', 'extractor_initials', 'extraction_date'
            ],
            'validation_rules': {
                'sample_size_per_arm': '>0',
                'study_duration_months': '>0',
                'number_arms': '>0 and <=10'
            }
        }

        # Initialize empty form for batch
        initial_data = []
        for _, study in df.iterrows():
            row = {col: '' for col in form_template['columns']}
            row.update({
                'study_id': study.get('study_id', ''),
                'pmid': study.get('pmid', ''),
                'title': study.get('title', ''),
                'extractor_initials': 'TBD',
                'extraction_date': datetime.now().strftime('%Y-%m-%d'),
                'verification_status': 'Pending'
            })
            initial_data.append(row)

        form_template['initial_data'] = initial_data
        return form_template

    def _create_intervention_details_form(self, df: pd.DataFrame) -> Dict:
        """Create intervention details extraction form."""
        form_template = {
            'columns': [
                'study_id', 'pmid', 'study_design', 'intervention_category',
                'intervention_components', 'intervention_intensity',
                'intervention_frequency', 'intervention_duration_months',
                'technology_requirements', 'personnel_fte', 'training_provided',
                'training_method', 'implementation_team', 'fidelity_measures',
                'process_measures', 'comparator_description', 'standard_practices',
                'intervention_development', 'implementation_challenges',
                'sustainability_plan', 'extractor_initials', 'extraction_date'
            ],
            'intervention_categories': [
                'Pre-authorization/prior approval',
                'Prospective audit and feedback (PAF)',
                'Rapid diagnostic pathways',
                'Computerized decision support (CDSS)/e-prescribing',
                'Education and guidelines',
                'Combination interventions'
            ],
            'required_fields': [
                'study_id', 'pmid', 'intervention_category', 'intervention_components',
                'implementation_team', 'comparator_description', 'extractor_initials'
            ]
        }

        # Initialize empty form
        initial_data = []
        for _, study in df.iterrows():
            row = {col: '' for col in form_template['columns']}
            row.update({
                'study_id': study.get('study_id', ''),
                'pmid': study.get('pmid', ''),
                'study_design': 'ITS',  # Most are ITS
                'extractor_initials': 'TBD',
                'extraction_date': datetime.now().strftime('%Y-%m-%d')
            })
            initial_data.append(row)

        form_template['initial_data'] = initial_data
        return form_template

    def _create_outcome_data_form(self, df: pd.DataFrame) -> Dict:
        """Create outcome data extraction form."""
        form_template = {
            'columns': [
                'study_id', 'pmid', 'outcome_name', 'outcome_definition',
                'measurement_method', 'time_points', 'baseline_value',
                'post_value', 'absolute_change', 'relative_change',
                'effect_estimate', 'confidence_interval_lower',
                'confidence_interval_upper', 'p_value', 'statistical_model',
                'adjustment_variables', 'missing_data_handling',
                'intention_to_treat', 'clinical_significance', 'extractor_initials',
                'extraction_date', 'data_source_page'
            ],
            'outcome_categories': {
                'mortality': ['30-day mortality', 'In-hospital mortality', 'All-cause mortality'],
                'cdi_incidence': ['CDI cases per 10,000 patient-days'],
                'mdro_incidence': ['MRSA bacteremia', 'VRE bacteremia', 'CRE bacteremia', 'ESBL+ bacteremia'],
                'antibiotic_consumption': ['DOT per 1,000 patient-days', 'DDD per 1,000 patient-days'],
                'length_of_stay': ['Mean LOS (days)'],
                'costs': ['Total antibiotic costs ($)', 'Cost per patient ($)']
            },
            'data_types': {
                'baseline_value': 'float',
                'post_value': 'float',
                'absolute_change': 'float',
                'relative_change': 'float',
                'confidence_interval_lower': 'float',
                'confidence_interval_upper': 'float',
                'p_value': 'float',
                'data_source_page': 'string'
            },
            'validation_rules': {
                'p_value': '>=0 and <=1',
                'effect_estimate': '!=0',
                'confidence_interval_lower': '!=""',
                'confidence_interval_upper': '!=""'
            }
        }

        # Initialize form with one row per primary outcome per study
        initial_data = []
        study_outcomes = {
            'mortality': '30-day mortality',
            'cdi_incidence': 'CDI per 10,000 patient-days',
            'mdro_incidence': 'MRSA/VRE/CRE bacteremia rates',
            'antibiotic_consumption': 'DOT/DDD per 1,000 patient-days'
        }

        for _, study in df.iterrows():
            targets = study.get('extraction_targets', [])
            for target in targets:
                if target in study_outcomes:
                    row = {col: '' for col in form_template['columns']}
                    row.update({
                        'study_id': study.get('study_id', ''),
                        'pmid': study.get('pmid', ''),
                        'outcome_name': target,
                        'outcome_definition': study_outcomes[target],
                        'measurement_method': 'Prospective surveillance',
                        'statistical_model': 'ITS analysis',
                        'extractor_initials': 'TBD',
                        'extraction_date': datetime.now().strftime('%Y-%m-%d')
                    })
                    initial_data.append(row)

        form_template['initial_data'] = initial_data
        return form_template

    def _create_quality_assessment_form(self, df: pd.DataFrame) -> Dict:
        """Create quality assessment form based on study design."""
        form_template = {
            'rob_2_domains': {
                '1_randomization_process': {
                    'description': 'Randomization process adequately described?',
                    'options': ['Yes', 'No', 'Not applicable (not RCT)']
                },
                '2_deviations_from_intervention': {
                    'description': 'Deviations from intended interventions avoided?',
                    'options': ['Yes', 'No', 'Not applicable (not RCT)']
                },
                '3_missing_outcome_data': {
                    'description': 'Missing outcome data adequately addressed?',
                    'options': ['Yes', 'No', 'Not applicable']
                },
                '4_measurement_of_outcomes': {
                    'description': 'Outcome measures well-defined and consistently applied?',
                    'options': ['Yes', 'No', 'Not applicable']
                },
                '5_selection_of_reported_results': {
                    'description': 'Selection of reported results appropriate?',
                    'options': ['Yes', 'No', 'Not applicable']
                }
            },
            'its_domains': {
                '1_secular_trends': {
                    'description': 'Protection against secular changes?',
                    'options': ['Adequate', 'Inadequate', 'Unsure']
                },
                '2_detection_bias': {
                    'description': 'Protection against detection bias?',
                    'options': ['Adequate', 'Inadequate', 'Unsure']
                },
                '3_outcome_completeness': {
                    'description': 'Completeness of outcome data adequate?',
                    'options': ['Adequate', 'Inadequate', 'Unsure']
                },
                '4_baseline_characteristics': {
                    'description': 'Baseline characteristics similar?',
                    'options': ['Similar', 'Not similar', 'Unsure']
                }
            },
            'columns': [
                'study_id', 'pmid', 'assessment_type', 'domain', 'assessment',
                'supporting_evidence', 'judgment', 'overall_rob', 'comments',
                'assessor_initials', 'assessment_date'
            ]
        }

        # Initialize form
        initial_data = []
        for _, study in df.iterrows():
            study_design = 'ITS'  # Most studies in this batch

            domains = form_template['its_domains'] if study_design == 'ITS' else form_template['rob_2_domains']

            for domain_key, domain_info in domains.items():
                row = {
                    'study_id': study.get('study_id', ''),
                    'pmid': study.get('pmid', ''),
                    'assessment_type': 'ITS' if study_design == 'ITS' else 'RoB-2',
                    'domain': domain_info['description'],
                    'assessment': '',
                    'supporting_evidence': '',
                    'judgment': '',
                    'overall_rob': '',
                    'comments': '',
                    'assessor_initials': 'TBD',
                    'assessment_date': datetime.now().strftime('%Y-%m-%d')
                }
                initial_data.append(row)

        form_template['initial_data'] = initial_data
        return form_template

    def _create_extraction_checklist(self) -> List[Dict]:
        """Create extraction checklist for reviewers."""
        return [
            {
                'step': 1,
                'description': 'Obtain full-text article',
                'required_actions': ['Access PDF or PMC', 'Note access date', 'Check for supplementary materials'],
                'completion_criteria': ['PDF obtained and readable'],
                'estimated_time': '5-10 minutes'
            },
            {
                'step': 2,
                'description': 'Read abstract and introduction',
                'required_actions': ['Note study objectives', 'Identify study design', 'Note inclusion/exclusion criteria'],
                'completion_criteria': ['Study purpose understood'],
                'estimated_time': '10 minutes'
            },
            {
                'step': 3,
                'description': 'Extract study characteristics',
                'required_actions': ['Complete all required fields', 'Note any missing information', 'Document data sources'],
                'completion_criteria': ['All required fields completed'],
                'estimated_time': '15-20 minutes'
            },
            {
                'step': 4,
                'description': 'Extract intervention details',
                'required_actions': ['Identify primary intervention type', 'Document all components', 'Note implementation team'],
                'completion_criteria': ['Intervention fully characterized'],
                'estimated_time': '20-25 minutes'
            },
            {
                'step': 5,
                'description': 'Extract outcome data',
                'required_actions': ['Record all effect estimates with CIs', 'Note measurement methods', 'Document statistical models'],
                'completion_criteria': ['Effect estimates and uncertainty measures captured'],
                'estimated_time': '25-30 minutes'
            },
            {
                'step': 6,
                'description': 'Complete quality assessment',
                'required_actions': ['Score all domains', 'Provide supporting evidence', 'Make overall judgment'],
                'completion_criteria': ['All domains assessed'],
                'estimated_time': '15-20 minutes'
            },
            {
                'step': 7,
                'description': 'Cross-check extractions',
                'required_actions': ['Verify data consistency', 'Check calculations', 'Flag uncertainties'],
                'completion_criteria': ['Extraction validated'],
                'estimated_time': '10 minutes'
            },
            {
                'step': 8,
                'description': 'Complete and submit',
                'required_actions': ['Save all forms', 'Generate extraction report', 'Submit for verification'],
                'completion_criteria': ['All forms submitted'],
                'estimated_time': '5 minutes'
            }
        ]

    def _create_validation_rules(self) -> Dict:
        """Create validation rules for extracted data."""
        return {
            'study_characteristics': {
                'sample_size_per_arm': {'type': 'integer', 'range': [1, 10000]},
                'study_duration_months': {'type': 'float', 'range': [1, 120]},
                'number_arms': {'type': 'integer', 'range': [2, 10]}
            },
            'outcome_data': {
                'effect_estimate': {'type': 'float', 'range': [-100, 100]},
                'confidence_interval_lower': {'type': 'float'},
                'confidence_interval_upper': {'type': 'float'},
                'p_value': {'type': 'float', 'range': [0, 1]}
            },
            'cross_validation_rules': [
                'CI lower bound should be < effect estimate',
                'CI upper bound should be > effect estimate',
                'Effect direction should match verbal description',
                'Sample sizes should be consistent between text and tables'
            ]
        }

    def generate_batch_package(self, batch_studies_df: pd.DataFrame, extraction_forms: Dict) -> Dict:
        """
        Generate complete batch extraction package.

        Args:
            batch_studies_df: Batch studies DataFrame
            extraction_forms: Extraction forms dictionary

        Returns:
            Complete batch package dictionary
        """
        print("Generating batch extraction package...")

        # Create batch package
        batch_package = {
            'batch_metadata': {
                'batch_number': extraction_forms['batch_info']['batch_number'],
                'creation_date': datetime.now().isoformat(),
                'batch_size': len(batch_studies_df),
                'estimated_completion_time': extraction_forms['batch_info']['estimated_completion_time'],
                'priority_level': extraction_forms['batch_info']['priority_level'],
                'extraction_deadline': (datetime.now().replace(day=datetime.now().day + 14)).strftime('%Y-%m-%d')
            },
            'studies_list': batch_studies_df.to_dict('records'),
            'extraction_forms': extraction_forms,
            'quality_control': {
                'double_extraction_required': True,
                'minimum_double_extraction_percentage': 20,
                'discrepancy_resolution_process': 'Third reviewer arbitration',
                'acceptance_criteria': '100% agreement on intervention classification, effect estimates within 10% for continuous outcomes'
            },
            'progress_tracking': {
                'total_studies': len(batch_studies_df),
                'completed_studies': 0,
                'verified_studies': 0,
                'pending_verification': len(batch_studies_df)
            },
            'resources': {
                'extraction_manual': 'Refer to workflow guide in main directory',
                'data_dictionary': 'Available in project docs',
                'support_contact': 'Team lead for extraction questions'
            }
        }

        return batch_package

def main():
    """Main function to create batch extraction package."""

    print("Hospital Antimicrobial Stewardship Batch Data Extraction Starter")
    print("=" * 70)

    # File paths - dynamically find the latest review plan
    import glob
    review_plan_pattern = "../01_literature_search/full_text_review_plan_*.json"
    matching_files = glob.glob(review_plan_pattern)
    if matching_files:
        review_plan_file = matching_files[-1]  # Get the latest file
        print(f"Found review plan file: {review_plan_file}")
    else:
        # If no review plan exists, create a simple batch from medium priority studies
        print("No review plan found, creating batch from included studies directly...")
        review_plan_file = None

    included_studies_file = "../01_literature_search/included_studies_for_review_20251013_100509.csv"

    # Check if files exist
    if review_plan_file and not os.path.exists(review_plan_file):
        print(f"Error: Review plan file not found: {review_plan_file}")
        return

    if not os.path.exists(included_studies_file):
        print(f"Error: Included studies file not found: {included_studies_file}")
        return

    print("🔄 AVAILABLE BATCH OPTIONS:")
    print("  1. Batch 1: Medium priority studies (Already deployed)")
    print("  2. Batch 2: High-impact low-priority studies (Recommended)")
    print("  3. Batch 3: Remaining low-priority studies")
    print("  4. Custom batch selection")

    # For now, proceed with Batch 2 (next logical step)
    print("\n🚀 Creating BATCH 2: High-impact low-priority studies...")

    # Initialize batch manager
    batch_manager = BatchExtractionManager(review_plan_file, included_studies_file)

    # Select high-impact studies from low-priority pool
    batch_studies_df, batch_info = batch_manager.select_second_batch(batch_size=10)

    if batch_studies_df.empty:
        print("Error: No studies selected for batch extraction")
        return

    # Prepare extraction forms
    extraction_forms = batch_manager.prepare_extraction_forms(batch_studies_df, batch_info)

    # Generate batch package
    batch_package = batch_manager.generate_batch_package(batch_studies_df, extraction_forms)

    # Save batch package
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save batch package
    batch_package_file = f"batch_extraction_package_{timestamp}.json"
    with open(batch_package_file, 'w') as f:
        json.dump(batch_package, f, indent=2)
    print(f"\nBatch extraction package saved to: {batch_package_file}")

    # Save batch studies
    batch_studies_file = f"batch_{batch_info['batch_number']}_studies_{timestamp}.csv"
    batch_studies_df.to_csv(batch_studies_file, index=False)
    print(f"Batch studies saved to: {batch_studies_file}")

    # Generate batch instructions
    instructions_file = f"batch_{batch_info['batch_number']}_extraction_instructions_{timestamp}.txt"

    with open(instructions_file, 'w') as f:
        f.write(f"Batch {batch_info['batch_number']} Data Extraction Instructions\n")
        f.write("=" * 40 + "\n\n")

        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("BATCH OVERVIEW:\n")
        f.write(f"  • Batch number: {batch_info['batch_number']}\n")
        f.write(f"  • Number of studies: {batch_info['batch_size']}\n")
        f.write(f"  • Priority level: {batch_info['priority_level']}\n")
        f.write(f"  • Estimated completion time: {batch_info['estimated_completion_time']}\n")
        f.write(f"  • Deadline: {batch_package['batch_metadata']['extraction_deadline']}\n\n")

        f.write("EXTRACTION PRIORITIES:\n")
        for i, priority in enumerate(batch_info['extraction_priorities'], 1):
            f.write(f"  {i}. {priority}\n")
        f.write("\n")

        f.write("REQUIRED FILES:\n")
        f.write(f"  • batch_{batch_info['batch_number']}_studies_*.csv - Study list with priorities\n")
        f.write("  • batch_extraction_package_*.json - Complete extraction forms\n")
        f.write("  • workflow_guide_*.txt - Step-by-step instructions\n\n")

        f.write("QUALITY CONTROL REQUIREMENTS:\n")
        f.write("  • Double extraction: 20% of studies\n")
        f.write("  • Discrepancy resolution: Third reviewer arbitration\n")
        f.write("  • Agreement threshold: 100% on key variables\n\n")

        f.write("NEXT STEPS:\n")
        f.write("  1. Assign studies to reviewers\n")
        f.write("  2. Obtain full-text articles\n")
        f.write("  3. Complete extractions using forms\n")
        f.write("  4. Cross-validate 20% of studies\n")
        f.write("  5. Submit for verification\n\n")

        f.write("CONTACT INFORMATION:\n")
        f.write("  • For extraction questions: Team lead\n")
        f.write("  • For technical support: Data manager\n")
        f.write("  • For progress updates: Project coordinator\n")

    print(f"Batch instructions saved to: {instructions_file}")

    # Print summary
    print("\n" + "="*50)
    print("BATCH EXTRACTION PACKAGE SUMMARY")
    print("="*50)
    print(f"🎯 Batch Size: {batch_info['batch_size']} studies")
    print(f"⭐ Priority: {batch_info['priority_level']}")
    print(f"⏱️  Estimated Time: {batch_info['estimated_completion_time']}")
    print(f"📋 Forms Generated: 4 extraction forms + checklists")
    print(f"✅ Quality Control: Double extraction protocol included")
    print("\n🚀 Batch 1 extraction package ready for deployment!")
    print("\n💡 Tip: Start with studies having 'mortality' outcomes for highest impact")

if __name__ == "__main__":
    main()
