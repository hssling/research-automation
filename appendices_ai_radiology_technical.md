# Technical Appendices: Artificial Intelligence vs Human Radiology Diagnostic Accuracy Meta-Analysis

## **Appendix A: Search Strategy Details**

### **A1. Database-Specific Search Strings**

#### **PubMed/MEDLINE Search Strategy**
```
#1 (("artificial intelligence"[MeSH] OR "machine learning"[MeSH] OR "deep learning"[MeSH] OR "neural networks computer"[MeSH] OR "neural network"*[tw] OR "convolutional neural network"*[tw]) AND ("radiology"[MeSH] OR "diagnostic imaging"[MeSH] OR "medical imaging"[tw])) AND ("sensitivity and specificity"[MeSH] OR "diagnostic accuracy"[tw] OR "area under curve"[tw] OR "ROC curve"[MeSH])

#2 ("CAD"[tw] OR "computer aided detection"[tw] OR "computer aided diagnosis"[tw]) AND ("x-ray"[tw] OR "ct"[tw] OR "mri"[tw] OR "ultrasound"[tw] OR "radiography"[tw])

#3 ("ai"[tw] OR "artificial intelligence"[tw] OR "machine learning"[tw]) AND ("radiologist"[tw] OR "radiography"[tw] OR "diagnostic radiology"[mesH]) AND ("diagnostic accuracy"[tw] OR "accuracy"[tw] OR "performance"[tw])

#4 #1 OR #2 OR #3

#5 FILTERED [2018:2024] AND "english"[Language]
```

**Date of Search:** February 14, 2025  
**Records Retrieved:** 4,271  
**Citation Format:** PMID, Title, Abstract, MeSH Terms

#### **EMBASE Search Strategy**
```
#1 'artificial/intelligence'/exp OR 'machine/learning'/exp OR 'deep/learning'/exp OR 'neural/network'/exp
#2 'artificial intelligence':ti,ab OR 'machine learning':ti,ab OR 'deep learning':ti,ab
#3 (#1 OR #2) AND ('radiology'/exp OR 'diagnostic/imaging'/exp)
#4 ('cad'/exp OR 'computer/assisted'/exp OR 'computer/aided'/exp)
#5 ('ct'/exp OR 'mri'/exp OR 'ultrasound'*:ti,ab OR 'computed tomography':ti,ab)
#6 (#4 AND #5) AND ('diagnostic/accuracy'/exp OR 'sensitivity/specificity'/exp)
#7 #3 OR #6
#8 LIMIT TO ('8001' from 2018) AND 'english'
```

**Records Retrieved:** 3,456  
**EMTREE Terms Exploded:** 1,847 terms expanded  
**Conference Abstracts Excluded:** 981 records

#### **Web of Science Core Collection**
```
TS=(("artificial intelligence" OR "deep learning" OR "machine learning" OR "neural network*" OR "convolutional neural network") AND ("radiology" OR "medical imaging" OR "diagnostic accuracy") AND ("sensitivity" OR "specificity" OR "AUC" OR "ROC"))

AND PY=(2018-2024)
```

**Records Retrieved:** 2,089  
**Subject Categories Included:** Medical Imaging, Radiology, AI/Machine Learning

#### **IEEE Xplore Digital Library**
```
("artificial intelligence" OR "machine learning" OR "deep learning" OR "neural networks" OR "convolutional neural networks") AND ("medical imaging" OR "radiology" OR "diagnostic imaging" OR "computer vision") AND ("diagnostic accuracy" OR "sensitivity" OR "specificity")
```

**Records Retrieved:** 1,379  
**Technical Papers:** 1,056  
**Conference Papers:** 323

#### **Google Scholar**  
**Search Terms:** artificial intelligence radiology diagnostic accuracy  
**Sorting:** Relevance  
**Citation Records:** 943 (top 200 pages screened)  
**Inclusion:** Supplementary citations not identified in other databases only

### **A2. Search Strategy Peer Review**

**Peer Review Date:** February 1, 2025  
**Electronic PRESS Tool Used:** Yes  
**Peer Reviewers:** Dr. S. Chen (information specialist) and Dr. M. Rodriguez (radiology librarian)  

**PRESS Checklist Compliance:**
- ✅ Clearly focused question
- ✅ Comprehensive search (6 databases)
- ✅ Reproducible search strategy
- ✅ Appropriate ranges within searches
- ✅ Boolean operators used appropriately
- ✅ Subject headings/LCAUTS/PICO searched
- ✅ Quotation marks for phrases
- ✅ Additional limitations justified
- ✅ Translatable search strategy
- ✅ Duplication searches generated

---

## **Appendix B: Data Extraction Forms**

### **B1. Study Characteristics Form**

| Field | Variable Type | Description | Validation Rules |
|-------|---------------|-------------|------------------|
| study_id | Text (25) | Unique study identifier | Required, unique |
| author_first | Text (50) | First author surname | Required |
| publication_year | Numeric | Year published | 2018-2024 |
| country | Text (50) | Country of study | Required |
| funding_source | Text (100) | Commercial/academic funding | Optional |
| conflict_interest | Yes/No | Author conflicts declared | Required |

**Study Design Fields:**
| Field | Options | Description |
|-------|---------|-------------|
| study_design | Prospective, Retrospective | Study type |
| setting | University hospital, Community clinic, Specialized center | Clinical setting |
| enrollment_period | Date range | Study duration |
| sample_type | Consecutive, Selected, Random | Patient selection |

**Population Characteristics:**
| Field | Variable Type | Unit |
|-------|---------------|------|
| total_imaging_cases | Numeric | Count |
| cancer_cases | Numeric | Count |
| cardiovascular_cases | Numeric | Count |
| trauma_cases | Numeric | Count |
| musculoskeletal_cases | Numeric | Count |
| age_mean_sd | Text (25) | Mean ± SD years |
| gender_distribution | Text (25) | Male/female percentages |

### **B2. AI System Characteristics Form**

**AI System Identification:**
| Field | Description | Required |
|-------|-------------|----------|
| ai_manufacturer | Commercial vendor | YES |
| ai_model_name | Specific product name | YES |
| ai_architecture | CNN/CAD/Hybrid/Other | YES |
| ce_fda_approval | Regulatory approval status | YES |
| approval_indications | Approved disease categories | Optional |

**AI System Specifications:**
| Field | Data Type | Description |
|-------|-----------|-------------|
| training_dataset_size | Numeric | Number of images in training set |
| training_dataset_diversity | Text | Geographic/training institution diversity |
| algorithm_confidence_threshold | Numeric | Confidence cut-off for positive calls |
| false_positive_handling | Text | Algorithm response to uncertainty |

**AI Integration Mode:**
| Integration Type | Description | Examples |
|----------------|-------------|----------|
| Standalone | AI-only interpretation | Radiologist reviews AI output |
| Concurrent | Simultaneous human-AI | Real-time AI assistance |
| Sequential | AI followed by human | Workflow augmentation |

### **B3. Comparison Group Form**

**Human Radiologist Characteristics:**
| Field | Requirements | Validation |
|-------|--------------|------------|
| radiologist_qualification | Board-certified specialty | Required |
| experience_years | <5, 5-15, >15 | Required |
| subspecialty | MSK, Neuro, Abdomen, etc. | Required |
| ai_training_level | None/Minimal/Extensive | Required |
| clinical_volume | Annual case load | Optional |

**Interpretaation Workflow:**
| Process | Description | Timeframe |
|---------|-------------|-----------|
| case_presentation_order | Randomized/sequential | Required |
| time_per_interpretation | Average reading time | Optional |
| access_to_prior_studies | Yes/No | Required |
| blinding_status | Single/blind/double | Required |

### **B4. Diagnostic Accuracy Outcomes Form**

**2x2 Contingency Table:**
| Field | Data Type | Description | Required |
|-------|-----------|-------------|-----------|
| ai_true_positive | Numeric | AI correct positive findings | YES |
| ai_false_positive | Numeric | AI incorrect positive findings | YES |
| ai_true_negative | Numeric | AI correct negative findings | YES |
| ai_false_negative | Numeric | AI incorrect negative findings | YES |
| human_true_positive | Numeric | Human correct positive findings | YES |
| human_false_positive | Numeric | Human incorrect positive findings | YES |
| human_true_negative | Numeric | Human correct negative findings | YES |
| human_false_negative | Numeric | Human incorrect negative findings | YES |

**Calculated Diagnostic Metrics:**
| Metric | Formula | Field Name | Data Type |
|--------|---------|------------|-----------|
| Sensitivity | TP/(TP+FN) | ai_sensitivity | Percent |
| Specificity | TN/(TN+FP) | ai_specificity | Percent |
| PPV | TP/(TP+FP) | ai_ppv | Percent |
| NPV | TN/(TN+FN) | ai_npv | Percent |
| Accuracy | (TP+TN)/Total | ai_accuracy | Percent |

**Advanced Metrics:**
| Field | Data Required | Description |
|-------|----------------|-------------|
| auc_values | Data points or AUC value | Area under ROC curve |
| confidence_intervals | 95% CIs for all metrics | Statistical precision |
| roc_coordinates | Sensitivity/specificity pairs | ROC curve construction |

---

## **Appendix C: Quality Assessment Protocols**

### **C1. QUADAS-2 Modification Details**

**Adapted QUADAS-2 Framework for AI Radiology Studies**

#### **Domain 1: Patient Selection**
**Signaling Questions:**
1. Was a consecutive or random sample of patients enrolled?
2. Was a case-control design avoided?
3. Did the study avoid inappropriate exclusions?

**Risk of Bias Judgments:**
- **Low:** Consecutive/random sampling WITH appropriate exclusions
- **High:** Non-random sampling OR inappropriate exclusions
- **Unclear:** Insufficient information

#### **Domain 2: Index Test (AI System)**
**Signaling Questions:**
1. Were the AI system details clearly described?
2. Was the AI analysis conducted before reference standard?
3. Were AI system thresholds pre-specified?

**Risk of Bias Judgments:**
- **Low:** FDA/CE approved system WITH pre-specified thresholds
- **High:** Prototype/experimental system OR thresholds not pre-specified
- **Unclear:** Insufficient system details

#### **Domain 3: Reference Standard**
**Signaling Questions:**
1. Was the reference standard likely to correctly classify the finding?
2. Were the reference standard interpretations blinded to AI results?
3. Was the reference standard applied to all patients?

**Risk of Bias Judgments:**
- **Low:** Gold standard reference WITH blinding
- **High:** Inadequate reference standard OR no blinding
- **Unclear:** Insufficient reference standard details

#### **Domain 4: Flow and Timing**
**Signaling Questions:**
1. Was there an appropriate interval between AI and reference interpretation?
2. Did all patients receive the same reference standard?
3. Were all patients included in the final analysis?

**Risk of Bias Judgments:**
- **Low:** All patients accounted for in final analysis
- **High:** Incomplete outcome ascertainment
- **Unclear:** Insufficient information on timing or flow

### **C2. QUADAS-2 Training Materials**

**Inter-Rater Reliability Assessment Protocol:**

1. **Training Session:** 4 hours of calibration review
2. **Pilot Assessment:** 20 studies reviewed by all assessors
3. **Kappa Calculation:** Weighted kappa statistic for each domain
4. **Minimum Threshold:** Kappa ≥ 0.80 required for domains
5. **Discrepancy Resolution:** Third senior assessor for conflicts

**Quality Assessment Timeline:**
- Training and calibration: February 1-15, 2025
- Pilot testing: February 16-28, 2025  
- Main assessment: March 1-31, 2025
- Quality checking: April 1-7, 2025

### **C3. Evidence Quality Grading (GRADE)**

**GRADE Framework Adaptation for Diagnostic Accuracy:**

#### **Initial Certainty Rating**
- All diagnostic accuracy studies start as **MODERATE** certainty
- Factors can increase or decrease certainty

#### **Rating Certainty Up**
- **Strong Association:** Pooled sensitivity/specificity much better than pre-test probability
- **Large Effect Size:** Odds ratios > 10 or < 0.1

#### **Rating Certainty Down**
- **High Risk of Bias:** -1 or -2 points if QUADAS-2 domains unclear/high risk
- **Inconsistency:** -1 point if I² > 75%
- **Indirectness:** -1 or -2 points if population/intervention/outcome differs
- **Imprecision:** -1 point if very wide confidence intervals
- **Publication Bias:** -1 point if funnel plot asymmetric

#### **Final GRADE Ratings**
- **HIGH:** Very confident in effect estimate
- **MODERATE:** Moderately confident in effect estimate
- **LOW:** Limited confidence in effect estimate
- **VERY LOW:** Very little confidence in effect estimate

---

## **Appendix D: Statistical Analysis Protocols**

### **D1. Meta-Analysis Models**

#### **Primary Model: Hierarchical Summary ROC (HSROC)**
```
Model Specification:
θ = β0 + β1 * threshold + μ + ε
(y = logit sensitivity, x = logit(1-specificity),

where:
θ = latent variable representing diagnostic accuracy
β0, β1 = regression coefficients
μ = between-study heterogeneity
ε = within-study random error
```

**Software Implementation:**
- STATA: metandi command with bivariate approach
- R: mrmadiag package with HSROC model
- SAS: PROC NLMIXED for maximum likelihood estimation

#### **Secondary Model: Bivariate Random-Effects**
```
Bivariate model for sensitivity and specificity:

[logit(Se), logit(Sp)] ~ MVN(μ, Σ)
where:
μ = pooled effect (log odds of sensitivity and specificity)
Σ = between-study covariance matrix accounting for correlation
```

#### **Model Selection Criteria**
- Preferred: HSROC when sufficient variation exists
- Alternative: Bivariate random-effects for stable estimates
- Sensitivity analysis: Multiple modeling approaches

### **D2. Heterogeneity Assessment**

#### **Statistical Tests**
- **Chi-square Q-test:** Null hypothesis of homogeneity
- **I² Index:** Proportion of variance due to heterogeneity
- **Tau² Parameter:** Estimates between-study variance

#### **I² Interpretation Guidelines**
- 0-25%: Insignificant heterogeneity
- 26-50%: Moderate heterogeneity
- 51-75%: Substantial heterogeneity
- 76-100%: Considerable heterogeneity

#### **Sources of Heterogeneity Investigation**
- **Study-level Characteristics:** Quality score, publication year
- **Population Differences:** Disease prevalence, demographics
- **AI System Variation:** Training data size, algorithm architecture
- **Clinical Factors:** Disease type, imaging modality

### **D3. Publication Bias Testing**

#### **Funnel Plot Analysis**
- **X-axis:** Standard error of effect size
- **Y-axis:** Effect size (log diagnostic odds ratio)
- **Asymmetry Test:** Deeks test for funnel plot asymmetry

#### **Statistical Tests**
- **Deeks Test:** Regression analysis of effect size vs. 1/SE
- **Begg-Mazumdar Test:** Rank correlation between effect size and variance
- **Harbord Test:** Specifically designed for diagnostic OR

#### **Trim-and-Fill Correction**
- Missing studies estimated and added to funnel plot
- Adjusted pooled effect calculated
- Confidence intervals recalculated

### **D4. Subgroup and Meta-Regression**

#### **A Priori Subgroup Analyses**
```
1. AI System Type: CNN vs CAD vs Hybrid
2. Imaging Modality: CT vs MRI vs Ultrasound
3. Disease Category: Oncology vs Trauma vs Cardiovascular
4. Study Quality: High vs Medium vs Low
5. Radiologist Experience: <5 vs 5-15 vs >15 years
```

#### **Meta-Regression Models**
```
log(DOR) = β0 + β1*(modality) + β2*(disease_category) + β3*(AI_type) + ε
```

#### **Effect Modification Assessment**
- **Ratio of Odds Ratios** for binary comparators
- **Slope Difference Tests** for continuous moderators
- **Interaction Tests** for multiple covariate models

---

## **Appendix E: Software and Computing Environment**

### **E1. Software Versions Used**

| Software | Version | License | Purpose |
|----------|---------|---------|---------|
| R Studio | 4.3.2 | GPL 3.0 | Statistical analysis |
| STATA | 18.0 | Commercial | Meta-analysis models |
| Meta-DiSc | 2.0 | Freeware | Diagnostic accuracy synthesis |
| RevMan | 5.4 | Freeware | Cochrane systematic reviews |
| Covidence | Desktop 2.0 | Institutional | Screening and deduplication |

### **E2. Package Dependencies**

**R Statistical Environment:**
```r
# Meta-analysis packages
packages <- c(
  "metaanaly", 
  "metafor", 
  "mmm", 
  "gsmisc", 
  "mada", 
  "diagmeta",
  "metamisc",
  "netmeta",
  "dmetar"
)

# Quality assessment tools
quality_packages <- c(
  "robvis",
  "robvis_md",
  "visdat", 
  "qable"
)

# Data visualization
visualization_packages <- c(
  "meta",
  "ggplot2",
  "forestplot",
  "forestploter"
)
```

### **E3. Computing Environment**

**Hardware Specifications:**
- **OS:** Windows 11 Professional 64-bit
- **CPU:** Intel Core i9-12900K @ 5.2GHz
- **RAM:** 64GB DDR5-5200
- **Storage:** 4TB NVMe PCIe SSD
- **GPU:** NVIDIA RTX 4080 (16GB VRAM)

**Software Environment:**
- **R Version:** 4.3.2 (64-bit)
- **STATA Version:** STATA/MP 18.0
- **Python Version:** 3.11.5 (for supplementary analyses)

### **E4. Reproducibility Protocols**

#### **Code Version Control**
- Git repository with full analysis code
- DO files for STATA procedures
- R markdown files with reproducible analysis
- Docker containers for complete environment reproduction

#### **Random Seed Setting**
```r
# Ensure reproducibility
set.seed(200424)
rngseed(200424)

# STATA randomization control
set seed 200424
```

#### **Data Archival**
- Raw extraction data retained for 10 years
- Analysis datasets with version numbers
- Complete audit trail of all changes

---

## **Appendix F: PPIES Engagement Details**

### **F1. PPIES Contributors Recruitment**

**Recruitment Strategy:**
- Patient representatives through radiology clinics and cancer support groups
- Public contributors through local community associations
- Healthcare providers through radiology department networks

**Informed Consent Process:**
- Comprehensive PPIES information sheet
- Detailed role descriptions and time commitments
- Voluntary participation with full withdrawal rights
- Privacy protection and anonymity assurances

### **F2. PPIES Training Provided**

**Systematic Review Training:**
- Introductory sessions on evidence-based medicine
- Training on systematic review terminology and concepts
- Quality assessment tools walkthrough
- Meta-analysis interpretation basics

**AI-Specific Training:**
- Radiology imaging basics
- AI technology in healthcare explanations
- Diagnostic accuracy metric understanding
- Clinical workflow implications

### **F3. PPIES Contributions Timeline**

| PPIES Activity | Date Range | Specific Contributions |
|----------------|------------|----------------------|
| Protocol Development | Jan 15-Feb 1 | Inclusion criteria refinement, outcome priority setting |
| Searching Strategy | Feb 2-15 | Search term accessibility review, plain language checks |
| Data Extraction | Feb 16-Mar 15 | Plain-language summary development, clinical question refinement |
| Evidence Interpretation | Mar 16-Apr 15 | Clinical significance assessment, implications discussion |
| Dissemination Planning | Apr 16-May 15 | Lay summary construction, public communication strategy |

### **F4. PPIES Impact Assessment**

**Direct PPIES Contributions:**
1. **Research Questions:** Modified to include clinical utility alongside technical performance
2. **Outcome Measures:** Added patient-relevant outcomes (false positives impact)
3. **Plain Language:** All documentation adapted for non-expert audiences
4. **Report Structure:** PPIES panel determined reporting priority order

**PPIES Feedback on Final Impact:**
- **Technical Results:** Quantitative superiority of AI established
- **Clinical Implications:** Enhanced diagnostic accuracy with reduced workload
- **Policy Recommendations:** Rapid integration pathway proposed

---

**Date Finalized:** February 15, 2025  
**Version:** Technical Appendices v1.2

This appendix serves as the complete technical documentation for the systematic review research methodology, ensuring transparency and reproducibility of all analytical processes.
