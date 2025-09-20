# PRISMA 2020 Flow Diagram: Artificial Intelligence vs Human Radiology Diagnostic Accuracy Meta-Analysis

**Review Title:** Artificial Intelligence vs Human Radiology Diagnostic Accuracy: A Systematic Review and Meta-Analysis

**Review Question:** "Does AI-assisted radiological interpretation demonstrate superior diagnostic accuracy compared to human-only interpretation across CT, MRI, and ultrasound modalities?"

**Date of Final Search:** January 31, 2025

---

## **PRISMA 2020 Flow Diagram**

```mermaid
flowchart TD
    A[Records identified from databases<br/>PubMed/MEDLINE: 4,271<br/>EMBASE: 3,456<br/>Cochrane CENTRAL: 127<br/>Web of Science: 2,089<br/>IEEE Xplore: 1,379<br/>Google Scholar: 943<br/>Total: 12,265] --> B[Deduplication using Covidence<br/>Records removed: 3,214<br/>Records after deduplication: 9,051]

    B --> C[Title and abstract screening<br/>Excluded: 8,342<br/>Reasons for exclusion:<br/>- Not relevant topic: 4,713 (56.5%)<br/>- Not diagnostic accuracy study: 1,958 (23.5%)<br/>- Conference abstracts only: 1,247 (14.9%)<br/>- Non-English language: 311 (3.7%)<br/>- Animal studies: 113 (1.4%)]

    C --> D[Records screened from full-text<br/>Potentially relevant: 709]

    D --> E[Full-text articles assessed<br/>Eligible for inclusion: 189<br/>Reasons for exclusion:<br/>- Insufficient data for meta-analysis: 287<br/>- No human comparison group: 154<br/>- Non-FDA/CE approved AI: 43<br/>- Non-clinical validation study: 36]

    E --> F[Reports included in meta-analysis: 189<br/>Total imaging cases: 98,743<br/>Studies with sensitivity/specificity: 189<br/>Studies with AUC data: 142]

    F --> G[Included study characteristics<br/>CT/MRI: 68%<br/>Ultrasound: 32%<br/>Prospective studies: 47%<br/>Retrospective: 53%<br/>Publication years: 2018-2024]
```

---

## **PRISMA 2020 Checklist Verification**

| Section/Topic | # | Checklist Item | Location in Report or Protocol |
|---------------|---|----------------|-------------------------------|
| **TITLE** | 1 | Title | Manuscript Title Section |
| | 2 | Abstract | Manuscript Abstract Section |
| | 3 | Introduction | Background and Rationale Sections |
| **METHODS** | 4 | Eligibility criteria | PROSPERO Protocol and Methods Section |
| | 5 | Information sources | Search Strategy Section |
| | 6 | Search strategy | Electronic Database Searches Section |
| | 7 | Selection process | Study Records Section |
| | 8 | Data collection process | Data Extraction Section |
| | 9 | Data items | Data Items to Extract Section |
| | 10 | Risk of bias assessment | Risk of Bias Assessment Section |
| | 11 | Effect measures | Summary Measures Section |
| | 12 | Synthesis methods | Data Analysis Section |
| | 13 | Reporting bias assessment | Addressing Missing Data Section |
| | 14 | Certainty assessment | Confidence in Cumulative Evidence Section |
| **RESULTS** | 15 | Study selection | PRISMA Flow Diagram and Results Section |
| | 16 | Study characteristics | Study Characteristics Tables |
| | 17 | Risk of bias | Quality Assessment Results Section |
| | 18 | Results of individual studies | Forest Plots and Data Tables |
| | 19 | Results of syntheses | Meta-Analysis Results Section |
| | 20 | Reporting biases | Publication Bias Analysis Section |
| | 21 | Certainty of evidence | GRADE Assessment Section |
| **DISCUSSION** | 22 | Discussion of results | Interpretation and Implications Section |
| | 23 | Limitations | Strengths and Limitations Section |
| | 24 | Conclusions | Study Conclusion Section |
| **OTHER** | 25 | Registration and protocol | PROSPERO Registration Section |
| | 26 | Support | Funding and Declarations Section |
| | 27 | Competing interests | Conflicts of Interest Section |

---

## **Detailed Exclusion Documentation**

### **Title/Abstract Screening Exclusions (N=8,342)**

| Reason for Exclusion | Number | Percentage |
|---------------------|--------|------------|
| Not relevant to AI or radiology | 4,713 | 56.5% |
| Not diagnostic accuracy study | 1,958 | 23.5% |
| Conference abstracts or posters only | 1,247 | 14.9% |
| Non-English language | 311 | 3.7% |
| Animal or preclinical studies | 113 | 1.4% |
| **Total Excluded** | **8,342** | **100.0%** |

### **Full-Text Assessment Exclusions (N=520)**

| Reason for Exclusion | Number | Percentage |
|---------------------|--------|------------|
| Insufficient data for meta-analysis (no 2x2 GUANSE or AUC) | 287 | 55.2% |
| No direct comparison with human radiologists | 154 | 29.6% |
| Experimental/non-clinical AI systems only | 43 | 8.3% |
| Non-English full text despite English abstract | 36 | 6.9% |
| **Total Excluded** | **520** | **100.0%** |

---

## **Study Characteristics Summary**

### **Included Studies Demographics (N=189)**

| Characteristic | N | Percentage |
|----------------|---|------------|
| **Study Design** | | |
| Prospective cohort | 89 | 47.1% |
| Retrospective cohort | 100 | 52.9% |
| **Image Modality** | | |
| Computed Tomography (CT) | 98 | 51.9% |
| Magnetic Resonance Imaging (MRI) | 44 | 23.3% |
| Ultrasound | 47 | 24.9% |
| **Primary Disease Category** | | |
| Oncology | 89 | 47.1% |
| Trauma | 45 | 23.8% |
| Cardiovascular | 35 | 18.5% |
| Musculoskeletal | 20 | 10.6% |
| **Publication Year** | | |
| 2018-2020 | 56 | 29.6% |
| 2021-2023 | 98 | 51.9% |
| 2024 | 35 | 18.5% |
| **Geographic Region** | | |
| North America | 87 | 46.0% |
| Europe | 65 | 34.4% |
| Asia-Pacific | 32 | 16.9% |
| Other | 5 | 2.6% |

### **Artificial Intelligence System Characteristics**

| AI System Type | N | Description |
|----------------|---|-------------|
| Convolutional Neural Networks | 142 | Deep learning image analysis |
| Computer-Aided Detection | 31 | Targeted pathology detection |
| Hybrid Models | 16 | Ensemble approaches |
| **Total AI Systems** | **189** | **Multiple systems per study** |

---

## **Quality Assessment Summary**

### **QUADAS-2 Quality Assessment Results**

| Domain | Low Risk | Unclear Risk | High Risk |
|---------|----------|--------------|-----------|
| Patient Selection | 89 (47.1%) | 78 (41.3%) | 22 (11.6%) |
| Index Test | 156 (82.5%) | 33 (17.5%) | 0 (0.0%) |
| Reference Standard | 178 (94.2%) | 11 (5.8%) | 0 (0.0%) |
| Flow and Timing | 167 (88.4%) | 22 (11.6%) | 0 (0.0%) |
| **Overall Quality Score** | **High: 167 (88.4%)** | **Medium: 22 (11.6%)** | **Low: 0 (0.0%)** |

---

## **PRISMA 2020 Submission Details**

**Submission Date:** February 14, 2025

**Generated Flow Diagram Figures:**
- Main flow diagram (Figure 1)
- Supplemental exclusion detail tables (Tables A1-A3)
- Study characteristics histograms (Figures B1-B4)

**Reporting Software Used:**
- PRISMA 2020 R package (version 1.0.0)
- GraphPad Prism (quality assessment summaries)
- Adobe Illustrator CC (final formatting)

**Filename for Submission:**
`PRISMA_2020_Flow_Diagram_AI_Radiology_Meta_Analysis.pdf`

---

**Date of Last Update:** February 14, 2025
**Version:** 1.2
**Corresponding Author Contact:** Available in manuscript
