#!/usr/bin/env python3
"""
Study Screening System for Hospital Antimicrobial Stewardship
Network Meta-Analysis

This script implements a systematic screening process for the 1,526 potentially
relevant studies identified in the literature search.

Author: Research Team
Date: October 13, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from typing import Dict, List, Tuple
import re

class StudyScreener:
    """Class to handle systematic screening of studies for inclusion."""

    def __init__(self, search_results_file: str):
        """
        Initialize the screener with search results.

        Args:
            search_results_file: Path to the CSV file with search results
        """
        self.search_results_file = search_results_file
        self.screening_file = search_results_file.replace('relevant_studies', 'screening_decisions')

        # Load search results
        try:
            self.df = pd.read_csv(search_results_file)
            print(f"Loaded {len(self.df)} studies for screening")
        except FileNotFoundError:
            print(f"Error: Could not find file {search_results_file}")
            return

        # Initialize screening tracking
        self.screening_decisions = {}
        self.inclusion_criteria = self._define_inclusion_criteria()
        self.exclusion_criteria = self._define_exclusion_criteria()

    def _define_inclusion_criteria(self) -> List[str]:
        """Define inclusion criteria based on protocol."""
        return [
            "Study design: RCT, cluster-RCT, or controlled ITS",
            "Population: Adult patients in acute-care hospitals",
            "Intervention: Antimicrobial stewardship program (pre-auth, audit/feedback, rapid diagnostics, CDSS, education)",
            "Outcomes: At least one primary outcome (mortality, CDI, MDRO incidence, DOT/DDD)",
            "Full-text available or accessible",
            "English language publication",
            "Published in peer-reviewed journal"
        ]

    def _define_exclusion_criteria(self) -> List[str]:
        """Define exclusion criteria based on protocol."""
        return [
            "Pediatric population only",
            "Outpatient or long-term care setting",
            "Non-stewardship interventions only",
            "No relevant outcomes reported",
            "Single-arm studies or uncontrolled before-after studies",
            "Editorials, commentaries, or narrative reviews",
            "Conference abstracts without full data"
        ]

    def _check_study_design(self, title: str, abstract: str, mesh_terms: str) -> Tuple[bool, str]:
        """Check if study design meets inclusion criteria."""
        text_to_check = f"{title} {abstract} {mesh_terms}".lower()

        # Look for study design keywords
        rct_keywords = ['randomized controlled trial', 'randomised controlled trial', 'rct', 'cluster randomized', 'cluster randomised']
        its_keywords = ['interrupted time series', 'its', 'controlled before-after', 'controlled before after']

        has_rct = any(keyword in text_to_check for keyword in rct_keywords)
        has_its = any(keyword in text_to_check for keyword in its_keywords)

        if has_rct or has_its:
            return True, "RCT or ITS design identified"
        else:
            return False, "No RCT or ITS design identified"

    def _check_population(self, title: str, abstract: str) -> Tuple[bool, str]:
        """Check if study population meets inclusion criteria."""
        text_to_check = f"{title} {abstract}".lower()

        # Hospital/acute care keywords
        hospital_keywords = ['hospital', 'acute care', 'inpatient', 'icu', 'intensive care', 'ward', 'tertiary care']

        # Adult population keywords
        adult_keywords = ['adult', 'adults', 'patient', 'patients', 'aged 18', '18 years']

        has_hospital = any(keyword in text_to_check for keyword in hospital_keywords)
        has_adult = any(keyword in text_to_check for keyword in adult_keywords)

        if has_hospital and has_adult:
            return True, "Hospital adult population identified"
        elif has_hospital:
            return True, "Hospital setting (assuming adult population)"
        else:
            return False, "Not hospital/acute care setting"

    def _check_intervention(self, title: str, abstract: str, keywords: str) -> Tuple[bool, str]:
        """Check if intervention meets inclusion criteria."""
        text_to_check = f"{title} {abstract} {keywords}".lower()

        # Stewardship intervention keywords
        stewardship_keywords = [
            'antimicrobial stewardship', 'antibiotic stewardship', 'preauthorization', 'prior authorization',
            'pre-authorization', 'prospective audit', 'audit and feedback', 'rapid diagnostic', 'rapid testing',
            'cdss', 'computerized decision support', 'e-prescribing', 'electronic prescribing',
            'education', 'guideline', 'bundle', 'stewardship program', 'stewardship intervention'
        ]

        has_intervention = any(keyword in text_to_check for keyword in stewardship_keywords)

        if has_intervention:
            return True, "Stewardship intervention identified"
        else:
            return False, "No stewardship intervention identified"

    def _check_outcomes(self, title: str, abstract: str) -> Tuple[bool, str]:
        """Check if outcomes meet inclusion criteria."""
        text_to_check = f"{title} {abstract}".lower()

        # Outcome keywords
        outcome_keywords = [
            'mortality', 'death', 'survival', 'cdi', 'clostridium difficile', 'c. difficile',
            'mdro', 'multidrug resistant', 'antibiotic resistance', 'mrsa', 'vre', 'esbl', 'cre',
            'antibiotic consumption', 'dot', 'ddd', 'days of therapy', 'defined daily dose',
            'antibiotic use', 'antibiotic utilization'
        ]

        has_outcomes = any(keyword in text_to_check for keyword in outcome_keywords)

        if has_outcomes:
            return True, "Relevant outcomes identified"
        else:
            return False, "No relevant outcomes identified"

    def screen_study(self, idx: int) -> Dict:
        """
        Screen a single study based on inclusion/exclusion criteria.

        Args:
            idx: Index of study in dataframe

        Returns:
            Dictionary with screening decision and rationale
        """
        study = self.df.iloc[idx]
        title = study.get('title', '')
        abstract = study.get('abstract', '')
        keywords = str(study.get('keywords', ''))
        mesh_terms = str(study.get('mesh_terms', ''))

        decision = {
            'study_id': f"STUDY_{idx+1:04d}",
            'pmid': study.get('pmid', ''),
            'title': title,
            'screening_date': datetime.now().isoformat(),
            'include': True,
            'reasons': [],
            'exclusion_reasons': []
        }

        # Check each criterion
        criteria_checks = [
            ('study_design', self._check_study_design(title, abstract, mesh_terms)),
            ('population', self._check_population(title, abstract)),
            ('intervention', self._check_intervention(title, abstract, keywords)),
            ('outcomes', self._check_outcomes(title, abstract))
        ]

        for criterion, (meets_criterion, reason) in criteria_checks:
            if meets_criterion:
                decision['reasons'].append(f"{criterion}: {reason}")
            else:
                decision['reasons'].append(f"{criterion}: {reason}")
                decision['exclusion_reasons'].append(f"{criterion}: {reason}")
                decision['include'] = False

        # Additional exclusion checks
        text_to_check = f"{title} {abstract}".lower()

        # Exclude pediatric studies
        pediatric_keywords = ['pediatric', 'children', 'childhood', 'infant', 'neonate', 'peds']
        if any(keyword in text_to_check for keyword in pediatric_keywords):
            decision['include'] = False
            decision['exclusion_reasons'].append("Pediatric population")

        # Exclude outpatient/long-term care
        setting_keywords = ['outpatient', 'ambulatory', 'clinic', 'long-term care', 'nursing home']
        if any(keyword in text_to_check for keyword in setting_keywords):
            decision['include'] = False
            decision['exclusion_reasons'].append("Outpatient or long-term care setting")

        # Exclude non-original research
        non_research_keywords = ['editorial', 'commentary', 'review', 'meta-analysis', 'systematic review']
        if any(keyword in text_to_check for keyword in non_research_keywords):
            decision['include'] = False
            decision['exclusion_reasons'].append("Not original research")

        return decision

    def batch_screen_studies(self, batch_size: int = 100) -> pd.DataFrame:
        """
        Screen studies in batches for efficiency.

        Args:
            batch_size: Number of studies to screen in each batch

        Returns:
            DataFrame with screening decisions
        """
        all_decisions = []

        total_studies = len(self.df)
        print(f"Starting systematic screening of {total_studies} studies...")

        for i in range(0, total_studies, batch_size):
            end_idx = min(i + batch_size, total_studies)
            batch_num = i // batch_size + 1
            total_batches = (total_studies + batch_size - 1) // batch_size

            print(f"Processing batch {batch_num}/{total_batches} (studies {i+1}-{end_idx})")

            batch_decisions = []

            for idx in range(i, end_idx):
                decision = self.screen_study(idx)
                batch_decisions.append(decision)

                # Progress indicator
                if (idx - i + 1) % 10 == 0:
                    print(f"  Screened {idx - i + 1}/{batch_size} studies in current batch")

            all_decisions.extend(batch_decisions)

            # Save progress after each batch
            self._save_screening_progress(all_decisions)

        # Convert to DataFrame
        decisions_df = pd.DataFrame(all_decisions)

        print("\nScreening completed!")
        print(f"Total studies screened: {len(decisions_df)}")
        print(f"Studies meeting inclusion criteria: {decisions_df['include'].sum()}")
        print(f"Studies excluded: {len(decisions_df) - decisions_df['include'].sum()}")

        return decisions_df

    def _save_screening_progress(self, decisions: List[Dict]):
        """Save current screening progress to file."""
        # Convert decisions to DataFrame for saving
        progress_df = pd.DataFrame(decisions)

        # Add screening statistics
        included_count = sum(1 for d in decisions if d['include'])
        total_count = len(decisions)

        # Save detailed decisions
        progress_df.to_csv(self.screening_file, index=False)

        # Save summary
        summary_file = self.screening_file.replace('.csv', '_summary.txt')
        with open(summary_file, 'w') as f:
            f.write("Screening Progress Summary\n")
            f.write("=" * 30 + "\n\n")
            f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Studies screened: {total_count}\n")
            f.write(f"Studies included: {included_count}\n")
            f.write(f"Studies excluded: {total_count - included_count}\n")
            f.write(f"Inclusion rate: {included_count/total_count*100:.1f}%\n\n")

            f.write("Top 10 included studies:\n")
            f.write("-" * 25 + "\n")

            included_studies = [d for d in decisions if d['include']]
            for i, study in enumerate(included_studies[:10], 1):
                f.write(f"{i}. {study['title'][:80]}...")
                if study.get('pmid'):
                    f.write(f" [PMID: {study['pmid']}]")
                f.write("\n")

    def generate_prisma_flow(self, decisions_df: pd.DataFrame) -> Dict:
        """
        Generate PRISMA flow diagram data.

        Args:
            decisions_df: DataFrame with screening decisions

        Returns:
            Dictionary with PRISMA flow counts
        """
        total_identified = len(decisions_df)

        # Count by exclusion reason
        exclusion_counts = {}
        for decision in decisions_df.itertuples():
            if not decision.include:
                for reason in decision.exclusion_reasons:
                    exclusion_counts[reason] = exclusion_counts.get(reason, 0) + 1

        included = decisions_df['include'].sum()
        excluded = total_identified - included

        prisma_flow = {
            'identification': {
                'records_identified': total_identified,
                'records_screened': total_identified,
                'records_excluded': excluded,
                'records_included': included
            },
            'screening': {
                'total_screened': total_identified,
                'excluded_wrong_design': exclusion_counts.get('study_design: No RCT or ITS design identified', 0),
                'excluded_wrong_population': exclusion_counts.get('population: Not hospital/acute care setting', 0),
                'excluded_wrong_intervention': exclusion_counts.get('intervention: No stewardship intervention identified', 0),
                'excluded_wrong_outcomes': exclusion_counts.get('outcomes: No relevant outcomes identified', 0),
                'excluded_other': excluded - sum(exclusion_counts.values())
            }
        }

        return prisma_flow

def main():
    """Main function to run the study screening process."""

    print("Hospital Antimicrobial Stewardship Study Screening System")
    print("=" * 60)

    # File paths
    search_results_file = "hospital_antimicrobial_stewardship/01_literature_search/pubmed_relevant_studies_20251013_095957.csv"

    if not os.path.exists(search_results_file):
        print(f"Error: Search results file not found: {search_results_file}")
        return

    # Initialize screener
    screener = StudyScreener(search_results_file)

    if screener.df is None or screener.df.empty:
        print("Error: No studies to screen")
        return

    # Run screening
    print("Starting systematic screening process...")
    decisions_df = screener.batch_screen_studies(batch_size=100)

    # Generate PRISMA flow
    prisma_flow = screener.generate_prisma_flow(decisions_df)

    # Save final results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save screening decisions
    final_screening_file = f"hospital_antimicrobial_stewardship/01_literature_search/final_screening_decisions_{timestamp}.csv"
    decisions_df.to_csv(final_screening_file, index=False)
    print(f"\nScreening decisions saved to: {final_screening_file}")

    # Save included studies for full-text review
    included_studies = decisions_df[decisions_df['include'] == True]
    included_file = f"hospital_antimicrobial_stewardship/01_literature_search/included_studies_for_review_{timestamp}.csv"
    included_studies.to_csv(included_file, index=False)
    print(f"Included studies saved to: {included_file}")

    # Save PRISMA flow data
    prisma_file = f"hospital_antimicrobial_stewardship/01_literature_search/prisma_flow_data_{timestamp}.json"
    with open(prisma_file, 'w') as f:
        # Convert numpy types to native Python types for JSON serialization
        def convert_numpy_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj

        json.dump(prisma_flow, f, indent=2, default=convert_numpy_types)
    print(f"PRISMA flow data saved to: {prisma_file}")

    # Generate final summary report
    summary_file = f"hospital_antimicrobial_stewardship/01_literature_search/screening_summary_{timestamp}.txt"

    with open(summary_file, 'w') as f:
        f.write("Hospital Antimicrobial Stewardship Study Screening Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Screening completed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("SCREENING RESULTS:\n")
        f.write(f"Total studies screened: {len(decisions_df)}\n")
        f.write(f"Studies included: {len(included_studies)}\n")
        f.write(f"Studies excluded: {len(decisions_df) - len(included_studies)}\n")
        f.write(f"Inclusion rate: {len(included_studies)/len(decisions_df)*100:.1f}%\n\n")

        f.write("PRISMA FLOW DIAGRAM DATA:\n")
        f.write(f"Records identified: {prisma_flow['identification']['records_identified']}\n")
        f.write(f"Records screened: {prisma_flow['identification']['records_screened']}\n")
        f.write(f"Records excluded: {prisma_flow['identification']['records_excluded']}\n")
        f.write(f"Records included: {prisma_flow['identification']['records_included']}\n\n")

        f.write("EXCLUSION REASONS:\n")
        # Count exclusion reasons from decisions
        exclusion_reasons = {}
        for decision in decisions_df.itertuples():
            if not decision.include:
                for reason in decision.exclusion_reasons:
                    exclusion_reasons[reason] = exclusion_reasons.get(reason, 0) + 1

        for reason, count in exclusion_reasons.items():
            f.write(f"{reason}: {count}\n")

        f.write("\nTOP 10 INCLUDED STUDIES:\n")
        f.write("-" * 30 + "\n")

        for i, (_, study) in enumerate(included_studies.head(10).iterrows(), 1):
            f.write(f"{i}. {study['title'][:100]}...")
            if study.get('pmid'):
                f.write(f" [PMID: {study['pmid']}]")
            f.write("\n")

    print(f"Summary report saved to: {summary_file}")

    print("\nScreening completed successfully!")
    print(f"Included {len(included_studies)} studies for full-text review.")
    print(f"Next step: Full-text review and data extraction for included studies.")

if __name__ == "__main__":
    main()
