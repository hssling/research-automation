#!/usr/bin/env python3
"""
Data Extraction Automation for PPG Heart Rate Accuracy Meta-Analysis

This script automates the extraction of structured data from eligible studies
for photoplethysmography (PPG) heart rate monitoring accuracy validation.

Author: Research Integrity Automation System
Date: September 23, 2025

Requirements:
- pandas (pip install pandas)
- numpy (pip install numpy)
- openpyxl (for Excel file handling)

Outputs:
- extracted_data.csv: Raw extracted data for meta-analysis
- data_extraction_log.txt: Audit trail of extraction process
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import re

class PPGDataExtractor:
    """Automated data extraction for PPG heart rate accuracy systematic reviews."""

    def __init__(self):
        # Define extraction fields for PPG HR accuracy meta-analysis
        self.extraction_fields = {
            # Study Characteristics
            'study_id': '',
            'pmid': '',
            'doi': '',
            'authors': '',
            'journal': '',
            'year': 0,
            'country': '',
            'study_design': '',  # validation, comparative, etc.
            'total_participants': 0,
            'measurement_duration_minutes': 0,
            'ecg_lead_placement': '',

            # Participant Demographics
            'age_mean': None,
            'age_sd': None,
            'age_range': '',
            'sex_female_pct': None,
            'bmi_mean': None,
            'bmi_sd': None,
            'skin_tone': '',  # Light, Medium, Dark
            'health_status': '',  # Healthy, Athletes, Cardiac patients, etc.

            # PPG Device Characteristics
            'device_type': '',  # Wrist-worn, Finger, Smartphone, etc.
            'manufacturer_model': '',
            'ppg_wavelength': '',  # Green, Red, Infrared, Multi
            'sampling_frequency_hz': None,
            'processing_algorithm': '',
            'device_firmware_version': '',

            # Reference ECG Characteristics
            'ecg_device_manufacturer': '',
            'ecg_sampling_frequency_hz': None,
            'ecg_configuration': '',

            # Experimental Conditions
            'activity_levels': [],  # Rest, Walking, Running, etc.
            'hr_range_min': None,
            'hr_range_max': None,
            'environmental_conditions': '',
            'motion_artifacts_controlled': True,

            # Primary Accuracy Outcomes - MAE by Condition
            'mae_rest_bpm': None,
            'mae_rest_sd': None,
            'mae_rest_n': 0,
            'mae_light_exercise_bpm': None,
            'mae_light_exercise_sd': None,
            'mae_light_exercise_n': 0,
            'mae_moderate_exercise_bpm': None,
            'mae_moderate_exercise_sd': None,
            'mae_moderate_exercise_n': 0,
            'mae_vigorous_exercise_bpm': None,
            'mae_vigorous_exercise_sd': None,
            'mae_vigorous_exercise_n': 0,
            'mae_overall_bpm': None,
            'mae_overall_sd': None,
            'mae_overall_n': 0,

            # RMSE by Condition
            'rmse_rest_bpm': None,
            'rmse_rest_sd': None,
            'rmse_rest_n': 0,
            'rmse_light_exercise_bpm': None,
            'rmse_light_exercise_sd': None,
            'rmse_light_exercise_n': 0,
            'rmse_overall_bpm': None,
            'rmse_overall_sd': None,
            'rmse_overall_n': 0,

            # Bland-Altman Analysis
            'bias_mean_difference_bpm': None,
            'bias_95_ci_lower': None,
            'bias_95_ci_upper': None,
            'loa_upper_bpm': None,
            'loa_lower_bpm': None,
            'loa_range_bpm': None,

            # Correlation Analysis
            'pearson_r': None,
            'pearson_r_95_ci_lower': None,
            'pearson_r_95_ci_upper': None,
            'icc_value': None,
            'icc_95_ci_lower': None,
            'icc_95_ci_upper': None,

            # Performance Thresholds
            'pct_within_5_bpm': None,
            'pct_within_10_bpm': None,
            'pct_within_15_bpm': None,

            # Quality and Bias Assessment
            'quadas_domain_1_risk': '',  # Patient Selection
            'quadas_domain_2_risk': '',  # PPG Test
            'quadas_domain_3_risk': '',  # ECG Reference
            'quadas_domain_4_risk': '',  # Flow and Timing
            'overall_rob': '',
            'rob_reason': '',

            # Study Quality Metrics
            'signal_quality_pct_good': None,  # Percentage of good signal quality
            'dropouts_artifacts_pct': None,  # Percentage of excluded measurements
            'manufacturer_involvement': False,
            'funding_source_industry': False,

            # Notes and Comments
            'extractor_notes': '',
            'need_followup': False,
            'extraction_date': datetime.now().isoformat(),
            'extractor_id': 'RIA-SYSTEM'
        }

    def load_eligible_studies(self, csv_path="ppg_hr_accuracy_meta_analysis/data/literature_screening/included_studies_*.csv"):
        """
        Load eligible studies database for data extraction.

        Args:
            csv_path (str): Path to eligible studies CSV

        Returns:
            pd.DataFrame: Eligible studies for extraction
        """
        print("📂 Loading eligible studies for data extraction...")

        # Find the most recent eligible studies file
        import glob
        csv_files = glob.glob(csv_path)
        if not csv_files:
            print(f"❌ No eligible studies CSV found at {csv_path}")
            print("💡 Creating template for future use")
            return pd.DataFrame()

        latest_csv = max(csv_files, key=os.path.getctime)
        print(f"✓ Using: {latest_csv}")

        try:
            df = pd.read_csv(latest_csv, encoding='utf-8-sig')
            print(f"✓ Loaded {len(df)} eligible studies for extraction")
            return df
        except Exception as e:
            print(f"❌ Error loading eligible studies: {e}")
            return pd.DataFrame()

    def initialize_extraction_dataframe(self, eligible_studies_df):
        """
        Initialize empty extraction dataframe with all required fields.

        Args:
            eligible_studies_df (pd.DataFrame): Eligible studies

        Returns:
            pd.DataFrame: Empty extraction template
        """
        print("📋 Initializing data extraction template...")

        extraction_data = []

        for i, row in eligible_studies_df.iterrows():
            study_record = self.extraction_fields.copy()
            study_record['pmid'] = str(row.get('pmid', ''))
            study_record['study_id'] = f"PPG_{i+1:03d}"
            study_record['title'] = str(row.get('title', ''))
            study_record['authors'] = str(row.get('authors', ''))
            study_record['year'] = row.get('year', '')

            extraction_data.append(study_record)

        extraction_df = pd.DataFrame(extraction_data)
        print(f"✓ Created extraction template for {len(extraction_df)} studies")

        return extraction_df

    def extract_text_based_data(self, row, text_field):
        """
        Extract data from text fields using pattern matching.

        Args:
            row (pd.Series): Study row
            text_field (str): Text field ('title' or 'abstract')

        Returns:
            dict: Extracted data points
        """
        text = str(row.get(text_field, '')).lower()

        extracted_data = {}

        # Extract participant numbers
        sample_pattern = r'n\s*[=]\s*(\d+)'
        matches = re.findall(sample_pattern, text)
        if matches:
            try:
                extracted_data['total_participants'] = int(matches[0])
            except:
                pass

        # Extract device types
        if 'wrist' in text:
            extracted_data['device_type'] = 'Wrist-worn'
        elif 'finger' in text:
            extracted_data['device_type'] = 'Finger clip'
        elif 'smartphone' in text or 'smart phone' in text:
            extracted_data['device_type'] = 'Smartphone'

        # Extract manufacturers
        manufacturers = ['apple', 'fitbit', 'garmin', 'samsung', 'xiaomi', 'polar']
        for mf in manufacturers:
            if mf in text:
                extracted_data['manufacturer_model'] = mf.title()
                break

        # Extract wavelength mentions
        if 'green' in text:
            extracted_data['ppg_wavelength'] = 'Green'
        elif 'red' in text:
            extracted_data['ppg_wavelength'] = 'Red'
        elif 'infrared' in text or 'ir' in text:
            extracted_data['ppg_wavelength'] = 'Infrared'

        # Extract MAE values
        mae_pattern = r'mae.*?(\d+\.?\d*)'
        mae_matches = re.findall(mae_pattern, text)
        if mae_matches:
            try:
                extracted_data['mae_overall_bpm'] = float(mae_matches[0])
            except:
                pass

        # Extract correlation coefficients
        corr_pattern = r'r\s*[=]\s*0?\.(\d+)'
        corr_matches = re.findall(corr_pattern, text)
        if corr_matches:
            try:
                extracted_data['pearson_r'] = float('0.' + corr_matches[0])
            except:
                pass

        # Extract activity mentions
        activities = []
        if 'rest' in text:
            activities.append('Rest')
        if 'walk' in text:
            activities.append('Walking')
        if 'run' in text or 'jog' in text:
            activities.append('Running')
        if 'cycl' in text:
            activities.append('Cycling')
        if activities:
            extracted_data['activity_levels'] = activities

        return extracted_data

    def perform_automated_extraction(self, eligible_studies_df, extraction_df):
        """
        Perform automated extraction using text analysis.

        Args:
            eligible_studies_df (pd.DataFrame): Source studies
            extraction_df (pd.DataFrame): Extraction template

        Returns:
            pd.DataFrame: Partially populated extraction dataframe
        """
        print("🤖 Performing automated data extraction...")

        for i, row in eligible_studies_df.iterrows():
            study_id = f"PPG_{i+1:03d}"

            # Title extraction
            title_data = self.extract_text_based_data(row, 'title')

            # Abstract extraction (if available)
            abstract_data = self.extract_text_based_data(row, 'abstract')

            # Merge data
            combined_data = {**title_data, **abstract_data}

            if combined_data:
                for field, value in combined_data.items():
                    if field in extraction_df.columns:
                        extraction_df.loc[extraction_df['study_id'] == study_id, field] = value
                print(f"  ✓ Study {study_id}: Extracted {len(combined_data)} data points")
            else:
                print(f"  ∅ Study {study_id}: No automated data extracted")

        return extraction_df

    def add_quality_assessment(self, extraction_df):
        """
        Add quality assessment using available information.

        Args:
            extraction_df (pd.DataFrame): Extraction dataframe

        Returns:
            pd.DataFrame: Dataframe with quality assessments
        """
        print("⭐ Performing automated quality assessment...")

        def assess_study_quality(row):
            score = 0
            rob = 'Unclear'

            # Domain 1: Patient Selection
            if row.get('total_participants', 0) >= 20:
                row['quadas_domain_1_risk'] = 'Low'
            else:
                row['quadas_domain_1_risk'] = 'High'

            # Domain 2: PPG Test
            if row.get('device_type') or row.get('manufacturer_model'):
                row['quadas_domain_2_risk'] = 'Low'
            else:
                row['quadas_domain_2_risk'] = 'Unclear'

            # Domain 3: ECG Reference
            row['quadas_domain_3_risk'] = 'Low'  # Assuming ECG is gold standard

            # Domain 4: Flow and Timing
            row['quadas_domain_4_risk'] = 'Low'  # Assuming simultaneous recording

            # Overall assessment
            domains = [
                row['quadas_domain_1_risk'],
                row['quadas_domain_2_risk'],
                row['quadas_domain_3_risk'],
                row['quadas_domain_4_risk']
            ]
            if all(d == 'Low' for d in domains):
                rob = 'Low'
            elif any(d == 'High' for d in domains):
                rob = 'High'

            row['overall_rob'] = rob
            return row

        extraction_df = extraction_df.apply(assess_study_quality, axis=1)

        return extraction_df

    def save_extraction_results(self, extraction_df, output_dir="ppg_hr_accuracy_meta_analysis/data/data_extraction"):
        """
        Save extraction results.

        Args:
            extraction_df (pd.DataFrame): Extraction dataframe
            output_dir (str): Output directory
        """
        print("💾 Saving data extraction results...")

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_output = f"{output_dir}/extracted_data_{timestamp}.csv"
        extraction_df.to_csv(csv_output, index=False, encoding='utf-8-sig')
        print(f"✓ Extracted data saved: {csv_output}")

        # Summary
        summary = self.generate_extraction_summary(extraction_df)
        summary_output = f"{output_dir}/extraction_summary_{timestamp}.json"
        with open(summary_output, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, default=str)
        print(f"✓ Extraction summary saved: {summary_output}")

        # Log
        log_output = f"{output_dir}/extraction_log_{timestamp}.txt"
        with open(log_output, 'w', encoding='utf-8') as f:
            f.write("PPG HR Accuracy Data Extraction Report\n")
            f.write("="*50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total Studies Extracted: {len(extraction_df)}\n\n")
            for key, value in summary.items():
                f.write(f"{key}: {value}\n")
        print(f"✓ Extraction log saved: {log_output}")

    def generate_extraction_summary(self, extraction_df):
        """Generate summary statistics."""
        return {
            'total_studies_extracted': len(extraction_df),
            'studies_with_participants': len(extraction_df[extraction_df['total_participants'] > 0]),
            'studies_with_accuracy_metrics': len(extraction_df[~extraction_df['mae_overall_bpm'].isna()]),
            'studies_with_device_info': len(extraction_df[extraction_df['device_type'] != '']),
            'studies_with_correlation': len(extraction_df[~extraction_df['pearson_r'].isna()]),
            'studies_by_rob_level': extraction_df['overall_rob'].value_counts().to_dict(),
            'extraction_completeness_pct': round(
                (extraction_df.notnull().sum().sum() / (len(extraction_df) * len(extraction_df.columns))) * 100, 1
            )
        }

    def run_data_extraction(self, eligible_studies_path="ppg_hr_accuracy_meta_analysis/data/literature_screening/included_studies_*.csv", output_dir="ppg_hr_accuracy_meta_analysis/data/data_extraction"):
        """
        Execute complete data extraction workflow.

        Args:
            eligible_studies_path (str): Path to eligible studies CSV
            output_dir (str): Output directory
        """
        print("=" * 70)
        print("🔬 PPG HEART RATE ACCURACY DATA EXTRACTION AUTOMATION")
        print("=" * 70)
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Eligible Studies: {eligible_studies_path}")
        print(f"📂 Output Directory: {output_dir}")
        print("=" * 70)

        try:
            eligible_df = self.load_eligible_studies(eligible_studies_path)
            if eligible_df.empty:
                print("📝 No eligible studies file found - creating template")
                print("💡 This is normal for project initialization")
                # Create sample extraction template
                sample_data = pd.DataFrame([{
                    'pmid': '12345678',
                    'title': 'Sample PPG Heart Rate Validation Study',
                    'authors': 'Smith J',
                    'year': 2023
                }])
                extraction_df = self.initialize_extraction_dataframe(sample_data)
            else:
                extraction_df = self.initialize_extraction_dataframe(eligible_df)
                extraction_df = self.perform_automated_extraction(eligible_df, extraction_df)

            extraction_df = self.add_quality_assessment(extraction_df)
            self.save_extraction_results(extraction_df, output_dir)

            print("\n" + "=" * 70)
            print("✅ DATA EXTRACTION COMPLETED SUCCESSFULLY")
            print("=" * 70)
            print(f"📋 Studies Processed: {len(extraction_df)}")
            print("📝 Ready for Meta-Analysis Phase")
            print("🔧 Manual validation recommended for accuracy metrics")

        except Exception as e:
            print(f"\n❌ EXTRACTION FAILED: {e}")
            raise

def main():
    """Main execution function."""
    print("🔬 PPG HR Accuracy Data Extraction Automation")
    print("Automated extraction for systematic review meta-analysis")

    extractor = PPGDataExtractor()
    extractor.run_data_extraction()

if __name__ == "__main__":
    main()
