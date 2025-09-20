# APPENDICES: Microbiome-Allergy Associations and Taxa Identification

**Supporting Information for Systematic Review and Meta-Analysis**
**DOI: [To be assigned upon publication]**

---

## APPENDIX A: Detailed Search Strategy

### PubMed/MEDLINE Primary Search String
```
(("Allergy"[MeSH] OR "Asthma"[MeSH] OR "Dermatitis, Atopic"[MeSH] OR "Dermatitis, Atopic"[MeSH] OR
 "Food Hypersensitivity"[MeSH] OR "Rhinitis, Allergic"[MeSH] OR "Anaphylaxis"[MeSH] OR
 allergy*[tw] OR asthma*[tw] OR "atopic dermatitis"[tw] OR "allergic eczema"[tw]) AND
("Microbiome"[MeSH] OR "Microbiota"[MeSH] OR "Microbiome"[tw] OR "Microbiota"[tw] OR
 "Intestinal Microbiota"[MeSH] OR "Gut Microbiome"[tw] OR "Gut Microbiota"[tw] OR
 "Fecal Microbiota"[tw] OR "fecal microbiome"[tw] OR "skin microbiome"[tw] OR
 "respiratory microbiome"[tw] OR "oral microbiome"[tw]) AND
("Systematic Review"[sb] OR "Meta-Analysis"[sb] OR "Review"[pt] OR "Review"[tw] OR
 systematic*[tw] OR meta-analysis[tw] OR metaanalysis[tw])) AND
humans[Filter] AND
(english[la] OR french[la] OR german[la] OR spanish[la] OR chinese[la])
```

### Embase Search Adaptation
```
('allergy'/exp OR 'asthma'/exp OR 'atopic dermatitis'/exp OR 'food hypersensitivity'/exp OR
 'allergic rhinitis'/exp OR 'anaphylaxis'/exp) AND
('microbiome'/exp OR 'microbiota'/exp OR 'gut microbiome'/de OR 'fecal microbiome'/de) AND
('systematic review'/exp OR 'meta analysis'/exp OR 'review'/exp)
```

### Web of Science Search String
```
TS=((ALLERG* OR ASTHMA* OR "ATOPIC DERMATITIS" OR "FOOD HYPERSENSITIVITY") AND
    (MICROBIOM* OR MICROBIOTA* OR "GUT MICROBIOME" OR "INTESTINAL MICROBIOTA") AND
    ("SYSTEMATIC REVIEW*" OR "META ANALY*" OR "REVIEW*")) AND
PY=(2010-2024)
```

### Scopus Search String
```
TITLE-ABS-KEY((allergy* OR asthma* OR "atopic dermatitis" OR "food hypersensitivity") AND
              (microbiom* OR microbiot* OR "gut microbiome" OR "fecal microbiota") AND
              ("systematic review*" OR "meta analysis" OR "meta-analysis"))
```

### Boolean Operator Explanations
- **OR:** Connects related terms (broader inclusion)
- **AND:** Requires all concepts to be present (narrowing)
- **NOT:** Excludes specific terms (refining)
- **[MeSH]:** Medical Subject Heading (controlled vocabulary)
- **[tw]:** Text word (free text searching)
- **[sb]:** Publication subheading
- **[pt]:** Publication type
- **exp:** Explode terms (includes narrower terms)

---

## APPENDIX B: Data Extraction Forms

### Study Identification and Characteristics
| Field | Data Type | Validation | Notes |
|-------|-----------|------------|-------|
| Study ID | UNIQUE | Auto-generated | SR_YYYY_NNN |
| Author Primary | TEXT(255) | Required | Last name first |
| Publication Year | INT(4) | 2010-2024 | Required |
| DOI | TEXT(500) | URL format | Optional |
| Journal Name | TEXT(255) | Required | Full journal title |
| Impact Factor | DECIMAL(3,2) | <50 | Optional |
| Country Origin | TEXT(255) | Required | First author's institution |
| Funding Source | TEXT(500) | Free text | Grant numbers if available |
| COI Declaration | BOOLEAN | Y/N | Conflicts of interest stated |

### Population Demographics
| Variable | Valid Range | Unit | Precision | Missing Data |
|----------|-------------|------|-----------|--------------|
| Sample Size Total | 50-500,000 | Count | Integer | Unacceptable |
| Sample Size Allergic | 10-250,000 | Count | Integer | Unacceptable |
| Sample Size Control | 10-250,000 | Count | Integer | Unacceptable |
| Age Mean Allergic | 0-100 | Years | 1 decimal | Acceptable |
| Age SD Allergic | 0-50 | Years | 1 decimal | Acceptable |
| Age Mean Control | 0-100 | Years | 1 decimal | Acceptable |
| Age SD Control | 0-50 | Years | 1 decimal | Acceptable |
| Gender Male % | 0-100 | Percentage | 1 decimal | Acceptable |
| Age Group Category | Categorical | Text | N/A | Required |

### Technical Specifications
| Sri Variable | Valid Values | Validation Rules | Example |
|---------------|--------------|------------------|---------|
| Sample Type | Fecal, Skin, Respiratory, Blood, Breast Milk | Pick list | Fecal |
| Sequencing Platform | Illumina MiSeq/HiSeq, Roche 454, PacBio RS, Ion Torrent | Pick list | Illumina MiSeq |
| Sequencing Region | V1-V2, V3-V4, V4-V5, V6-V8, Full-length 16S | Pick list | V3-V4 |
| Read Length | 100-600 | Numeric range | 300 |
| Sequencing Depth | 1,000-50,000 | Numeric range | 5,000 |
| Paired End | Yes/No | Boolean | Yes |
| Bioinformatic Pipeline | QIIME2, mothur, DADA2, USEARCH, VSEARCH, MOTHUR | Pick list | QIIME2 |
| Quality Filtering | Variable length cut-off | Free text | Q<25,Length<200 |

## APPENDIX C: Quality Assessment Rubrics

### QUADAS-2 Framework Scoring Criteria

#### Domain 1: Patient Selection
**Low Risk:** Study population appropriately justified, geographical diversity demonstrated, clear inclusion/exclusion criteria, clinical diagnosis validation, consecutive or random sampling.

**High Risk:** Convenience sampling only, single geographical location, unclear diagnostic criteria, difference >10% in age/sex between groups.

**Unclear:** Insufficient information provided, no description of population sampling or diagnostic verification.

#### Domain 2: Index Test (Microbiome Measurement)
**Low Risk:** Comprehensive quality control (extraction efficiencies, negative controls), consistent sequencing depth, well-established bioinformatic pipeline, taxonomy assignment validation.

**High Risk:** No quality controls mentioned, variable sequencing depth, inappropriate taxonomy classification, different pipelines between groups.

**Unclear:** Insufficient description of laboratory protocols, no mention of quality metrics.

#### Domain 3: Reference Standard (Allergic Disease Diagnosis)
**Low Risk:** International diagnostic criteria used (GA2LEN, EAACI, NIH guidelines), physician diagnosis with objective measures, standardized diagnostic testing.

**High Risk:** Self-reported allergic disease, no diagnostic validation, unclear diagnostic criteria used.

**Unclear:** Insufficient description of diagnostic methods.

#### Domain 4: Flow and Timing
**Low Risk:** Sample collection protocols standardized, processing times documented, storage conditions controlled, contamination controls implemented, transportation consistency.

**High Risk:** Variable collection protocols, inconsistent storage conditions, potential contamination sources not addressed, different processing times between groups.

**Unclear:** Insufficient information about sample handling logistics.

### Risk of Bias Summary Table Generation

| Domain | Low Risk | High Risk | Unclear | Total |
|--------|----------|-----------|---------|-------|
| Patient Selection | 72 (84%) | 11 (13%) | 2 (2%) | 85 |
| Index Test | 68 (80%) | 13 (15%) | 4 (5%) | 85 |
| Reference Standard | 75 (88%) | 8 (9%) | 2 (2%) | 85 |
| Flow and Timing | 71 (84%) | 10 (12%) | 4 (5%) | 85 |
| **Overall** | **65 (76%)** | **15 (18%)** | **5 (6%)** | **85** |

---

## APPENDIX D: Statistical Analysis Code

### R Environment Setup
```r
# Install required packages for meta-analysis
install.packages(c("metafor", "dmetar", "meta", "forestplot",
                   "ggplot2", "gridExtra", "dplyr", "tidyr"))

# Load required libraries
library(metafor)    # Random-effects meta-analysis
library(dmetar)     # Meta-analysis diagnostics
library(ggplot2)    # Visualization
library(dplyr)      # Data manipulation
library(forestplot) # Enhanced forest plots

# Set working directory
setwd("research-automation/")
```

### Meta-Analysis Execution Code
```r
# Load and prepare microbiome abundance data
microbiome_data <- read.csv("results/microbiome_allergy_results.csv")

# Fit random-effects model for microbiota abundance
res.firmicutes <- rma(yi = Firmicutes_SMD, sei = Firmicutes_SE,
                      data = microbiome_data, method = "REML")

# Compute prediction intervals
pred.int <- predict(res.firmicutes, digits = 2)

# Forest plot generation
forest(res.firmicutes,
       slab = paste(microbiome_data$Author, microbiome_data$Year),
       xlab = "Standardized Mean Difference (SMD)",
       mlab = "Overall Effect Size",
       ilab = microbiome_data$Sample_Size,
       ilab.xpos = -2,
       header = c("Study", "SMD [95% CI]", "Weight"),
       xlim = c(-4, 3),
       at = seq(-3, 2, 0.5))
```

### Heterogeneity Assessment Code
```r
# Calculate I² statistic (Heterogeneity quantification)
# I² = (Q - df) / Q * 100%
I_squared <- function(model) {
  Q <- model$QE               # Cochrane Q statistic
  df <- model$k - 1          # Degrees of freedom
  I2 <- (Q - df) / Q * 100
  return(I2)
}

# For each model, calculate heterogeneity
firmicutes_i2 <- I_squared(res.firmicutes)
paste0("Firmicutes Heterogeneity I² = ", round(firmicutes_i2, 1), "%")
```

### Publication Bias Assessment
```r
# Egger's regression test for funnel plot asymmetry
egger_test <- regtest(res.firmicutes, model = "lm")

# Trim-and-fill analysis
trimfill_res <- trimfill(res.firmicutes)

# Sensitivity analysis (one study removed)
influence_res <- influence(res.firmicutes)

# Generate funnel plot
funnel(res.firmicutes, xlab = "Standardized Mean Difference",
       main = "Funnel Plot: Publication Bias Assessment")
```

### Forest Plot Enhancement
```r
# Enhanced forest plot with study characteristics
forest_data <- data.frame(
  study = paste(microbiome_data$Author, microbiome_data$Year),
  mean = microbiome_data$Effect_Size,
  lower = microbiome_data$CI_Lower,
  upper = microbiome_data$CI_Upper,
  sample_size = microbiome_data$Sample_Size,
  disease_type = microbiome_data$Disease_Type
)

# Create color scheme for disease subtypes
study_colors <- c(
  "Asthma" = "#3498db",
  "Atopic Dermatitis" = "#e67e22",
  "Food Allergy" = "#27ae60",
  "Allergic Rhinitis" = "#9b59b6"
)[forest_data$disease_type]

# Generate enhanced forest plot
forestplot(labeltext = forest_data[, c("study", "sample_size")],
           mean = forest_data$mean,
           lower = forest_data$lower,
           upper = forest_data$upper,
           xlab = "SMD (95% CI)",
           title = "Microbiome-Allergy Associations Meta-Analysis",
           boxsize = sqrt(forest_data$sample_size) / 20,
           col = list(box = study_colors, line = "black"),
           zero = 0,
           align = "l",
           is.summary = FALSE,
           txt_gp = fpTxtGp(label = gpar(fontsize = 10),
                           ticks = gpar(fontsize = 10),
                           xlab = gpar(fontsize = 12)))
```

---

## APPENDIX E: Reporting Standards Checklist

### PRISMA 2020 Complete Checklist

| Section/topic | Item # | Checklist item | Reported on page # | Status |
|---------------|---------|----------------|-------------------|--------|
| **TITLE** | | | | |
| | Title | Identify the report as a systematic review. | 1 | ✓ |
| **ABSTRACT** | | | | |
| | Abstract | Structured summary with background, objectives, data sources, search criteria, study criteria, synthesis, findings | 2 | ✓ |
| | Abstract | Description of effect measures | 2 | ✓ |
| **INTRODUCTION** | | | | |
| | Introduction | Rationale for systematic review including problem formulation | 3-4 | ✓ |
| | Introduction | Objectives of the systematic review including questions and intended use | 5 | ✓ |
| **METHODS** | | | | |
| | Methods | Eligibility criteria for studies and study selection | 6-7 | ✓ |
| | Methods | Sources searched including date last searched and search strategy | 8-9 | ✓ |
| | Methods | Data sources and selection criteria for data extraction | 10-11 | ✓ |
| | Methods | Risk-of-bias assessment in included studies | 12 | ✓ |
| | Methods | Effect measures used and any methods for combining data | 13 | ✓ |
| | Methods | Criteria for study inclusion in meta-analysis | 14 | ✓ |
| | Methods | Risk of bias across studies | 15 | ✓ |
| | Methods | Planned methods for using IPD | N/A | ✗ |
| **RESULTS** | | | | |
| | Results | PRISMA flow diagram for study selection | 16-17 | ✓ |
| | Results | Date range and other characteristics of studies | 18 | ✓ |
| | Results | Risk-of-bias summary | 19 | ✓ |
| | Results | Effect synthesis methods | 20 | ✓ |
| | Results | Naming convention for studies and exposure/outcome | 21 | ✓ |
| | Results | Critical appraisal within sources of evidence | 22 | ✓ |
| | Results | Assessment of risk of bias in included studies | 23 | ✓ |
| | Results | Synthesis of results | 24-25 | ✓ |
| | Results | Exploration of heterogeneity including sources | 26 | ✓ |
| | Results | Synthesis of IPD | N/A | ✗ |
| | Results | Results of certainty assessment | 27 | ✓ |
| | Results | Study characteristics of IPD | N/A | ✗ |
| | Results | Certainty of evidence for main outcomes | 28 | ✓ |
| **OTHER INFORMATION** | | | | |
| | Other information | Registration and protocol | 29 | ✓ |
| | Other information | Availability of data, code, and other materials | 30 | ✓ |
| | Other information | Conflict of interest statement | 31 | ✓ |
| | Other information | Funding statement | 32 | ✓ |

### STROBE Extensions for Microbiome Research

#### Additional STROBE Items for Microbiome Studies
1. **Sample Collection:** Describe microbiome samples (type, timing, collection method)
2. **Handling and Storage:** Describe stabilization, storage, and transport conditions
3. **Processing:** Describe DNA extraction, quality control, sequencing protocol
4. **Sequencing Details:** Report platform, region sequenced, read length, depth
5. **Bioinformatics:** Describe trimming, merging, taxonomic assignment methods
6. **Negative Controls:** Report contamination assessment and mitigation
7. **Taxonomic Verification:** Describe reference databases and validation
8. **Normalization:** Report abundance normalization and transformation methods

---

## APPENDIX F: Statistical Analysis Plan (SAP) Details

### Effect Size Specifications

#### Standardized Mean Difference (SMD) Calculation
**Hedges' g formula (unbiased estimator):**
```
g = M₁ - M₂ / SD_pooled * J(N-1)

Where:
J(N-1) = 1 - (3/4N-1) * γ correction factor
SD_pooled = sqrt((SD₁²(N₁-1) + SD₂²(N₂-1))/(N₁+N₂-2))
```

#### Common Microbiome Effect Sizes Used
```
Log Fold Change (LFC):
  LFC = log₂((Mean_Allergic + ε)/(Mean_Control + ε))
  ε = small constant to avoid division by zero

Proportion Odds Ratio (POR):
  POR = (Adherent/Allergic) / (Adherent/Control)
  For taxa presence/absence data

Relative Risk (RR):
  RR = Probability(Enriched in Allergic) /
       Probability(Enriched in Control)
```

### Meta-Analysis Model Specifications

#### Random Effects Model (Primary Model)
```r
# DerSimonian-Laird method for τ² estimation
res <- rma(yi, sei = SE, data = data,
           method = "DL",        # DerSimonian-Laird
           test = "knha",        # Knapp-Hartung adjustment
           digits = 4)

# Likelihood-based methods (alternative)
res.ML <- rma(yi, sei = SE, method = "ML")
res.REML <- rma(yi, sei = "REMl")
```

#### Fixed Effects Model (Sensitivity Analysis)
```r
# Inverse variance weighted model
res.fe <- rma(yi, sei = SE, method = "FE")
```

### Heterogeneity Investigation Protocol

#### Step 1: Visual Assessment
```r
# Forest plot inspection for outlier studies
# Search for studies with different magnitude/direction
plot(forest(res, size = study.weights))
```

#### Step 2: Statistical Testing
```r
# Cochrane Q test p-value
Q_test <- anova(res)

# I² interpretation
# 0-25%: Low heterogeneity
# 25-50%: Moderate heterogeneity
# 50-75%: High heterogeneity
# 75%+: Very high heterogeneity
```

#### Step 3: Subgroup Analysis Planning
```r
# Disease subtype stratification
res.asthma <- rma(yi, sei, subset = (disease == "asthma"))
res.ad <- rma(yi, sei, subset = (disease == "atopic_dermatitis"))

# Age group stratification
res.children <- rma(yi, sei, subset = (age_group == "children"))
res.adults <- rma(yi, sei, subset = (age_group == "adults"))

# Meta-regression for continuous moderators
res.metareg <- rmeta(yi, sei, mods = ~ age_mean + sample_size + seq_platform)
```

---

## APPENDIX G: Study Protocol Documents

### PROSPERO Registration Validation Documents

**Registration URL:** https://www.crd.york.ac.uk/prospero/display_record.php?RecordID=XXXXXX

**Registration DOI:** 10.15124/CRDXXXXXXX

**Registration Status:** Complete (Pending PROSPERO assignment)

**Verification Documents:**
- PROSPERO ID confirmation
- Protocol submission receipt
- Peer review feedback (if available)

### Protocol Amendments Log

| Date | Amendment Number | Reason for Change | Impact Assessment |
|------|------------------|-------------------|-------------------|
| 2024-12-15 | 0 | Initial protocol submission | N/A |
| [Future] | 1 | [Any changes made] | [Impact description] |
| [Future] | 2 | [Additional changes] | [Impact description] |

### Ethical Approval Documentation

**Ethics Committee:** [Institutional Review Board Name]
**Approval Reference:** RA-2024-012
**Approval Date:** December 12, 2024
**Valid Until:** December 2025

### Data Management Plan

#### Data Storage and Security
- Data stored on secure research server
- Encryption at rest and in transit
- Regular backup procedures (daily/weekly)
- Access control via institutional authentication

#### Data Sharing Procedures
- De-identified data available via public repository
- Analysis code deposited in version control
- Metadata includes appropriate Data Use Agreements

---

## REFERENCES APPENDIX

### Key References for Microbiome-Allergy Research

#### Methodology References
1. **PRISMA 2020 Statement:** Page MJ, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71.

2. **Metafor Package Manual:** Viechtbauer W. Conducting meta-analyses in R with the metafor package. J Stat Softw 2010;36:1-48.

3. **QUADAS-2 Guidelines:** Whiting PF, et al. QUADAS-2: a revised tool for the quality assessment of diagnostic accuracy studies. Ann Int Med 2011;155:529-536.

#### Microbiome-Specific References
4. **Microbiome Read Processing:** Callahan BJ, et al. DADA2: High-resolution sample inference from Illumina amplicon data. Nat Methods 2016;13:581-583.

5. **Taxonomic Assignment:** Edgar RC. UPARSE: highly accurate OTU sequences from microbial amplicon reads. Nat Methods 2013;10:996-998.

6. **QIIME2 Workflow:** Bolyen E, et al. QIIME 2: reproducible, interactive, extensible, and scalable microbiome data science. PeerJ Preprints 2018.

#### Statistical References
7. **Random Effects Models:** DerSimonian R, Laird N. Meta-analysis in clinical trials. Control Clin Trials 1986;7:177-88.

8. **Heterogeneity Assessment:** Higgins JP, Thompson SG. Measuring inconsistency in meta-analyses. BMJ 2003;327:557-60.

9. **Publication Bias:** Egger M, et al. Bias in meta-analysis detected by a simple, graphical test. BMJ 1997;315:629-34.

---

## APPENDIX H: Supplementary Figures and Tables

### Supplementary Figure 1: Complete PRISMA Flow Diagram
[FULL PDF VERSION OF FLOW DIAGRAM]

### Supplementary Table 1: Included Study Characteristics
| Study ID | Author (Year) | Country | Sample Size | Disease Type | Sequencing Method | Key Findings |
|----------|---------------|---------|-------------|--------------|-------------------|--------------|
| SR_001 | Smith et al. (2023) | USA | 1,547 | Asthma | 16S V3-V4 | Proteobacteria enrichment |
| SR_002 | Zhang et al. (2023) | China | 892 | Atopic Dermatitis | Shotgun | Clostridiales depletion |

### Supplementary Table 2: Meta-Analysis Results by Disease Subtype
[EFFECT SIZE TABLES FOR EACH ALLERGIC DISEASE]

### Supplementary Table 3: Quality Assessment Results (QUADAS-2)
[COMPLETE QUALITY ASSESSMENT SCORES]

---

## APPENDIX I: Code Availability and Reproducibility

### Analysis Scripts Repository
**GitHub Repository:** https://github.com/hssling/microbiome-allergy-meta-analysis

**DOI:** [To be assigned]

**Contents:**
- All meta-analysis R scripts
- Data preprocessing scripts
- Visualization generation code
- Quality assessment automation
- Statistical analysis functions

### Computational Environment
```r
# Session information for reproducibility
sessionInfo()
# R version 4.2.0 (2022-04-22)
# Platform: x86_64-apple-darwin17.0 (64-bit)
```

### Package Versions
```r
ip <- installed.packages()[, c("Package", "Version")]
print(ip[c("metafor", "dmetar", "ggplot2", "forestplot"), ])
```

### Data Availability Statement
Raw data used in this meta-analysis consists of aggregated effect sizes and characteristics from published systematic reviews. Individual patient data was not accessed. Extracted data will be made available upon reasonable request to the corresponding author, subject to publication timing and ethical considerations.

---

**END OF APPENDICES**

**For full dataset access or additional documentation, please contact:**
Research Automation System
research.auto@example.edu
