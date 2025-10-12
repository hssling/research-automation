"""
Automated Data Extraction System
Intelligent form generation and automated data collection for systematic reviews
"""

import pandas as pd
import numpy as np
import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import json
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataExtractionField:
    """Represents a single data extraction field"""

    def __init__(self, name: str, field_type: str, description: str,
                 validation_rules: Dict = None, extraction_patterns: List[str] = None):
        self.name = name
        self.field_type = field_type  # 'text', 'numeric', 'categorical', 'boolean', 'date'
        self.description = description
        self.validation_rules = validation_rules or {}
        self.extraction_patterns = extraction_patterns or []
        self.ml_model = None

    def validate_value(self, value: Any) -> Tuple[bool, str]:
        """Validate a value against field rules"""
        if pd.isna(value) or value == '':
            if self.validation_rules.get('required', False):
                return False, "Required field is empty"
            return True, ""

        # Type validation
        if self.field_type == 'numeric':
            try:
                float(value)
            except (ValueError, TypeError):
                return False, f"Value must be numeric, got: {value}"

        elif self.field_type == 'categorical':
            allowed_values = self.validation_rules.get('allowed_values', [])
            if allowed_values and value not in allowed_values:
                return False, f"Value must be one of {allowed_values}, got: {value}"

        elif self.field_type == 'boolean':
            if str(value).lower() not in ['true', 'false', '1', '0', 'yes', 'no']:
                return False, f"Boolean field must be true/false, got: {value}"

        # Range validation for numeric fields
        if self.field_type == 'numeric' and 'min' in self.validation_rules:
            try:
                num_value = float(value)
                if num_value < self.validation_rules['min']:
                    return False, f"Value must be >= {self.validation_rules['min']}, got: {num_value}"
            except (ValueError, TypeError):
                pass

        return True, ""

    def extract_from_text(self, text: str) -> Optional[Any]:
        """Extract field value from text using patterns"""
        if not self.extraction_patterns:
            return None

        for pattern in self.extraction_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if self.field_type == 'numeric':
                    return float(match.group(1))
                return match.group(1)

        return None


class DataExtractionForm:
    """Represents a complete data extraction form"""

    def __init__(self, name: str, description: str, fields: List[DataExtractionField]):
        self.name = name
        self.description = description
        self.fields = {field.name: field for field in fields}
        self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert form to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'fields': {name: {
                'type': field.field_type,
                'description': field.description,
                'validation_rules': field.validation_rules,
                'extraction_patterns': field.extraction_patterns
            } for name, field in self.fields.items()},
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataExtractionForm':
        """Create form from dictionary"""
        fields = []
        for field_data in data.get('fields', {}).values():
            field = DataExtractionField(
                name=field_data['name'],
                field_type=field_data['type'],
                description=field_data['description'],
                validation_rules=field_data.get('validation_rules', {}),
                extraction_patterns=field_data.get('extraction_patterns', [])
            )
            fields.append(field)

        form = cls(data['name'], data['description'], fields)
        if 'created_at' in data:
            form.created_at = datetime.fromisoformat(data['created_at'])
        return form

    def validate_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a complete data extraction record"""
        validation_results = {}

        for field_name, field in self.fields.items():
            value = record.get(field_name)
            is_valid, error_msg = field.validate_value(value)
            validation_results[field_name] = {
                'valid': is_valid,
                'error': error_msg,
                'value': value
            }

        return validation_results

    def auto_extract(self, title: str, abstract: str, full_text: str = "") -> Dict[str, Any]:
        """Attempt automated extraction from study text"""
        extracted_data = {}

        # Combine all available text
        full_text_combined = f"{title} {abstract} {full_text}"

        for field_name, field in self.fields.items():
            # Try pattern-based extraction first
            extracted_value = field.extract_from_text(full_text_combined)

            # TODO: Add ML-based extraction here
            # if extracted_value is None and field.ml_model:
            #     extracted_value = field.ml_model.predict(full_text_combined)

            extracted_data[field_name] = extracted_value

        return extracted_data


class AutomatedDataExtractor:
    """Main automated data extraction system"""

    def __init__(self, forms_dir: str = "research-automation-core/forms"):
        self.forms_dir = Path(forms_dir)
        self.forms_dir.mkdir(parents=True, exist_ok=True)
        self.forms = {}
        self.load_forms()

    def create_extraction_form(self, name: str, description: str, fields_config: List[Dict[str, Any]]) -> DataExtractionForm:
        """Create a new data extraction form"""
        fields = []

        for field_config in fields_config:
            field = DataExtractionField(
                name=field_config['name'],
                field_type=field_config['type'],
                description=field_config.get('description', ''),
                validation_rules=field_config.get('validation_rules', {}),
                extraction_patterns=field_config.get('extraction_patterns', [])
            )
            fields.append(field)

        form = DataExtractionForm(name, description, fields)
        self.forms[name] = form

        # Save form
        self.save_form(form)

        logger.info(f"Created extraction form: {name}")
        return form

    def get_default_forms(self) -> Dict[str, DataExtractionForm]:
        """Get default pre-configured extraction forms"""

        forms = {}

        # Systematic Review - Study Characteristics Form
        study_form = self.create_extraction_form(
            "study_characteristics",
            "Basic study characteristics extraction form",
            [
                {
                    'name': 'study_id',
                    'type': 'text',
                    'description': 'Unique study identifier',
                    'validation_rules': {'required': True}
                },
                {
                    'name': 'study_title',
                    'type': 'text',
                    'description': 'Full study title',
                    'validation_rules': {'required': True}
                },
                {
                    'name': 'authors',
                    'type': 'text',
                    'description': 'Study authors'
                },
                {
                    'name': 'publication_year',
                    'type': 'numeric',
                    'description': 'Year of publication',
                    'validation_rules': {'min': 1900, 'max': 2030},
                    'extraction_patterns': [r'(\d{4})']  # Extract 4-digit years
                },
                {
                    'name': 'journal',
                    'type': 'text',
                    'description': 'Journal name'
                },
                {
                    'name': 'study_design',
                    'type': 'categorical',
                    'description': 'Study design type',
                    'validation_rules': {
                        'allowed_values': ['RCT', 'Cohort', 'Case-control', 'Cross-sectional', 'Systematic review', 'Meta-analysis', 'Other']
                    }
                },
                {
                    'name': 'sample_size',
                    'type': 'numeric',
                    'description': 'Total sample size',
                    'validation_rules': {'min': 1},
                    'extraction_patterns': [
                        r'n\s*=\s*(\d+)',
                        r'sample\s+size.*?\b(\d+)\b',
                        r'(\d+)\s+participants'
                    ]
                },
                {
                    'name': 'country',
                    'type': 'text',
                    'description': 'Country where study was conducted'
                },
                {
                    'name': 'funding_source',
                    'type': 'text',
                    'description': 'Source of funding'
                }
            ]
        )
        forms['study_characteristics'] = study_form

        # Meta-analysis - Effect Size Form
        meta_form = self.create_extraction_form(
            "meta_analysis_data",
            "Effect size extraction for meta-analysis",
            [
                {
                    'name': 'study_id',
                    'type': 'text',
                    'description': 'Unique study identifier',
                    'validation_rules': {'required': True}
                },
                {
                    'name': 'intervention',
                    'type': 'text',
                    'description': 'Intervention group description',
                    'validation_rules': {'required': True}
                },
                {
                    'name': 'control',
                    'type': 'text',
                    'description': 'Control group description',
                    'validation_rules': {'required': True}
                },
                {
                    'name': 'outcome_measure',
                    'type': 'text',
                    'description': 'Outcome measure assessed',
                    'validation_rules': {'required': True}
                },
                {
                    'name': 'intervention_mean',
                    'type': 'numeric',
                    'description': 'Mean value for intervention group',
                    'extraction_patterns': [
                        r'intervention.*?mean.*?(\d+\.?\d*)',
                        r'treatment.*?mean.*?(\d+\.?\d*)'
                    ]
                },
                {
                    'name': 'intervention_sd',
                    'type': 'numeric',
                    'description': 'Standard deviation for intervention group',
                    'extraction_patterns': [
                        r'intervention.*?sd.*?(\d+\.?\d*)',
                        r'treatment.*?sd.*?(\d+\.?\d*)',
                        r'intervention.*?standard.*?deviation.*?(\d+\.?\d*)'
                    ]
                },
                {
                    'name': 'control_mean',
                    'type': 'numeric',
                    'description': 'Mean value for control group',
                    'extraction_patterns': [
                        r'control.*?mean.*?(\d+\.?\d*)',
                        r'placebo.*?mean.*?(\d+\.?\d*)'
                    ]
                },
                {
                    'name': 'control_sd',
                    'type': 'numeric',
                    'description': 'Standard deviation for control group',
                    'extraction_patterns': [
                        r'control.*?sd.*?(\d+\.?\d*)',
                        r'placebo.*?sd.*?(\d+\.?\d*)'
                    ]
                },
                {
                    'name': 'intervention_n',
                    'type': 'numeric',
                    'description': 'Sample size for intervention group',
                    'validation_rules': {'min': 1}
                },
                {
                    'name': 'control_n',
                    'type': 'numeric',
                    'description': 'Sample size for control group',
                    'validation_rules': {'min': 1}
                },
                {
                    'name': 'effect_size',
                    'type': 'numeric',
                    'description': 'Pre-calculated effect size'
                },
                {
                    'name': 'standard_error',
                    'type': 'numeric',
                    'description': 'Standard error of effect size'
                },
                {
                    'name': 'confidence_interval',
                    'type': 'text',
                    'description': 'Confidence interval (e.g., 95% CI)'
                }
            ]
        )
        forms['meta_analysis_data'] = meta_form

        return forms

    def extract_from_studies(self, studies_csv: str, form_name: str,
                           output_file: str = None) -> pd.DataFrame:
        """Extract data from multiple studies using specified form"""

        logger.info(f"Loading studies from {studies_csv}")
        studies_df = pd.read_csv(studies_csv)
        logger.info(f"Loaded {len(studies_df)} studies for extraction")

        if form_name not in self.forms:
            raise ValueError(f"Form '{form_name}' not found. Available forms: {list(self.forms.keys())}")

        form = self.forms[form_name]

        extraction_results = []

        for idx, study in studies_df.iterrows():
            study_data = {
                'original_study_id': study.get('pmid', study.get('study_id', f'study_{idx+1}')),
                'extraction_timestamp': datetime.now().isoformat(),
                'form_name': form_name,
                'extraction_method': 'automated'
            }

            # Try automated extraction
            title = study.get('title', '')
            abstract = study.get('abstract', '')
            full_text = study.get('full_text', '')

            extracted = form.auto_extract(title, abstract, full_text)

            # Add human verification fields
            for field_name in form.fields.keys():
                study_data[field_name + '_auto'] = extracted.get(field_name)
                study_data[field_name + '_manual'] = None
                study_data[field_name + '_final'] = extracted.get(field_name)
                study_data[field_name + '_confidence'] = 0.5  # Auto-extraction confidence

            # Add original study data
            for col in studies_df.columns:
                study_data[f'original_{col}'] = study[col]

            extraction_results.append(study_data)

            if (idx + 1) % 50 == 0:
                logger.info(f"Processed {idx + 1}/{len(studies_df)} studies")

        result_df = pd.DataFrame(extraction_results)

        if output_file:
            result_df.to_csv(output_file, index=False)
            logger.info(f"Extraction results saved to {output_file}")

        logger.info(f"Completed automated extraction: {len(result_df)} records")
        return result_df

    def validate_extractions(self, extraction_csv: str, form_name: str) -> pd.DataFrame:
        """Validate extracted data against form rules"""

        logger.info(f"Loading extractions from {extraction_csv}")
        df = pd.read_csv(extraction_csv)

        if form_name not in self.forms:
            raise ValueError(f"Form '{form_name}' not found")

        form = self.forms[form_name]

        validation_results = []

        for idx, row in df.iterrows():
            record = {}
            for field_name in form.fields.keys():
                final_col = f"{field_name}_final"
                if final_col in row:
                    record[field_name] = row[final_col]

            validation = form.validate_record(record)
            validation['study_id'] = row.get('study_id', f'row_{idx}')
            validation_results.append(validation)

        validation_df = pd.DataFrame(validation_results)

        # Summary statistics
        total_records = len(validation_df)
        invalid_records = 0

        field_errors = {}
        for field_name in form.fields.keys():
            if f"{field_name}_error" in validation_df.columns:
                error_count = validation_df[f"{field_name}_error"].notna().sum()
                field_errors[field_name] = error_count

                # Count records with any errors
                invalid_records += (validation_df[f"{field_name}_valid"] == False).sum()

        logger.info("Validation Summary:")
        logger.info(f"Total records: {total_records}")
        logger.info(f"Records with errors: {invalid_records}")
        logger.info("Field-specific errors:")
        for field, count in field_errors.items():
            logger.info(f"  {field}: {count} errors")

        return validation_df

    def save_form(self, form: DataExtractionForm):
        """Save extraction form to disk"""
        form_path = self.forms_dir / f"{form.name}.json"
        with open(form_path, 'w') as f:
            json.dump(form.to_dict(), f, indent=2)
        logger.info(f"Saved form: {form.name}")

    def load_forms(self):
        """Load all saved extraction forms"""
        if not self.forms_dir.exists():
            return

        for form_file in self.forms_dir.glob("*.json"):
            with open(form_file, 'r') as f:
                form_data = json.load(f)
                form = DataExtractionForm.from_dict(form_data)
                self.forms[form.name] = form

        logger.info(f"Loaded {len(self.forms)} extraction forms")


# Template forms for different research types
DEFAULT_FORMS = {
    'systematic_review': [
        {
            'name': 'study_characteristics',
            'type': 'text',
            'description': 'Study characteristics form',
            'validation_rules': {'required': True}
        },
        {
            'name': 'methodology_quality',
            'type': 'text',
            'description': 'Quality assessment form'
        }
    ],
    'meta_analysis': [
        {
            'name': 'effect_sizes',
            'type': 'text',
            'description': 'Effect size extraction form',
            'validation_rules': {'required': True}
        },
        {
            'name': 'study_characteristics',
            'type': 'text',
            'description': 'Study characteristics form',
            'validation_rules': {'required': True}
        }
    ],
    'clinical_trial': [
        {
            'name': 'trial_characteristics',
            'type': 'text',
            'description': 'Trial characteristics form',
            'validation_rules': {'required': True}
        },
        {
            'name': 'outcome_measures',
            'type': 'text',
            'description': 'Outcome measures form',
            'validation_rules': {'required': True}
        },
        {
            'name': 'adverse_events',
            'type': 'text',
            'description': 'Adverse events form'
        }
    ]
}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automated Data Extraction System")
    parser.add_argument("action", choices=["extract", "validate", "create-form"],
                       help="Action to perform")
    parser.add_argument("--studies", help="CSV file with studies to extract from")
    parser.add_argument("--form", help="Extraction form name")
    parser.add_argument("--output", help="Output file")
    parser.add_argument("--form-config", help="JSON file with form configuration")

    args = parser.parse_args()

    extractor = AutomatedDataExtractor()

    if args.action == "extract":
        if not args.studies or not args.form:
            parser.error("--studies and --form required for extraction")

        result_df = extractor.extract_from_studies(args.studies, args.form, args.output)
        print(f"Extraction completed: {len(result_df)} records")

    elif args.action == "validate":
        if not args.studies or not args.form:
            parser.error("--studies and --form required for validation")

        validation_df = extractor.validate_extractions(args.studies, args.form)
        print("Validation completed")

    elif args.action == "create-form":
        if not args.form_config:
            parser.error("--form-config required for form creation")

        with open(args.form_config, 'r') as f:
            config = json.load(f)

        fields_config = config.get('fields', [])
        form = extractor.create_extraction_form(
            config['name'],
            config.get('description', ''),
            fields_config
        )
        print(f"Created form: {form.name}")
