#!/usr/bin/env python3
"""
Data Extraction Script
Automated and semi-automated data extraction from full-text articles
"""

import pandas as pd
import os
from datetime import datetime

class DataExtractor:
    def __init__(self):
        self.extraction_fields = []

    def extract_from_studies(self, studies_csv, output_file=None):
        """Extract data from included studies"""
        if output_file is None:
            output_file = f"extracted_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        studies_df = pd.read_csv(studies_csv)

        # Create extraction template
        extraction_data = []

        for _, study in studies_df.iterrows():
            study_data = {
                'study_id': study.get('pmid', study.get('study_id', '')),
                'title': study.get('title', ''),
                'extraction_date': datetime.now().isoformat(),
                'extractor': os.getenv('USER', 'automated'),
            }

            # Add custom extraction fields
            for field in self.extraction_fields:
                study_data[field] = ''  # Placeholder for manual entry

            extraction_data.append(study_data)

        extraction_df = pd.DataFrame(extraction_data)
        extraction_df.to_csv(output_file, index=False)
        print(f"Created extraction template for {len(extraction_data)} studies: {output_file}")

        return extraction_df

    def validate_extractions(self, extraction_file, validation_rules=None):
        """Validate extracted data against rules"""
        df = pd.read_csv(extraction_file)

        # Basic validation
        validation_report = {
            'total_studies': len(df),
            'missing_data': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.to_dict()
        }

        # Custom validation rules
        if validation_rules:
            validation_report['custom_validations'] = self._apply_validation_rules(df, validation_rules)

        return validation_report

    def _apply_validation_rules(self, df, rules):
        """Apply custom validation rules"""
        validations = {}
        # [Custom validation logic]
        return validations

def main():
    extractor = DataExtractor()

    # Configure extraction fields
    extractor.extraction_fields = [
        'study_design', 'sample_size', 'population_characteristics',
        'intervention_details', 'control_details', 'outcome_measures',
        'effect_size', 'confidence_interval', 'p_value'
    ]

    # Extract data
    extractor.extract_from_studies('screened_studies.csv')

if __name__ == "__main__":
    main()