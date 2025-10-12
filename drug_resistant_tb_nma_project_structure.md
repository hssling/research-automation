# Drug-Resistant Tuberculosis NMA Project Structure

## Project Overview
**Title:** Network Meta-Analysis of BPaL/BPaLM vs Alternative Regimens for Drug-Resistant Tuberculosis

**PICO Framework:**
- **P:** Adults/adolescents with MDR/RR-TB (± FQ resistance)
- **I/C:** BPaL, BPaLM, short MDR, individualized long regimens
- **O:** Cure %, relapse %, SAEs (neuropathy, myelosuppression, QTc)

## Directory Structure
```
drug_resistant_tb_nma/
├── 00_protocol/
│   ├── study_protocol.md
│   ├── prospero_registration.md
│   ├── pico_framework.md
│   └── ethical_considerations.md
├── 01_literature_search/
│   ├── search_strategy.md
│   ├── literature_search_results.csv
│   ├── search_validation_report.md
│   └── prisma_flow_diagram.py
├── 02_data_extraction/
│   ├── data_extraction_form.md
│   ├── extracted_data.csv
│   ├── double_extraction_validation.py
│   └── extraction_quality_report.md
├── 03_statistical_analysis/
│   ├── nma_protocol.md
│   ├── bayesian_nma_model.R
│   ├── component_network_model.R
│   ├── statistical_analysis_plan.md
│   └── sensitivity_analyses.R
├── 04_results/
│   ├── league_tables.csv
│   ├── sucra_rankings.csv
│   ├── forest_plots.R
│   ├── rank_heat_plot.py
│   └── results_summary.md
├── 05_manuscript/
│   ├── manuscript_draft.md
│   ├── manuscript_final.md
│   ├── supplementary_materials.md
│   └── response_to_reviewers.md
├── 06_validation/
│   ├── validation_framework.md
│   ├── risk_of_bias_assessment.csv
│   ├── certainty_of_evidence.md
│   └── audit_report.md
└── 07_publication/
    ├── submission_checklist.md
    ├── journal_requirements.md
    ├── data_sharing_statement.md
    └── publication_package.zip
