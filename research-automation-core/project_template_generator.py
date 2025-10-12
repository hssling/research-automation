"""
Research Project Template Generator
Creates standardized project structures and configurations for different research types
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import subprocess
import sys

class ResearchProjectTemplate:
    """
    Template generator for standardized research project structures
    """

    def __init__(self, template_dir: str = "research-automation-core/templates"):
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(parents=True, exist_ok=True)

    def create_project(self, project_name: str, research_type: str,
                      output_dir: str = ".", **kwargs) -> str:
        """
        Create a new research project with standard structure

        Args:
            project_name: Name of the research project
            research_type: Type of research (systematic_review, meta_analysis, etc.)
            output_dir: Directory where project should be created
            **kwargs: Additional project-specific parameters

        Returns:
            Path to created project directory
        """
        project_dir = Path(output_dir) / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Get project structure based on research type
        structure = self._get_project_structure(research_type, project_name, **kwargs)

        # Create directory structure
        self._create_directories(project_dir, structure['directories'])

        # Create standard files
        self._create_files(project_dir, structure['files'])

        # Initialize git repository if requested
        if kwargs.get('init_git', True):
            self._init_git_repo(project_dir)

        print(f"Created research project: {project_name} ({research_type})")
        print(f"Location: {project_dir.absolute()}")

        return str(project_dir)

    def _get_project_structure(self, research_type: str, project_name: str, **kwargs) -> Dict[str, Any]:
        """Get the standard structure for a research project type"""

        structures = {
            "systematic_review": self._get_systematic_review_structure(project_name, **kwargs),
            "meta_analysis": self._get_meta_analysis_structure(project_name, **kwargs),
            "bibliometrics": self._get_bibliometrics_structure(project_name, **kwargs),
            "omics_single": self._get_omics_structure(project_name, **kwargs),
            "observational_study": self._get_observational_structure(project_name, **kwargs),
            "clinical_trial": self._get_clinical_trial_structure(project_name, **kwargs)
        }

        return structures.get(research_type, self._get_custom_structure(project_name, **kwargs))

    def _get_systematic_review_structure(self, project_name: str, **kwargs) -> Dict[str, Any]:
        """Structure for systematic reviews"""
        return {
            "directories": [
                "data/literature_search",
                "data/literature_screening",
                "data/data_extraction",
                "data/risk_of_bias",
                "scripts",
                "protocols",
                "results",
                "manuscript",
                "supplementary_materials"
            ],
            "files": {
                "data/literature_search/search_strategy.txt": self._get_search_strategy_template(),
                "data/literature_screening/inclusion_criteria.md": self._get_inclusion_criteria_template(),
                "data/literature_screening/exclusion_criteria.md": self._get_exclusion_criteria_template(),
                "data/data_extraction/forms/data_extraction_form.xlsx": self._get_data_extraction_form_template(),
                "protocols/prisma_protocol.md": self._get_prisma_protocol_template(project_name),
                "protocols/prospero_registration.md": self._get_prospero_registration_template(project_name),
                "scripts/pubmed_search.py": self._get_pubmed_search_script(),
                "scripts/screening.py": self._get_screening_script(),
                "scripts/data_extraction.py": self._get_data_extraction_script(),
                "manuscript/manuscript_draft.md": self._get_manuscript_template(project_name, "systematic_review"),
                "README.md": self._get_readme_template(project_name, "systematic_review"),
                "data/.gitkeep": "",
                "results/.gitkeep": ""
            }
        }

    def _get_meta_analysis_structure(self, project_name: str, **kwargs) -> Dict[str, Any]:
        """Structure for meta-analyses"""
        return {
            "directories": [
                "data/literature_search",
                "data/literature_screening",
                "data/data_extraction",
                "data/data_for_meta_analysis",
                "scripts",
                "protocols",
                "results/plots",
                "results/statistics",
                "manuscript",
                "supplementary_materials/validation_reports"
            ],
            "files": {
                "data/data_for_meta_analysis/data_analysis_template.csv": self._get_meta_analysis_data_template(),
                "protocols/cochrane_protocol.md": self._get_cochrane_protocol_template(project_name),
                "scripts/meta_analysis.R": self._get_meta_analysis_script(),
                "scripts/plot_generator.R": self._get_plot_generator_script(),
                "scripts/subgroup_analysis.R": self._get_subgroup_analysis_script(),
                "scripts/meta_regression.R": self._get_meta_regression_script(),
                "results/statistics/analysis_report.txt": "Meta-analysis statistical results will be saved here",
                "manuscript/manuscript_draft.md": self._get_manuscript_template(project_name, "meta_analysis"),
                "supplementary_materials/validation_reports/study_quality_assessment.md": self._get_quality_assessment_template(),
                "README.md": self._get_readme_template(project_name, "meta_analysis")
            }
        }

    def _get_bibliometrics_structure(self, project_name: str, **kwargs) -> Dict[str, Any]:
        """Structure for bibliometric analyses"""
        return {
            "directories": [
                "data/literature_database",
                "data/citation_networks",
                "data/author_networks",
                "scripts",
                "results/visualization",
                "results/statistics",
                "manuscript",
                "bibliographic_databases"
            ],
            "files": {
                "data/literature_database/comprehensive_bibliography.bib": self._get_bib_file_template(),
                "protocols/bibliometric_study_protocol.md": self._get_bibliometric_protocol_template(project_name),
                "scripts/bibliometric_analysis.R": self._get_bibliometric_analysis_script(),
                "scripts/citation_network_analysis.R": self._get_citation_network_script(),
                "scripts/coauthorship_analysis.R": self._get_coauthorship_analysis_script(),
                "results/statistics/bibliometric_indicators.csv": "Bibliometric indicators will be saved here",
                "manuscript/manuscript_draft.md": self._get_manuscript_template(project_name, "bibliometric_analysis"),
                "README.md": self._get_readme_template(project_name, "bibliometric_analysis")
            }
        }

    def _get_omics_structure(self, project_name: str, **kwargs) -> Dict[str, Any]:
        """Structure for single omics analyses"""
        return {
            "directories": [
                "data/raw_data",
                "data/processed_data",
                "data/differential_expression",
                "data/pathway_analysis",
                "scripts/preprocessing",
                "scripts/analysis",
                "results/qc_plots",
                "results/de_analysis",
                "results/pathway_results",
                "manuscript",
                "supplementary_materials"
            ],
            "files": {
                "data/raw_data/README_data.md": self._get_omics_data_readme(),
                "scripts/preprocessing/data_preprocessing.R": self._get_omics_preprocessing_script(),
                "scripts/analysis/de_analysis.R": self._get_de_analysis_script(),
                "scripts/analysis/pathway_enrichment.R": self._get_pathway_enrichment_script(),
                "scripts/analysis/gene_set_analysis.R": self._get_gsa_script(),
                "results/qc_plots/qc_report.html": "QC analysis reports will be generated here",
                "protocols/omics_study_protocol.md": self._get_omics_protocol_template(project_name),
                "manuscript/manuscript_draft.md": self._get_manuscript_template(project_name, "omics_analysis"),
                "README.md": self._get_readme_template(project_name, "omics_analysis")
            }
        }

    def _get_observational_structure(self, project_name: str, **kwargs) -> Dict[str, Any]:
        """Structure for observational studies"""
        return {
            "directories": [
                "data/raw_data",
                "data/processed_data",
                "data/statistical_analysis",
                "scripts",
                "results/tables",
                "results/figures",
                "manuscript",
                "supplementary_materials"
            ],
            "files": {
                "protocols/study_protocol.md": self._get_observational_protocol_template(project_name),
                "scripts/statistical_analysis.R": self._get_statistical_analysis_script(),
                "scripts/data_visualization.R": self._get_data_visualization_script(),
                "data/study_variables.xlsx": self._get_study_variables_template(),
                "manuscript/manuscript_draft.md": self._get_manuscript_template(project_name, "observational_study"),
                "README.md": self._get_readme_template(project_name, "observational_study")
            }
        }

    def _get_clinical_trial_structure(self, project_name: str, **kwargs) -> Dict[str, Any]:
        """Structure for clinical trials"""
        return {
            "directories": [
                "data/raw_trial_data",
                "data/processed_data",
                "data/adverse_events",
                "data/efficacy_analysis",
                "scripts",
                "results/efficacy",
                "results/safety",
                "results/statistical",
                "manuscript",
                "ct_materials"
            ],
            "files": {
                "protocols/clinical_trial_protocol.md": self._get_clinical_trial_protocol_template(project_name),
                "scripts/trial_analysis.R": self._get_trial_analysis_script(),
                "scripts/adverse_event_analysis.R": self._get_ae_analysis_script(),
                "data/crfs/case_report_forms.xslx": "CRF templates will be defined here",
                "ct_materials/consort_flowchart.md": self._get_consort_template(),
                "manuscript/manuscript_draft.md": self._get_manuscript_template(project_name, "clinical_trial"),
                "README.md": self._get_readme_template(project_name, "clinical_trial")
            }
        }

    def _get_custom_structure(self, project_name: str, **kwargs) -> Dict[str, Any]:
        """Default custom structure"""
        return {
            "directories": ["data", "scripts", "results", "manuscript"],
            "files": {
                "README.md": self._get_readme_template(project_name, "custom"),
                "scripts/analysis_template.py": self._get_custom_analysis_template(),
                "data/.gitkeep": "",
                "results/.gitkeep": ""
            }
        }

    def _create_directories(self, base_dir: Path, directories: List[str]):
        """Create directory structure"""
        for directory in directories:
            (base_dir / directory).mkdir(parents=True, exist_ok=True)

    def _create_files(self, base_dir: Path, files: Dict[str, str]):
        """Create files with content"""
        for file_path, content in files.items():
            full_path = base_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def _init_git_repo(self, project_dir: Path):
        """Initialize git repository with error handling for Windows permission issues"""
        try:
            # Check if git is available
            result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("Git not available, skipping git initialization")
                return

            # Remove any existing .git directory to avoid conflicts
            git_dir = project_dir / '.git'
            if git_dir.exists():
                import shutil
                try:
                    shutil.rmtree(git_dir)
                except Exception as e:
                    print(f"Warning: Could not remove existing .git directory: {e}")
                    return

            # Initialize git repository
            subprocess.run(['git', 'init'], cwd=project_dir, check=True, capture_output=True, timeout=30)
            subprocess.run(['git', 'add', '.'], cwd=project_dir, check=True, capture_output=True, timeout=60)
            subprocess.run(['git', 'commit', '-m', 'Initial project structure'], cwd=project_dir, check=True, capture_output=True, timeout=60)

        except subprocess.TimeoutExpired:
            print("Warning: Git operations timed out, skipping git initialization")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Git operation failed (likely permission issue): {e}")
        except Exception as e:
            print(f"Warning: Could not initialize git repository: {e}")

    # Template content methods
    def _get_search_strategy_template(self) -> str:
        return """# SEARCH STRATEGY
## PICOS Framework
- **Population:**
- **Intervention:**
- **Comparison:**
- **Outcome:**
- **Study Design:**

## Database Search Terms
- PubMed: [terms]
- Cochrane: [terms]
- Embase: [terms]
- Web of Science: [terms]

## Search Date: YYYY-MM-DD
## Search Update: YYYY-MM-DD"""

    def _get_inclusion_criteria_template(self) -> str:
        return """# INCLUSION CRITERIA
1. Study Design:
2. Population:
3. Intervention/Exposure:
4. Outcome Measures:
5. Language:
6. Publication Year:
7. Geographic Location:"""

    def _get_exclusion_criteria_template(self) -> str:
        return """# EXCLUSION CRITERIA
1. Study Design:
2. Population:
3. Intervention/Exposure:
4. Outcome Measures:
5. Language:
6. Publication Year:
7. Geographic Location:"""

    def _get_data_extraction_form_template(self) -> str:
        return """Study ID,Study Title,Authors,Year,Country,Study Design,Sample Size,Intervention/Exposure,Comparator,Outcome Measures,Results,Notes"""

    def _get_prisma_protocol_template(self, project_name: str) -> str:
        return f"""# PRISMA Protocol for {project_name}

## Review Title
{project_name}

## Review Registration
PROSPERO: [Registration ID]

## Review Type
Systematic Review and Meta-Analysis

## Authors
[List of authors]

## Background/Summary
[Background and rationale]

## Objectives
[Review objectives]

## Eligibility Criteria

### Inclusion Criteria
[List]

### Exclusion Criteria
[List]

## Information Sources
- PubMed/MEDLINE
- Cochrane CENTRAL
- Embase
- Web of Science
- ClinicalTrials.gov

## Search Strategy
[Detailed search strategies for each database]

## Selection Process
1. Title and abstract screening by [number] reviewers
2. Full-text review by [number] reviewers
3. Conflicts resolved by [method]

## Data Collection Process
[Data extraction process description]

## Data Items
[List of data items to be collected]

## Study Risk of Bias Assessment
[Risk of bias assessment methods]

## Effect Measures
[Outcome measures and effect size calculations]

## Synthesis Methods
[Data synthesis and analysis methods]

## Reporting Bias Assessment
[Methods for assessing reporting biases]

## Certainty Assessment
[GRADE approach or other certainty assessment methods]"""

    def _get_prospero_registration_template(self, project_name: str) -> str:
        return f"""# PROSPERO Registration for {project_name}

## Title: {project_name}

## Stage of Review: Planning

## Details

### Review question
[Specific review question]

### Searches
- Will include PubMed, Cochrane, Embase
- Search dates: [start] to [end]

### Types of study to be included
- Systematic reviews
- Randomized controlled trials
- Quasi-experimental studies
- Observational studies

### Condition or domain being studied
[Domain]

### Participants/population
[Population details]

### Intervention(s), exposure(s)
[Intervention details]

### Comparator(s)/control
[Comparator details]

### Outcome
[Outcome measures]

### Timeframe
[Timeframe for outcomes]

### PROSPERO registration number
[TBD]"""

    def _get_pubmed_search_script(self) -> str:
        return '''#!/usr/bin/env python3
"""
PubMed Literature Search Script
Automated search and download from PubMed database
"""

import requests
import pandas as pd
import time
from datetime import datetime
import os

def search_pubmed(query, max_results=1000):
    """Search PubMed and return results as DataFrame"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    # Search
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "usehistory": "y"
    }

    search_response = requests.get(f"{base_url}/esearch.fcgi", params=search_params)
    search_data = search_response.text

    # Parse IDs
    ids = []
    # [Parsing logic would go here]

    return ids

def main():
    # Search configuration
    search_queries = [
        # Define your search queries here
    ]

    for query in search_queries:
        print(f"Searching: {query}")
        ids = search_pubmed(query)

        # Save results
        df = pd.DataFrame({"pmid": ids})
        output_file = f"pubmed_search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved {len(ids)} results to {output_file}")

if __name__ == "__main__":
    main()'''

    def _get_screening_script(self) -> str:
        return '''#!/usr/bin/env python3
"""
Literature Screening Script
Automated and semi-automated screening of titles and abstracts
"""

import pandas as pd
import re
import os

class LiteratureScreener:
    def __init__(self):
        self.inclusion_keywords = []
        self.exclusion_keywords = []

    def screen_titles_abstracts(self, csv_file, include_column='title_abstract', output_file=None):
        """Screen studies based on title/abstract"""
        if output_file is None:
            output_file = csv_file.replace('.csv', '_screened.csv')

        df = pd.read_csv(csv_file)

        # Apply inclusion/exclusion criteria
        df['screening_decision'] = df[include_column].apply(self._classify_abstract)

        # Save screened results
        df.to_csv(output_file, index=False)
        print(f"Screened {len(df)} studies. Results saved to {output_file}")

        return df

    def _classify_abstract(self, text):
        """Classify abstract based on keywords"""
        text_lower = str(text).lower()

        # Check exclusion keywords
        for keyword in self.exclusion_keywords:
            if keyword.lower() in text_lower:
                return 'exclude'

        # Check inclusion keywords
        include_count = 0
        for keyword in self.inclusion_keywords:
            if keyword.lower() in text_lower:
                include_count += 1

        # Decision logic
        if include_count >= 2:  # Require at least 2 inclusion keywords
            return 'include'
        elif include_count == 1:
            return 'maybe'
        else:
            return 'exclude'

def main():
    screen = LiteratureScreener()

    # Configure keywords
    screen.inclusion_keywords = [
        # Add your inclusion keywords
    ]

    screen.exclusion_keywords = [
        # Add your exclusion keywords
    ]

    # Screen literature
    screen.screen_titles_abstracts('literature_search_results.csv')

if __name__ == "__main__":
    main()'''

    def _get_data_extraction_script(self) -> str:
        return '''#!/usr/bin/env python3
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
    main()'''

    def _get_manuscript_template(self, project_name: str, research_type: str) -> str:
        return f"""# {project_name}

## Abstract
[Abstract will be written here]

## Introduction
[Introduction section]

## Methods
[Methods section content]

## Results
[Results section content]

## Discussion
[Discussion section content]

## Conclusion
[Conclusion]

## References
[References will be inserted here]

---
*This manuscript was generated using automated research tools*
*Research Type: {research_type}*
*Generated on: {datetime.now().isoformat()}*"""

    def _get_readme_template(self, project_name: str, research_type: str) -> str:
        return f"""# {project_name}
{research_type.replace('_', ' ').title()} Research Project

## Project Overview
- **Research Type:** {research_type.replace('_', ' ').title()}
- **Created:** {datetime.now().isoformat()}
- **Authors:** [Add authors]

## Project Structure
```
{project_name}/
├── data/                    # Research data
├── scripts/                 # Analysis scripts
├── results/                 # Analysis results
├── manuscript/              # Manuscript drafts
├── protocols/               # Study protocols
└── supplementary_materials/ # Additional resources
```

## Setup Instructions
1. Install required dependencies: `pip install -r requirements.txt`
2. Place your data in the appropriate data/ subdirectories
3. Run analysis scripts in order specified in pipeline

## Pipeline Overview
1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]

## Key Scripts
- `scripts/[main_script].py` - Main analysis
- `scripts/[plot_script].R` - Visualization
- `scripts/[report_script].py` - Report generation

## Data Management
- Raw data: `data/raw/`
- Processed data: `data/processed/`
- Analysis results: `results/`

## Documentation
- Protocol: `protocols/`
- Methods: `methods/`
- Supplementary materials: `supplementary_materials/`

## Version Control
This project uses Git for version control. All analysis scripts and results should be committed regularly.

## Contact
[Contact information]

---
*Generated by Research Automation Framework*"""

    # Placeholder methods for missing templates (to be implemented)
    def _get_meta_analysis_script(self) -> str:
        return "# Meta-analysis script placeholder - implement statistical analysis\n"

    def _get_plot_generator_script(self) -> str:
        return "# Plot generator script placeholder - implement visualizations\n"

    def _get_subgroup_analysis_script(self) -> str:
        return "# Subgroup analysis script placeholder\n"

    def _get_meta_regression_script(self) -> str:
        return "# Meta-regression script placeholder\n"

    def _get_quality_assessment_template(self) -> str:
        return "# Study Quality Assessment Template\n"

    def _get_bib_file_template(self) -> str:
        return "% Bibliography file placeholder\n@article{example2023,\n\ttitle={Example}\n}\n"

    def _get_bibliometric_protocol_template(self, project_name: str) -> str:
        return f"# Bibliometric Protocol for {project_name}\n## Methods\n[Bibliometric analysis methods]\n"

    def _get_bibliometric_analysis_script(self) -> str:
        return "# Bibliometric analysis script placeholder\n"

    def _get_citation_network_script(self) -> str:
        return "# Citation network analysis script placeholder\n"

    def _get_coauthorship_analysis_script(self) -> str:
        return "# Coauthorship analysis script placeholder\n"

    def _get_omics_preprocessing_script(self) -> str:
        return "# OMICs preprocessing script placeholder\n"

    def _get_de_analysis_script(self) -> str:
        return "# Differential expression analysis script placeholder\n"

    def _get_pathway_enrichment_script(self) -> str:
        return "# Pathway enrichment analysis script placeholder\n"

    def _get_gsa_script(self) -> str:
        return "# Gene set analysis script placeholder\n"

    def _get_omics_protocol_template(self, project_name: str) -> str:
        return f"# OMICs Protocol for {project_name}\n## Methods\n[OMICs analysis methods]\n"

    def _get_observational_protocol_template(self, project_name: str) -> str:
        return f"# Observational Study Protocol for {project_name}\n## Methods\n[Study methods]\n"

    def _get_statistical_analysis_script(self) -> str:
        return "# Statistical analysis script placeholder\n"

    def _get_data_visualization_script(self) -> str:
        return "# Data visualization script placeholder\n"

    def _get_study_variables_template(self) -> str:
        return "Variable Name,Description,Type,Units\n"

    def _get_clinical_trial_protocol_template(self, project_name: str) -> str:
        return f"# Clinical Trial Protocol for {project_name}\n## Methods\n[Trial methods]\n"

    def _get_trial_analysis_script(self) -> str:
        return "# Trial analysis script placeholder\n"

    def _get_ae_analysis_script(self) -> str:
        return "# Adverse event analysis script placeholder\n"

    def _get_consort_template(self) -> str:
        return "# CONSORT Flowchart Template\n[Flowchart description]\n"

    def _get_custom_analysis_template(self) -> str:
        return "# Custom analysis script template\n# Add your analysis code here\n"

    # Additional template methods would go here for other script templates
    # (meta_analysis.R, bibliometric_analysis.R, etc.)

    def _get_meta_analysis_data_template(self) -> str:
        return """study_id,study_name,authors,year,country,study_design,sample_size,intervention_mean,intervention_sd,control_mean,control_sd,effect_size,standard_error,p_value"""

    def _get_cochrane_protocol_template(self, project_name: str) -> str:
        return f"""# Cochrane Protocol: {project_name}

## Title Registration
[Protocol title]

## Review question
[Specific review question]

## Background
[Background and rationale]

## Objectives
[Review objectives]

## Methods

### Criteria for considering studies for this review
#### Types of studies
- Randomized controlled trials
- Quasi-randomized controlled trials

#### Types of participants
[Participant criteria]

#### Types of interventions
[Intervention and comparator details]

#### Types of outcome measures
[Primary and secondary outcomes]

### Search methods for identification of studies
[Detailed search strategies]

### Data collection and analysis
[Data collection and analysis methods]

## Declarations of interest
[Conflict of interest statements]"""

    def _get_omics_data_readme(self) -> str:
        return """# OMICS DATA ORGANIZATION

## Raw Data Directory Structure
```
raw_data/
├── metadata/           # Sample metadata and experimental design
├── expression/         # Gene expression matrices
├── phenotype/          # Phenotype/clinical data
├── annotation/         # Gene annotations and pathways
└── qc_reports/         # Raw data quality control reports
```

## Data Formats
- Expression data: CSV format (.csv)
- Metadata: Excel format (.xlsx)
- Annotations: GMT format for gene sets
- QC reports: HTML format

## Naming Conventions
- Expression files: `[dataset]_[platform]_expression.csv`
- Metadata files: `[dataset]_metadata.xlsx`
- Sample naming: `[dataset]_[condition]_[replicate]`

## Quality Control
- Raw data QC should be performed before analysis
- Normalized data will be saved in processed_data/"""
