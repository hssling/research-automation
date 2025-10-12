"""
AI-Assisted Manuscript Generation System
Automated scientific writing and manuscript formatting using AI and templates
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import json
from datetime import datetime
import re
import textwrap
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManuscriptSection:
    """Represents a section of a scientific manuscript"""

    def __init__(self, name: str, title: str, content_type: str = 'narrative',
                 required: bool = True, word_limit: Optional[int] = None):
        self.name = name
        self.title = title
        self.content_type = content_type  # 'narrative', 'methods', 'results', 'references'
        self.required = required
        self.word_limit = word_limit
        self.content = ""
        self.metadata = {}

    def generate_content(self, data_sources: Dict[str, Any], template_patterns: Dict[str, str]) -> str:
        """Generate content for this section using AI and templates"""
        # This would integrate with AI models for content generation
        # For now, we'll use template-based generation

        pattern = template_patterns.get(self.name, "")

        # Fill in template variables
        content = self._fill_template(pattern, data_sources)

        # Apply word limit if specified
        if self.word_limit and len(content.split()) > self.word_limit:
            content = self._truncate_content(content, self.word_limit)

        self.content = content
        return content

    def _fill_template(self, template: str, data: Dict[str, Any]) -> str:
        """Fill template variables with actual data"""

        # Simple variable substitution
        filled_content = template

        # Replace common placeholders
        replacements = {
            '{{DATE}}': datetime.now().strftime('%B %Y'),
            '{{YEAR}}': datetime.now().strftime('%Y'),
            '{{TOTAL_STUDIES}}': str(data.get('total_studies', 0)),
            '{{STUDY_TYPE}}': str(data.get('study_type', 'studies')),
            '{{OUTCOME_MEASURE}}': str(data.get('outcome_measure', '')),
            '{{INTERVENTION}}': str(data.get('intervention', '')),
            '{{CONTROL}}': str(data.get('control', '')),
        }

        # Add meta-analysis results
        if 'meta_results' in data:
            meta = data['meta_results']
            primary = meta.get('primary_results', {})
            replacements.update({
                '{{EFFECT_SIZE}}': ".3f" if 'overall_effect' in primary else '',
                '{{CI_LOWER}}': ".3f" if 'ci_lower' in primary else '',
                '{{CI_UPPER}}': ".3f" if 'ci_upper' in primary else '',
                '{{P_VALUE}}': ".3f" if 'p_value' in primary else '',
                '{{I2}}': ".1f" if 'I2' in primary.get('heterogeneity_test', {}) else '',
            })

        for placeholder, value in replacements.items():
            filled_content = filled_content.replace(placeholder, value)

        return filled_content

    def _truncate_content(self, content: str, word_limit: int) -> str:
        """Truncate content to word limit while preserving sentence structure"""
        words = content.split()
        if len(words) <= word_limit:
            return content

        truncated = ' '.join(words[:word_limit])

        # Try to end at sentence boundary
        last_sentence_end = max(
            truncated.rfind('.'), truncated.rfind('!'), truncated.rfind('?')
        )

        if last_sentence_end > word_limit * 0.7:  # If we're not truncating too much
            truncated = truncated[:last_sentence_end + 1]

        return truncated + "..."


class ManuscriptTemplate:
    """Template for different types of scientific manuscripts"""

    def __init__(self, template_name: str, journal_style: str = 'general'):
        self.template_name = template_name
        self.journal_style = journal_style
        self.sections = {}
        self.templates = {}

    def add_section(self, section: ManuscriptSection):
        """Add a section to the template"""
        self.sections[section.name] = section

    def set_section_template(self, section_name: str, template: str):
        """Set template pattern for a section"""
        self.templates[section_name] = template

    def generate_manuscript(self, data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete manuscript from data sources"""

        manuscript = {
            'title': self._generate_title(data_sources),
            'abstract': self._generate_abstract(data_sources),
            'sections': {},
            'references': [],
            'metadata': {
                'generated_date': datetime.now().isoformat(),
                'template': self.template_name,
                'journal_style': self.journal_style
            }
        }

        # Generate each section
        for section_name, section in self.sections.items():
            template = self.templates.get(section_name, "")
            content = section.generate_content(data_sources, {section_name: template})
            manuscript['sections'][section.name] = {
                'title': section.title,
                'content': content,
                'word_count': len(content.split()),
                'required': section.required
            }

        # Generate references if data available
        if 'study_data' in data_sources:
            manuscript['references'] = self._generate_references(data_sources['study_data'])

        return manuscript

    def _generate_title(self, data_sources: Dict[str, Any]) -> str:
        """Generate manuscript title"""
        intervention = data_sources.get('intervention', '')
        outcome = data_sources.get('outcome_measure', '')
        study_type = data_sources.get('study_type', 'systematic review')

        title = f"The Effect of {intervention} on {outcome}: A {study_type.title()}"

        # Add meta-analysis indicator if applicable
        if 'meta_results' in data_sources:
            title += " and Meta-Analysis"

        return title

    def _generate_abstract(self, data_sources: Dict[str, Any]) -> str:
        """Generate structured abstract"""

        abstract_parts = []

        # Background
        background = f"Background: This study examines the effect of {data_sources.get('intervention', 'intervention')} on {data_sources.get('outcome_measure', 'outcome measure')}."
        abstract_parts.append(background)

        # Methods
        methods = f"Methods: {data_sources.get('methods_summary', 'A systematic review was conducted')}."
        abstract_parts.append(methods)

        # Results
        if 'meta_results' in data_sources:
            meta = data_sources['meta_results']
            primary = meta.get('primary_results', {})

            effect_size = primary.get('overall_effect', 0)
            p_value = primary.get('p_value', 1)

            if p_value < 0.05:
                result_text = ".3f"
            else:
                result_text = "no significant effect"

            results = f"Results: {result_text} was found (p = {p_value:.3f})."
        else:
            results = f"Results: {data_sources.get('results_summary', 'Results are presented')}. "

        abstract_parts.append(results)

        # Conclusion
        if 'conclusion' in data_sources:
            conclusion = f"Conclusion: {data_sources['conclusion']}"
        else:
            conclusion = "Conclusion: Further research is warranted."

        abstract_parts.append(conclusion)

        return " ".join(abstract_parts)

    def _generate_references(self, study_data: List[Dict[str, Any]]) -> List[str]:
        """Generate formatted references"""

        references = []

        for study in study_data:
            # Basic reference formatting
            authors = study.get('authors', 'Unknown')
            year = study.get('publication_year', 'Unknown')
            title = study.get('title', 'Unknown Title')
            journal = study.get('journal', 'Unknown Journal')

            # Create basic APA-style reference
            reference = f"{authors} ({year}). {title}. {journal}."

            references.append(reference)

        return references

    def export_to_markdown(self, manuscript: Dict[str, Any]) -> str:
        """Export manuscript to Markdown format"""

        md_content = []

        # Title
        md_content.append(f"# {manuscript['title']}\n")

        # Abstract
        md_content.append("## Abstract\n")
        md_content.append(f"{manuscript['abstract']}\n")

        # Keywords (if available)
        keywords = manuscript.get('keywords', [])
        if keywords:
            md_content.append("**Keywords:** " + ', '.join(keywords) + "\n")

        # Sections
        for section_name, section_data in manuscript['sections'].items():
            md_content.append(f"## {section_data['title']}\n")
            md_content.append(f"{section_data['content']}\n")

            # Add word count in comment
            word_count = section_data.get('word_count', 0)
            if section_data.get('word_limit'):
                md_content.append(f"<!-- Word count: {word_count}/{section_data['word_limit']} -->\n")

        # References
        if manuscript.get('references'):
            md_content.append("## References\n")
            for i, ref in enumerate(manuscript['references'], 1):
                md_content.append(f"{i}. {ref}\n")
            md_content.append("")

        # Metadata
        md_content.append("---")
        md_content.append("<!-- Manuscript Metadata -->")
        for key, value in manuscript.get('metadata', {}).items():
            md_content.append(f"<!-- {key}: {value} -->")
        md_content.append("-->")

        return '\n'.join(md_content)


class AIManuscriptAssistant:
    """AI-powered manuscript writing assistant"""

    def __init__(self):
        self.templates = {}
        self.load_default_templates()

    def load_default_templates(self):
        """Load default manuscript templates for different types"""

        # Systematic Review Template
        sr_template = ManuscriptTemplate("systematic_review", "general")

        # Add sections with templates
        sections_data = [
            ("introduction", "Introduction", """
The importance of {{OUTCOME_MEASURE}} in {{STUDY_TYPE}} has been increasingly recognized.
This systematic review aims to synthesize evidence regarding the effect of {{INTERVENTION}}
compared to {{CONTROL}} on {{OUTCOME_MEASURE}}.

Systematic reviews provide comprehensive evidence for clinical decision-making
and policy development. Previous studies have shown mixed results regarding
the efficacy of {{INTERVENTION}} for {{OUTCOME_MEASURE}}.

The objective of this review is to critically appraise and synthesize
available evidence on the effect of {{INTERVENTION}} on {{OUTCOME_MEASURE}}.
            """, 500),

            ("methods", "Methods", """
This systematic review was conducted according to the Preferred Reporting Items
for Systematic reviews and Meta-Analyses (PRISMA) guidelines.

We searched multiple electronic databases including PubMed, Cochrane Library,
and Web of Science from inception to {{DATE}}. Search terms included keywords
related to {{INTERVENTION}}, {{OUTCOME_MEASURE}}, and {{STUDY_TYPE}}.

Two reviewers independently screened titles and abstracts, followed by full-text
review. Data extraction was performed using standardized forms. Risk of bias
was assessed using the Cochrane Risk of Bias tool for randomized trials.
            """, 800),

            ("results", "Results", """
The systematic search identified {{TOTAL_STUDIES}} studies that met inclusion criteria.

Study characteristics are summarized in Table 1. The studies included
participants from various settings and used different methodological approaches.

The primary outcome measure was {{OUTCOME_MEASURE}}. Results showed that
{{INTERVENTION}} {{RESULT_INTERPRETATION}} compared to {{CONTROL}}.

Forest plot analysis revealed {{HETEROGENEITY_LEVEL}} heterogeneity (I² = {{I2}}%).
Publication bias was assessed using funnel plots and showed {{BIAS_ASSESSMENT}}.

Subgroup analyses by study design and participant characteristics showed
consistent findings across most subgroups.
            """, 800),

            ("discussion", "Discussion", """
This systematic review provides comprehensive evidence on the effect of {{INTERVENTION}}
on {{OUTCOME_MEASURE}}. Our findings demonstrate that {{INTERVENTION}}
{{RESULT_IMPLICATIONS}}.

The strengths of this review include the comprehensive search strategy,
rigorous methodology, and assessment of risk of bias. However, limitations
include {{STUDY_LIMITATIONS}}.

Our results are consistent with previous research showing {{CONTEXT_FINDINGS}}.
The clinical implications suggest that {{INTERVENTION}} should be {{CLINICAL_RECOMMENDATIONS}}.

Further research is needed to address {{FUTURE_RESEARCH_NEEDS}}.
            """, 800),

            ("conclusion", "Conclusion", """
In conclusion, this systematic review demonstrates that {{INTERVENTION}}
has {{OVERALL_FINDINGS}} on {{OUTCOME_MEASURE}}. These findings should inform
clinical practice and future research in this area.
            """, 250)
        ]

        for section_data in sections_data:
            section = ManuscriptSection(section_data[0], section_data[1],
                                     word_limit=section_data[3])
            sr_template.add_section(section)
            sr_template.set_section_template(section_data[0], section_data[2])

        self.templates['systematic_review'] = sr_template

        # Meta-Analysis Template
        ma_template = ManuscriptTemplate("meta_analysis", "general")

        # Add meta-analysis specific sections
        ma_sections = [
            ("introduction", "Introduction", sections_data[0][2], 500),  # Same as SR
            ("methods", "Methods", sections_data[1][2] + """

For meta-analysis, we used random-effects models due to expected heterogeneity.
Effect sizes were calculated as standardized mean differences. Heterogeneity
was assessed using I² statistic and Cochran's Q test. Publication bias was
evaluated using funnel plots and Egger's test.
            """, 1000),

            ("results", "Results", """
Of {{TOTAL_STUDIES}} included studies, {{META_STUDIES}} were included in meta-analysis
with a total of {{TOTAL_SAMPLE_SIZE}} participants.

The pooled effect size was {{EFFECT_SIZE}} (95% CI: {{CI_LOWER}}, {{CI_UPPER}}; p = {{P_VALUE}}).
This represents a {{EFFECT_MAGNITUDE}} effect size.

Heterogeneity was {{HETEROGENEITY_LEVEL}} (I² = {{I2}}%, p {{HET_P_VALUE}}).
Subgroup analyses showed {{SUBGROUP_FINDINGS}}.

Publication bias assessment indicated {{BIAS_RESULTS}}.
Sensitivity analyses confirmed the robustness of findings.
            """, 1000),

            ("discussion", "Discussion", sections_data[3][2], 800),
            ("conclusion", "Conclusion", sections_data[4][2], 250)
        ]

        for section_data in ma_sections:
            section = ManuscriptSection(section_data[0], section_data[1],
                                     word_limit=section_data[3])
            ma_template.add_section(section)
            ma_template.set_section_template(section_data[0], section_data[2])

        self.templates['meta_analysis'] = ma_template

    def generate_manuscript(self, template_type: str,
                          data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete manuscript using specified template"""

        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")

        template = self.templates[template_type]

        # Enhance data sources with AI-generated content
        enhanced_data = self._enhance_content(data_sources)

        manuscript = template.generate_manuscript(enhanced_data)

        # Add quality checks and suggestions
        manuscript['quality_checks'] = self._perform_quality_checks(manuscript)
        manuscript['writing_suggestions'] = self._generate_writing_suggestions(manuscript)

        return manuscript

    def _enhance_content(self, data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI/content analysis to enhance manuscript data"""

        enhanced = data_sources.copy()

        # Add interpretations based on results
        if 'meta_results' in enhanced:
            meta = enhanced['meta_results']
            primary = meta.get('primary_results', {})

            effect_size = primary.get('overall_effect', 0)
            p_value = primary.get('p_value', 1)

            if p_value < 0.05:
                if abs(effect_size) < 0.2:
                    enhanced['effect_magnitude'] = 'small but significant'
                    enhanced['clinical_significance'] = 'may not be clinically meaningful'
                elif abs(effect_size) < 0.5:
                    enhanced['effect_magnitude'] = 'moderate'
                    enhanced['clinical_significance'] = 'likely clinically meaningful'
                else:
                    enhanced['effect_magnitude'] = 'large'
                    enhanced['clinical_significance'] = 'substantial clinical impact'

                enhanced['result_interpretation'] = f"significantly improved {data_sources.get('outcome_measure', 'outcomes')}"
                enhanced['overall_findings'] = f"a {enhanced['effect_magnitude']} beneficial effect"
            else:
                enhanced['result_interpretation'] = f"did not significantly affect {data_sources.get('outcome_measure', 'outcomes')}"
                enhanced['overall_findings'] = "no significant effect"

        return enhanced

    def _perform_quality_checks(self, manuscript: Dict[str, Any]) -> Dict[str, Any]:
        """Perform quality checks on generated manuscript"""

        checks = {}

        # Word count checks
        for section_name, section_data in manuscript.get('sections', {}).items():
            word_count = section_data.get('word_count', 0)
            word_limit = section_data.get('word_limit')

            if word_limit:
                if word_count > word_limit * 1.1:  # 10% over limit
                    checks[f"{section_name}_length"] = "warning"
                elif word_count < word_limit * 0.8:  # 20% under limit
                    checks[f"{section_name}_length"] = "too_short"
                else:
                    checks[f"{section_name}_length"] = "good"

        # Content checks
        content_warnings = []

        # Check for missing key elements
        abstract = manuscript.get('abstract', '')
        if len(abstract.split()) < 150:
            content_warnings.append("Abstract may be too short")

        # Check section completeness
        for section_name, section_data in manuscript.get('sections', {}).items():
            content = section_data.get('content', '')
            if len(content.strip()) < 50:
                content_warnings.append(f"Section '{section_data.get('title', section_name)}' appears incomplete")

        checks['content_warnings'] = content_warnings

        return checks

    def _generate_writing_suggestions(self, manuscript: Dict[str, Any]) -> List[str]:
        """Generate writing improvement suggestions"""

        suggestions = []

        # Analyze readability
        for section_name, section_data in manuscript.get('sections', {}).items():
            content = section_data.get('content', '')

            # Simple checks
            if content.count('The') > content.count('the') * 2:
                suggestions.append(f"Consider reducing passive voice in {section_data.get('title', section_name)}")

            # Check for common errors
            if 'data are' in content.lower():
                suggestions.append("Review subject-verb agreement (data is/are)")

        # General suggestions
        suggestions.extend([
            "Consider adding implications for clinical practice",
            "Include limitations clearly and specifically",
            "Ensure all abbreviations are defined on first use",
            "Consider adding a statement about funding and conflicts of interest"
        ])

        return suggestions

    def export_manuscript(self, manuscript: Dict[str, Any],
                         format_type: str = 'markdown',
                         output_file: str = None) -> str:
        """Export manuscript in various formats"""

        if format_type == 'markdown':
            content = self.templates.get(manuscript.get('metadata', {}).get('template'), ManuscriptTemplate('default')).export_to_markdown(manuscript)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Manuscript exported to {output_file}")

        return content


        # CLI Interface and utilities
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Manuscript Generation System")
    parser.add_argument("data_file", help="JSON file with study data and results")
    parser.add_argument("--template", choices=['systematic_review', 'meta_analysis'],
                       default='systematic_review', help="Manuscript template type")
    parser.add_argument("--output", help="Output file for manuscript")
    parser.add_argument("--format", choices=['markdown'], default='markdown', help="Output format")

    args = parser.parse_args()

    # Load data
    with open(args.data_file, 'r') as f:
        data_sources = json.load(f)

    # Generate manuscript
    assistant = AIManuscriptAssistant()
    manuscript = assistant.generate_manuscript(args.template, data_sources)

    # Export
    content = assistant.export_manuscript(manuscript, args.format, args.output)

    if not args.output:
        print("Generated Manuscript:")
        print("=" * 50)
        print(content[:1000] + "..." if len(content) > 1000 else content)

    print("\nManuscript generation completed!")
    print(f"Template used: {args.template}")
    print(f"Output file: {args.output if args.output else 'printed to console'}")

    # Show quality checks
    checks = manuscript.get('quality_checks', {})
    warnings = checks.get('content_warnings', [])
    if warnings:
        print(f"\n⚠️  Content warnings ({len(warnings)}):")
        for warning in warnings[:3]:  # Show first 3
            print(f"  - {warning}")

    # Show suggestions
    suggestions = manuscript.get('writing_suggestions', [])
    if suggestions:
        print(f"\n💡 Writing suggestions ({len(suggestions)}):")
        for suggestion in suggestions[:3]:  # Show first 3
            print(f"  - {suggestion}")
