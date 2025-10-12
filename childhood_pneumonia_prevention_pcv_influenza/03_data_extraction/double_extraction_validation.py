#!/usr/bin/env python3
"""
Dual Independent Data Extraction Validation for PCV Effectiveness Systematic Review
Ensures robust quality control through double extraction methodology
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

class DoubleExtractionValidator:
    """Handles double data extraction and validation for systematic reviews"""

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.extraction_dir = self.project_dir / "03_data_extraction"
        self.reports_dir = self.extraction_dir / "validation_reports"
        self.reports_dir.mkdir(exist_ok=True)

    def load_extraction_data(self):
        """Load data from both extractors"""
        try:
            # Assuming two extractors save their files with identifiers
            data_extractor1 = pd.read_csv(self.extraction_dir / "extracted_data_extractor1.csv")
            data_extractor2 = pd.read_csv(self.extraction_dir / "extracted_data_extractor2.csv")

            print(f"Loaded {len(data_extractor1)} records from Extractor 1")
            print(f"Loaded {len(data_extractor2)} records from Extractor 2")

            return data_extractor1, data_extractor2

        except FileNotFoundError as e:
            print(f"Error: Extraction files not found. {e}")
            print("Need both extracted_data_extractor1.csv and extracted_data_extractor2.csv")
            return None, None

    def calculate_agreement_metrics(self, data1: pd.DataFrame, data2: pd.DataFrame, variables_to_check: list):
        """Calculate agreement statistics between two extractors"""
        results = {}
        total_records = len(data1)

        print(f"\n=== INTER-EXTRACTOR AGREEMENT ANALYSIS ===")
        print(f"Total records: {total_records}")
        print(f"Variables checked: {', '.join(variables_to_check)}")

        for var in variables_to_check:
            if var not in data1.columns or var not in data2.columns:
                print(f"Warning: Variable '{var}' not found in one or both datasets")
                continue

            # Handle missing values consistently
            val1 = data1[var].fillna('MISSING')
            val2 = data2[var].fillna('MISSING')

            # Calculate agreement statistics
            matches = (val1 == val2).sum()
            total_valid = len(val1)
            agreement_rate = matches / total_valid * 100

            # Calculate Cohen's Kappa for categorical variables
            if var in ['study_design', 'income_level', 'outcome_primary']:
                try:
                    from sklearn.metrics import cohen_kappa_score
                    kappa = cohen_kappa_score(val1, val2)
                    kappa_interpretation = self.interpret_kappa(kappa)
                except ImportError:
                    kappa = 'sklearn not available'
                    kappa_interpretation = 'N/A'
            else:
                kappa = 'N/A'
                kappa_interpretation = 'N/A'

            results[var] = {
                'matches': int(matches),
                'total_valid': total_valid,
                'agreement_rate': round(agreement_rate, 2),
                'kappa_score': kappa,
                'kappa_interpretation': kappa_interpretation
            }

            print(f"{var}: {agreement_rate:.1f}% agreement (Cohen's κ: {kappa})")

            discrepancies = val1[val1 != val2]
            if len(discrepancies) > 0:
                print(f"  - Discrepancies: {len(discrepancies)}")
                print(f"  - Examples: {discrepancies.head(3).to_dict()}")

        return results

    def interpret_kappa(self, kappa: float) -> str:
        """Interpret Cohen's Kappa values"""
        if kappa < 0:
            return "Poor agreement"
        elif kappa < 0.20:
            return "Slight agreement"
        elif kappa < 0.40:
            return "Fair agreement"
        elif kappa < 0.60:
            return "Moderate agreement"
        elif kappa < 0.80:
            return "Substantial agreement"
        elif kappa < 0.90:
            return "Almost perfect agreement"
        else:
            return "Perfect agreement"

    def validate_numeric_consistency(self, data1: pd.DataFrame, data2: pd.DataFrame):
        """Validate numeric consistency for key outcomes"""
        numeric_vars = ['rr_lci', 'rr_uci', 'num_events', 'person_years']

        print(f"\n=== NUMERIC CONSISTENCY CHECK ===")

        for var in numeric_vars:
            if var in data1.columns and var in data2.columns:
                try:
                    val1 = pd.to_numeric(data1[var], errors='coerce')
                    val2 = pd.to_numeric(data2[var], errors='coerce')

                    mean_diff = abs(val1 - val2).mean()
                    max_diff = abs(val1 - val2).max()

                    print(f"{var}:")
                    print(".2f")
                    print(".2f")

                    # Flag major discrepancies
                    if max_diff > 5:  # Arbitrary threshold
                        high_diff_cases = (abs(val1 - val2) > 5).sum()
                        print(f"  - Major discrepancies (>5): {high_diff_cases} cases")

                except Exception as e:
                    print(f"  - Error processing {var}: {e}")

    def generate_arbitration_log(self, data1: pd.DataFrame, data2: pd.DataFrame, variables_to_check: list):
        """Generate log of discrepancies requiring arbitration"""
        arbitration_cases = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for idx in data1.index:
            study_id = data1.loc[idx, 'study_id']
            discrepancies = {}

            for var in variables_to_check:
                if var in data1.columns and var in data2.columns:
                    val1 = data1.loc[idx, var]
                    val2 = data2.loc[idx, var]

                    if pd.isna(val1) and pd.isna(val2):
                        continue
                    elif str(val1) != str(val2):
                        discrepancies[var] = {
                            'extractor1': val1,
                            'extractor2': val2
                        }

            if discrepancies:
                arbitration_cases.append({
                    'study_id': study_id,
                    'discrepancies': discrepancies
                })

        # Save arbitration log
        arbitration_file = self.reports_dir / f"arbitration_cases_{timestamp}.json"
        with open(arbitration_file, 'w') as f:
            json.dump({
                'total_arbitration_cases': len(arbitration_cases),
                'timestamp': timestamp,
                'cases': arbitration_cases
            }, f, indent=2, default=str)

        print(f"\nArbitration log saved: {arbitration_file}")
        print(f"Cases requiring arbitration: {len(arbitration_cases)}")

        return arbitration_cases

    def generate_validation_report(self, agreement_metrics: dict, arbitration_cases: list):
        """Generate comprehensive validation report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"double_extraction_validation_report_{timestamp}.md"

        # Overall statistics
        total_vars = len(agreement_metrics)
        high_agreement_vars = sum(1 for v in agreement_metrics.values() if v['agreement_rate'] >= 90)
        max_discrepancies = max(len(case['discrepancies']) for case in arbitration_cases) if arbitration_cases else 0

        report_content = f"""# Double Data Extraction Validation Report
**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview
- **Total variables assessed:** {total_vars}
- **Variables with ≥90% agreement:** {high_agreement_vars} ({high_agreement_vars/total_vars*100:.1f}%)
- **Total arbitration cases:** {len(arbitration_cases)}
- **Maximum discrepancies per study:** {max_discrepancies}

## Agreement Metrics by Variable

| Variable | Agreement Rate (%) | Cohen's Kappa | Interpretation |
|----------|-------------------|---------------|----------------|
"""

        for var_name, metrics in agreement_metrics.items():
            kappa_display = ".3f" if isinstance(metrics['kappa_score'], (int, float)) else str(metrics['kappa_score'])
            report_content += f"| {var_name} | {metrics['agreement_rate']:.1f} | {kappa_display} | {metrics['kappa_interpretation']} |\n"

        report_content += "\n## Arbitration Summary\n"

        if arbitration_cases:
            report_content += "- **Studies requiring arbitration:** " + ", ".join([case['study_id'] for case in arbitration_cases])
        else:
            report_content += "- **All studies show perfect agreement - no arbitration needed**"

        report_content += "\n\n## Quality Assessment\n"

        # Quality thresholds
        if high_agreement_vars / total_vars >= 0.8:
            report_content += "- ✅ **Overall Quality:** High (≥80% variables with ≥90% agreement)\n"
        elif high_agreement_vars / total_vars >= 0.6:
            report_content += "- ⚠️ **Overall Quality:** Moderate (60-79% variables with ≥90% agreement)\n"
        else:
            report_content += "- ❌ **Overall Quality:** Low (<60% variables with ≥90% agreement)\n"

        report_content += f"- **Arbitration burden:** {len(arbitration_cases)} cases ({len(arbitration_cases)/len(agreement_metrics.get('study_id', {'total_valid': 1})['total_valid'])*100:.1f}% of studies)\n"

        report_content += "\n## Recommendations\n"
        if len(arbitration_cases) == 0:
            report_content += "- Proceed to data synthesis without arbitration\n"
        elif len(arbitration_cases) < 5:
            report_content += "- Minor arbitration required - continue with systematic review\n"
        else:
            report_content += "- Significant arbitration required - consider additional training or re-extraction\n"

        # Save report
        with open(report_file, 'w') as f:
            f.write(report_content)

        print(f"\nValidation report saved: {report_file}")
        print("Double extraction validation complete!")

        return report_content

def main():
    """Main validation workflow"""
    project_dir = "childhood_pneumonia_prevention_pcv_influenza"

    if not Path(project_dir).exists():
        print(f"Project directory not found: {project_dir}")
        return

    validator = DoubleExtractionValidator(project_dir)

    # Load data from two extractors
    data1, data2 = validator.load_extraction_data()

    if data1 is None or data2 is None:
        print("Cannot proceed without both extractor datasets.")
        print("Required files:")
        print("- 03_data_extraction/extracted_data_extractor1.csv")
        print("- 03_data_extraction/extracted_data_extractor2.csv")
        return

    # Variables to check for agreement
    critical_variables = [
        'study_id', 'study_design', 'country', 'income_level',
        'pcv_product', 'pcv_schedule', 'outcome_primary',
        'rr_lci', 'rr_uci', 'num_events', 'person_years'
    ]

    # Perform validation steps
    agreement_metrics = validator.calculate_agreement_metrics(data1, data2, critical_variables)
    validator.validate_numeric_consistency(data1, data2)
    arbitration_cases = validator.generate_arbitration_log(data1, data2, critical_variables)
    validator.generate_validation_report(agreement_metrics, arbitration_cases)

    # Summary for paper
    print(f"\n{'='*50}")
    print("VALIDATION SUMMARY FOR MANUSCRIPT")
    print(f"{'='*50}")
    print(f"Variables with high agreement (≥90%): {sum(1 for v in agreement_metrics.values() if v['agreement_rate'] >= 90)}/{len(agreement_metrics)}")
    print(f"Studies requiring arbitration: {len(arbitration_cases)}")
    print("✅ Double extraction quality assessment complete"
if __name__ == "__main__":
    main()
