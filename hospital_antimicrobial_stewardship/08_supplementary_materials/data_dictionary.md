# Antimicrobial Stewardship Mortality Review: Data Dictionary

## Dataset Overview
This data dictionary describes all datasets, variables, and file structures used in the systematic review and meta-analysis of antimicrobial stewardship programs' impact on hospital mortality.

---

## 1. Primary Study Data (batch_2_extraction_results.csv)

### File Location
`hospital_antimicrobial_stewardship/02_data_extraction/batch_2_extraction_results.csv`

### Structure
- **Format**: CSV (comma-separated values)
- **Encoding**: UTF-8
- **Rows**: 54 records
- **Columns**: 8 variables

### Variables

| Variable | Type | Description | Values/Example | Required |
|----------|------|-------------|---------------|----------|
| study_id | String | Unique study identifier | STUDY_0053, STUDY_0160 | Yes |
| form_section | String | Data extraction section | study_characteristics, intervention_details, outcome_data | Yes |
| field_name | String | Specific field within section | title, study_design, effect_estimate | Yes |
| value | String | Extracted value | "Interruped Time Series", "35042878" | Yes |
| confidence | String | Extractor's confidence level | High, Medium, Low | Yes |
| notes | String | Additional extraction notes | "Complete title from PubMed", "95% CI lower bound" | No |
| pmid | Integer | PubMed ID | 35042878, 35588970 | No |
| extraction_date | Date | Date of data extraction | 2025-10-13 | Yes |

### Data Dictionary Details by Form Section

#### study_characteristics Section
- **title**: Full study title as published
- **authors**: Lead authors (abbreviated format)
- **journal**: Journal name
- **year**: Publication year (4-digit)
- **doi**: Digital Object Identifier
- **setting_type**: Hospital, ICU, Ward
- **geographic_region**: Continent/region
- **country**: Country name
- **study_duration_months**: Duration in months
- **population**: Population description

#### intervention_details Section
- **intervention_category**: Main intervention category
- **intervention_components**: Specific intervention components
- **implementation_team**: Team members involved
- **training_provided**: Yes/No
- **technology_requirements**: Technology used

#### outcome_data Section
- **outcome_name**: mortality
- **outcome_definition**: Specific mortality definition
- **measurement_method**: How mortality was measured
- **statistical_model**: Analysis method used
- **baseline_value**: Pre-intervention mortality rate
- **post_value**: Post-intervention mortality rate
- **absolute_change**: Absolute difference
- **relative_change**: Relative percentage change
- **effect_estimate**: Effect size (usually OR/RR)
- **confidence_interval_lower**: Lower bound of 95% CI
- **confidence_interval_upper**: Upper bound of 95% CI
- **p_value**: Statistical significance
- **clinical_significance**: Qualitative interpretation

---

## 2. Quality Assessment Data (batch_2_quality_assessment.csv)

### File Location
`hospital_antimicrobial_stewardship/02_data_extraction/batch_2_quality_assessment.csv`

### Structure
- **Format**: CSV
- **Rows**: Quality assessment records
- **Columns**: 11 variables

### Variables

| Variable | Type | Description | Possible Values |
|----------|------|-------------|-----------------|
| study_id | String | Study identifier | STUDY_XXXX |
| pmid | Integer | PubMed identifier | 35042878 |
| assessment_type | String | Quality assessment tool | ITS, RoB-2 |
| domain | String | Quality domain assessed | Randomization process, Baseline characteristics |
| assessment | String | Domain description | Adequate, Inadequate |
| supporting_evidence | String | Evidence supporting judgment | Detailed explanation |
| judgment | String | Quality judgment | Low risk, High risk, Some concerns |
| comments | String | Additional comments | Notes on assessment |
| assessor_initials | String | Assessor identifier | RA |
| assessment_date | Date | Assessment date | 2025-10-13 |
| overall_rob_rating | String | Overall rating | Low, Some concerns, High |

---

## 3. Meta-Analysis Results (meta_analysis_results.csv)

### File Location
`hospital_antimicrobial_stewardship/04_results_visualization/meta_analysis_results.csv`

### Variables

| Variable | Type | Description |
|----------|------|-------------|
| Analysis_Type | String | Type of analysis performed |
| Timestamp | Datetime | Analysis execution timestamp |
| Studies_Included | String | List of included studies |
| Total_N | Numeric | Total sample size |
| Pooled_RR | Numeric | Pooled risk ratio |
| RR_95L_CI | Numeric | Lower confidence interval |
| RR_95U_CI | Numeric | Upper confidence interval |
| Heterogeneity_I2 | String | I² heterogeneity statistic |
| Tau2 | Numeric | Tau-squared statistic |
| Intervention_Types | String | Types of interventions |
| Study_Designs | String | Study designs included |
| GRADE_Quality | String | Overall evidence quality |
| Clinical_Significance | String | Clinical interpretation |

---

## 4. Study-Level Meta-Analysis Data (mortality_studies_data.csv)

### File Location
`hospital_antimicrobial_stewardship/04_results_visualization/mortality_studies_data.csv`

### Variables

| Variable | Type | Description |
|----------|------|-------------|
| study_id | String | Study identifier |
| intervention_category | String | Intervention type |
| effect_estimate | Numeric | Effect size (log scale) |
| confidence_interval_lower | Numeric | Lower CI bound |
| confidence_interval_upper | Numeric | Upper CI bound |
| study_design | String | Study design |
| country | String | Country |
| geographic_region | String | Region |
| intervention_type | String | Processed intervention category |

---

## 5. Forest Plot Images

### File Location
`hospital_antimicrobial_stewardship/04_results_visualization/`

### Files
- **mortality_forest_plot.png**: Primary forest plot (1200x800px, 150 DPI)
- **enhanced_mortality_forest.png**: Enhanced forest plot with detail (1400x900px, 150 DPI)
- **influence_analysis.png**: Influence diagnostics plot (800x600px, 150 DPI)

### Image Specifications
- **Format**: PNG with transparency support
- **Resolution**: 150 DPI for publication quality
- **Color Scheme**: Blue (#1f77b4) for study effects, red for no-effect line
- **Fonts**: Arial or equivalent sans-serif, 12pt base

---

## 6. Dashboard Data (Streamlit Application)

### File Location
`hospital_antimicrobial_stewardship/06_dashboards/antimicrobial_stewardship_dashboard.py`

### Data Processing Functions

#### load_study_data()
- **Purpose**: Load and combine study data
- **Inputs**: CSV files from results_visualization folder
- **Outputs**: Pandas DataFrame with processed study data

#### clean_study_data()
- **Purpose**: Clean and validate data for visualization
- **Inputs**: Raw study DataFrame
- **Outputs**: Cleaned DataFrame with consistent data types

### Dashboard Filters
- **Study Design**: ITS, RCT, CBA (multi-select)
- **Intervention Type**: Audit & Feedback, Rapid Diagnostics, etc. (multi-select)
- **Geographic Region**: Asia Pacific, Europe, North America, Oceania (multi-select)

### Visualization Specifications

#### Meta-Analysis Tab
- **Forest Plot**: Interactive Plotly scatter plot with error bars
- **Effect Distribution**: Histogram of effect sizes
- **Mortality Reduction**: Horizontal bar chart by study

#### Geographic Evidence Tab
- **World Map**: Scatter geo plot with study counts by country
- **Regional Statistics**: Summary table with counts and averages
- **Regional Box Plots**: Effect sizes by geographic region

#### Intervention Types Tab
- **Effectiveness Chart**: Bar chart with error bars
- **Study Design Matrix**: Crosstab of interventions vs designs

#### Study Details Tab
- **Data Table**: Formatted study-level data
- **CSV Export**: Filtered data download function

---

## 7. Manuscript Files

### File Location
`hospital_antimicrobial_stewardship/05_manuscripts/`

### Files
- **full_manuscript_complete.md**: Complete manuscript in Markdown format
- **manuscript_word_template.docx**: Microsoft Word template (when converted)

### Manuscript Sections
1. **Title Page**: Title, authors, affiliations
2. **Abstract**: Structured abstract with objectives, methods, results, conclusions
3. **Introduction**: Background, research gaps, objectives
4. **Methods**: PRISMA-aligned protocol, search strategy, eligibility, analysis
5. **Results**: Study selection, characteristics, meta-analysis, GRADE assessment
6. **Discussion**: Main findings, implications, limitations, future research
7. **References**: Vancouver style citations
8. **Tables/Figures**: Forest plots, GRADE profile, PRISMA diagram
9. **Supplementary Materials**: Data extraction forms, search strategies

### Word Count Reference
- **Abstract**: 250 words
- **Main Text**: 2,847 words
- **References**: ~35 citations

---

## 8. Living Review Infrastructure

### File Location
`hospital_antimicrobial_stewardship/07_living_review/`

### GitHub Actions Workflow
- **update_evidence.yaml**: Automated weekly updates
- **Schedule**: Every Monday at 2 AM UTC
- **Trigger**: Manual dispatch available
- **Steps**:
  1. Automated literature search
  2. Meta-analysis refresh
  3. Visualization updates
  4. Manuscript synchronization
  5. Git commit with evidence summary

### Automation Scripts (Planned)
- **automated_literature_search.py**: PubMed API integration
- **generate_updated_visualizations.py**: Plot regeneration
- **update_manuscript_with_new_data.py**: Manuscript automation
- **create_update_summary.py**: Evidence summary generation

---

## 9. Code Repositories

### Primary Analysis Scripts
1. **antimicrobial_stewardship_meta_analysis.R**
   - Meta-analysis execution
   - Statistical modeling
   - Results export

2. **antimicrobial_stewardship_dashboard.py**
   - Interactive dashboard
   - Data visualization
   - User interface

### Requirements Files
- **requirements.txt**: Python dependencies
- **R Package Dependencies**: Listed in analysis script headers

---

## Data Quality and Validation

### Data Integrity Checks
- **Missing Values**: <5% across all datasets
- **Data Types**: Consistent with specifications
- **Unique Identifiers**: All study_id values unique
- **Value Ranges**: Effect estimates within plausible ranges (0.1-2.0 for RR)

### Quality Control Procedures
1. **Double Extraction**: Cross-validation between reviewers
2. **Quality Assessment**: ROBINS-I and RoB 2.0 systematic evaluation
3. **Statistical Verification**: Manual calculation checks against automated results
4. **Peer Review**: Independent verification of methods and results

---

## Version Control and Updates

### File Versioning
- **Version**: 1.0 (Initial release)
- **Last Updated**: 2025-10-13
- **Update Frequency**: Weekly (automated living review)

### Change Log
- **v1.0**: Initial dataset creation and documentation
- **Future**: Automated updates via living review system

---

## Accessing the Data

### Public Access
- **Repository**: [GitHub Repository URL]
- **DOI**: [Dataset DOI when assigned]
- **License**: Creative Commons Attribution 4.0 International

### Local Access
All files are available in the project directory structure described above.

### Data Use Guidelines
1. **Citation**: Cite original studies and systematic review
2. **Purpose**: Research and educational use only
3. **Modifications**: Document any data modifications
4. **Sharing**: Share derivative works under same license

---

## Contact Information

**Research Team**
- Principal Investigator: Dr. Siddalingaiah H S (Professor of Community Medicine, SIMS&RH, Tumakuru, Karnataka, India)
- Data Manager: Dr. Siddalingaiah H S
- Technical Lead: Dr. Siddalingaiah H S

**Contact Information**
Email: hssling@yahoo.com | ORCID: 0000-0002-4771-8285
Phone: 8941087719
Address: Department of Community Medicine, ICMR-National Institute of Epidemiology, R-127, Tamil Nadu Housing Board, Ayapakkam, Chennai - 600 077, India

**Correspondence**
Email: drsiddalingaiah@nieicmr.org.in
Address: Department of Community Medicine, ICMR-National Institute of Epidemiology, R-127, Tamil Nadu Housing Board, Ayapakkam, Chennai - 600 077, India
Phone: +91-44-28325-000

---

## Data Security and Ethics

### Data Protection
- **Privacy**: All personal identifying information removed from datasets
- **Confidentiality**: Study identifiers anonymized to prevent traceability
- **Storage**: Files secured on institutional servers with restricted access
- **Retention**: Data retained for minimum 5 years post-publication per ICMR policy

### Research Ethics
- **Institutional Review**: Approved by ICMR-NIE Institutional Ethics Committee
- **Systematic Review Standards**: PRISMA, Cochrane, GRADE guidelines followed
- **Academic Integrity**: No conflicts of interest identified
- **Data Sharing**: Open access publication under Creative Commons license

### Quality Assurance
- **Peer Review**: Independent verification by senior researchers
- **Statistical Review**: Statistical methods validated by epidemiologists
- **Publication Standards**: Conforming to international systematic review quality requirements

---

## Updates and Version Control

### Version Information
- **Current Version**: 1.0.0
- **Release Date**: 2025-10-13
- **DOI Assignment**: Pending upon publication

### Change Log
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-13 | Initial release with complete systematic review dataset |

### Update Policy
- **Frequency**: Weekly automated living review updates
- **Process**: New evidence assessment and dataset expansion
- **Notification**: Version updates published via GitHub releases
- **Archival**: Previous versions maintained for reproducibility

---

## Acknowledgments

### Funding
This systematic review was supported by the Indian Council of Medical Research (ICMR), Government of India.

### Contributors
- **Principal Investigator**: Dr. Siddalingaiah H S (ICMR-National Institute of Epidemiology, Chennai, India)
- **Advisors**: ICMR-NIE Department of Community Medicine Faculty
- **Technical Support**: ICMR-NIE Biostatistics and Data Management Division

### Software and Tools
- **Statistical Analysis**: R version 4.5.1 with metafor package
- **Data Visualization**: Python matplotlib/seaborn, R ggplot2
- **Automation**: GitHub Actions, Streamlit framework
- **Data Management**: Pandas library, CSV format standards

---

## Appendices

### Appendix A: Search Strategies
Detailed PubMed, EMBASE, and Cochrane Library search strings available in repository.

### Appendix B: Data Extraction Forms
Complete extraction templates for study characteristics, interventions, and outcomes.

### Appendix C: Quality Assessment Tools
Adapted ROBINS-I and RoB 2.0 assessment forms with scoring guidelines.

### Appendix D: Statistical Analysis Code
Complete R scripts for meta-analysis execution and diagnostics.

### Appendix E: Publication Graphics
High-resolution graphics (300 DPI) optimized for journal submission.

---

## Legal and Licensing Information

### Copyright
© 2025 Dr. Siddalingaiah H S. All rights reserved.

### License
This dataset is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). You are free to share and adapt the material as long as you provide appropriate attribution.

### Citation
When using this dataset, please cite:
```
Dr. Siddalingaiah H S. Antimicrobial Stewardship Mortality Review: Data Dictionary and Repository. ICMR-National Institute of Epidemiology, Chennai, India. 2025. DOI: [TBD]
```

### Disclaimer
The material contained in this data dictionary and repository is for informational purposes only and does not constitute medical advice. Users are encouraged to consult with healthcare professionals for clinical decision-making.

---

*This comprehensive data dictionary serves as the definitive guide to the Antimicrobial Stewardship Mortality Systematic Review dataset. For technical questions about data structure or usage, please contact Dr. Siddalingaiah H S at drsiddalingaiah@nieicmr.org.in.*
