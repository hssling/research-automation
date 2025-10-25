#!/usr/bin/env python3
"""
Full-Text Review Workflow for Hospital Antimicrobial Stewardship
Network Meta-Analysis

This script provides a comprehensive workflow and framework for conducting
full-text review and complete data extraction when full-text articles
are available.

Author: Research Team
Date: October 13, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ReviewStatus(Enum):
    """Status of full-text review process."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REQUIRES_ATTENTION = "requires_attention"

@dataclass
class FullTextStudy:
    """Represents a study requiring full-text review."""
    study_id: str
    pmid: str
    title: str
    priority: str
    estimated_review_time: str
    key_extraction_targets: List[str]
    review_status: ReviewStatus
    assigned_reviewer: str = ""
    review_deadline: str = ""

class FullTextReviewManager:
    """Manages the full-text review workflow and data extraction process."""

    def __init__(self, included_studies_file: str, gap_analysis_file: str = None):
        """
        Initialize the full-text review manager.

        Args:
            included_studies_file: Path to included studies CSV
            gap_analysis_file: Path to gap analysis JSON (optional)
        """
        self.included_studies_file = included_studies_file
        self.gap_analysis_file = gap_analysis_file

        # Load data
        self._load_study_data()
        self._load_gap_analysis()

        # Initialize review workflow
        self.studies_for_review = []
        self.review_assignments = {}
        self.extraction_templates = {}

    def _load_study_data(self):
        """Load included studies data."""
        try:
            self.studies_df = pd.read_csv(self.included_studies_file)
            print(f"Loaded {len(self.studies_df)} studies for full-text review workflow")
        except FileNotFoundError:
            print(f"Error: Could not find file {self.included_studies_file}")
            self.studies_df = None

    def _load_gap_analysis(self):
        """Load gap analysis if available."""
        if self.gap_analysis_file and os.path.exists(self.gap_analysis_file):
            try:
                with open(self.gap_analysis_file, 'r') as f:
                    self.gap_analysis = json.load(f)
                print("Loaded gap analysis data")
            except:
                self.gap_analysis = None
                print("Could not load gap analysis")
        else:
            self.gap_analysis = None

    def create_full_text_review_plan(self) -> Dict:
        """
        Create a comprehensive full-text review plan.

        Returns:
            Dictionary with review plan and assignments
        """
        print("Creating full-text review plan...")
        print("=" * 50)

        # Prioritize studies based on gap analysis
        prioritized_studies = self._prioritize_studies_for_review()

        # Create review workflow
        workflow = {
            'total_studies': len(self.studies_df),
            'studies_by_priority': self._categorize_studies_by_priority(prioritized_studies),
            'estimated_review_time': self._estimate_total_review_time(prioritized_studies),
            'review_timeline': self._create_review_timeline(prioritized_studies),
            'quality_control_plan': self._create_quality_control_plan(),
            'data_extraction_templates': self._create_extraction_templates()
        }

        return workflow

    def _prioritize_studies_for_review(self) -> List[FullTextStudy]:
        """Prioritize studies based on research importance and data gaps."""
        prioritized_studies = []

        for _, study in self.studies_df.iterrows():
            # Determine priority based on study characteristics
            priority = self._determine_study_priority(study)

            # Identify key extraction targets
            key_targets = self._identify_key_extraction_targets(study)

            # Estimate review time
            review_time = self._estimate_review_time(study, key_targets)

            full_text_study = FullTextStudy(
                study_id=study.get('study_id', ''),
                pmid=study.get('pmid', ''),
                title=study.get('title', ''),
                priority=priority,
                estimated_review_time=review_time,
                key_extraction_targets=key_targets,
                review_status=ReviewStatus.PENDING
            )

            prioritized_studies.append(full_text_study)

        # Sort by priority (High > Medium > Low)
        priority_order = {'High': 3, 'Medium': 2, 'Low': 1}
        prioritized_studies.sort(
            key=lambda x: (priority_order.get(x.priority, 0),
                          x.estimated_review_time),
            reverse=True
        )

        return prioritized_studies

    def _determine_study_priority(self, study: pd.Series) -> str:
        """Determine priority level for a study."""
        priority_score = 0

        # Check study design (RCTs get higher priority)
        if 'rct' in study.get('title', '').lower() or 'randomized' in study.get('title', '').lower():
            priority_score += 3
        elif 'cluster' in study.get('title', '').lower():
            priority_score += 2

        # Check intervention type (complex interventions get higher priority)
        title_abstract = f"{study.get('title', '')} {study.get('abstract', '')}".lower()
        if any(keyword in title_abstract for keyword in ['combination', 'multifaceted', 'bundle']):
            priority_score += 2
        elif any(keyword in title_abstract for keyword in ['rapid diagnostic', 'cdss', 'computerized']):
            priority_score += 1

        # Check outcomes (studies with multiple outcomes get higher priority)
        if 'mortality' in title_abstract:
            priority_score += 2
        if any(keyword in title_abstract for keyword in ['cdi', 'mdro', 'resistance']):
            priority_score += 1

        # Determine final priority
        if priority_score >= 6:
            return 'High'
        elif priority_score >= 3:
            return 'Medium'
        else:
            return 'Low'

    def _identify_key_extraction_targets(self, study: pd.Series) -> List[str]:
        """Identify key data elements to extract for a study."""
        targets = []

        # Always needed for NMA
        targets.extend([
            'precise_effect_estimates',
            'confidence_intervals',
            'statistical_significance',
            'sample_size_per_arm',
            'baseline_characteristics'
        ])

        # Check study focus areas
        title_abstract = f"{study.get('title', '')} {study.get('abstract', '')}".lower()

        if 'mortality' in title_abstract:
            targets.append('detailed_mortality_results')
        if any(keyword in title_abstract for keyword in ['cdi', 'clostridium']):
            targets.append('cdi_diagnostic_methods')
        if any(keyword in title_abstract for keyword in ['mdro', 'resistance']):
            targets.append('microbiology_methods')
        if any(keyword in title_abstract for keyword in ['cost', 'economic']):
            targets.append('cost_effectiveness_data')

        return targets

    def _estimate_review_time(self, study: pd.Series, targets: List[str]) -> str:
        """Estimate time required for full-text review."""
        base_time = 30  # Base 30 minutes

        # Adjust based on number of targets
        time_adjustment = len(targets) * 5  # 5 minutes per target

        # Adjust based on study complexity
        if 'combination' in study.get('title', '').lower():
            time_adjustment += 15
        elif 'multifaceted' in study.get('title', '').lower():
            time_adjustment += 10

        total_minutes = base_time + time_adjustment

        if total_minutes <= 45:
            return '30-45 minutes'
        elif total_minutes <= 60:
            return '45-60 minutes'
        else:
            return '60+ minutes'

    def _categorize_studies_by_priority(self, studies: List[FullTextStudy]) -> Dict:
        """Categorize studies by priority level."""
        categories = {'High': [], 'Medium': [], 'Low': []}

        for study in studies:
            categories[study.priority].append({
                'study_id': study.study_id,
                'pmid': study.pmid,
                'title': study.title[:80] + '...' if len(study.title) > 80 else study.title,
                'estimated_time': study.estimated_review_time,
                'key_targets': study.key_extraction_targets
            })

        return categories

    def _estimate_total_review_time(self, studies: List[FullTextStudy]) -> Dict:
        """Estimate total time required for review."""
        total_studies = len(studies)

        # Estimate time by priority
        time_by_priority = {'High': 0, 'Medium': 0, 'Low': 0}
        time_minutes = {'High': 0, 'Medium': 0, 'Low': 0}

        for study in studies:
            priority = study.priority

            # Convert time string to minutes
            time_str = study.estimated_review_time
            if '30-45' in time_str:
                minutes = 37
            elif '45-60' in time_str:
                minutes = 52
            elif '60+' in time_str:
                minutes = 75
            else:
                minutes = 45  # default

            time_by_priority[priority] += minutes
            time_minutes[priority] += minutes

        total_hours = sum(time_minutes.values()) / 60

        return {
            'total_studies': total_studies,
            'total_hours': round(total_hours, 1),
            'time_by_priority': {k: round(v/60, 1) for k, v in time_minutes.items()},
            'average_time_per_study': round(total_hours * 60 / total_studies, 1)
        }

    def _create_review_timeline(self, studies: List[FullTextStudy]) -> Dict:
        """Create a realistic review timeline."""
        # Assume 2-3 reviewers working in parallel
        studies_per_week_per_reviewer = 8  # Conservative estimate

        high_priority = [s for s in studies if s.priority == 'High']
        medium_priority = [s for s in studies if s.priority == 'Medium']
        low_priority = [s for s in studies if s.priority == 'Low']

        # Estimate weeks needed
        total_studies = len(studies)
        total_weeks = (total_studies / studies_per_week_per_reviewer) / 2  # 2 reviewers

        timeline = {
            'estimated_completion_weeks': round(total_weeks, 1),
            'high_priority_studies': len(high_priority),
            'medium_priority_studies': len(medium_priority),
            'low_priority_studies': len(low_priority),
            'recommended_schedule': {
                'week_1_2': 'Complete all high priority studies',
                'week_3_4': 'Complete medium priority studies',
                'week_5_6': 'Complete low priority studies and quality checks'
            }
        }

        return timeline

    def _create_quality_control_plan(self) -> Dict:
        """Create quality control plan for data extraction."""
        return {
            'double_extraction_requirement': '20% of studies or minimum 10 studies',
            'discrepancy_resolution': 'Third reviewer arbitration',
            'data_validation_checks': [
                'Effect estimates within plausible ranges',
                'Confidence intervals properly calculated',
                'Baseline characteristics balanced between groups',
                'Outcome definitions consistent with protocol',
                'Statistical methods appropriate for study design'
            ],
            'quality_metrics': [
                'Inter-rater agreement (Kappa statistic)',
                'Data completeness percentage',
                'Extraction error rate',
                'Protocol adherence score'
            ]
        }

    def _create_extraction_templates(self) -> Dict:
        """Create detailed extraction templates for each data category."""
        return {
            'study_characteristics_template': self._create_study_characteristics_template(),
            'intervention_details_template': self._create_intervention_details_template(),
            'outcome_data_template': self._create_outcome_data_template(),
            'quality_assessment_template': self._create_quality_assessment_template()
        }

    def _create_study_characteristics_template(self) -> Dict:
        """Create template for study characteristics extraction."""
        return {
            'required_fields': [
                'exact_sample_size_per_arm',
                'detailed_baseline_characteristics',
                'precise_study_duration',
                'exact_inclusion_exclusion_criteria',
                'detailed_setting_description'
            ],
            'optional_but_important': [
                'power_calculation_details',
                'interim_analysis_plans',
                'protocol_deviations',
                'loss_to_follow_up_reasons'
            ],
            'extraction_notes': [
                'Extract exact numbers, not rounded values',
                'Note any discrepancies between protocol and implementation',
                'Document all baseline characteristics, even if not statistically significant'
            ]
        }

    def _create_intervention_details_template(self) -> Dict:
        """Create template for intervention details extraction."""
        return {
            'required_fields': [
                'exact_intervention_components',
                'implementation_fidelity_measures',
                'training_programs_details',
                'resource_requirements',
                'intervention_timing_and_duration'
            ],
            'implementation_checklist': [
                'Was intervention implemented as planned?',
                'Were there any modifications during study?',
                'How was intervention fidelity monitored?',
                'What was the uptake rate among eligible patients?',
                'Were there any barriers to implementation?'
            ]
        }

    def _create_outcome_data_template(self) -> Dict:
        """Create template for outcome data extraction."""
        return {
            'required_fields': [
                'exact_effect_estimates_with_ci',
                'precise_p_values',
                'time_to_event_data',
                'intention_to_treat_results',
                'per_protocol_results'
            ],
            'outcome_specific_instructions': {
                'mortality': 'Extract hazard ratios if time-to-event analysis used',
                'cdi': 'Note diagnostic criteria and testing frequency',
                'mdro': 'Document resistance definitions and testing methods',
                'antibiotic_consumption': 'Extract both DOT and DDD if available'
            }
        }

    def _create_quality_assessment_template(self) -> Dict:
        """Create template for quality assessment."""
        return {
            'rob_2_assessment': [
                'Randomization process',
                'Deviations from intended interventions',
                'Missing outcome data',
                'Measurement of outcomes',
                'Selection of reported results'
            ],
            'its_quality_assessment': [
                'Protection against secular changes',
                'Protection against detection bias',
                'Completeness of outcome data',
                'Protection against selection bias',
                'Appropriate analysis methods'
            ]
        }

    def generate_full_text_review_package(self) -> Dict:
        """
        Generate complete package for full-text review.

        Returns:
            Dictionary with all necessary materials for full-text review
        """
        print("Generating full-text review package...")
        print("=" * 45)

        # Create review plan
        review_plan = self.create_full_text_review_plan()

        # Generate study packages
        study_packages = self._generate_study_packages()

        # Create data extraction workbook
        extraction_workbook = self._create_data_extraction_workbook()

        # Generate quality control guidelines
        qc_guidelines = self._generate_quality_control_guidelines()

        package = {
            'review_plan': review_plan,
            'study_packages': study_packages,
            'extraction_workbook': extraction_workbook,
            'quality_control': qc_guidelines,
            'workflow_checklist': self._create_workflow_checklist(),
            'troubleshooting_guide': self._create_troubleshooting_guide()
        }

        return package

    def _generate_study_packages(self) -> List[Dict]:
        """Generate individual study packages for review."""
        study_packages = []

        for study in self.studies_for_review:
            package = {
                'study_id': study.study_id,
                'pmid': study.pmid,
                'priority': study.priority,
                'extraction_targets': study.key_extraction_targets,
                'estimated_time': study.estimated_review_time,
                'required_data_elements': self._get_required_elements_for_study(study),
                'extraction_form_template': self._create_study_specific_template(study),
                'quality_checklist': self._create_study_quality_checklist(study)
            }

            study_packages.append(package)

        return study_packages

    def _get_required_elements_for_study(self, study: FullTextStudy) -> List[str]:
        """Get required data elements for a specific study."""
        required_elements = [
            'complete_sample_size_data',
            'baseline_characteristics_table',
            'intervention_details',
            'outcome_results_with_uncertainty',
            'statistical_analysis_details'
        ]

        # Add study-specific requirements
        if 'mortality' in ' '.join(study.key_extraction_targets):
            required_elements.append('survival_analysis_details')
        if 'cdi' in ' '.join(study.key_extraction_targets):
            required_elements.append('microbiology_methods')
        if 'economic' in ' '.join(study.key_extraction_targets):
            required_elements.append('cost_analysis_details')

        return required_elements

    def _create_study_specific_template(self, study: FullTextStudy) -> Dict:
        """Create study-specific extraction template."""
        return {
            'study_overview': {
                'title': study.title,
                'pmid': study.pmid,
                'priority': study.priority
            },
            'extraction_sections': [
                'publication_details',
                'study_design',
                'participants',
                'interventions',
                'outcomes',
                'statistical_analysis',
                'results',
                'quality_assessment'
            ],
            'critical_data_points': study.key_extraction_targets
        }

    def _create_study_quality_checklist(self, study: FullTextStudy) -> List[str]:
        """Create quality checklist for a study."""
        return [
            'Study design clearly described',
            'Randomization method adequate',
            'Blinding appropriate for outcomes',
            'Sample size calculation reported',
            'Baseline characteristics balanced',
            'Outcome measures well-defined',
            'Statistical methods appropriate',
            'Results clearly reported',
            'Conclusions supported by data',
            'Conflicts of interest disclosed'
        ]

    def _create_data_extraction_workbook(self) -> Dict:
        """Create data extraction workbook structure."""
        return {
            'workbook_structure': {
                'sheet_1': 'study_characteristics',
                'sheet_2': 'intervention_details',
                'sheet_3': 'outcome_data',
                'sheet_4': 'quality_assessment',
                'sheet_5': 'extraction_notes'
            },
            'validation_rules': [
                'Sample sizes must be positive integers',
                'Percentages must be between 0-100',
                'Effect estimates must include measures of uncertainty',
                'P-values must be between 0-1',
                'Dates must be in YYYY-MM-DD format'
            ],
            'required_fields_checklist': [
                'Study design clearly classified',
                'Sample size per arm recorded',
                'Effect estimates with CI extracted',
                'Statistical significance noted',
                'Quality assessment completed'
            ]
        }

    def _generate_quality_control_guidelines(self) -> Dict:
        """Generate quality control guidelines."""
        return {
            'double_extraction_protocol': {
                'percentage_required': '20% of studies',
                'minimum_number': '10 studies',
                'selection_method': 'Random selection across priority levels',
                'resolution_process': 'Third reviewer arbitration for discrepancies'
            },
            'data_validation_checks': [
                'Cross-check sample sizes between text and tables',
                'Verify effect estimates against reported statistics',
                'Confirm statistical test appropriateness',
                'Validate baseline balance between groups',
                'Check for selective outcome reporting'
            ],
            'quality_metrics': [
                'Inter-rater reliability (Kappa)',
                'Data completeness percentage',
                'Extraction accuracy rate',
                'Protocol adherence score'
            ]
        }

    def _create_workflow_checklist(self) -> List[str]:
        """Create workflow checklist for reviewers."""
        return [
            'Obtain full-text article (PDF/PMC)',
            'Read title and abstract for context',
            'Review methods section thoroughly',
            'Extract study characteristics',
            'Extract intervention details',
            'Extract outcome data with precision',
            'Complete quality assessment',
            'Document any uncertainties',
            'Cross-check all extracted data',
            'Submit for verification'
        ]

    def _create_troubleshooting_guide(self) -> Dict:
        """Create troubleshooting guide for common issues."""
        return {
            'common_issues': {
                'missing_data': 'Note what is missing and why',
                'unclear_methods': 'Contact corresponding author if critical',
                'inconsistent_results': 'Check for data entry errors',
                'protocol_deviations': 'Document and assess impact'
            },
            'resolution_strategies': [
                'Mark unclear fields as "unclear" with explanation',
                'Use "not reported" only when explicitly stated',
                'Document assumptions made during extraction',
                'Flag studies needing corresponding author contact'
            ],
            'escalation_criteria': [
                'Critical outcome data missing',
                'Major protocol deviations',
                'Inconsistent reporting throughout article',
                'Statistical analysis unclear'
            ]
        }

def main():
    """Main function to create full-text review workflow."""

    print("Full-Text Review Workflow Generator")
    print("=" * 40)

    # File paths - go up one directory from current location and construct path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    included_studies_file = os.path.join(parent_dir, "01_literature_search", "included_studies_for_review_20251013_100509.csv")

    if not os.path.exists(included_studies_file):
        print(f"Error: Included studies file not found: {included_studies_file}")
        return

    # Initialize review manager
    review_manager = FullTextReviewManager(included_studies_file)

    if review_manager.studies_df is None or review_manager.studies_df.empty:
        print("Error: No studies to create review workflow for")
        return

    # Generate complete review package
    print("Generating comprehensive full-text review package...")
    review_package = review_manager.generate_full_text_review_package()

    # Save review package components
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Use current directory for saving files
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Save review plan
    plan_file = os.path.join(output_dir, f"full_text_review_plan_{timestamp}.json")
    with open(plan_file, 'w') as f:
        json.dump(review_package['review_plan'], f, indent=2)
    print(f"\nReview plan saved to: {plan_file}")

    # Save study packages
    study_packages_file = os.path.join(output_dir, f"study_packages_{timestamp}.json")
    with open(study_packages_file, 'w') as f:
        json.dump(review_package['study_packages'], f, indent=2)
    print(f"Study packages saved to: {study_packages_file}")

    # Save extraction workbook template
    workbook_file = os.path.join(output_dir, f"data_extraction_workbook_template_{timestamp}.json")
    with open(workbook_file, 'w') as f:
        json.dump(review_package['extraction_workbook'], f, indent=2)
    print(f"Extraction workbook template saved to: {workbook_file}")

    # Save quality control guidelines
    qc_file = os.path.join(output_dir, f"quality_control_guidelines_{timestamp}.json")
    with open(qc_file, 'w') as f:
        json.dump(review_package['quality_control'], f, indent=2)
    print(f"Quality control guidelines saved to: {qc_file}")

    # Generate comprehensive workflow guide
    workflow_guide_file = os.path.join(output_dir, f"full_text_review_workflow_guide_{timestamp}.txt")

    with open(workflow_guide_file, 'w') as f:
        f.write("Full-Text Review Workflow Guide\n")
        f.write("=" * 35 + "\n\n")

        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Review plan summary
        plan = review_package['review_plan']
        f.write("REVIEW PLAN SUMMARY:\n")
        f.write(f"Total studies requiring full-text review: {plan['total_studies']}\n")

        # Fix the nested quote issue by extracting the value first
        estimated_time = plan['estimated_review_time']
        total_hours = estimated_time['total_hours']
        f.write(f"Estimated completion time: {total_hours} hours\n")

        f.write(f"Recommended timeline: {plan['review_timeline']['estimated_completion_weeks']} weeks\n\n")

        # Priority breakdown
        f.write("STUDIES BY PRIORITY:\n")
        for priority, studies in plan['studies_by_priority'].items():
            f.write(f"  {priority}: {len(studies)} studies\n")
        f.write("\n")

        # Workflow checklist
        f.write("WORKFLOW CHECKLIST:\n")
        for i, item in enumerate(review_package['workflow_checklist'], 1):
            f.write(f"  {i}. {item}\n")
        f.write("\n")

        # Quality control reminders
        f.write("QUALITY CONTROL REMINDERS:\n")
        for item in review_package['quality_control']['data_validation_checks']:
            f.write(f"  • {item}\n")
        f.write("\n")

        # Common troubleshooting
        f.write("TROUBLESHOOTING COMMON ISSUES:\n")
        for issue, solution in review_package['troubleshooting_guide']['common_issues'].items():
            f.write(f"  {issue}: {solution}\n")
        f.write("\n")

        # Data extraction templates summary
        f.write("DATA EXTRACTION SECTIONS:\n")
        for section in review_package['extraction_workbook']['workbook_structure'].values():
            f.write(f"  • {section}\n")
        f.write("\n")

        f.write("EXTRACTION TIPS:\n")
        f.write("  • Extract exact values, not rounded approximations\n")
        f.write("  • Note page numbers for future reference\n")
        f.write("  • Document any uncertainties or assumptions\n")
        f.write("  • Cross-check numbers between text and tables\n")
        f.write("  • Flag any data inconsistencies for resolution\n")
        f.write("  • Complete quality assessment for each study\n\n")

        f.write("FINAL REMINDERS:\n")
        f.write("  • Maintain detailed extraction notes\n")
        f.write("  • Follow protocol definitions strictly\n")
        f.write("  • Submit completed extractions for verification\n")
        f.write("  • Contact team lead for any uncertainties\n")

    print(f"Workflow guide saved to: {workflow_guide_file}")

    print("\nFull-text review workflow package generated successfully!")
    print("PACKAGE CONTENTS:")
    print(f"  • Review plan: {len(review_package['review_plan']['studies_by_priority'])} priority categories")
    print(f"  • Study packages: {len(review_package['study_packages'])} individual study guides")
    print(f"  • Extraction workbook: {len(review_package['extraction_workbook']['workbook_structure'])} sections")
    print(f"  • Quality control: {len(review_package['quality_control']['data_validation_checks'])} validation checks")
    print("  • Workflow checklist: Complete step-by-step guide")
    print("  • Troubleshooting guide: Solutions for common issues")
    print("\nNEXT STEPS:")
    print("  1. Obtain full-text access to the 76 included studies")
    print("  2. Assign studies to reviewers based on priority")
    print("  3. Follow the detailed workflow guide for systematic extraction")
    print("  4. Implement quality control measures")
    print("  5. Resolve any data gaps or uncertainties")

if __name__ == "__main__":
    main()
