# PPG Heart Rate Accuracy Meta-Analysis: Project Initiation Notes

**Project Started:** September 23, 2025
**Status:** Project structure and templates created
**Focus:** Photoplethysmography-based heart rate monitoring device accuracy vs. ECG reference

---

## 📁 Project Structure Created

### Directory Layout
```
ppg_hr_accuracy_meta_analysis/
├── protocol.md                                    # Systematic review protocol
├── detailed_search_strategy.md                    # Database search strategies
├── data_extraction_form.md                        # Standardized data extraction template
├── preliminary_notes.md                           # This file
├── scripts/
│   └── data_extraction.py                         # Automated data extraction script
└── data/
    ├── literature_search_results/                 # Future database search exports
    ├── literature_screening/
    │   └── template_included_studies.csv          # Screening results template
    └── data_extraction/                           # Future extracted data files
```

---

## 🎯 Project Objectives

### Primary Research Question
What is the accuracy of photoplethysmography (PPG)-based heart rate monitoring devices compared to electrocardiography (ECG) as the reference standard?

### Specific Aims
1. **Comprehensively review** PPG HR accuracy literature (2010-2025)
2. **Meta-analyze** mean absolute error (MAE), root mean square error (RMSE), and correlation coefficients
3. **Identify factors** influencing PPG accuracy (device type, demographic variables, activity level)
4. **Provide guidance** for clinical and consumer PPG device usage

---

## 📋 Core Documents Created

### 1. Protocol (`protocol.md`)
- PROSPERO registration template
- Background and rationale
- Eligibility criteria (PPG devices vs ECG reference)
- Search strategy overview
- Data extraction and synthesis methods
- Timeline and deliverables outline

### 2. Search Strategy (`detailed_search_strategy.md`)
- Database-specific search strings (PubMed, EmBase, IEEE Xplore, Scopus)
- Concept identification and term expansion
- Inclusion/exclusion filters
- Quality control metrics
- Supplementary search methods

### 3. Data Extraction Form (`data_extraction_form.md`)
- Standardized form for PPG study data extraction
- Study characteristics, participant demographics, device specifications
- Accuracy outcomes (MAE, RMSE, Bland-Altman, correlation)
- Quality assessment (QUADAS-2 adapted)
- Comprehensive field set for meta-analysis

### 4. Data Extraction Script (`scripts/data_extraction.py`)
- Automated extraction framework using text pattern matching
- Quality assessment algorithms
- Summary statistics generation
- Ready for future literature data processing

### 5. Screening Templates (`data/literature_screening/`)
- Empty CSV template with PPG-specific screening fields
- Headers for study characteristics and screening decisions

---

## 🔬 Research Methodology Framework

### Study Eligibility
- **Index Test:** PPG-based HR monitoring (wrist, finger, smartphone)
- **Reference Standard:** ECG (any lead configuration)
- **Outcomes:** Quantitative accuracy metrics (MAE, RMSE, correlation, bias limits)
- **Study Designs:** Validation studies, comparative studies, diagnostic accuracy studies

### Data Extraction Fields
- Study metadata (authors, journal, year, country)
- Participant characteristics (age, sex, BMI, health status)
- Device specifications (manufacturer, type, wavelength, sampling rate)
- Experimental conditions (activity levels, environmental factors)
- Accuracy metrics (MAE by condition, Bland-Altman analysis, correlations)
- Quality assessment domains

### Statistical Analysis Plan
- **Meta-Analysis:** Random effects models for pooled accuracy estimates
- **Heterogeneity:** I² statistic and subgroup analyses
- **Subgroups:** Device type, activity level, demographic factors, PPG characteristics
- **Quality Assessment:** QUADAS-2 adapted for device accuracy studies

---

## 📊 Expected Deliverables (Future)

### Manuscripts
- Full systematic review manuscript
- Supplementary materials with complete datasets
- PRISMA flowchart and checklist

### Results
- Forest plots of accuracy outcomes
- Bland-Altman plot summaries
- Funnel plots for publication bias assessment
- Subgroup analysis visualizations

### Statistical Analysis
- Meta-analysis code (R/Python)
- Effect size calculations
- Heterogeneity and sensitivity analyses

---

## 📅 Next Steps Outline

### Phase 1: Literature Search (1-2 weeks)
- Execute PubMed, EmBase, IEEE Xplore, Scopus searches
- Grey literature review (manufacturer data, FCC clearance docs)
- International clinical trial registry searches

### Phase 2: Screening and Selection (2-3 weeks)
- Title/abstract screening by independent reviewers
- Full-text assessment with conflict resolution
- PRISMA flowchart documentation

### Phase 3: Data Extraction (3-4 weeks)
- Double-independent data extraction
- Risk of bias assessment
- Data synthesis preparation

### Phase 4: Meta-Analysis (4-6 weeks)
- Statistical analysis and modeling
- Subgroup and sensitivity analyses
- Table and figure generation

### Phase 5: Manuscript Development (4-5 weeks)
- Full manuscript writing
- Peer review preparation
- Journal submission

---

## 📈 Quality Assurance Standards

### Methodology Compliance
- PRISMA 2020 guidelines
- Cochrane Handbook methods
- GRADE framework for evidence quality
- PROSPERO prospective registration

### Transparency Measures
- Complete search syntax documentation
- Data extraction templates
- Statistical analysis code
- All decisions documented with rationale

### Validation Procedures
- Double-screening for eligibility
- Independent data extraction
- Risk of bias duplicate assessment
- Sensitivity analyses for robustness

---

## 💡 Project Notes and Considerations

### Methodological Considerations
- PPG technology evolution over time (2010-2025) may introduce heterogeneity
- ECG lead configuration variations (single lead vs 12-lead)
- Activity intensity measurement standardization challenges
- Motion artifact handling algorithms manufacturer-specific

### Potential Challenges
- ECG reference standard quality and timing synchronization
- PPG signal quality assessment and dropout rates
- Activity classification precision
- Publication bias toward positive accuracy results

### Strengths of Current Setup
- Comprehensive automated data extraction framework
- Detailed data extraction form covering all accuracy aspects
- Quality assessment adapted specifically for device validation
- Flexible statistical framework for continuous accuracy outcomes

---

## 📞 Contact and Documentation

This project is part of the systematic research automation framework. All templates and scripts are designed for reproducible, high-quality systematic reviews in the medical device accuracy domain.

**Status:** Ready for literature search execution
**Files Created:** 7 initial project files
**Automation Level:** High (automated extraction and quality assessment frameworks implemented)
