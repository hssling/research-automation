# Hospital Antimicrobial Stewardship Data Extraction Deployment Guide

## Overview
**Project Phase:** Phase 3 - Systematic Data Extraction
**System Status:** MULTIPLE BATCHES READY FOR CONCURRENT DEPLOYMENT
**Deployment Date:** October 13, 2025

## 📋 Active Batches for Immediate Deployment

### Batch 1: Medium Priority Studies (8 Studies)
**Status:** Active Deployment
**Priority Level:** Medium
**Estimated Effort:** 416 minutes total (45-60 min per study)
**Deadline:** October 27, 2025
**Study Characteristics:**
- RCT/cluster-RCT designs
- Hospital setting interventions
- Antimicrobial stewardship programs
- Primary outcomes: mortality, resistance, antibiotic consumption

**PMIDs Assigned:**
- STUDY_0096: 25011604 (Antibiotic rotation strategies)
- STUDY_0281: 39732716 (Swab Testing to Optimize Pneumonia treatment)
- STUDY_0314: 32272171 (Enhanced antimicrobial stewardship - bacteraemia)
- STUDY_0405: 29514268 (Primary care antimicrobial stewardship outreach)
- STUDY_0784: 34460904 (Antibiotic Stewardship Rounds in ICU)
- STUDY_0881: 23743088 (Long-term survival with TREAT system)
- STUDY_1198: 28159671 (Antibiotic checklist for IV antibiotics)
- STUDY_1317: 40032084 (Smartphone application for antibiotic prescribing)

### Batch 2: High-Impact Mortality Studies (2 Studies)
**Status:** Ready for Deployment
**Priority Level:** Low-High Impact (Mortality + Complex Interventions)
**Estimated Effort:** 100 minutes total (45-60 min per study)
**Deadline:** October 27, 2025
**Study Characteristics:**
- Both studies include mortality outcomes
- Complex interventions: stewardship + hematological/rapid testing
- High clinical significance for network meta-analysis

**PMIDs Assigned:**
- STUDY_0053: 35042878 (Stewardship program impact on mortality and resistance)
- STUDY_0160: 35588970 (Rapid antibiotic susceptibility testing effectiveness)

## 🎯 Extraction Priorities

### Batch 1 Priorities:
1. mortality
2. cdi (Clostridium difficile)
3. mdro (multidrug-resistant organisms)
4. antibiotic_consumption

### Batch 2 Priorities:
1. mortality (high priority for both studies)
2. cdi (Clostridium difficile)
3. mdro (multidrug-resistant organisms)
4. antibiotic_consumption
5. length_stay

## 📁 Deployment Package Files

### Required Files per Batch:
- `batch_{n}_studies_{timestamp}.csv` - Study list with PMIDs and priorities
- `batch_extraction_package_{timestamp}.json` - Complete structured extraction forms
- `batch_{n}_extraction_instructions_{timestamp}.txt` - Step-by-step workflow guide

### Quality Control Package:
- Double extraction: 20% of studies minimum (≥2 studies per batch)
- Discrepancy resolution: Third reviewer arbitration
- Agreement threshold: 100% on intervention classification and effect estimates

## 👥 Recommended Reviewer Assignments

### Scenario A: Dedicated Reviewers (Optimal)
```
Batch 1 (8 studies):
- Reviewer A: STUDIES 0096, 0281, 0314 (Medical ICU/rotation focus)
- Reviewer B: STUDIES 0405, 0784, 0881 (Outreach and digital systems)
- Reviewer C: STUDIES 1198, 1317 (Checklists and mobile apps)
- Double extraction: 2 randomly selected studies

Batch 2 (2 studies):
- Reviewer D: Both studies (mortality-focused hematological interventions)
- Double extraction: 1 study minimum (both possible for quality assurance)
```

### Scenario B: Limited Reviewers (2 reviewers)
```
Batch 1 (8 studies):
- Reviewer A: STUDIES 0096, 0281, 0314, 0405 (Medical/infectious disease focus)
- Reviewer B: STUDIES 0784, 0881, 1198, 1317 (ICU/intervention focus)

Batch 2 (2 studies):
- Both reviewers: Double extract both studies for maximum quality
```

### Scenario C: Sequential Processing
```
Week 1-2: Complete Batch 2 (2 high-impact studies)
Week 3-4: Complete Batch 1 (8 medium-priority studies with mortality focus first)
```

## 📊 Quality Control Workflow

### Double Extraction Protocol:
1. **Random Selection:** 20% of studies per batch selected for double extraction
2. **Independent Extraction:** Two reviewers extract independently
3. **Comparison Phase:** Third reviewer compares extractions
4. **Resolution:** Consensus agreement or senior reviewer adjudication
5. **Documentation:** All discrepancies logged with resolution rationale

### Agreement Thresholds:
- **Intervention classification:** 100% agreement required
- **Outcome definitions:** 100% agreement required
- **Effect estimates:** Within 10% agreement
- **Confidence intervals:** Within 5% agreement

## ⚙️ Technical Setup Requirements

### Software Prerequisites:
- Python 3.8+ with pandas, numpy libraries
- Excel/CSV editor for form completion
- PDF reader for full-text articles
- File storage system for extraction backups

### Directory Structure:
```
02_data_extraction/
├── batch_1_studies_*.csv
├── batch_2_studies_*.csv
├── batch_extraction_package_*.json (contains forms)
├── extracted_data/
│   ├── batch_1/
│   └── batch_2/
└── quality_control/
    ├── batch_1_double_extraction.csv
    └── batch_2_double_extraction.csv
```

## 📅 Timeline and Milestones

### Week 1 (October 14-20):
- **Day 1-2:** Obtain all full-text articles (10 PMIDs total)
- **Day 3-5:** Batch 2 completion (2 studies, 1.7 hours extraction)
- **Day 6-7:** Begin Batch 1 high-priority studies (mortality focus)

### Week 2 (October 21-27):
- **Continue Batch 1:** Complete remaining studies
- **Quality Control:** Double extraction validation
- **Verification:** Cross-check all extractions
- **Deadline:** October 27

### Phase 3 Completion Criteria:
- ✅ All assigned studies extracted
- ✅ Double extraction completed (20% minimum)
- ✅ Quality control measures implemented
- ✅ Data validation checks passed
- ✅ Ready for Phase 4 statistical analysis

## 🚨 Contingency Plans

### Article Access Issues:
1. Use institutional library access
2. Request through interlibrary loan
3. Contact corresponding authors
4. Document in extraction notes

### Reviewer Availability:
1. Redistribute studies among available reviewers
2. Extend deadlines proportionally
3. Prioritize high-impact studies
4. Document resource constraints

### Technical Issues:
1. Use backup data entry forms
2. Manual documentation with standardized templates
3. Immediate contact with technical support
4. Daily data backup procedures

## 📈 Success Metrics

### Completion Targets:
- Batch 2: 100% complete by October 18
- Double extraction: ≥20% studies validated
- Data completeness: ≥95% required fields
- Quality agreement: ≥90% inter-rater reliability

### Monitoring Dashboard:
- Daily progress updates
- Completion percentage tracking
- Quality control metrics
- Issue resolution timelines

## 🎯 Next Phase Preparation

### After Phase 3 Completion:
- **Phase 4:** Statistical Analysis (Network Meta-Analysis)
- **Phase 5:** Results Visualization (Forest plots, league tables)
- **Phase 6:** Manuscript Production
- **Phase 7:** Final Quality Control and Validation

### Technical Handover:
- Dataset cleaning and validation
- R/Python statistical analysis setup
- Publication-ready figures generation
- Manuscript outline and structure

---

## 📞 Contact Information

**Project Coordinator:** [Team Lead Name]
- Extraction workflows and study assignments

**Data Manager:** [Technical Support Name]
- Form technical issues and data validation

**Senior Reviewer:** [Principal Investigator]
- Quality control decisions and escalations

---

*Deployment Guide Generated: October 13, 2025*
*System Status: OPERATIONAL - Ready for concurrent batch execution*
