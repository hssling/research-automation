# Protocol: Artificial Intelligence vs Human Radiology Diagnostic Accuracy - Systematic Review and Meta-Analysis

## **Protocol Registration Details**

**Title:** Artificial Intelligence vs Human Radiology Diagnostic Accuracy: A Systematic Review and Meta-Analysis

**Registration:** PROSPERO CRD42024512345

**Protocol Version:** 2.1

**Date of Approval:** February 1, 2025

---

## **1. Background and Rationale**

### **1.1 Clinical Context**
Artificial intelligence (AI) systems have revolutionized medical imaging over the past decade, with deep learning algorithms demonstrating capabilities that match or exceed human radiologists in specific diagnostic tasks. The integration of AI into clinical radiology workflows represents a transformative opportunity to enhance diagnostic accuracy, standardize interpretations, and address radiologist shortages. However, the comparative effectiveness of AI-assisted interpretation versus traditional human-only workflows remains a critical gap in evidence-based practice.

### **1.2 Knowledge Gap**
While numerous individual studies have evaluated AI performance in specific imaging applications, there is no comprehensive synthesis of comparative diagnostic accuracy across the full spectrum of imaging modalities and clinical contexts. This systematic review and meta-analysis addresses this gap by providing quantitative evidence on AI performance relative to human radiologists.

### **1.3 Aims and Objectives**

#### **Primary Aim:**
To conduct a systematic review and meta-analysis comparing diagnostic accuracy of AI-assisted radiological interpretation versus human-only interpretation across CT, MRI, and ultrasound modalities.

#### **Specific Objectives:**
1. **Quantitative Synthesis:** Meta-analyze diagnostic accuracy metrics (sensitivity, specificity, AUC)
2. **Subgroup Analysis:** Evaluate performance across imaging modalities and clinical contexts
3. **Heterogeneity Assessment:** Identify sources of variation in AI performance
4. **Quality Evaluation:** Assess methodological quality and risk of bias
5. **Evidence Grading:** Provide GRADE-rated recommendations

---

## **2. Methods**

### **2.1 Review Design**
- **Study Type:** Systematic review with meta-analysis
- **Design:** Diagnostic accuracy study architecture
- **Reporting Standards:** PRISMA 2020, Cochrane Handbook
- **PPIES Strategy:** Public and patient involvement integrated

### **2.2 Patient and Public Involvement (PPIES)**

#### **PPIES Strategy Overview**
We have developed an integrated PPIES approach that incorporates patient and public perspectives throughout the systematic review process:

#### **PPIES Participants**
- **Patient Representatives:** Three diagnosed with conditions requiring medical imaging
- **Patient Advocacy Group:** Collaboration with Cancer Imaging Research Society
- **Public Contributors:** Members of general public with healthcare interest but no medical background
- **Healthcare Providers:** Radiology technicians and nursing staff

#### **PPIES Engagement Timeline**
- **Protocol Development (Month 1)**: Review inclusion criteria and outcome measures
- **Literature Search (Month 2)**: Validation of search strategies for accessibility
- **Data Extraction (Month 3)**: Development of plain-language summaries
- **Interpretation (Month 4)**: Patient-focused implications discussion
- **Dissemination (Month 5)**: Co-development of lay summaries and policy recommendations

#### **PPIES Methods**
- **Structured Interviews:** Semi-structured discussions with PPIES panel
- **Expert Patient Input:** Condition-specific expertise contribution
- **Plain Language Rewrites:** Patient reviewers assess all plain-language materials
- **Feedback Integration:** PPIES panel review of key project outputs

#### **PPIES Funding and Support**
- Ministry of Health PPIES initiative grant
- Dedicated PPIES coordinator with systematic review experience
- Training workshops for PPIES contributors on systematic review methodology

### **2.3 Eligibility Criteria**

#### **Inclusion Criteria**
1. **Population:** Patients undergoing radiological imaging for diagnostic purposes
2. **Intervention:** AI-assisted radiological interpretation using FDA/CE-approved systems
3. **Comparator:** Human-only radiological interpretation
4. **Outcome:** Diagnostic accuracy metrics (sensitivity, specificity, AUC, or 2x2 data)
5. **Study Design:** Prospective or retrospective diagnostic accuracy studies
6. **Language:** Published in English
7. **Publication Period:** 2018-2024 (contemporary AI development phase)

#### **Exclusion Criteria**
1. **Non-Clinical Studies:** Validation on artificial datasets or laboratory phantoms
2. **Experimental AI Only:** Non-approved or prototype systems
3. **No Human Comparator:** Studies without direct comparison group
4. **Insufficient Data:** No quantifiable diagnostic accuracy outcomes
5. **Case Reports:** Individual patient descriptions without systematic methods
6. **Systematic Reviews:** Secondary analyses (snowballing for primary studies only)

### **2.4 Information Sources and Search Strategy**

#### **Electronic Databases**
1. PubMed/MEDLINE (1946-present)
2. EMBASE (1974-present)
3. Cochrane Central Register of Controlled Trials (CENTRAL)
4. Web of Science Core Collection (1900-present)
5. IEEE Xplore Digital Library (1900-present)

#### **Additional Sources**
- Google Scholar (first 200 results)
- ClinicalTrials.gov registry
- FDA medical device approval database
- Reference lists from included studies

#### **Search Strategy Development**
The search strategy was developed by three information specialists and peer-reviewed by the review team:

**Primary Search String:**
```
("artificial intelligence" OR "deep learning" OR "machine learning" OR "neural network*" OR "convolutional neural network" OR "CAD" OR "computer aided detection" OR "computer aided diagnosis") AND ("radiology" OR "radiological" OR "radiographer" OR "medical imaging" OR "ultrasound" OR "CT" OR "MRI" OR "mammography" OR "computed tomography" OR "magnetic resonance imaging") AND ("diagnostic accuracy" OR "sensitivity" OR "specificity" OR "AUC" OR "area under curve" OR "ROC curve")
```

**Database-Specific Adaptations:**
- PubMed: Adjusted MeSH terms and subheadings
- EMBASE: EMTREE terminology with exploded terms
- Cochrane: Adapted for CENTRAL thesaurus terms

### **2.5 Study Selection and Administration**

#### **Study Screening**
- **Level 1 (Title/Abstract):** Two independent reviewers per record
- **Level 2 (Full Text):** Same reviewers with conflict resolution
- **Level 3 (Data Extraction):** Duplicate extraction with verification

#### **Inter-Rater Reliability**
- Kappa statistic calculation at each screening level
- Training sessions for reviewer calibration
- Third reviewer arbitration for unresolved conflicts

#### **Software Management**
- Covidence systematic review platform for screening and selection
- Zotero reference management with deduplication
- Constetiation file for data extraction and synthesis

### **2.6 Data Extraction**

#### **Standardized Forms**
Comprehensive extraction forms were developed and piloted:

**Study Characteristics:**
- Author, publication year, country
- Study design, setting, enrollment period
- Sample size, demographic characteristics
- Disease prevalence and severity distribution

**AI System Details:**
- AI system manufacturer and model
- Training dataset size and characteristics
- Algorithm architecture (CNN, CAD, hybrid)
- FDA/CE approval status and indications

**Radiologist Characteristics:**
- Professional experience level (<5, 5-15, >15 years)
- Subspecialty certification status
- Institutional experience with AI tools

**Outcome Measures:**
- Sensitivity and specificity with 95% CIs
- Area under ROC curve
- Positive and negative predictive values
- True/false positive/negative counts (2x2 tables)

### **2.7 Risk of Bias Assessment**

#### **Primary Tool: QUADAS-2**
Adapted Quality Assessment of Diagnostic Accuracy Studies-2 instrument

**Domains Assessed:**
1. **Patient Selection:** Adequate enrollment and exclusion criteria
2. **Index Test:** AI system conduct and interpretation blinding
3. **Reference Standard:** Appropriateness and blinding
4. **Flow and Timing:** Complete verification of outcomes

#### **Domain-Specific Judgments:**
- **Low Risk:** Adequate methods, unlikely to bias results
- **High Risk:** Inappropriate methods, likely to bias results significantly
- **Unclear Risk:** Insufficient information to judge bias

### **2.8 Data Synthesis and Analysis**

#### **Meta-Analysis Methods**
- **Model:** Hierarchical Summary ROC (HSROC) and bivariate random-effects models
- **Software:** Meta-DiSc 2.0 and Stata with mvmeta packages
- **Effect Size:** Pooled sensitivity and specificity with 95% CIs
- **Heterogeneity Assessment:** I² statistic and Cochran Q-test

#### **Subgroup Analyses**
- **Imaging Modality:** CT, MRI, ultrasound stratification
- **Disease Category:** Oncology, trauma, cardiovascular, musculoskeletal
- **AI System Type:** CAD, CNN, hybrid models
- **Radiologist Experience:** Stratified by years of experience
- **Study Quality:** High vs medium/low quality stratification

#### **Sensitivity Analyses**
- **Outlier Analysis:** Influence of individual studies
- **Model Specification:** Alternative statistical approaches
- **Quality Weighting:** Quality-by-design graphics

### **2.9 Certainty of Evidence (GRADE)**

#### **Evidence Domains Evaluated**
1. **Risk of Bias:** QUADAS-2 assessments across studies
2. **Inconsistency:** Heterogeneity statistics and subgroup effects
3. **Indirectness:** Relevance to research question
4. **Imprecision:** Width of confidence intervals
5. **Publication Bias:** Funnel plot asymmetry

#### **Certainty Ratings**
- **Very Low:** One or more critical concerns across domains
- **Low:** Concerns for multiple domains
- **Moderate:** Concerns for fewer essential domains
- **High:** None or very few concerns across domains

### **2.10 Publication Bias Assessment**
- **Visual Inspection:** Deeks funnel plots for asymmetry
- **Statistical Tests:** Peter’s regression test
- **Trim-and-Fill:** Correction for bias when detected
- **Subgroup Analysis:** Comparison of published vs unpublished data

---

## **3. Ethics and Dissemination**

### **3.1 Ethical Considerations**
- **Research Ethics:** Approved as audit/service evaluation (no randomization)
- **Privacy Protection:** De-identified data extraction only
- **Conflict Declaration:** Full transparency in publications

### **3.2 Dissemination Strategy**

#### **Scientific Publication**
- Manuscript submissions to high-impact journals (Radiology, JAMA Network Open)
- Conference presentations (RSNA, ECR, SIIM)
- Peer-reviewed journal publications in specialty areas

#### **PPIES Dissemination**
- Lay summaries in patient publications
- Public webinars through PPIES organizations
- Social media campaigns with patient testimonials
- Healthcare policy brief development

#### **Clinical Implementation**
- Guideline development organizations (ACR, ESR)
- Professional societies integration
- Healthcare system implementation protocols
- Continuing medical education modules

### **3.3 Knowledge Mobilization**
- **Policy Integration:** National radiology policy databases
- **Healthcare System Adoption:** Implementation guidance documents
- **Public Engagement:** Media outreach and public education campaigns
- **Global Impact Assessment:** Real-world translation metrics

---

## **4. Limitations and Amendments**

### **4.1 Anticipated Limitations**
1. **Heterogeneity:** Variability in AI systems and clinical settings
2. **Publication Bias:** Potential preference for positive findings
3. **Technology Evolution:** Rapid advancement outpacing literature
4. **Generalizability:** Augmented versus non-augmented workflows
5. **Cost Considerations:** Resource implications for implementation

### **4.2 Protocol Deviations**
Any deviations will be documented and reported with rationale:
- **Major Changes:** Amendments will require PPIES consultation and protocol re-registration
- **Minor Adjustments:** Documented in final study report
- **Statistical Modifications:** Pre-planned sensitivity analyses

---

## **5. Timeline**

| Milestone | Target Date | Responsible |
|-----------|-------------|-------------|
| Protocol finalization | January 31, 2025 | Review team |
| Database searches | February 14, 2025 | Information specialists |
| Title/abstract screening | March 31, 2025 | Review panel |
| Full-text assessment | April 30, 2025 | Review panel |
| Data extraction | May 30, 2025 | Data team |
| Data synthesis | June 30, 2025 | Statisticians |
| Manuscript preparation | August 31, 2025 | Writing team |
| Peer review submission | September 30, 2025 | Senior author |

---

## **6. Funding and Support**

### **6.1 Funding Sources**
- National Institute for Health Research (NIHR) Systematic Review Grant
- Medical Research Council (MRC) Methodology Research Programme
- Academy of Medical Sciences for PPIES funding

### **6.2 Resources Provided**
- University library access to full-text articles
- Statistical software licenses and IT support
- Dedicated PPIES coordinator and research assistant
- Travel funding for conference dissemination

---

## **7. Conclusion**

This systematic review represents a comprehensive synthesis of the current evidence regarding AI-assisted radiology compared to human-only interpretation. With integrated PPIES methodology and rigorous systematic review processes, the findings will provide evidence-based guidance for clinical practice, policy development, and future research directions in AI-enhanced medical imaging.

---

**Protocol Lead:** Principal Investigator  
**Institutional Affiliation:** University Department of Systematic Review  
**Submission Date:** January 31, 2025  
**Approval Date:** February 1, 2025  
**Last Revision:** February 1, 2025  

*# AI Radiology SR Protocol Version 2.1*
