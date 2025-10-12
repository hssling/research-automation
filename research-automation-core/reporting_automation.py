"""
Reporting Automation System
PRISMA flowcharts, compliance reporting, and automated documentation
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
from datetime import datetime
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, BoxStyle, Rectangle
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PRISMAData:
    """Data structure for PRISMA flowchart"""

    identification: int = 0
    screening: int = 0
    eligibility: int = 0
    included: int = 0
    duplicates: int = 0
    full_text_screened: int = 0
    records_excluded_screening: int = 0
    records_excluded_eligibility: int = 0
    reasons_screening: Dict[str, int] = None
    reasons_eligibility: Dict[str, int] = None

    def __post_init__(self):
        if self.reasons_screening is None:
            self.reasons_screening = {}
        if self.reasons_eligibility is None:
            self.reasons_eligibility = {}


class PRISMAFlowchartGenerator:
    """Generate PRISMA flowcharts automatically"""

    def __init__(self):
        self.colors = {
            'identification': '#e1f5fe',
            'screening': '#fff3e0',
            'eligibility': '#f3e5f5',
            'included': '#e8f5e8',
            'excluded': '#ffebee'
        }
        self.font_size = 10

    def generate_flowchart(self, prisma_data: PRISMAData,
                          output_file: str = 'prisma_flowchart.png',
                          title: str = 'PRISMA Flow Diagram') -> str:
        """Generate PRISMA flowchart"""

        logger.info("Generating PRISMA flowchart")

        # Create figure with custom size
        fig, ax = plt.subplots(figsize=(12, 16))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')

        # Draw boxes
        y_position = 85

        # Identification box
        id_text = f"Records identified from\ndatabases (n={prisma_data.identification})"
        self._draw_box(ax, 15, y_position, 70, 8, id_text, self.colors['identification'])

        y_position -= 15

        # Duplicates removed
        dup_text = f"Records after duplicates removed\n(n={prisma_data.identification - prisma_data.duplicates})"
        self._draw_box(ax, 15, y_position, 70, 8, dup_text, self.colors['identification'])

        y_position -= 12

        # Screening box
        screening_text = f"Records screened\n(n={prisma_data.screening})"
        self._draw_box(ax, 15, y_position, 35, 8, screening_text, self.colors['screening'])

        y_position -= 10

        # Records excluded at screening
        excluded_screening = prisma_data.screening - prisma_data.full_text_screened
        if excluded_screening > 0:
            excl_screening_text = f"Records excluded\n(n={excluded_screening})"
            self._draw_box(ax, 55, y_position, 35, 8, excl_screening_text, self.colors['excluded'],
                          reasons=prisma_data.reasons_screening)

            # Draw arrow from screening to excluded
            self._draw_arrow(ax, 35, y_position + 7, 55, y_position + 4)

        # Full-text screening
        y_position -= 15
        full_text_text = f"Full-text articles assessed\nfor eligibility\n(n={prisma_data.full_text_screened})"
        self._draw_box(ax, 15, y_position, 35, 10, full_text_text, self.colors['eligibility'])

        y_position -= 12

        # Records excluded at eligibility
        excluded_eligibility = prisma_data.full_text_screened - prisma_data.included
        if excluded_eligibility > 0:
            excl_elig_text = f"Full-text articles excluded,\nwith reasons\n(n={excluded_eligibility})"
            self._draw_box(ax, 55, y_position, 35, 10, excl_elig_text, self.colors['excluded'],
                          reasons=prisma_data.reasons_eligibility)

            # Draw arrow from eligibility assessment to excluded
            self._draw_arrow(ax, 35, y_position + 9, 55, y_position + 7)

        # Studies included
        y_position -= 18
        included_text = f"Studies included in\nqualitative synthesis\n(n={prisma_data.included})"
        self._draw_box(ax, 15, y_position, 70, 8, included_text, self.colors['included'])

        # If meta-analysis
        if hasattr(prisma_data, 'meta_analysis') and prisma_data.meta_analysis > 0:
            y_position -= 12
            meta_text = f"Studies included in\nquantitative synthesis\n(meta-analysis)\n(n={prisma_data.meta_analysis})"
            self._draw_box(ax, 15, y_position, 70, 10, meta_text, self.colors['included'])

        # Add arrows connecting the flow
        self._draw_arrow(ax, 50, 91, 50, 92)  # From identification down
        self._draw_arrow(ax, 35, 82, 35, 70)  # From duplicates to screening
        self._draw_arrow(ax, 35, 57, 35, 40)  # From screening to full-text

        # Title
        plt.suptitle(title, fontsize=14, fontweight='bold', y=0.95)

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"PRISMA flowchart saved to {output_file}")
        return output_file

    def _draw_box(self, ax, x: float, y: float, width: float, height: float,
                  text: str, color: str, reasons: Dict[str, int] = None):
        """Draw a PRISMA flowchart box"""

        # Create box
        box = FancyBboxPatch((x, y), width, height,
                           boxstyle="round,pad=0.05",
                           facecolor=color,
                           edgecolor='black',
                           linewidth=1.5)
        ax.add_patch(box)

        # Add text
        ax.text(x + width/2, y + height/2, text,
               ha='center', va='center', fontsize=self.font_size,
               fontweight='normal', wrap=True)

        # Add reasons if provided
        if reasons:
            reasons_text = []
            for reason, count in reasons.items():
                if count > 0:
                    reasons_text.append(f"{reason}: {count}")

            if reasons_text:
                reasons_str = "\n".join(reasons_text)

                # Place reasons below the box
                ax.text(x + width/2, y - 0.5, reasons_str,
                       ha='center', va='top', fontsize=8,
                       fontstyle='italic', wrap=True)

    def _draw_arrow(self, ax, x1: float, y1: float, x2: float, y2: float):
        """Draw an arrow between boxes"""

        ax.arrow(x1, y1, x2 - x1, y2 - y1,
                head_width=1.5, head_length=1.5,
                fc='black', ec='black', linewidth=1.5)

    def generate_from_search_history(self, search_data: pd.DataFrame,
                                   screening_data: pd.DataFrame = None) -> PRISMAData:
        """Generate PRISMA data from search and screening data"""

        prisma_data = PRISMAData()

        # Records identified
        prisma_data.identification = len(search_data)

        # Remove duplicates (assume based on duplicates column or calculate)
        if 'is_duplicate' in search_data.columns:
            prisma_data.duplicates = search_data['is_duplicate'].sum()
        else:
            # Simple deduplication estimate
            prisma_data.duplicates = int(len(search_data) * 0.1)  # 10% estimate

        prisma_data.screening = len(search_data) - prisma_data.duplicates

        # Full-text screening
        if screening_data is not None and not screening_data.empty:
            prisma_data.full_text_screened = len(screening_data)
            prisma_data.included = screening_data['included'].sum() if 'included' in screening_data.columns else 0
            prisma_data.records_excluded_eligibility = prisma_data.full_text_screened - prisma_data.included

            # Extract exclusion reasons
            if 'exclusion_reason' in screening_data.columns:
                reasons = screening_data[screening_data['included'] == False]['exclusion_reason'].value_counts()
                prisma_data.reasons_eligibility = reasons.to_dict()

        # Calculate screening exclusions
        prisma_data.records_excluded_screening = prisma_data.screening - prisma_data.full_text_screened

        return prisma_data


class ComplianceReporter:
    """Generate compliance reports for research standards"""

    def __init__(self):
        self.standards = {
            'PRISMA': self._check_prisma_compliance,
            'Cochrane': self._check_cochrane_compliance,
            'CONSORT': self._check_consort_compliance,
            'STROBE': self._check_strobe_compliance
        }

    def generate_compliance_report(self, project_data: Dict[str, Any],
                                 standards: List[str] = ['PRISMA']) -> Dict[str, Any]:
        """Generate compliance report for specified standards"""

        report = {
            'generated_date': datetime.now().isoformat(),
            'project_info': project_data.get('metadata', {}),
            'standards_checked': standards,
            'compliance_results': {},
            'overall_compliance': {},
            'recommendations': []
        }

        for standard in standards:
            if standard in self.standards:
                checker = self.standards[standard]
                compliance_result = checker(project_data)
                report['compliance_results'][standard] = compliance_result

                # Calculate overall compliance for this standard
                if 'items' in compliance_result:
                    completed = sum(1 for item in compliance_result['items'].values() if item.get('status') == 'completed')
                    total = len(compliance_result['items'])
                    compliance_percent = (completed / total) * 100 if total > 0 else 0

                    report['overall_compliance'][standard] = {
                        'completed_items': completed,
                        'total_items': total,
                        'compliance_percentage': compliance_percent,
                        'status': self._get_compliance_status(compliance_percent)
                    }

        # Generate recommendations
        report['recommendations'] = self._generate_compliance_recommendations(report)

        return report

    def _check_prisma_compliance(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check PRISMA guideline compliance"""

        prisma_items = {
            'title': {'required': True, 'description': 'Title'},
            'abstract': {'required': True, 'description': 'Structured abstract'},
            'introduction': {'required': True, 'description': 'Background/rationale'},
            'objectives': {'required': True, 'description': 'Objectives'},
            'methods': {'required': True, 'description': 'Protocol and registration'},
            'eligibility_criteria': {'required': True, 'description': 'Eligibility criteria'},
            'information_sources': {'required': True, 'description': 'Information sources'},
            'search': {'required': True, 'description': 'Search strategy'},
            'study_selection': {'required': True, 'description': 'Study selection'},
            'data_collection': {'required': True, 'description': 'Data collection process'},
            'data_items': {'required': True, 'description': 'Data items'},
            'study_risk_of_bias': {'required': True, 'description': 'Risk of bias assessment'},
            'effect_measures': {'required': True, 'description': 'Effect measures'},
            'dealing_with_missing_data': {'required': True, 'description': 'Missing data handling'},
            'selection_of_studies': {'required': False, 'description': 'Criteria for study selection'},
            'data_synthesis': {'required': True, 'description': 'Data synthesis'},
            'reporting_bias_assessment': {'required': True, 'description': 'Publication bias assessment'},
            'certainty_assessment': {'required': True, 'description': 'Certainty of evidence assessment'},
            'study_results': {'required': True, 'description': 'Study results'},
            'study_characteristics': {'required': True, 'description': 'Study characteristics'},
            'risk_of_bias_results': {'required': True, 'description': 'Risk of bias in studies'},
            'results_of_individual_studies': {'required': True, 'description': 'Results of individual studies'},
            'results_of_syntheses': {'required': True, 'description': 'Results of syntheses'},
            'certainty_of_evidence': {'required': True, 'description': 'Certainty of evidence'},
            'discussion': {'required': True, 'description': 'Discussion and conclusions'},
            'limitations': {'required': True, 'description': 'Limitations of the review'},
            'conclusions': {'required': True, 'description': 'Conclusions'},
            'funding': {'required': True, 'description': 'Funding'},
            'conflict_of_interest': {'required': True, 'description': 'Conflict of interest'},
            'registration': {'required': True, 'description': 'Registration and protocol'},
            'support': {'required': True, 'description': 'Support'},
            'declarations': {'required': True, 'description': 'Competing interests declaration'},
            'availability': {'required': True, 'description': 'Data availability statement'},
        }

        # Check compliance based on available data
        compliance_status = {}
        manuscript = project_data.get('manuscript', {})

        for item_key, item_info in prisma_items.items():
            if item_key in ['title', 'abstract']:
                status = 'completed' if manuscript.get(item_key) else 'missing'
            elif item_key in manuscript.get('sections', {}):
                section_data = manuscript['sections'][item_key]
                word_count = section_data.get('word_count', 0)
                status = 'completed' if word_count > 10 else 'incomplete'
            elif item_key in project_data:
                status = 'completed'
            else:
                status = 'missing'

            compliance_status[item_key] = {
                'description': item_info['description'],
                'required': item_info['required'],
                'status': status
            }

        return {
            'standard': 'PRISMA 2020',
            'items': compliance_status,
            'summary': self._summarize_compliance(compliance_status)
        }

    def _check_cochrane_compliance(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check Cochrane Handbook compliance"""

        cochrane_items = {
            'question_formulation': True,
            'study_selection': True,
            'data_collection': True,
            'bias_assessment': True,
            'data_synthesis': True,
            'GRADE_assessment': False,  # Optional
            'protocol_registration': True,
            'peer_review': False  # Not always required
        }

        compliance_status = {}

        for item, required in cochrane_items.items():
            if item in project_data:
                status = 'completed'
            elif required:
                status = 'missing'
            else:
                status = 'optional'

            compliance_status[item] = {
                'required': required,
                'status': status
            }

        return {
            'standard': 'Cochrane Handbook',
            'items': compliance_status,
            'summary': self._summarize_compliance(compliance_status)
        }

    def _check_consort_compliance(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check CONSORT compliance for clinical trials"""

        consort_items = {
            'title_abstract': True,
            'introduction': True,
            'methods': True,
            'trial_design': True,
            'participants': True,
            'interventions': True,
            'outcomes': True,
            'sample_size': True,
            'randomization': True,
            'blinding': True,
            'statistical_methods': True,
            'results': True,
            'participant_flow': True,
            'recruitment': True,
            'baseline_data': True,
            'outcomes_numbers': True,
            'ancillary_analyses': True,
            'adverse_events': True,
            'discussion': True,
            'generalizability': True,
            'interpretation': True,
            'registration': True,
            'protocol': True,
            'funding': True
        }

        compliance_status = {}

        for item, required in consort_items.items():
            if item in project_data.get('manuscript', {}).get('sections', {}):
                status = 'completed'
            elif required:
                status = 'missing'
            else:
                status = 'optional'

            compliance_status[item] = {
                'required': required,
                'status': status
            }

        return {
            'standard': 'CONSORT 2010',
            'items': compliance_status,
            'summary': self._summarize_compliance(compliance_status)
        }

    def _check_strobe_compliance(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check STROBE compliance for observational studies"""

        strobe_items = {
            'title_abstract': True,
            'introduction': True,
            'methods': True,
            'study_design': True,
            'setting': True,
            'participants': True,
            'variables': True,
            'data_sources': True,
            'bias': True,
            'study_size': True,
            'quantitative_variables': True,
            'statistical_methods': True,
            'results': True,
            'participants': True,
            'descriptive_data': True,
            'outcome_data': True,
            'main_results': True,
            'other_analyses': True,
            'discussion': True,
            'limitations': True,
            'interpretation': True,
            'generalizability': True,
            'funding': True
        }

        compliance_status = {}

        for item, required in strobe_items.items():
            if item in project_data.get('manuscript', {}).get('sections', {}):
                status = 'completed'
            elif required:
                status = 'missing'
            else:
                status = 'optional'

            compliance_status[item] = {
                'required': required,
                'status': status
            }

        return {
            'standard': 'STROBE',
            'items': compliance_status,
            'summary': self._summarize_compliance(compliance_status)
        }

    def _summarize_compliance(self, compliance_status: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize compliance status"""

        completed = sum(1 for item in compliance_status.values() if item.get('status') == 'completed')
        required_missing = sum(1 for item in compliance_status.values()
                              if item.get('required') and item.get('status') == 'missing')

        total_required = sum(1 for item in compliance_status.values() if item.get('required'))

        return {
            'completed_items': completed,
            'required_missing': required_missing,
            'total_items': len(compliance_status),
            'total_required': total_required,
            'compliance_rate': completed / len(compliance_status) if len(compliance_status) > 0 else 0
        }

    def _get_compliance_status(self, compliance_percentage: float) -> str:
        """Get overall compliance status"""

        if compliance_percentage >= 90:
            return 'Excellent'
        elif compliance_percentage >= 75:
            return 'Good'
        elif compliance_percentage >= 60:
            return 'Adequate'
        elif compliance_percentage >= 40:
            return 'Needs improvement'
        else:
            return 'Poor'

    def _generate_compliance_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving compliance"""

        recommendations = []

        for standard, results in report.get('compliance_results', {}).items():
            summary = results.get('summary', {})
            compliance_rate = summary.get('compliance_rate', 0)

            if compliance_rate < 0.8:
                recommendations.append(f"Improve {standard} compliance - currently {compliance_rate:.1%}")

            if summary.get('required_missing', 0) > 0:
                recommendations.append(f"Complete missing {standard} items: {summary['required_missing']} required items are missing")

        return recommendations

    def export_report(self, report: Dict[str, Any], output_file: str = 'compliance_report.md') -> str:
        """Export compliance report to file"""

        md_content = []

        md_content.append(f"# Research Compliance Report\n")
        md_content.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Standards overview
        md_content.append("## Standards Overview\n")
        md_content.append("| Standard | Compliance Rate | Status | Completed/Total |\n")
        md_content.append("|----------|----------------|--------|----------------|\n")

        for standard, compliance in report.get('overall_compliance', {}).items():
            completed = compliance.get('completed_items', 0)
            total = compliance.get('total_items', 0)
            rate = compliance.get('compliance_percentage', 0)
            status = compliance.get('status', '')

            md_content.append(".1f"
                           f"{completed}/{total} |\n")

        md_content.append("")

        # Detailed results
        for standard, results in report.get('compliance_results', {}).items():
            md_content.append(f"## {standard} Compliance Details\n")

            items = results.get('items', {})
            summary = results.get('summary', {})

            md_content.append(f"**Overall:** {summary.get('compliance_rate', 0):.1%} "
                            f"({summary.get('completed_items', 0)}/{summary.get('total_items', 0)} items)\n")

            if items:
                md_content.append("\n### Itemized Checklist\n")

                for item_key, item_data in items.items():
                    status = item_data.get('status', 'unknown')
                    required = item_data.get('required', False)
                    description = item_data.get('description', item_key)

                    checkmark = "✅" if status == 'completed' else "❌" if status == 'missing' else "⚠️"
                    required_text = " (Required)" if required else " (Optional)"

                    md_content.append(".1f")

                md_content.append("")

        # Recommendations
        if report.get('recommendations'):
            md_content.append("## Recommendations\n")

            for rec in report['recommendations']:
                md_content.append(f"- {rec}\n")

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(''.join(md_content))

        logger.info(f"Compliance report exported to {output_file}")
        return output_file


class AutomatedReporter:
    """Main automated reporting system"""

    def __init__(self):
        self.prisma_generator = PRISMAFlowchartGenerator()
        self.compliance_reporter = ComplianceReporter()

    def generate_full_report_package(self, project_data: Dict[str, Any],
                                   output_dir: str = 'research_reports') -> Dict[str, Any]:
        """Generate complete reporting package"""

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        logger.info("Generating comprehensive research reporting package")

        reports = {}

        # PRISMA flowchart
        prisma_data = self._extract_prisma_data(project_data)
        if prisma_data:
            prisma_file = self.prisma_generator.generate_flowchart(
                prisma_data,
                output_file=str(output_path / 'prisma_flowchart.png')
            )
            reports['prisma_flowchart'] = prisma_file

        # Compliance reports
        standards = ['PRISMA']  # Default to PRISMA
        if project_data.get('study_type') == 'clinical_trial':
            standards.append('CONSORT')
        elif project_data.get('study_type') in ['cohort', 'case_control']:
            standards.append('STROBE')

        compliance_report = self.compliance_reporter.generate_compliance_report(
            project_data, standards
        )

        compliance_file = self.compliance_reporter.export_report(
            compliance_report,
            output_file=str(output_path / 'compliance_report.md')
        )
        reports['compliance_report'] = compliance_file

        # Meta-analysis report
        if 'meta_results' in project_data:
            meta_report = self._generate_meta_analysis_report(
                project_data, output_path
            )
            reports.update(meta_report)

        # Quality assessment summary
        if 'quality_assessment' in project_data:
            quality_report = self._generate_quality_summary(
                project_data['quality_assessment'], output_path
            )
            reports['quality_summary'] = quality_report

        # Generate summary report
        summary_file = self._generate_summary_report(reports, project_data, output_path)
        reports['summary_report'] = summary_file

        logger.info(f"Generated {len(reports)} reports in {output_dir}")
        return reports

    def _extract_prisma_data(self, project_data: Dict[str, Any]) -> Optional[PRISMAData]:
        """Extract PRISMA data from project data"""

        # Try different sources
        if 'prisma_data' in project_data:
            return project_data['prisma_data']

        # Extract from search and screening data
        if 'search_results' in project_data and 'screening_results' in project_data:
            prisma_data = self.prisma_generator.generate_from_search_history(
                project_data['search_results'],
                project_data['screening_results']
            )
            return prisma_data

        # Manual extraction
        if 'literature_search_results' in project_data:
            search_results = pd.DataFrame(project_data['literature_search_results'])
            prisma_data = PRISMAData()

            prisma_data.identification = len(search_results)

            # Estimate duplicates
            prisma_data.duplicates = int(len(search_results) * 0.1)

            prisma_data.screening = len(search_results) - prisma_data.duplicates

            # Try to get screening data
            if 'literature_screening' in project_data:
                screening_df = pd.DataFrame(project_data['literature_screening'])
                prisma_data.full_text_screened = len(screening_df)
                prisma_data.included = screening_df.get('included', pd.Series([True]*len(screening_df))).sum()

            return prisma_data

        return None

    def _generate_meta_analysis_report(self, project_data: Dict[str, Any],
                                     output_path: Path) -> Dict[str, str]:
        """Generate detailed meta-analysis report"""

        meta_results = project_data.get('meta_results', {})

        if not meta_results:
            return {}

        report_file = output_path / 'meta_analysis_detailed_report.md'
        plot_dir = output_path / 'plots'
        plot_dir.mkdir(exist_ok=True)

        # This would integrate with meta_analyzer.py for detailed reports
        # For now, create a basic report

        report_content = f"""# Meta-Analysis Detailed Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

Overall Effect Size: {meta_results.get('primary_results', {}).get('overall_effect', 'N/A')}
Heterogeneity (I²): {meta_results.get('primary_results', {}).get('heterogeneity_test', {}).get('I2', 'N/A')}%

## Methodology

- Method: {meta_results.get('primary_method', 'Unknown')}
- Studies included: {meta_results.get('total_studies', 0)}
- Effect measure: Standardized mean difference

## Results Interpretation

{self._interpret_meta_results(meta_results)}

## Recommendations

{self._generate_meta_recommendations(meta_results)}
"""

        with open(report_file, 'w') as f:
            f.write(report_content)

        return {'meta_analysis_report': str(report_file), 'plots_dir': str(plot_dir)}

    def _interpret_meta_results(self, meta_results: Dict[str, Any]) -> str:
        """Interpret meta-analysis results"""

        primary = meta_results.get('primary_results', {})
        overall_effect = primary.get('overall_effect', 0)
        p_value = primary.get('p_value', 1)
        i2 = primary.get('heterogeneity_test', {}).get('I2', 0)

        interpretation = []

        # Effect size interpretation
        if abs(overall_effect) < 0.2:
            interpretation.append("Small effect size observed.")
        elif abs(overall_effect) < 0.5:
            interpretation.append("Moderate effect size observed.")
        else:
            interpretation.append("Large effect size observed.")

        # Statistical significance
        if p_value < 0.05:
            interpretation.append("Results are statistically significant.")
        else:
            interpretation.append("Results are not statistically significant.")

        # Heterogeneity
        if i2 < 25:
            interpretation.append("Low heterogeneity suggests consistent findings.")
        elif i2 < 50:
            interpretation.append("Moderate heterogeneity observed.")
        elif i2 < 75:
            interpretation.append("Substantial heterogeneity requires investigation.")
        else:
            interpretation.append("Considerable heterogeneity suggests effect modifiers.")

        return " ".join(interpretation)

    def _generate_meta_recommendations(self, meta_results: Dict[str, Any]) -> str:
        """Generate recommendations based on meta-analysis results"""

        recommendations = []

        primary = meta_results.get('primary_results', {})
        i2 = primary.get('heterogeneity_test', {}).get('I2', 0)

        if i2 > 50:
            recommendations.append("Investigate sources of heterogeneity with subgroup analyses.")
            recommendations.append("Consider random-effects model for future analyses.")

        if len(meta_results.get('study_data', [])) < 10:
            recommendations.append("Consider additional studies to increase statistical power.")

        return "\n".join([f"- {rec}" for rec in recommendations])

    def _generate_quality_summary(self, quality_data: Dict[str, Any],
                                output_path: Path) -> str:
        """Generate quality assessment summary"""

        summary_file = output_path / 'quality_assessment_summary.md'

        summary_content = f"""# Quality Assessment Summary
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

{quality_data.get('total_studies', 0)} studies assessed using {', '.join(quality_data.get('tools_used', []))} tools.

## Results

{self._format_quality_results(quality_data)}
"""

        with open(summary_file, 'w') as f:
            f.write(summary_content)

        return str(summary_file)

    def _format_quality_results(self, quality_data: Dict[str, Any]) -> str:
        """Format quality assessment results"""

        formatted = []

        for tool_name, summary in quality_data.get('summary', {}).items():
            formatted.append(f"### {tool_name}")

            for risk_level, data in summary.get('overall_risk_distribution', {}).items():
                formatted.append(f"- {risk_level}: {data['count']} studies ({data['percentage']:.1f}%)")

        return "\n".join(formatted)

    def _generate_summary_report(self, reports: Dict[str, Any],
                               project_data: Dict[str, Any],
                               output_path: Path) -> str:
        """Generate summary of all reports"""

        summary_file = output_path / 'reporting_package_summary.md'

        summary_content = f"""# Research Reporting Package Summary
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Information

- **Project Type:** {project_data.get('study_type', 'Unknown')}
- **Total Studies:** {project_data.get('total_studies', 0)}
- **Generated Reports:** {len(reports)}

## Generated Reports

"""

        for report_name, report_path in reports.items():
            display_name = report_name.replace('_', ' ').title()
            summary_content += f"- **{display_name}:** {report_path}\n"

        # Compliance summary
        summary_content += "\n## Compliance Status\n\n"

        # Include compliance summary if available
        # This would be expanded with actual compliance checking

        summary_content += "## Usage Recommendations\n\n"
        summary_content += "- Use PRISMA flowchart in manuscript methods section\n"
        summary_content += "- Include compliance report in supplementary materials\n"
        summary_content += "- Reference quality assessment results in discussion\n"
        summary_content += "- Use meta-analysis results for evidence synthesis\n"

        with open(summary_file, 'w') as f:
            f.write(summary_content)

        return str(summary_file)


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automated Reporting System")
    parser.add_argument("project_data", help="JSON file with project data")
    parser.add_argument("--output-dir", default="research_reports",
                       help="Output directory for reports")
    parser.add_argument("--standards", nargs='+', default=['PRISMA'],
                       help="Reporting standards to check")

    args = parser.parse_args()

    # Load project data
    with open(args.project_data, 'r') as f:
        project_data = json.load(f)

    # Generate reports
    reporter = AutomatedReporter()
    reports = reporter.generate_full_report_package(project_data, args.output_dir)

    print("Research reporting package generated!")
    print("\nGenerated reports:")
    for name, path in reports.items():
        print(f"  {name}: {path}")

    print(f"\nAll reports saved to: {args.output_dir}")
