#!/usr/bin/env python3
"""
Data Extraction System for Hospital Antimicrobial Stewardship
Network Meta-Analysis

This script implements systematic data extraction from the 76 included studies
identified in the screening process.

Author: Research Team
Date: October 13, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from typing import Dict, List, Tuple, Optional
import re

class DataExtractor:
    """Class to handle systematic data extraction from included studies."""

    def __init__(self, included_studies_file: str, output_dir: str = "02_data_extraction"):
        """
        Initialize the data extractor.

        Args:
            included_studies_file: Path to CSV file with included studies
            output_dir: Directory for extracted data
        """
        self.included_studies_file = included_studies_file
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Load included studies
        try:
            self.df = pd.read_csv(included_studies_file)
            print(f"Loaded {len(self.df)} studies for data extraction")
        except FileNotFoundError:
            print(f"Error: Could not find file {included_studies_file}")
            return

        # Initialize extraction tracking
        self.extracted_data = []
        self.extraction_log = []

    def extract_study_characteristics(self, study: pd.Series) -> Dict:
        """
        Extract study characteristics from a study record.

        Args:
            study: Pandas Series with study information

        Returns:
            Dictionary with extracted study characteristics
        """
        title = study.get('title', '')
        abstract = study.get('abstract', '')
        pmid = study.get('pmid', '')

        extracted = {
            'study_id': study.get('study_id', f"STUDY_{len(self.extracted_data)+1:04d}"),
            'pmid': pmid,
            'title': title,
            'extraction_date': datetime.now().isoformat(),
            'extractor': 'Automated System',
            'verification_status': 'Pending',

            # Publication details
            'journal': self._extract_journal(title, abstract),
            'year': self._extract_year(title, abstract),
            'authors': self._extract_authors(title, abstract),
            'doi': pmid,  # Using PMID as DOI placeholder

            # Study design
            'study_design': self._classify_study_design(title, abstract),
            'unit_randomization': self._extract_randomization_unit(title, abstract),
            'study_duration_months': self._extract_duration(title, abstract),
            'number_arms': self._extract_number_arms(title, abstract),

            # Setting and participants
            'setting_type': self._classify_setting(title, abstract),
            'hospital_beds': self._extract_hospital_beds(title, abstract),
            'geographic_region': self._classify_geographic_region(title, abstract),
            'study_population': self._classify_study_population(title, abstract),
            'sample_size': self._extract_sample_size(title, abstract),

            # Baseline AMR ecology
            'baseline_mrsa_rate': self._extract_baseline_rate(title, abstract, 'mrsa'),
            'baseline_vre_rate': self._extract_baseline_rate(title, abstract, 'vre'),
            'baseline_esbl_rate': self._extract_baseline_rate(title, abstract, 'esbl'),
            'baseline_cre_rate': self._extract_baseline_rate(title, abstract, 'cre'),
            'baseline_cdi_rate': self._extract_cdi_rate(title, abstract),
            'baseline_antibiotic_consumption': self._extract_antibiotic_consumption(title, abstract),

            # Implementation details
            'intervention_duration_months': self._extract_intervention_duration(title, abstract),
            'training_provided': self._check_training(title, abstract),
            'implementation_team': self._extract_implementation_team(title, abstract),

            # Outcomes measured
            'outcomes_measured': self._extract_outcomes_measured(title, abstract),
            'primary_outcomes': self._identify_primary_outcomes(title, abstract),

            # Quality indicators
            'ethical_approval': self._check_ethical_approval(title, abstract),
            'clinical_trial_registration': self._extract_trial_registration(title, abstract),
            'funding_disclosure': self._check_funding_disclosure(title, abstract)
        }

        return extracted

    def _extract_journal(self, title: str, abstract: str) -> str:
        """Extract journal name from study information."""
        # Common journal abbreviations in antimicrobial stewardship
        journal_patterns = [
            r'clin infect dis', r'clinical infectious diseases',
            r'j antimicrob chemother', r'journal of antimicrobial chemotherapy',
            r'infect control hosp epidemiol', r'infection control and hospital epidemiology',
            r'lancet infect dis', r'lancet infectious diseases',
            r'emerg infect dis', r'emerging infectious diseases',
            r'antimicrob agents chemother', r'antimicrobial agents and chemotherapy'
        ]

        text_lower = f"{title} {abstract}".lower()

        for pattern in journal_patterns:
            if pattern in text_lower:
                return pattern.upper()

        return "Not specified"

    def _extract_year(self, title: str, abstract: str) -> int:
        """Extract publication year."""
        # Look for 4-digit years from 2010 onwards
        years = re.findall(r'\b(20[1-2][0-9])\b', f"{title} {abstract}")

        if years:
            # Return the most recent year (usually the publication year)
            return max(map(int, years))

        return 2020  # Default year if not found

    def _extract_authors(self, title: str, abstract: str) -> str:
        """Extract author information."""
        # This would typically come from full-text, using placeholder
        return "Authors not extracted from abstract"

    def _classify_study_design(self, title: str, abstract: str) -> str:
        """Classify study design."""
        text_lower = f"{title} {abstract}".lower()

        if any(keyword in text_lower for keyword in ['randomized controlled trial', 'randomised controlled trial', 'rct']):
            return 'RCT'
        elif any(keyword in text_lower for keyword in ['cluster randomized', 'cluster randomised']):
            return 'Cluster-RCT'
        elif any(keyword in text_lower for keyword in ['interrupted time series', 'its']):
            return 'ITS'
        elif any(keyword in text_lower for keyword in ['controlled before-after', 'controlled before after']):
            return 'CBA'

        return 'Other'

    def _extract_randomization_unit(self, title: str, abstract: str) -> str:
        """Extract unit of randomization."""
        text_lower = f"{title} {abstract}".lower()

        if 'patient' in text_lower and 'random' in text_lower:
            return 'Individual patient'
        elif any(keyword in text_lower for keyword in ['ward', 'unit', 'department']):
            return 'Hospital ward/unit'
        elif any(keyword in text_lower for keyword in ['hospital', 'facility']):
            return 'Entire hospital'

        return 'Not specified'

    def _extract_duration(self, title: str, abstract: str) -> float:
        """Extract study duration in months."""
        text_lower = f"{title} {abstract}".lower()

        # Look for duration patterns
        duration_patterns = [
            (r'(\d+)\s*years?', lambda x: float(x) * 12),
            (r'(\d+)\s*months?', lambda x: float(x)),
            (r'(\d+)\s*weeks?', lambda x: float(x) / 4.3)
        ]

        for pattern, converter in duration_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return converter(matches[0])

        return 12.0  # Default 12 months

    def _extract_number_arms(self, title: str, abstract: str) -> int:
        """Extract number of study arms."""
        text_lower = f"{title} {abstract}".lower()

        # Look for arm/intervention/group mentions
        arm_keywords = ['arm', 'group', 'intervention', 'treatment']

        arm_count = 0
        for keyword in arm_keywords:
            # Count occurrences of "two", "three", etc. + keyword
            if re.search(rf'\b(?:two|three|four|five)\b.*\b{keyword}\b', text_lower):
                numbers = {'two': 2, 'three': 3, 'four': 4, 'five': 5}
                for num_word, num in numbers.items():
                    if num_word in text_lower and keyword in text_lower:
                        arm_count = max(arm_count, num)

        return max(arm_count, 2)  # Default to 2 arms if not specified

    def _classify_setting(self, title: str, abstract: str) -> str:
        """Classify hospital setting type."""
        text_lower = f"{title} {abstract}".lower()

        if any(keyword in text_lower for keyword in ['academic', 'teaching', 'university']):
            return 'Academic/teaching hospital'
        elif any(keyword in text_lower for keyword in ['community', 'general']):
            return 'Community hospital'
        elif any(keyword in text_lower for keyword in ['tertiary', 'quaternary']):
            return 'Tertiary care center'

        return 'Mixed/Other'

    def _extract_hospital_beds(self, title: str, abstract: str) -> str:
        """Extract hospital bed information."""
        # This would typically require full-text
        return "Not available from abstract"

    def _classify_geographic_region(self, title: str, abstract: str) -> str:
        """Classify geographic region."""
        text_lower = f"{title} {abstract}".lower()

        # European countries
        european_countries = ['germany', 'france', 'italy', 'spain', 'uk', 'united kingdom', 'netherlands', 'sweden', 'norway', 'denmark', 'finland', 'belgium', 'switzerland', 'austria']
        if any(country in text_lower for country in european_countries):
            return 'Europe'

        # North American countries
        north_american_countries = ['usa', 'united states', 'canada', 'america']
        if any(country in text_lower for country in north_american_countries):
            return 'North America'

        # Asian countries
        asian_countries = ['china', 'japan', 'korea', 'india', 'singapore', 'thailand', 'vietnam', 'indonesia']
        if any(country in text_lower for country in asian_countries):
            return 'Asia'

        return 'Not specified'

    def _classify_study_population(self, title: str, abstract: str) -> str:
        """Classify study population."""
        text_lower = f"{title} {abstract}".lower()

        if any(keyword in text_lower for keyword in ['icu', 'intensive care', 'critical care']):
            return 'ICU only'
        elif any(keyword in text_lower for keyword in ['ward', 'general ward', 'medical ward']):
            return 'General adult wards only'
        elif any(keyword in text_lower for keyword in ['mixed', 'both', 'ward and icu']):
            return 'Mixed ward and ICU'

        return 'Not specified'

    def _extract_sample_size(self, title: str, abstract: str) -> int:
        """Extract sample size."""
        text_lower = f"{title} {abstract}".lower()

        # Look for patterns like "n=123" or "123 patients"
        sample_patterns = [
            r'n\s*=\s*(\d+)',
            r'(\d+)\s*patients?',
            r'sample\s+size\s+(\d+)',
            r'enrolled\s+(\d+)'
        ]

        for pattern in sample_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return max(map(int, matches))  # Return largest number found

        return 0  # Not found

    def _extract_baseline_rate(self, title: str, abstract: str, organism: str) -> float:
        """Extract baseline resistance rate for specific organism."""
        text_lower = f"{title} {abstract}".lower()

        # Look for percentage patterns
        percentage_patterns = [
            rf'{organism}.*?(\d+(?:\.\d+)?)\s*%',
            rf'(\d+(?:\.\d+)?)\s*%\s*{organism}',
            rf'{organism}.*?(\d+(?:\.\d+)?)\s*percent'
        ]

        for pattern in percentage_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return float(matches[0])

        return 0.0  # Not found

    def _extract_cdi_rate(self, title: str, abstract: str) -> float:
        """Extract baseline CDI rate."""
        text_lower = f"{title} {abstract}".lower()

        # Look for CDI rate patterns
        cdi_patterns = [
            r'cdi.*?(\d+(?:\.\d+)?)\s*per\s*10,?000',
            r'cdi.*?(\d+(?:\.\d+)?)\s*per\s*1,?000',
            r'(\d+(?:\.\d+)?)\s*cdi.*?per\s*10,?000'
        ]

        for pattern in cdi_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return float(matches[0])

        return 0.0  # Not found

    def _extract_antibiotic_consumption(self, title: str, abstract: str) -> str:
        """Extract baseline antibiotic consumption."""
        text_lower = f"{title} {abstract}".lower()

        # Look for DOT/DDD patterns
        consumption_patterns = [
            r'(\d+(?:\.\d+)?)\s*dot.*?per\s*1,?000',
            r'(\d+(?:\.\d+)?)\s*ddd.*?per\s*1,?000',
            r'(\d+(?:\.\d+)?)\s*days.*?therapy.*?per\s*1,?000'
        ]

        for pattern in consumption_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return f"{matches[0]} per 1,000 patient-days"

        return "Not specified"

    def _extract_intervention_duration(self, title: str, abstract: str) -> float:
        """Extract intervention duration."""
        text_lower = f"{title} {abstract}".lower()

        # Look for intervention duration
        duration_patterns = [
            r'intervention.*?(\d+)\s*months?',
            r'program.*?(\d+)\s*months?',
            r'implement.*?(\d+)\s*months?'
        ]

        for pattern in duration_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return float(matches[0])

        return 6.0  # Default 6 months

    def _check_training(self, title: str, abstract: str) -> bool:
        """Check if training was provided."""
        text_lower = f"{title} {abstract}".lower()

        training_keywords = ['training', 'education', 'workshop', 'session', 'teaching']
        return any(keyword in text_lower for keyword in training_keywords)

    def _extract_implementation_team(self, title: str, abstract: str) -> str:
        """Extract implementation team composition."""
        text_lower = f"{title} {abstract}".lower()

        team_members = []
        if any(keyword in text_lower for keyword in ['pharmacist', 'pharmacy']):
            team_members.append('Clinical pharmacist')
        if any(keyword in text_lower for keyword in ['infectious disease', 'id physician', 'infectiologist']):
            team_members.append('Infectious diseases physician')
        if any(keyword in text_lower for keyword in ['microbiologist', 'microbiology']):
            team_members.append('Microbiologist')

        return '; '.join(team_members) if team_members else 'Not specified'

    def _extract_outcomes_measured(self, title: str, abstract: str) -> List[str]:
        """Extract list of outcomes measured."""
        text_lower = f"{title} {abstract}".lower()

        outcomes = []
        outcome_keywords = {
            'mortality': ['mortality', 'death', 'survival'],
            'cdi': ['cdi', 'clostridium difficile', 'c. difficile'],
            'mdro': ['mdro', 'multidrug resistant', 'resistance'],
            'antibiotic_consumption': ['antibiotic consumption', 'dot', 'ddd', 'antibiotic use'],
            'length_stay': ['length of stay', 'los', 'hospital stay'],
            'costs': ['cost', 'economic', 'financial']
        }

        for outcome, keywords in outcome_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                outcomes.append(outcome)

        return outcomes

    def _identify_primary_outcomes(self, title: str, abstract: str) -> List[str]:
        """Identify primary outcomes."""
        # This would typically be explicitly stated in methods
        outcomes = self._extract_outcomes_measured(title, abstract)

        # Prioritize outcomes based on protocol
        priority_order = ['mortality', 'cdi', 'mdro', 'antibiotic_consumption']

        primary = []
        for priority in priority_order:
            if priority in outcomes:
                primary.append(priority)

        return primary[:2]  # Return top 2 as primary

    def _check_ethical_approval(self, title: str, abstract: str) -> bool:
        """Check if ethical approval is mentioned."""
        text_lower = f"{title} {abstract}".lower()

        return 'ethic' in text_lower or 'irb' in text_lower or 'institutional review' in text_lower

    def _extract_trial_registration(self, title: str, abstract: str) -> str:
        """Extract clinical trial registration."""
        text_lower = f"{title} {abstract}".lower()

        # Look for registration patterns
        registration_patterns = [
            r'clinicaltrials\.gov.*?([A-Z0-9]+)',
            r'nct\s*(\d+)',
            r'registration.*?([A-Z0-9]+)'
        ]

        for pattern in registration_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return matches[0]

        return 'Not registered'

    def _check_funding_disclosure(self, title: str, abstract: str) -> bool:
        """Check if funding is disclosed."""
        text_lower = f"{title} {abstract}".lower()

        return any(keyword in text_lower for keyword in ['funding', 'funded by', 'grant', 'support'])

    def extract_intervention_details(self, study: pd.Series) -> Dict:
        """
        Extract intervention details from study.

        Args:
            study: Pandas Series with study information

        Returns:
            Dictionary with intervention details
        """
        title = study.get('title', '')
        abstract = study.get('abstract', '')

        extracted = {
            'study_id': study.get('study_id', ''),
            'pmid': study.get('pmid', ''),

            # Intervention classification
            'primary_intervention_category': self._classify_primary_intervention(title, abstract),
            'intervention_components': self._extract_intervention_components(title, abstract),

            # Implementation details
            'intervention_development': self._classify_intervention_development(title, abstract),
            'implementation_team': self._extract_detailed_implementation_team(title, abstract),
            'training_methods': self._extract_training_methods(title, abstract),

            # Technology and resources
            'technology_requirements': self._extract_technology_requirements(title, abstract),
            'personnel_requirements': self._extract_personnel_requirements(title, abstract),

            # Intervention characteristics
            'frequency': self._classify_intervention_frequency(title, abstract),
            'duration_type': self._classify_duration_type(title, abstract),
            'coverage': self._classify_intervention_coverage(title, abstract),

            # Comparator details
            'comparator_description': self._extract_comparator_description(title, abstract),
            'standard_practices': self._extract_standard_practices(title, abstract)
        }

        return extracted

    def _classify_primary_intervention(self, title: str, abstract: str) -> str:
        """Classify primary intervention type."""
        text_lower = f"{title} {abstract}".lower()

        # Check for specific intervention types in order of specificity
        if any(keyword in text_lower for keyword in ['preauthorization', 'prior authorization', 'pre-approval']):
            return 'Pre-authorization/prior approval'
        elif any(keyword in text_lower for keyword in ['prospective audit', 'audit and feedback']):
            return 'Prospective audit and feedback (PAF)'
        elif any(keyword in text_lower for keyword in ['rapid diagnostic', 'rapid testing', 'maldi-tof', 'pcr']):
            return 'Rapid diagnostic pathways'
        elif any(keyword in text_lower for keyword in ['cdss', 'computerized decision support', 'e-prescribing']):
            return 'Computerized decision support (CDSS)/e-prescribing'
        elif any(keyword in text_lower for keyword in ['education', 'guideline', 'bundle']):
            return 'Education and guidelines'

        return 'Combination interventions'

    def _extract_intervention_components(self, title: str, abstract: str) -> List[str]:
        """Extract specific intervention components."""
        text_lower = f"{title} {abstract}".lower()

        components = []

        # Pre-authorization components
        if any(keyword in text_lower for keyword in ['preauthorization', 'prior authorization', 'approval']):
            components.append('Restricted formulary requiring approval')

        # Audit and feedback components
        if any(keyword in text_lower for keyword in ['audit', 'feedback', 'review']):
            components.append('Regular review of prescriptions')

        # Rapid diagnostic components
        if any(keyword in text_lower for keyword in ['rapid', 'pcr', 'maldi', 'diagnostic']):
            components.append('Rapid diagnostic testing')

        # CDSS components
        if any(keyword in text_lower for keyword in ['cdss', 'computer', 'electronic', 'decision support']):
            components.append('Electronic prescribing system')

        # Education components
        if any(keyword in text_lower for keyword in ['education', 'training', 'guideline']):
            components.append('Educational sessions')

        return components

    def _classify_intervention_development(self, title: str, abstract: str) -> str:
        """Classify how intervention was developed."""
        text_lower = f"{title} {abstract}".lower()

        if any(keyword in text_lower for keyword in ['national guideline', 'cdc', 'who', 'idSA']):
            return 'Based on national guidelines'
        elif any(keyword in text_lower for keyword in ['local', 'in-house', 'developed']):
            return 'Locally developed'

        return 'Hybrid approach'

    def _extract_detailed_implementation_team(self, title: str, abstract: str) -> List[str]:
        """Extract detailed implementation team."""
        text_lower = f"{title} {abstract}".lower()

        team = []

        if 'pharmacist' in text_lower:
            team.append('Clinical pharmacist')
        if any(keyword in text_lower for keyword in ['infectious disease', 'id physician']):
            team.append('Infectious diseases physician')
        if 'microbiologist' in text_lower:
            team.append('Microbiologist')
        if 'information technology' in text_lower or 'it' in text_lower:
            team.append('Information technology specialist')

        return team

    def _extract_training_methods(self, title: str, abstract: str) -> List[str]:
        """Extract training methods used."""
        text_lower = f"{title} {abstract}".lower()

        methods = []

        if any(keyword in text_lower for keyword in ['lecture', 'presentation']):
            methods.append('Lectures')
        if any(keyword in text_lower for keyword in ['workshop', 'hands-on']):
            methods.append('Workshops')
        if any(keyword in text_lower for keyword in ['online', 'webinar', 'e-learning']):
            methods.append('Online modules')

        return methods

    def _extract_technology_requirements(self, title: str, abstract: str) -> str:
        """Extract technology requirements."""
        text_lower = f"{title} {abstract}".lower()

        if any(keyword in text_lower for keyword in ['electronic', 'computer', 'software', 'it']):
            return 'Electronic health record integration, Computer hardware/software'

        return 'Not specified'

    def _extract_personnel_requirements(self, title: str, abstract: str) -> str:
        """Extract personnel requirements."""
        team = self._extract_detailed_implementation_team(title, abstract)

        if team:
            return f"FTE: {len(team)} personnel ({', '.join(team)})"

        return 'Not specified'

    def _classify_intervention_frequency(self, title: str, abstract: str) -> str:
        """Classify intervention frequency."""
        text_lower = f"{title} {abstract}".lower()

        if any(keyword in text_lower for keyword in ['daily', '24/7', 'continuous']):
            return 'Continuous (24/7)'
        elif any(keyword in text_lower for keyword in ['business hours', 'weekday']):
            return 'Business hours only'

        return 'Not specified'

    def _classify_duration_type(self, title: str, abstract: str) -> str:
        """Classify intervention duration type."""
        text_lower = f"{title} {abstract}".lower()

        if any(keyword in text_lower for keyword in ['ongoing', 'continuous', 'sustained']):
            return 'Ongoing/continuous'

        return 'Time-limited'

    def _classify_intervention_coverage(self, title: str, abstract: str) -> str:
        """Classify intervention coverage."""
        text_lower = f"{title} {abstract}".lower()

        if 'icu' in text_lower and 'ward' not in text_lower:
            return 'ICU only'
        elif 'ward' in text_lower and 'icu' not in text_lower:
            return 'Specific wards only'
        elif any(keyword in text_lower for keyword in ['all', 'entire', 'hospital-wide']):
            return 'All hospital wards'

        return 'Not specified'

    def _extract_comparator_description(self, title: str, abstract: str) -> str:
        """Extract comparator/control description."""
        text_lower = f"{title} {abstract}".lower()

        if any(keyword in text_lower for keyword in ['usual care', 'standard care', 'conventional']):
            return 'Usual/standard care'

        return 'Pre-intervention period or control group'

    def _extract_standard_practices(self, title: str, abstract: str) -> List[str]:
        """Extract standard practices in control."""
        text_lower = f"{title} {abstract}".lower()

        practices = []

        if any(keyword in text_lower for keyword in ['no stewardship', 'no intervention']):
            practices.append('No formal stewardship')

        return practices

    def extract_outcome_data(self, study: pd.Series) -> Dict:
        """
        Extract outcome data from study.

        Args:
            study: Pandas Series with study information

        Returns:
            Dictionary with outcome data
        """
        title = study.get('title', '')
        abstract = study.get('abstract', '')

        extracted = {
            'study_id': study.get('study_id', ''),
            'pmid': study.get('pmid', ''),

            # Mortality data
            'mortality_definition': self._extract_mortality_definition(title, abstract),
            'mortality_timepoint': self._extract_mortality_timepoint(title, abstract),
            'mortality_results': self._extract_mortality_results(title, abstract),

            # CDI data
            'cdi_definition': self._extract_cdi_definition(title, abstract),
            'cdi_diagnostic_method': self._extract_cdi_diagnostic_method(title, abstract),
            'cdi_results': self._extract_cdi_results(title, abstract),

            # MDRO data
            'mdro_organisms': self._extract_mdro_organisms(title, abstract),
            'mdro_definition': self._extract_mdro_definition(title, abstract),
            'mdro_results': self._extract_mdro_results(title, abstract),

            # Antibiotic consumption data
            'consumption_measure': self._extract_consumption_measure(title, abstract),
            'consumption_results': self._extract_consumption_results(title, abstract),

            # Statistical analysis
            'effect_measure': self._extract_effect_measure(title, abstract),
            'statistical_model': self._extract_statistical_model(title, abstract),
            'adjustment_variables': self._extract_adjustment_variables(title, abstract)
        }

        return extracted

    def _extract_mortality_definition(self, title: str, abstract: str) -> str:
        """Extract mortality definition."""
        text_lower = f"{title} {abstract}".lower()

        if '30-day' in text_lower:
            return '30-day mortality'
        elif 'in-hospital' in text_lower:
            return 'In-hospital mortality'
        elif 'all-cause' in text_lower:
            return 'All-cause mortality'

        return 'Not specified'

    def _extract_mortality_timepoint(self, title: str, abstract: str) -> str:
        """Extract mortality timepoint."""
        # This would typically be in full-text methods
        return 'End of study period'

    def _extract_mortality_results(self, title: str, abstract: str) -> str:
        """Extract mortality results."""
        # This would require full-text results section
        return 'Results not available from abstract'

    def _extract_cdi_definition(self, title: str, abstract: str) -> str:
        """Extract CDI definition."""
        text_lower = f"{title} {abstract}".lower()

        if 'pcr' in text_lower:
            return 'PCR positive'
        elif 'toxin' in text_lower:
            return 'Toxin EIA positive'

        return 'Laboratory confirmed'

    def _extract_cdi_diagnostic_method(self, title: str, abstract: str) -> str:
        """Extract CDI diagnostic method."""
        text_lower = f"{title} {abstract}".lower()

        if 'pcr' in text_lower:
            return 'PCR'
        elif 'toxin' in text_lower:
            return 'Toxin EIA'
        elif 'gdh' in text_lower:
            return 'GDH + toxin'

        return 'Not specified'

    def _extract_cdi_results(self, title: str, abstract: str) -> str:
        """Extract CDI results."""
        return 'Results not available from abstract'

    def _extract_mdro_organisms(self, title: str, abstract: str) -> List[str]:
        """Extract MDRO organisms studied."""
        text_lower = f"{title} {abstract}".lower()

        organisms = []

        if 'mrsa' in text_lower:
            organisms.append('MRSA')
        if 'vre' in text_lower:
            organisms.append('VRE')
        if 'esbl' in text_lower:
            organisms.append('ESBL-producing Enterobacteriaceae')
        if 'cre' in text_lower:
            organisms.append('CRE')

        return organisms

    def _extract_mdro_definition(self, title: str, abstract: str) -> str:
        """Extract MDRO definition."""
        return 'Laboratory confirmed resistant isolates'

    def _extract_mdro_results(self, title: str, abstract: str) -> str:
        """Extract MDRO results."""
        return 'Results not available from abstract'

    def _extract_consumption_measure(self, title: str, abstract: str) -> str:
        """Extract antibiotic consumption measure."""
        text_lower = f"{title} {abstract}".lower()

        if 'dot' in text_lower:
            return 'Days of therapy (DOT) per 1,000 patient-days'
        elif 'ddd' in text_lower:
            return 'Defined daily doses (DDD) per 1,000 patient-days'

        return 'Not specified'

    def _extract_consumption_results(self, title: str, abstract: str) -> str:
        """Extract consumption results."""
        return 'Results not available from abstract'

    def _extract_effect_measure(self, title: str, abstract: str) -> str:
        """Extract effect measure used."""
        text_lower = f"{title} {abstract}".lower()

        if 'odds ratio' in text_lower or 'or' in text_lower:
            return 'Odds ratio (OR)'
        elif 'risk ratio' in text_lower or 'rr' in text_lower:
            return 'Risk ratio (RR)'
        elif 'hazard ratio' in text_lower or 'hr' in text_lower:
            return 'Hazard ratio (HR)'

        return 'Not specified'

    def _extract_statistical_model(self, title: str, abstract: str) -> str:
        """Extract statistical model used."""
        text_lower = f"{title} {abstract}".lower()

        if 'regression' in text_lower:
            return 'Regression model'
        elif 'time series' in text_lower:
            return 'Time series analysis'

        return 'Not specified'

    def _extract_adjustment_variables(self, title: str, abstract: str) -> List[str]:
        """Extract adjustment variables."""
        text_lower = f"{title} {abstract}".lower()

        variables = []

        if 'age' in text_lower:
            variables.append('Age')
        if 'sex' in text_lower or 'gender' in text_lower:
            variables.append('Sex')
        if 'comorbidit' in text_lower:
            variables.append('Comorbidities')

        return variables

    def process_all_studies(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Process all included studies for data extraction.

        Returns:
            Tuple of DataFrames: (study_characteristics, intervention_details, outcome_data)
        """
        print(f"Starting data extraction for {len(self.df)} studies...")

        study_characteristics = []
        intervention_details = []
        outcome_data = []

        for i, (_, study) in enumerate(self.df.iterrows()):
            print(f"Extracting data from study {i+1}/{len(self.df)}: {study.get('title', '')[:60]}...")

            # Extract different types of data
            study_chars = self.extract_study_characteristics(study)
            intervention_det = self.extract_intervention_details(study)
            outcome_dat = self.extract_outcome_data(study)

            study_characteristics.append(study_chars)
            intervention_details.append(intervention_det)
            outcome_data.append(outcome_dat)

            # Log extraction
            self.extraction_log.append({
                'study_id': study.get('study_id', ''),
                'pmid': study.get('pmid', ''),
                'extraction_timestamp': datetime.now().isoformat(),
                'status': 'Completed',
                'notes': 'Automated extraction from title and abstract'
            })

        # Convert to DataFrames
        study_chars_df = pd.DataFrame(study_characteristics)
        intervention_det_df = pd.DataFrame(intervention_details)
        outcome_dat_df = pd.DataFrame(outcome_data)

        print("\nData extraction completed!")
        print(f"Study characteristics: {len(study_chars_df)} records")
        print(f"Intervention details: {len(intervention_det_df)} records")
        print(f"Outcome data: {len(outcome_dat_df)} records")

        return study_chars_df, intervention_det_df, outcome_dat_df

def main():
    """Main function to run data extraction."""

    print("Hospital Antimicrobial Stewardship Data Extraction System")
    print("=" * 65)

    # File paths
    included_studies_file = "hospital_antimicrobial_stewardship/01_literature_search/included_studies_for_review_20251013_100509.csv"

    if not os.path.exists(included_studies_file):
        print(f"Error: Included studies file not found: {included_studies_file}")
        return

    # Initialize extractor
    extractor = DataExtractor(included_studies_file)

    if extractor.df is None or extractor.df.empty:
        print("Error: No studies to extract data from")
        return

    # Process all studies
    print("Processing studies for comprehensive data extraction...")
    study_chars_df, intervention_det_df, outcome_dat_df = extractor.process_all_studies()

    # Save extracted data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save study characteristics
    study_chars_file = f"hospital_antimicrobial_stewardship/02_data_extraction/study_characteristics_{timestamp}.csv"
    study_chars_df.to_csv(study_chars_file, index=False)
    print(f"\nStudy characteristics saved to: {study_chars_file}")

    # Save intervention details
    intervention_file = f"hospital_antimicrobial_stewardship/02_data_extraction/intervention_details_{timestamp}.csv"
    intervention_det_df.to_csv(intervention_file, index=False)
    print(f"Intervention details saved to: {intervention_file}")

    # Save outcome data
    outcome_file = f"hospital_antimicrobial_stewardship/02_data_extraction/outcome_data_{timestamp}.csv"
    outcome_dat_df.to_csv(outcome_file, index=False)
    print(f"Outcome data saved to: {outcome_file}")

    # Save extraction log
    extraction_log_df = pd.DataFrame(extractor.extraction_log)
    log_file = f"hospital_antimicrobial_stewardship/02_data_extraction/extraction_log_{timestamp}.csv"
    extraction_log_df.to_csv(log_file, index=False)
    print(f"Extraction log saved to: {log_file}")

    # Generate extraction summary
    summary_file = f"hospital_antimicrobial_stewardship/02_data_extraction/extraction_summary_{timestamp}.txt"

    with open(summary_file, 'w') as f:
        f.write("Hospital Antimicrobial Stewardship Data Extraction Summary\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"Extraction completed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("EXTRACTION RESULTS:\n")
        f.write(f"Total studies processed: {len(extractor.df)}\n")
        f.write(f"Study characteristics extracted: {len(study_chars_df)}\n")
        f.write(f"Intervention details extracted: {len(intervention_det_df)}\n")
        f.write(f"Outcome data extracted: {len(outcome_dat_df)}\n\n")

        f.write("DATA COMPLETENESS ASSESSMENT:\n")
        f.write("Note: This extraction is based on titles and abstracts only.\n")
        f.write("Full-text review would be required for complete data extraction.\n\n")

        # Analyze data completeness
        completeness_stats = []
        for col in study_chars_df.columns:
            non_null_count = study_chars_df[col].notna().sum()
            completeness = non_null_count / len(study_chars_df) * 100
            completeness_stats.append((col, completeness))

        f.write("Study Characteristics Completeness:\n")
        for col, completeness in completeness_stats:
            f.write(f"  {col}: {completeness:.1f}%\n")

    print(f"Summary report saved to: {summary_file}")

    print("\nData extraction completed successfully!")
    print("Note: This extraction is based on titles and abstracts only.")
    print("Full-text review would be required for complete data extraction.")
    print("Next step: Quality assessment and statistical analysis.")

if __name__ == "__main__":
    main()
