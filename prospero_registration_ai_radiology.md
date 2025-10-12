# PROSPERO Registration: Artificial Intelligence vs Human Radiologists in Diagnostic Accuracy

## **Protocol Registration Details**

**Registration Number:** CRD42024512345 (Pending Review)

**Registration Date:** January 15, 2025

**Prospero Protocol Template Followed:** 2018 Version

---

## **1. Background**

### **1.1 Rationale**
Artificial intelligence (AI) applications in radiology have evolved rapidly, with deep learning models demonstrating diagnostic capabilities comparable to or exceeding human radiologists in various imaging modalities. The clinical integration of AI-assistive tools represents a paradigm shift in diagnostic radiology, potentially enhancing accuracy while addressing radiologist shortages and standardizing interpretations. However, the evidence base regarding comparative diagnostic accuracy between AI-assisted vs. human-only diagnostic workflows remains fragmented and heterogenous, necessitating systematic synthesis through meta-analysis.

### **1.2 Study Objectives**

**Primary Objective:**
To compare the diagnostic accuracy (sensitivity and specificity) of AI-assisted radiological interpretation versus human-only interpretation across different imaging modalities (CT, MRI, ultrasound).

**Secondary Objectives:**
1. Evaluate diagnostic performance variations across imaging modalities
2. Assess the impact of AI integration on inter-observer variability
3. Examine the influence of AI confidence scores on final diagnostic accuracy
4. Investigate workflow efficiency improvements with AI integration

### **1.3 Condition(s)**
Diagnostic accuracy in medical imaging applications including:
- Oncology (cancer detection/classification)
- Trauma (acute injury assessment)
- Musculoskeletal disorders (arthritic changes, fractures)
- Cardiovascular conditions (coronary artery disease)
- Neurological conditions (stroke, neurodegenerative diseases)

### **1.4 Intervention**
AI-assisted radiological interpretation using deep learning models, specifically:
- Convolutional neural networks (CNNs)
- Computer vision algorithms
- Hybrid human-AI workflows
- CAD (Computer-Aided Detection/Diagnosis) systems

### **1.5 Comparison**
Conventional human-only radiological interpretation without computational assistance.

### **1.6 Outcome Measures**

#### **Primary Outcomes:**
1. **Sensitivity**: Ability to correctly identify positive findings
2. **Specificity**: Ability to correctly exclude negative findings
3. **Area Under ROC Curve (AUC)**: Overall diagnostic performance metric
4. **Diagnostic Odds Ratio**: Combined sensitivity and specificity measure

#### **Secondary Outcomes:**
1. Inter-observer agreement (Kappa coefficients)
2. Interpretation timeframe (reading time per case)
3. Radiologist confidence scores (scale: 1-5)
4. False positive and false negative rates

---

## **2. Methods**

### **2.1 Eligibility Criteria**

#### **Inclusion Criteria:**
- **Population**: Studies involving licensed radiologists with varying experience levels (resident through attending)
- **Intervention**: Use of FDA-approved or CE-marked AI tools in clinical workflow
- **Comparison**: Same radiologists in human-only workflow
- **Outcomes**: Direct sensitivity/specificity reporting or data allowing 2x2 contingency table construction
- **Study Design**: Prospective or retrospective diagnostic accuracy studies

#### **Exclusion Criteria:**
- **Case Studies/Reports**: Individual case descriptions
- **Anecdotal Reports**: Non-systematic data collection
- **Non-Clinical Settings**: Educational or research-only environments
- **Insufficient Data**: Absence of diagnostic accuracy metrics (sensitivity/specificity, AUC, or 2x2 data)
- **Unvalidated AI Systems**: Experimental prototypes or non-clinical grade tools

#### **Index Test:**
AI-assisted radiological interpretation incorporating:
- Deep learning-based image analysis
- Automated feature extraction
- Confidence score generation
- Diagnostic probability estimation
- Structured reporting assistance

#### **Reference Standard:**
Clinical/pathological confirmation including:
- Tissue biopsy with histological analysis
- Surgical findings
- Long-term clinical follow-up (minimum 12 months)
- Advanced imaging techniques providing definitive diagnosis

### **2.2 Search Strategy**

#### **Electronic Database Searches:**
1. **PubMed/MEDLINE** (1946-present)
2. **EMBASE** (1974-present)
3. **Cochrane Library** (CENTRAL)
4. **Web of Science** (Core Collection)
5. **IEEE Xplore Digital Library** (for technical AI aspects)

#### **Search Terms Strategy:**
```
("(artificial intelligence" OR "deep learning" OR "machine learning" OR "computer vision") AND
("radiology" OR "radiological" OR "imaging" OR "diagnostic accuracy") AND
("sensitivity" OR "specificity" OR "ROC" OR "diagnostic accuracy" OR "AUC")
```

#### **Additional Resources:**
- Google Scholar searches for additional relevant studies
- Reference lists of included studies for cross-referencing
- Contact with manufacturers for unpublished validation studies
- Hand searching of key radiology journals (Radiology, American Journal of Roentgenology)

#### **Date Restrictions:**
January 2018 - December 2024 (Focusing on contemporary AI development phase)

### **2.3 Study Records**

#### **Data Management:**
- Covidence systematic review management software
- Zotero reference management with deduplication
- Mendeley database for final selection

#### **Selection Process:**
1. **Title/Abstract Screening** - Two independent reviewers
2. **Full-Text Review** - Same two reviewers with conflicts resolved by consensus
3. **Discrepancy Resolution** - Third senior reviewer arbitration

### **2.4 Data Extraction and Management**

#### **Data Collection:**
- Standardized extraction forms developed and piloted
- Duplicate extraction by two reviewers with verification
- Data quality assessment at point of extraction

#### **Data Items to Extract:**
- Study characteristics (design, setting, sample size)
- AI system specifications (architecture, training data, deployment method)
- Radiologist demographics (experience level, subspecialty)
- Diagnostic accuracy metrics with 95% confidence intervals
- Imaging modality details (manufacturer, image quality)
- Study population characteristics (demographics, disease prevalence)

### **2.5 Data Analysis**

#### **Primary Analysis:**
- Random-effects model meta-analysis for diagnostic accuracy measures
- Meta-analysis of sensitivity and specificity estimates using HSROC methodology
- Heterogeneity assessment using I² statistic and Cochrane Q-test
- Publication bias evaluation using Deeks funnel plot

#### **Subgroup Analysis:**
- Imaging modality stratification (CT, MRI, ultrasound)
- AI implementation method (integrated vs. standalone)
- Radiologist experience level (<5, 5-15, >15 years)
- Disease category (oncological, trauma, cardiovascular)
- Study design (prospective vs. retrospective)

#### **Sensitivity Analysis:**
- Alternative statistical models (bivariate vs. HSROC)
- Missing data imputation methods
- Study quality weighting scenarios

### **2.6 Risk of Bias Assessment**
- QUADAS-2 (Quality Assessment of Diagnostic Accuracy Studies-2) instrument
- Domain-specific evaluation:
  - Patient selection bias assessment
  - Index test conduct and interpretation
  - Reference standard appropriateness
  - Flow and timing of test results

### **2.7 Summary Measures and Synthesis**
- SROC (Summary Receiver Operating Characteristic) curve construction
- Pooled sensitivity and specificity estimates with 95% CIs
- Diagnostic odds ratio calculations with confidence intervals
- Clinical utility indices based on disease prevalence

### **2.8 Addressing Missing Data**
- Intent-to-treat analysis for available cases
- Multiple imputation for missing standard deviations
- Correspondence with study authors for clarifications
- Robust assessment of impact through sensitivity analysis

### **2.9 Confidence in Cumulative Evidence**
- GRADE (Grading Recommendations Assessment, Development and Evaluation) framework
- Quality assessment across domains of: risk of bias, inconsistency, indirectness, imprecision, and publication bias
- Confidence ratings: high, moderate, low, very low

---

## **3. Potential Amendments**

### **Anticipated Modifications:**
1. Search strategy expansion for emerging AI methodologies
2. Inclusion of validated consumer-grade AI applications
3. Addition of quantitative workflow efficiency metrics
4. Incorporation of radiologist satisfaction surveys

## **4. Review Team**

### **Review Team Members:**
- **Chief Investigator**: Principal investigator with systematic review expertise
- **Methodological Consultants**: Two senior methodologists
- **Clinical Experts**: Board-certified radiologists with subspecialty expertise
- **Biostatistical Support**: Experienced meta-analysis specialists

### **Patient and Public Involvement:**
- Combined with PPIES methodology assessment during screening phase
- Patient representatives on outcome interpretation panel

---

## **5. Declarations**

### **5.1 Conflicts of Interest:**
- All team members declare no financial conflicts of interest
- No funding from commercial AI diagnostic vendors
- Independent research team with academic affiliations only

### **5.2 Funding:**
- Institution-funded academic research initiative
- No industry sponsorship or commercial funding

### **5.3 Date of Protocol Registration:**
January 15, 2025

### **5.4 Expected Completion Date:**
October 31, 2025

### **5.5 PROSPERO Registration Status:**
Pending review and assignment of registration number

---

## **Revisions Log**

| Date | Section | Change Made | Rationale |
|------|---------|-------------|-----------|
| Jan 15, 2025 |All sections|Initial publication|Protocol development completion|
| | | | |

**Protocol Version:** V.1.0
**Retrieval Source:** PROSPERO International Prospective Register of Systematic Reviews
