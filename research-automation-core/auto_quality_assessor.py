"""
Automated Quality Assessment System
ROBIS, Cochrane, and GRADE assessment automation for systematic reviews
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import json
from datetime import datetime
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QualityDomain:
    """Represents a single quality assessment domain"""

    def __init__(self, name: str, question: str, criteria: Dict[str, Any],
                 scoring_method: str = 'categorical'):
        self.name = name
        self.question = question
        self.criteria = criteria
        self.scoring_method = scoring_method  # 'categorical', 'numerical', 'yes_no'

    def assess_answer(self, answer: Any) -> Tuple[str, int]:
        """Assess an answer against criteria to get risk level and score"""

        if self.scoring_method == 'categorical':
            for risk_level, conditions in self.criteria.items():
                if isinstance(conditions, list):
                    if answer in conditions:
                        return risk_level, self._get_risk_score(risk_level)
                elif answer == conditions:
                    return risk_level, self._get_risk_score(risk_level)

        elif self.scoring_method == 'yes_no':
            if answer in ['yes', 'Yes', 'Y', 'y', True, 1]:
                return 'Low', 1
            elif answer in ['no', 'No', 'N', 'n', False, 0]:
                return 'High', -1
            else:
                return 'Unclear', 0

        return 'Unclear', 0

    def _get_risk_score(self, risk_level: str) -> int:
        """Convert risk level to numerical score"""
        score_map = {
            'Low': 1,
            'Moderate': 0,
            'High': -1,
            'Critical': -2,
            'Unclear': 0
        }
        return score_map.get(risk_level, 0)


class QualityAssessmentTool:
    """Base class for quality assessment tools"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.domains = {}

    def add_domain(self, domain: QualityDomain):
        """Add an assessment domain"""
        self.domains[domain.name] = domain

    def assess_study(self, study_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess a single study"""

        results = {
            'study_id': study_data.get('study_id', ''),
            'assessment_tool': self.name,
            'assessment_date': datetime.now().isoformat(),
            'domain_assessments': {},
            'overall_risk': 'Unclear',
            'overall_score': 0
        }

        domain_scores = []

        for domain_name, domain in self.domains.items():
            answer = study_data.get(domain_name, study_data.get(f"{domain_name}_assessment"))

            if answer is not None:
                risk_level, score = domain.assess_answer(answer)
                results['domain_assessments'][domain_name] = {
                    'question': domain.question,
                    'answer': answer,
                    'risk_level': risk_level,
                    'score': score
                }
                domain_scores.append(score)
            else:
                results['domain_assessments'][domain_name] = {
                    'question': domain.question,
                    'answer': None,
                    'risk_level': 'Not assessed',
                    'score': 0
                }

        # Calculate overall assessment
        if domain_scores:
            avg_score = np.mean(domain_scores)
            if avg_score >= 0.5:
                results['overall_risk'] = 'Low'
            elif avg_score >= -0.5:
                results['overall_risk'] = 'Moderate'
            else:
                results['overall_risk'] = 'High'

            results['overall_score'] = avg_score

        return results


class ROBISTool(QualityAssessmentTool):
    """ROBIS (Risk of Bias in Systematic Reviews) Assessment Tool"""

    def __init__(self):
        super().__init__(
            "ROBIS",
            "Risk of Bias in Systematic Reviews - assesses bias in systematic review methodology"
        )

        # Phase 1: Eligibility criteria
        self.add_domain(QualityDomain(
            "eligibility_criteria",
            "Are eligibility criteria for the review appropriate?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear"]}
        ))

        # Phase 2: Identification and selection of studies
        self.add_domain(QualityDomain(
            "comprehensive_search",
            "Did the review adhere to predefined objectives and eligibility criteria?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear"]}
        ))

        self.add_domain(QualityDomain(
            "study_selection",
            "Were published and unpublished studies (including grey literature) searched for?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear", "Partial"]}
        ))

        # Phase 3: Data collection and study appraisal
        self.add_domain(QualityDomain(
            "data_collection",
            "Were data extracted and appraised by more than one reviewer independently?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear"]}
        ))

        self.add_domain(QualityDomain(
            "quality_appraisal",
            "Were methods for assessing risk of bias predefined?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear"]}
        ))

        # Phase 4: Synthesis and findings
        self.add_domain(QualityDomain(
            "synthesis_methods",
            "Were methods for synthesizing the evidence predefined?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear"]}
        ))

        self.add_domain(QualityDomain(
            "statistical_methods",
            "Were statistical methods appropriate for the synthesis?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear", "Partial"]}
        ))

        self.add_domain(QualityDomain(
            "publication_bias",
            "Was the potential for publication bias assessed and discussed?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear"]}
        ))


class CochraneTool(QualityAssessmentTool):
    """Cochrane Risk of Bias Tool (for randomized trials)"""

    def __init__(self):
        super().__init__(
            "Cochrane RoB 2.0",
            "Cochrane Risk of Bias Tool for randomized controlled trials"
        )

        # Domain 1: Randomization process
        self.add_domain(QualityDomain(
            "random_sequence",
            "Was the allocation sequence random?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear"]}
        ))

        self.add_domain(QualityDomain(
            "allocation_concealment",
            "Was the allocation adequately concealed?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear"]}
        ))

        # Domain 2: Deviations from intended interventions
        self.add_domain(QualityDomain(
            "intervention_adherence",
            "Were participants analyzed in the group they were randomized to?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear"]}
        ))

        # Domain 3: Missing outcome data
        self.add_domain(QualityDomain(
            "missing_data_handling",
            "Were outcome data missing or incomplete?",
            {"Low": ["No missing data", "Low attrition"], "High": ["High attrition"], "Unclear": ["Unclear"]}
        ))

        # Domain 4: Measurement of the outcome
        self.add_domain(QualityDomain(
            "outcome_measurement",
            "Were outcome assessors blinded to intervention allocation?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear", "Not possible"]}
        ))

        # Domain 5: Selection of the reported result
        self.add_domain(QualityDomain(
            "selective_reporting",
            "Are the reported results the same as those specified in the protocol?",
            {"Low": ["Yes"], "High": ["No"], "Unclear": ["Unclear", "No protocol"]}
        ))


class GRADETool:
    """GRADE (Grading of Recommendations Assessment, Development and Evaluation)"""

    def __init__(self):
        self.name = "GRADE"
        self.domains = {
            'risk_of_bias': {'weight': 0.25, 'description': 'Risk of bias across studies'},
            'inconsistency': {'weight': 0.25, 'description': 'Inconsistency of results across studies'},
            'indirectness': {'weight': 0.25, 'description': 'Indirectness of evidence'},
            'imprecision': {'weight': 0.25, 'description': 'Imprecision of effect estimates'},
            'publication_bias': {'weight': 0.0, 'description': 'Publication bias'}
        }

    def assess_evidence_quality(self, meta_results: Dict[str, Any],
                              study_characteristics: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall quality of evidence using GRADE"""

        assessment = {
            'assessment_date': datetime.now().isoformat(),
            'starting_quality': self._determine_starting_quality(study_characteristics),
            'domain_assessments': {},
            'final_quality': '',
            'confidence_rating': ''
        }

        quality_score = self._get_quality_score(assessment['starting_quality'])

        # Assess each domain
        for domain_name, domain_info in self.domains.items():
            domain_assessment = self._assess_domain(domain_name, meta_results, study_characteristics)
            assessment['domain_assessments'][domain_name] = domain_assessment

            if domain_assessment['downgrade']:
                quality_score -= domain_assessment['level']

        # Determine final quality
        assessment['final_quality'] = self._score_to_quality(quality_score)
        assessment['confidence_rating'] = self._get_confidence_rating(assessment['final_quality'])

        return assessment

    def _determine_starting_quality(self, study_characteristics: Dict[str, Any]) -> str:
        """Determine starting quality based on study design"""

        study_design = study_characteristics.get('study_design', '').lower()

        if 'randomized' in study_design or 'rct' in study_design:
            return 'High'
        elif 'cohort' in study_design or 'case-control' in study_design:
            return 'Moderate'
        else:
            return 'Low'

    def _assess_domain(self, domain_name: str, meta_results: Dict[str, Any],
                      study_characteristics: Dict[str, Any]) -> Dict[str, Any]:
        """Assess a specific GRADE domain"""

        domain_assessment = {'downgrade': False, 'level': 0, 'reasoning': ''}

        if domain_name == 'risk_of_bias':
            # Check heterogeneity and study quality
            i2 = meta_results.get('primary_results', {}).get('heterogeneity_test', {}).get('I2', 0)
            if i2 > 50:
                domain_assessment['downgrade'] = True
                domain_assessment['level'] = 1
                domain_assessment['reasoning'] = f'High heterogeneity (I² = {i2:.1f}%)'

        elif domain_name == 'inconsistency':
            i2 = meta_results.get('primary_results', {}).get('heterogeneity_test', {}).get('I2', 0)
            if i2 > 75:
                domain_assessment['downgrade'] = True
                domain_assessment['level'] = 2
                domain_assessment['reasoning'] = f'Considerable heterogeneity (I² = {i2:.1f}%)'

        elif domain_name == 'imprecision':
            # Check confidence interval width and sample size
            ci_lower = meta_results.get('primary_results', {}).get('ci_lower', 0)
            ci_upper = meta_results.get('primary_results', {}).get('ci_upper', 0)
            ci_width = abs(ci_upper - ci_lower)

            if ci_width > 0.5:  # Wide confidence interval
                domain_assessment['downgrade'] = True
                domain_assessment['level'] = 1
                domain_assessment['reasoning'] = f'Wide confidence interval (width = {ci_width:.3f})'

        elif domain_name == 'indirectness':
            # Check if outcomes are direct measures
            outcome_direct = study_characteristics.get('outcome_direct', True)
            if not outcome_direct:
                domain_assessment['downgrade'] = True
                domain_assessment['level'] = 1
                domain_assessment['reasoning'] = 'Indirect outcome measures used'

        return domain_assessment

    def _get_quality_score(self, quality: str) -> int:
        """Convert quality level to numerical score"""
        quality_map = {'High': 4, 'Moderate': 3, 'Low': 2, 'Very low': 1}
        return quality_map.get(quality, 2)

    def _score_to_quality(self, score: int) -> str:
        """Convert numerical score back to quality level"""
        if score >= 4:
            return 'High'
        elif score == 3:
            return 'Moderate'
        elif score == 2:
            return 'Low'
        else:
            return 'Very low'

    def _get_confidence_rating(self, quality: str) -> str:
        """Get confidence rating description"""
        ratings = {
            'High': 'We are very confident that the true effect lies close to that of the estimate',
            'Moderate': 'We are moderately confident in the effect estimate',
            'Low': 'Our confidence in the effect estimate is limited',
            'Very low': 'We have very little confidence in the effect estimate'
        }
        return ratings.get(quality, 'Confidence rating unclear')


class AutomatedQualityAssessor:
    """Main automated quality assessment system"""

    def __init__(self):
        self.tools = {
            'robis': ROBISTool(),
            'cochrane': CochraneTool(),
            'grade': GRADETool()
        }

    def assess_study_quality(self, studies_data: pd.DataFrame,
                           assessment_type: str = 'auto',
                           output_file: str = None) -> Dict[str, Any]:
        """Assess quality of multiple studies"""

        if assessment_type not in ['auto', 'robis', 'cochrane', 'grade']:
            raise ValueError(f"Unknown assessment type: {assessment_type}")

        logger.info(f"Starting quality assessment for {len(studies_data)} studies using {assessment_type}")

        # Determine which tools to use
        if assessment_type == 'auto':
            # Auto-detect based on study type
            study_designs = studies_data.get('study_design', pd.Series()).str.lower()

            if any('systematic' in design or 'review' in design for design in study_designs):
                tools_to_use = ['robis', 'grade']
            elif any('rct' in design or 'randomized' in design for design in study_designs):
                tools_to_use = ['cochrane', 'grade']
            else:
                tools_to_use = ['grade']  # Default to GRADE for evidence quality
        else:
            tools_to_use = [assessment_type]

        results = {
            'assessment_type': assessment_type,
            'tools_used': tools_to_use,
            'total_studies': len(studies_data),
            'assessments': {},
            'summary': {},
            'assessment_date': datetime.now().isoformat()
        }

        # Apply each tool
        for tool_name in tools_to_use:
            tool = self.tools[tool_name]
            tool_assessments = []

            for _, study in studies_data.iterrows():
                assessment = tool.assess_study(dict(study))
                tool_assessments.append(assessment)

            results['assessments'][tool_name] = tool_assessments

            # Generate summary for this tool
            results['summary'][tool_name] = self._generate_tool_summary(tool_assessments)

        if output_file:
            self.save_assessments(results, output_file)

        logger.info(f"Quality assessment completed using tools: {tools_to_use}")
        return results

    def _generate_tool_summary(self, assessments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics for a tool's assessments"""

        if not assessments:
            return {}

        risk_counts = {}
        domain_summaries = {}

        for assessment in assessments:
            overall_risk = assessment.get('overall_risk', 'Unclear')
            risk_counts[overall_risk] = risk_counts.get(overall_risk, 0) + 1

            # Summarize domain assessments
            for domain_name, domain_data in assessment.get('domain_assessments', {}).items():
                if domain_name not in domain_summaries:
                    domain_summaries[domain_name] = {
                        'question': domain_data.get('question', ''),
                        'risk_distribution': {}
                    }

                domain_risk = domain_data.get('risk_level', 'Unclear')
                domain_summaries[domain_name]['risk_distribution'][domain_risk] = \
                    domain_summaries[domain_name]['risk_distribution'].get(domain_risk, 0) + 1

        total = len(assessments)
        return {
            'total_assessments': total,
            'overall_risk_distribution': {
                risk: {'count': count, 'percentage': (count/total)*100}
                for risk, count in risk_counts.items()
            },
            'domain_summaries': domain_summaries
        }

    def assess_meta_analysis_quality(self, meta_results: Dict[str, Any],
                                   study_characteristics: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall quality of meta-analysis evidence using GRADE"""

        logger.info("Assessing meta-analysis quality using GRADE")

        grade_tool = self.tools['grade']
        grade_assessment = grade_tool.assess_evidence_quality(meta_results, study_characteristics)

        # Add additional meta-analysis specific assessments
        additional_assessments = {
            'heterogeneity_assessment': self._assess_heterogeneity_quality(meta_results),
            'publication_bias_check': self._assess_publication_bias(meta_results),
            'sample_size_evaluation': self._assess_sample_size(meta_results)
        }

        grade_assessment.update(additional_assessments)

        logger.info("Meta-analysis quality assessment completed")
        return grade_assessment

    def _assess_heterogeneity_quality(self, meta_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess heterogeneity quality implications"""

        primary_results = meta_results.get('primary_results', {})
        het_test = primary_results.get('heterogeneity_test', {})
        i2 = het_test.get('I2', 0)
        q_p = het_test.get('p_value', 1)

        assessment = {'I2': i2, 'q_p_value': q_p}

        if i2 < 25:
            assessment.update({
                'level': 'Low heterogeneity',
                'implication': 'Results are relatively consistent',
                'recommendation': 'Fixed-effects model appropriate'
            })
        elif i2 < 50:
            assessment.update({
                'level': 'Moderate heterogeneity',
                'implication': 'Some variability in effects',
                'recommendation': 'Consider random-effects model'
            })
        elif i2 < 75:
            assessment.update({
                'level': 'Substantial heterogeneity',
                'implication': 'Considerable variability in effects',
                'recommendation': 'Investigate sources of heterogeneity'
            })
        else:
            assessment.update({
                'level': 'Considerable heterogeneity',
                'implication': 'Major differences between studies',
                'recommendation': 'Do not pool results or investigate thoroughly'
            })

        return assessment

    def _assess_publication_bias(self, meta_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess publication bias implications"""

        study_data = meta_results.get('study_data', [])
        num_studies = len(study_data)

        assessment = {'num_studies': num_studies}

        if num_studies < 10:
            assessment.update({
                'bias_risk': 'High',
                'reasoning': f'Only {num_studies} studies - insufficient for bias assessment',
                'recommendation': 'Results should be interpreted cautiously'
            })
        else:
            # Could add more sophisticated checks here
            # For now, basic assessment
            assessment.update({
                'bias_risk': 'Uncertain',
                'reasoning': 'Sample size adequate but formal bias testing needed',
                'recommendation': 'Conduct formal statistical tests for publication bias'
            })

        return assessment

    def _assess_sample_size(self, meta_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess total sample size across studies"""

        study_data = meta_results.get('study_data', [])
        total_n = sum(study.get('sample_size', 0) for study in study_data)
        num_studies = len(study_data)

        assessment = {
            'total_sample_size': total_n,
            'number_of_studies': num_studies,
            'mean_sample_per_study': total_n / num_studies if num_studies > 0 else 0
        }

        if total_n < 100:
            assessment['sample_size_rating'] = 'Very small'
            assessment['power_concerns'] = 'High risk of type II error'
        elif total_n < 500:
            assessment['sample_size_rating'] = 'Small'
            assessment['power_concerns'] = 'Moderate risk of inadequate power'
        elif total_n < 2000:
            assessment['sample_size_rating'] = 'Adequate'
            assessment['power_concerns'] = 'Generally acceptable power'
        else:
            assessment['sample_size_rating'] = 'Large'
            assessment['power_concerns'] = 'Excellent statistical power'

        return assessment

    def save_assessments(self, results: Dict[str, Any], output_file: str):
        """Save assessment results to file"""

        # Convert to serializable format
        serializable_results = self._make_serializable(results)

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)

        logger.info(f"Assessment results saved to {output_file}")

    def _make_serializable(self, obj):
        """Convert numpy types to Python types for JSON serialization"""
        if isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        else:
            return obj

    def generate_quality_report(self, assessments: Dict[str, Any]) -> str:
        """Generate comprehensive quality assessment report"""

        report = f"""
# Quality Assessment Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Studies Assessed:** {assessments.get('total_studies', 0)}
**Tools Used:** {', '.join(assessments.get('tools_used', []))}

"""

        # Overall summaries
        for tool_name, summary in assessments.get('summary', {}).items():
            report += f"""
## {tool_name.upper()} Assessment Summary

**Tool:** {tool_name.replace('_', ' ').title()}

### Overall Risk Distribution
"""

            for risk_level, data in summary.get('overall_risk_distribution', {}).items():
                report += f"- **{risk_level} Risk:** {data['count']} studies ({data['percentage']:.1f}%)\n"

            # Domain summaries if available
            if summary.get('domain_summaries'):
                report += "\n### Domain-Level Assessments\n"

                for domain_name, domain_data in summary['domain_summaries'].items():
                    question = domain_data.get('question', '')[:100] + "..." if len(domain_data.get('question', '')) > 100 else domain_data.get('question', '')
                    report += f"\n**{domain_name.replace('_', ' ').title()}:**\n"
                    report += f"*{question}*\n"

                    for risk_level, count in domain_data.get('risk_distribution', {}).items():
                        percentage = (count / summary['total_assessments']) * 100
                        report += f"- {risk_level}: {count} ({percentage:.1f}%)\n"

        return report


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automated Quality Assessment System")
    parser.add_argument("input_file", help="CSV file with study data to assess")
    parser.add_argument("--assessment-type", choices=['auto', 'robis', 'cochrane', 'grade'],
                       default='auto', help="Type of assessment to perform")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--report", help="Generate detailed quality report")

    args = parser.parse_args()

    assessor = AutomatedQualityAssessor()

    # Load data
    studies_data = pd.read_csv(args.input_file)

    # Perform assessment
    results = assessor.assess_study_quality(studies_data, args.assessment_type, args.output)

    if args.report:
        report = assessor.generate_quality_report(results)
        with open(args.report, 'w') as f:
            f.write(report)
        print(f"Quality report saved to: {args.report}")

    print("Quality assessment completed successfully!")
    print(f"Results: {args.output if args.output else 'generated in memory'}")
    print(f"Assessment type: {args.assessment_type}")
    print(f"Tools used: {', '.join(results['tools_used'])}")
