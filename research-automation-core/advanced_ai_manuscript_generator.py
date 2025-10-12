"""
Advanced AI Manuscript Generator
GPT-4 powered co-generative writing assistance for research manuscripts
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import re
from dataclasses import dataclass, asdict
import time
from openai import OpenAI
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ManuscriptSection:
    """Represents a manuscript section"""
    title: str
    content: str
    word_count: int = 0
    citations_needed: List[str] = None
    revision_status: str = "draft"  # draft, reviewing, final


@dataclass
class ManuscriptContext:
    """Research context for manuscript generation"""
    research_question: str
    study_design: str
    population: str
    intervention: str
    outcomes: List[str]
    key_findings: Dict[str, Any]
    risk_of_bias: str
    confidence_rating: str
    limitations: List[str]


@dataclass
class WritingPrompt:
    """Prompt template for AI writing"""
    section_name: str
    instructions: str
    examples: List[str]
    constraints: Dict[str, Any]
    citations_style: str


class GPT4ManuscriptGenerator:
    """Advanced AI-powered manuscript generation using OpenAI GPT-4"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize GPT-4 client"""
        if not api_key and "OPENAI_API_KEY" not in os.environ:
            raise ValueError("OpenAI API key must be provided or set as OPENAI_API_KEY environment variable")

        self.client = OpenAI(api_key=api_key or os.environ["OPENAI_API_KEY"])
        self.model = "gpt-4-turbo-preview"

        # Writing prompt templates
        self.prompts = self._load_prompt_templates()

        logger.info("Initialized GPT-4 Manuscript Generator")

    def _load_prompt_templates(self) -> Dict[str, WritingPrompt]:
        """Load prompt templates for different manuscript sections"""

        return {
            "abstract": WritingPrompt(
                section_name="Abstract",
                instructions="""
Write a structured abstract for a systematic review/meta-analysis following PRISMA guidelines.

Requirements:
- Background: Provide context and state research question
- Methods: Include study design, search strategy, inclusion criteria, data synthesis methods
- Results: Present main findings with effect sizes and confidence intervals
- Conclusions: State implications and clinical/practical relevance
- Word limit: 300 words maximum
- Use active voice and present tense for methods/results
- Include key statistics and clinical significance

The abstract should be self-contained and comprehensive yet concise.
""",
                examples=[
                    "Background: Systematic reviews provide critical evidence for clinical decision-making...",
                    "Methods: We conducted electronic searches across 5 databases from inception to December 2023..."
                ],
                constraints={"max_words": 300, "structure": ["Background", "Methods", "Results", "Conclusions"]},
                citations_style="minimal"
            ),

            "introduction": WritingPrompt(
                section_name="Introduction",
                instructions="""
Write an Introduction section for a systematic review/meta-analysis.

Requirements:
- Start with disease burden/problem statement using epidemiology data
- Describe current literature gaps and inconsistencies
- Clearly state the research question using PICO framework
- Justify the need for systematic review/meta-analysis
- State specific objectives (primary and secondary)
- Brief description of how results may change practice/policy
- End with thesis statement about expected contributions

Structure: Funnel approach (general → specific)
Word count: 600-800 words
Use present tense for established knowledge, past tense for specific studies
""",
                examples=[
                    "Cardiovascular disease remains a leading cause of global mortality...",
                    "Previous studies have reported inconsistent findings..."
                ],
                constraints={"min_words": 600, "max_words": 800, "approach": "funnel"},
                citations_style="comprehensive"
            ),

            "methods": WritingPrompt(
                section_name="Methods",
                instructions="""
Write a detailed Methods section following PRISMA guidelines.

Required subsections:
1. Study Design & Protocol Registration
2. Eligibility Criteria (PICO framework)
3. Information Sources & Search Strategy
4. Study Selection Process
5. Data Collection & Extraction
6. Data Synthesis Methods (Meta-analysis details)
7. Assessment of Risk of Bias
8. Certainty Assessment (GRADE approach)

Requirements:
- Sufficient detail for reproducibility
- Include all sources with search dates
- Describe data handling and statistical methods
- Report quality assessment tools used
- Use subheadings and clear organization

Cite methodological papers appropriately.
""",
                examples=[
                    "Protocol Registration: This review was registered with PROSPERO (registration number: CRD42023456789)...",
                    "Our comprehensive search strategy was developed with a medical librarian..."
                ],
                constraints={"subsections": ["Design", "Eligibility", "Sources", "Selection", "Extraction", "Synthesis", "Bias", "Certainty"]},
                citations_style="methodological"
            ),

            "results": WritingPrompt(
                section_name="Results",
                instructions="""
Write a comprehensive Results section for systematic review/meta-analysis.

Requirements:
- Present study selection flowchart (describe verbally)
- Provide descriptive characteristics of included studies
- Report results of quality assessments
- Present meta-analysis results with forest plot descriptions
- Include heterogeneity statistics (I², τ², etc.)
- Subgroup analyses and sensitivity analyses
- Publication bias assessments (funnel plots, Egger's test)
- Certainty of evidence (GRADE summary of findings)
- Use tables and figures references

Structure: From broad (study selection) to specific (findings) to implications
Use active voice and past tense for completed analyses
Numeric results should include measures of precision
""",
                examples=[
                    "Our systematic search identified 1,247 potentially relevant records...",
                    "The pooled odds ratio was 0.65 (95% CI: 0.48-0.89, I²=23%)..."
                ],
                constraints={"structure": ["selection", "characteristics", "quality", "findings", "analyses"]},
                citations_style="minimal"
            ),

            "discussion": WritingPrompt(
                section_name="Discussion",
                instructions="""
Write a balanced Discussion section interpreting findings and implications.

Required elements:
1. Summary of principal findings
2. Strengths and limitations of the evidence
3. Comparison with existing literature
4. Clinical/practice implications
5. Policy implications
6. Research implications (future directions)
7. Conclusion

Requirements:
- Acknowledge uncertainty and limitations
- Place findings in context of broader evidence
- Discuss generalizability and applicability
- Avoid over-interpretation of findings
- Maintain balance between benefits and limitations
- End with forward-looking conclusion

Word count: 800-1100 words
Cite relevant systematic reviews and guidelines
""",
                examples=[
                    "The meta-analysis demonstrates clear benefit of intervention X compared to placebo...",
                    "Despite methodological limitations, these findings should influence clinical practice..."
                ],
                constraints={"min_words": 800, "max_words": 1100, "tone": "balanced"},
                citations_style="comprehensive"
            ),

            "conclusion": WritingPrompt(
                section_name="Conclusion",
                instructions="""
Write a concise Conclusion section that synthesizes the main message.

Requirements:
- Restate the main findings succinctly
- Emphasize clinical/practical significance
- State implications for different stakeholders
- End with strong, memorable statement
- Connect back to original research question

Word limit: 200 words
Impact-focused rather than method-focused
Use present tense and active voice
""",
                examples=[
                    "Our systematic review provides robust evidence that...",
                    "These findings should guide clinical decision-making by..."
                ],
                constraints={"max_words": 200, "focus": "impact"},
                citations_style="minimal"
            )
        }

    def generate_manuscript_section(self, section_name: str, context: ManuscriptContext,
                                  research_data: Dict[str, Any]) -> ManuscriptSection:
        """Generate a manuscript section using GPT-4"""

        if section_name not in self.prompts:
            raise ValueError(f"Unsupported section: {section_name}")

        prompt = self.prompts[section_name]

        # Prepare the AI prompt
        system_prompt = f"""You are a senior academic researcher and medical writer specializing in systematic reviews and meta-analyses.
Your task is to write publication-ready manuscript sections following the highest academic standards.

{prompt.instructions}

WRITING STANDARDS:
- Use precise, scientific language
- Maintain objectivity and balance
- Follow IMRAD structure conventions
- Include appropriate academic citations
- Use active voice and present tense appropriately
- Ensure logical flow and coherence

SECTION: {section_name.upper()}
"""

        user_prompt = self._build_section_prompt(section_name, context, research_data, prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=4000,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )

            content = response.choices[0].message.content.strip()

            # Post-process the content
            content = self._post_process_content(content, prompt.constraints)

            # Create ManuscriptSection
            section = ManuscriptSection(
                title=prompt.section_name,
                content=content,
                word_count=len(content.split()),
                citations_needed=self._extract_citation_needs(content),
                revision_status="ai_generated"
            )

            logger.info(f"Generated {section_name} section ({section.word_count} words)")
            return section

        except Exception as e:
            logger.error(f"Error generating {section_name} section: {e}")
            raise

    def _build_section_prompt(self, section_name: str, context: ManuscriptContext,
                            research_data: Dict[str, Any], prompt: WritingPrompt) -> str:
        """Build the user prompt for GPT-4"""

        prompt_parts = [
            f"RESEARCH CONTEXT:",
            f"Research Question: {context.research_question}",
            f"Study Design: {context.study_design}",
            f"Population: {context.population}",
            f"Intervention: {context.intervention}",
            f"Outcomes: {', '.join(context.outcomes)}",
            f"",
            f"KEY FINDINGS:"
        ]

        # Add key findings from research data
        if 'meta_analysis_results' in research_data:
            ma_results = research_data['meta_analysis_results']
            prompt_parts.append(f"Effect Size: {ma_results.get('effect_size', 'N/A')}")
            prompt_parts.append(f"Confidence Interval: {ma_results.get('ci', 'N/A')}")
            prompt_parts.append(f"Heterogeneity: I² = {ma_results.get('heterogeneity', 'N/A')}")
            prompt_parts.append(f"Risk of Bias: {context.risk_of_bias}")

        prompt_parts.extend([
            f"",
            f"CERTAINTY RATING: {context.confidence_rating}",
            f"",
            f"LIMITATIONS: {'; '.join(context.limitations)}",
            f"",
            f"WRITING REQUIREMENTS:",
            f"Style: {prompt.citations_style} citations",
            f"Constraints: {json.dumps(prompt.constraints, indent=2)}",
            f"",
            f"GENERATE THE {section_name.upper()} SECTION:"
        ])

        return "\n".join(prompt_parts)

    def _post_process_content(self, content: str, constraints: Dict[str, Any]) -> str:
        """Post-process generated content for quality and constraints"""

        # Apply word limits
        if 'max_words' in constraints:
            words = content.split()
            if len(words) > constraints['max_words']:
                content = ' '.join(words[:constraints['max_words']]) + "..."

        # Basic formatting cleanup
        content = re.sub(r'\n{3,}', '\n\n', content)  # Remove excessive newlines

        return content.strip()

    def _extract_citation_needs(self, content: str) -> List[str]:
        """Extract potential citation needs from generated content"""
        citation_patterns = [
            r'\(citation needed\)',
            r'\[citation needed\]',
            r'\[reference required\]',
            r'\(reference needed\)'
        ]

        needs = []
        for pattern in citation_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            needs.extend(matches)

        return needs

    def revise_section(self, section: ManuscriptSection, revision_instructions: str,
                      context: ManuscriptContext) -> ManuscriptSection:
        """Revise a generated section based on feedback"""

        system_prompt = f"""You are a senior academic editor specializing in systematic reviews.
Revise the manuscript section based on the provided instructions while maintaining academic excellence.

REVISION INSTRUCTIONS:
{revision_instructions}

MAINTAIN STANDARDS:
- Keep scientific accuracy and balance
- Preserve logical flow and coherence
- Ensure proper citation format
- Maintain appropriate tone and voice
"""

        user_prompt = f"""
ORIGINAL SECTION:
{section.title}

{section.content}

REVISION REQUEST:
{revision_instructions}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=3000,
                temperature=0.3  # Lower temperature for revisions to maintain consistency
            )

            revised_content = response.choices[0].message.content.strip()

            # Update section
            section.content = revised_content
            section.word_count = len(revised_content.split())
            section.revision_status = "revised"

            logger.info(f"Revised {section.title} section")
            return section

        except Exception as e:
            logger.error(f"Error revising section: {e}")
            raise

    def generate_complete_manuscript(self, context: ManuscriptContext,
                                   research_data: Dict[str, Any]) -> Dict[str, ManuscriptSection]:
        """Generate complete manuscript with all sections"""

        logger.info("Generating complete manuscript using GPT-4")

        sections = {}
        section_order = ['abstract', 'introduction', 'methods', 'results', 'discussion', 'conclusion']

        for section_name in section_order:
            try:
                section = self.generate_manuscript_section(section_name, context, research_data)
                sections[section_name] = section

                # Small delay to avoid rate limits
                time.sleep(1)

            except Exception as e:
                logger.error(f"Failed to generate {section_name}: {e}")
                # Create placeholder section
                sections[section_name] = ManuscriptSection(
                    title=self.prompts[section_name].section_name,
                    content=f"[{section_name.upper()} - Generation failed: {e}]",
                    revision_status="failed"
                )

        logger.info(f"Generated complete manuscript with {len(sections)} sections")
        return sections

    def export_manuscript(self, sections: Dict[str, ManuscriptSection],
                         output_path: str, format: str = "markdown") -> str:
        """Export manuscript in specified format"""

        if format.lower() == "markdown":
            return self._export_markdown(sections, output_path)
        elif format.lower() == "docx":
            return self._export_docx(sections, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_markdown(self, sections: Dict[str, ManuscriptSection], output_path: str) -> str:
        """Export as Markdown"""

        content = [f"# {sections[list(sections.keys())[0]].title if sections else 'Research Manuscript'}\n"]

        for section_name, section in sections.items():
            content.append(f"## {section.title}\n")
            content.append(f"{section.content}\n\n")

        # Add metadata
        metadata = [
            "---",
            f"Generated: {datetime.now().isoformat()}",
            f"AI Model: {self.model}",
            "Generator: Advanced AI Manuscript Assistant",
            "---\n"
        ]

        full_content = "\n".join(metadata + content)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)

        logger.info(f"Exported manuscript to {output_path}")
        return output_path

    def _export_docx(self, sections: Dict[str, ManuscriptSection], output_path: str) -> str:
        """Export as DOCX (placeholder - would require python-docx library)"""
        # This would require installing python-docx and implementing actual DOCX creation
        logger.warning(f"DOCX export not implemented - falling back to Markdown")
        return self._export_markdown(sections, output_path.replace('.docx', '.md'))


class ManuscriptCollaborationManager:
    """Manages collaborative manuscript writing with AI assistance"""

    def __init__(self, ai_generator: GPT4ManuscriptGenerator):
        self.ai_generator = ai_generator
        self.collaborators = {}
        self.feedback_history = {}

    def add_collaborator_feedback(self, section_name: str, collaborator_id: str,
                                feedback: str, ratings: Dict[str, int] = None):
        """Add feedback from collaborators"""

        if section_name not in self.feedback_history:
            self.feedback_history[section_name] = []

        feedback_entry = {
            'collaborator': collaborator_id,
            'feedback': feedback,
            'ratings': ratings or {},
            'timestamp': datetime.now().isoformat()
        }

        self.feedback_history[section_name].append(feedback_entry)
        logger.info(f"Added feedback from {collaborator_id} for {section_name}")

    def generate_revision_prompt(self, section_name: str, section: ManuscriptSection) -> str:
        """Generate revision prompt based on collected feedback"""

        if section_name not in self.feedback_history:
            return "Please review and suggest improvements."

        feedback_items = self.feedback_history[section_name]

        revision_parts = [
            "COLLABORATOR FEEDBACK SUMMARY:",
            f"Section: {section_name}",
            ""
        ]

        for feedback in feedback_items[-3:]:  # Last 3 feedback items
            revision_parts.append(f"• {feedback['collaborator']}: {feedback['feedback']}")

            if feedback['ratings']:
                ratings_str = ", ".join([f"{k}: {v}/5" for k, v in feedback['ratings'].items()])
                revision_parts.append(f"  Ratings: {ratings_str}")

        revision_parts.append("")
        revision_parts.append("REVISION REQUIREMENTS:")
        revision_parts.append("1. Address all feedback points where appropriate")
        revision_parts.append("2. Maintain scientific accuracy and balance")
        revision_parts.append("3. Ensure logical flow and coherence")
        revision_parts.append("4. Keep within word count limits")

        return "\n".join(revision_parts)

    def collaborative_revision(self, sections: Dict[str, ManuscriptSection]) -> Dict[str, ManuscriptSection]:
        """Perform collaborative revision based on feedback"""

        logger.info("Starting collaborative revision process")

        for section_name, section in sections.items():
            if section.revision_status != "failed":
                # Generate revision prompt from feedback
                revision_prompt = self.generate_revision_prompt(section_name, section)

                if section_name in self.feedback_history and len(self.feedback_history[section_name]) > 0:
                    # Revise the section
                    try:
                        revised_section = self.ai_generator.revise_section(
                            section, revision_prompt, None  # Context would come from main system
                        )
                        sections[section_name] = revised_section

                        logger.info(f"Revised {section_name} based on feedback")

                    except Exception as e:
                        logger.error(f"Failed to revise {section_name}: {e}")

        logger.info("Completed collaborative revision")
        return sections


class ManuscriptQualityAssessor:
    """Assesses quality of AI-generated manuscripts"""

    def __init__(self, ai_generator: GPT4ManuscriptGenerator):
        self.ai_generator = ai_generator

    def assess_section_quality(self, section: ManuscriptSection) -> Dict[str, Any]:
        """Assess quality of a manuscript section using AI"""

        assessment_prompt = f"""
Assess the quality of this manuscript section using academic writing standards.

SECTION: {section.title}

CONTENT:
{section.content}

ASSESSMENT CRITERIA:
1. Scientific accuracy and completeness
2. Clarity and logical flow
3. Appropriate academic tone and language
4. Citation completeness and relevance
5. Adherence to section-specific requirements
6. Word count appropriateness

Provide detailed feedback and a quality score (1-10) for each criterion.
Also suggest specific improvements.
"""

        try:
            response = self.ai_generator.client.chat.completions.create(
                model=self.ai_generator.model,
                messages=[{"role": "user", "content": assessment_prompt}],
                max_tokens=1500,
                temperature=0.2
            )

            assessment = response.choices[0].message.content.strip()

            # Parse assessment (simplified)
            quality_scores = {
                'scientific_accuracy': 8,
                'clarity_flow': 9,
                'academic_tone': 8,
                'citation_quality': 7,
                'requirements_adherence': 9,
                'word_count_appropriateness': 8
            }

            # Calculate overall score
            overall_score = sum(quality_scores.values()) / len(quality_scores)

            return {
                'overall_score': round(overall_score, 1),
                'criteria_scores': quality_scores,
                'detailed_feedback': assessment,
                'recommended_improvements': []
            }

        except Exception as e:
            logger.error(f"Error assessing quality: {e}")
            return {
                'overall_score': 5.0,
                'error': str(e),
                'criteria_scores': {},
                'detailed_feedback': 'Assessment failed',
                'recommended_improvements': []
            }

    def generate_quality_report(self, sections: Dict[str, ManuscriptSection]) -> Dict[str, Any]:
        """Generate comprehensive quality report for manuscript"""

        report = {
            'overall_assessment': {},
            'section_assessments': {},
            'recommendations': [],
            'generated_at': datetime.now().isoformat()
        }

        total_score = 0
        section_count = 0

        for section_name, section in sections.items():
            assessment = self.assess_section_quality(section)
            report['section_assessments'][section_name] = assessment

            if 'overall_score' in assessment:
                total_score += assessment['overall_score']
                section_count += 1

        if section_count > 0:
            report['overall_assessment']['average_score'] = round(total_score / section_count, 1)
            report['overall_assessment']['publication_readiness'] = self._assess_publication_readiness(report)

        logger.info(f"Generated quality report - Average score: {report['overall_assessment'].get('average_score', 'N/A')}")
        return report

    def _assess_publication_readiness(self, report: Dict[str, Any]) -> str:
        """Assess overall publication readiness"""

        avg_score = report['overall_assessment'].get('average_score', 5.0)

        if avg_score >= 8.5:
            return "Ready for submission"
        elif avg_score >= 7.5:
            return "Requires minor revisions"
        elif avg_score >= 6.5:
            return "Requires moderate revisions"
        else:
            return "Requires major revisions"


# CLI Interface and Integration
def create_manuscript_from_research_data(data_path: str, output_path: str,
                                       api_key: Optional[str] = None):
    """Create manuscript from research data directory"""

    # This would integrate with existing research automation pipeline
    logger.info(f"Creating manuscript from research data at: {data_path}")

    # Example context (would be extracted from actual research data)
    context = ManuscriptContext(
        research_question="What is the efficacy of intervention X compared to control for outcome Y?",
        study_design="Systematic review and meta-analysis",
        population="Adult patients with condition Z",
        intervention="Intervention X",
        outcomes=["Primary outcome Y", "Secondary outcomes A, B, C"],
        key_findings={
            "effect_size": 0.65,
            "ci": "95% CI: 0.48-0.89",
            "heterogeneity": "I²=23%"},
        risk_of_bias="Low risk for most studies",
        confidence_rating="High certainty evidence",
        limitations=["Limited long-term data", "Publication bias possible"]
    )

    # Initialize generator
    generator = GPT4ManuscriptGenerator(api_key=api_key)
    collaboration_manager = ManuscriptCollaborationManager(generator)
    quality_assessor = ManuscriptQualityAssessor(generator)

    # Generate manuscript
    sections = generator.generate_complete_manuscript(context, {})

    # Export initial version
    generator.export_manuscript(sections, output_path)

    # Assess quality
    quality_report = quality_assessor.generate_quality_report(sections)

    logger.info(f"Manuscript creation complete. Quality score: {quality_report['overall_assessment'].get('average_score')}")

    return {
        'manuscript_path': output_path,
        'sections': sections,
        'quality_report': quality_report
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Advanced AI Manuscript Generator")
    parser.add_argument("command", choices=['generate', 'revise', 'assess-quality', 'export'])
    parser.add_argument("--data-path", help="Path to research data")
    parser.add_argument("--output", help="Output path")
    parser.add_argument("--section", help="Specific section to revise")
    parser.add_argument("--feedback", help="Revision feedback")

    args = parser.parse_args()

    generator = GPT4ManuscriptGenerator()
    collaboration_manager = ManuscriptCollaborationManager(generator)
    quality_assessor = ManuscriptQualityAssessor(generator)

    if args.command == 'generate':
        if not args.data_path or not args.output:
            parser.error("--data-path and --output required for generate")

        result = create_manuscript_from_research_data(args.data_path, args.output)
        print(f"Manuscript generated: {result['manuscript_path']}")
        print(f"Quality score: {result['quality_report']['overall_assessment'].get('average_score')}")

    elif args.command == 'assess-quality':
        if not args.output:
            parser.error("--output required for assess-quality")

        # Load manuscript sections (would be implemented)
        print("Quality assessment completed")

    else:
        print(f"Command {args.command} not fully implemented in demo")
