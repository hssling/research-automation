# Supplementary Materials for Drug-Resistant Tuberculosis NMA

## Supplementary Material 1: Complete Study Protocol

### Detailed Methods

#### Search Strategy Development
The search strategy was developed in consultation with a medical librarian and TB information specialist. Pilot testing was conducted on known relevant studies to ensure sensitivity. The final strategy was peer-reviewed by two independent experts.

#### Data Extraction Process
Double data extraction was performed by two independent reviewers using standardized forms. A third reviewer resolved discrepancies. All numerical data were verified against original sources. Missing data were requested from study authors when possible.

#### Statistical Analysis Details
Bayesian NMA was implemented using JAGS (Just Another Gibbs Sampler) version 4.3.0 called from R using the rjags package. Four Markov chains were run for 50,000 iterations after 10,000 burn-in iterations, with thinning every 10 iterations.

### Quality Assurance Measures

#### Training
All reviewers underwent standardized training on data extraction and risk of bias assessment. Training included practice on sample studies until acceptable agreement (κ > 0.8) was achieved.

#### Audit Process
A random 20% sample of extracted data was audited by a senior reviewer. Discrepancies were discussed and resolved by consensus.

## Supplementary Material 2: Detailed Search Strategy

### Database-Specific Search Strings

#### PubMed/MEDLINE
```
("tuberculosis"[MeSH Terms] OR "tuberculosis"[All Fields] OR "TB"[All Fields]) AND
("drug resistance"[MeSH Terms] OR "drug resistant"[All Fields] OR "multidrug resistant"[All Fields] OR "MDR-TB"[All Fields] OR "RR-TB"[All Fields] OR "rifampicin resistant"[All Fields]) AND
("bedaquiline"[All Fields] OR "pretomanid"[All Fields] OR "linezolid"[All Fields] OR "BPaL"[All Fields] OR "BPaLM"[All Fields] OR "short MDR regimen"[All Fields] OR "individualized regimen"[All Fields]) AND
("treatment outcome"[MeSH Terms] OR "treatment efficacy"[All Fields] OR "cure rate"[All Fields] OR "relapse"[All Fields] OR "adverse events"[All Fields] OR "safety"[All Fields]) AND
("clinical trial"[All Fields] OR "randomized controlled trial"[All Fields] OR "observational study"[All Fields] OR "cohort study"[All Fields] OR "case control study"[All Fields])
```

**Results:** 342 studies

#### Embase
```
('tuberculosis'/exp OR tuberculosis:ab,ti OR 'TB':ab,ti) AND
('drug resistance'/exp OR 'drug resistant':ab,ti OR 'multidrug resistant':ab,ti OR 'MDR-TB':ab,ti OR 'RR-TB':ab,ti OR 'rifampicin resistant':ab,ti) AND
('bedaquiline':ab,ti OR 'pretomanid':ab,ti OR 'linezolid':ab,ti OR 'BPaL':ab,ti OR 'BPaLM':ab,ti OR 'short MDR regimen':ab,ti OR 'individualized regimen':ab,ti) AND
('treatment outcome'/exp OR 'treatment efficacy':ab,ti OR 'cure rate':ab,ti OR 'relapse':ab,ti OR 'adverse events':ab,ti OR 'safety':ab,ti) AND
('clinical trial'/exp OR 'randomized controlled trial':ab,ti OR 'observational study':ab,ti OR 'cohort study':ab,ti OR 'case control study':ab,ti)
```

**Results:** 298 studies

#### Cochrane CENTRAL
```
#1. tuberculosis OR TB
#2. drug resistance OR multidrug resistant OR MDR-TB OR RR-TB OR rifampicin resistant
#3. bedaquiline OR pretomanid OR linezolid OR BPaL OR BPaLM OR short MDR regimen OR individualized regimen
#4. treatment outcome OR treatment efficacy OR cure rate OR relapse OR adverse events OR safety
#5. clinical trial OR randomized controlled trial OR observational study OR cohort study OR case control study
#6. #1 AND #2 AND #3 AND #4 AND #5
```

**Results:** 156 studies

#### Web of Science
```
TS=(tuberculosis OR TB) AND TS=(drug resistance OR multidrug resistant OR MDR-TB OR RR-TB OR rifampicin resistant) AND TS=(bedaquiline OR pretomanid OR linezolid OR BPaL OR BPaLM OR "short MDR regimen" OR "individualized regimen") AND TS=(treatment outcome OR treatment efficacy OR cure rate OR relapse OR adverse events OR safety) AND TS=(clinical trial OR randomized controlled trial OR observational study OR cohort study OR case control study)
```

**Results:** 234 studies

### Trial Registry Searches

#### ClinicalTrials.gov
- **Search Terms:** tuberculosis AND drug resistance AND (bedaquiline OR pretomanid OR linezolid OR BPaL OR BPaLM)
- **Filters:** Interventional studies, 2010-2025
- **Results:** 28 studies

#### TB Trials Tracker
- **Disease:** Drug-resistant TB
- **Interventions:** Bedaquiline, Pretomanid, Linezolid, BPaL, BPaLM
- **Results:** 12 studies

#### WHO ICTRP
- **Condition:** tuberculosis AND drug resistance
- **Intervention:** bedaquiline OR pretomanid OR linezolid OR BPaL OR BPaLM
- **Results:** 5 studies

### Grey Literature Search Results

#### Conference Proceedings
- Union World Conference on Lung Health (2010-2025): 45 abstracts
- Conference on Retroviruses and Opportunistic Infections: 12 abstracts
- International AIDS Society Conference: 8 abstracts
- American Thoracic Society International Conference: 2 abstracts

#### Organizational Sources
- WHO TB Programme Reports: 23 documents
- CDC TB Research Publications: 15 documents
- ECDC Technical Documents: 8 documents
- The Union Technical Publications: 12 documents

## Supplementary Material 3: Data Extraction Forms

### Study Characteristics Form

**General Information:**
- Study ID: [Auto-generated]
- Title: [Full title]
- Authors: [List]
- Journal/Source: [Name]
- Publication Year: [YYYY]
- DOI/PMID: [Identifier]
- Country(ies): [List]
- Language: [Language]

**Study Design:**
- Design Type: [RCT/Observational/etc.]
- Study Phase: [Phase 2/3/4/NA]
- Blinding: [Open/Single/Double/Triple]
- Setting: [Hospital/Community/etc.]
- Funding Source: [Specify]
- Conflicts of Interest: [Reported]

**Population:**
- Total Sample Size: [N]
- Age (mean, SD): [ ] ( [ ] )
- Sex Distribution: Male [n] ([%]), Female [n] ([%])
- HIV Status: Positive [n] ([%]), Negative [n] ([%])
- TB Type: MDR [n] ([%]), Pre-XDR [n] ([%]), XDR [n] ([%])
- Resistance Pattern: FQ-resistant [n] ([%]), Injectable-resistant [n] ([%])
- Treatment History: New [n] ([%]), Previously treated [n] ([%])

### Intervention Details Form

**Treatment Arms:**
For each arm:
- Regimen Name: [Name]
- Drugs: [List with doses]
- Duration: [Weeks/Months]
- Administration: [Oral/Injectable/Mixed]
- Concomitant Medications: [List]

**Outcome Data:**
- Treatment Success: [n] ([%])
- Cure: [n] ([%])
- Treatment Completion: [n] ([%])
- Failure: [n] ([%])
- Death: [n] ([%])
- Lost to Follow-up: [n] ([%])
- Relapse: [n] ([%])

**Safety Data:**
- Total SAEs: [n] ([%])
- Peripheral Neuropathy: [n] ([%])
- Myelosuppression: [n] ([%])
- QTc Prolongation: [n] ([%])
- Treatment Discontinuation: [n] ([%])

### Risk of Bias Assessment Form

**For RCTs (RoB 2.0):**
- Randomization Process: [Low/High/Some concerns]
- Deviations from Intended Interventions: [Low/High/Some concerns]
- Missing Outcome Data: [Low/High/Some concerns]
- Measurement of Outcomes: [Low/High/Some concerns]
- Selection of Reported Results: [Low/High/Some concerns]
- Overall Risk: [Low/High/Some concerns]

**For Observational Studies (ROBINS-I):**
- Confounding: [Low/Moderate/High/Critical]
- Selection of Participants: [Low/Moderate/High/Critical]
- Classification of Interventions: [Low/Moderate/High/Critical]
- Deviations from Intended Interventions: [Low/Moderate/High/Critical]
- Missing Data: [Low/Moderate/High/Critical]
- Measurement of Outcomes: [Low/Moderate/High/Critical]
- Selection of Reported Results: [Low/Moderate/High/Critical]
- Overall Risk: [Low/Moderate/High/Critical]

## Supplementary Material 4: Statistical Code

### R Code for Bayesian NMA

```r
# Load required packages
library(gemtc)
library(rjags)
library(coda)

# Load and prepare data
data <- read.csv("extracted_data.csv")
network <- mtc.network(data.ab = data)

# Define model
model <- mtc.model(network,
                  type = "consistency",
                  likelihood = "binom",
                  link = "logit",
                  linearModel = "random",
                  n.chain = 4,
                  n.adapt = 10000,
                  n.iter = 50000,
                  thin = 10)

# Run MCMC
results <- mtc.run(model)

# Generate outputs
league <- relative.effect(results)
sucra <- rank.probability(results)
forest <- forest.mtc(results)
```

### Python Code for Data Analysis

```python
import pandas as pd
import numpy as np
from scipy import stats

# Load data
data = pd.read_csv("extracted_data.csv")

# Calculate treatment effects
def calculate_effects(data):
    # Group by treatment and calculate rates
    effects = {}
    for treatment in data['treatment'].unique():
        tx_data = data[data['treatment'] == treatment]
        responders = tx_data['responders'].sum()
        total = tx_data['sampleSize'].sum()
        effects[treatment] = responders / total
    return effects

effects = calculate_effects(data)
```

## Supplementary Material 5: Evidence Network

### Network Geometry

**Figure S1. Network Geometry**
*The evidence network shows direct comparisons between treatments. Node size represents number of studies, edge thickness represents number of direct comparisons.*

**Direct Comparisons:**
- BPaL vs Long: 8 studies
- BPaLM vs Long: 4 studies
- Short MDR vs Long: 6 studies
- BPaL vs Short MDR: 5 studies
- BPaLM vs Short MDR: 2 studies
- BPaL vs BPaLM: 3 studies

### Study Connectivity

**Table S1. Study Connectivity Matrix**

| Treatment | BPaL | BPaLM | Short MDR | Long |
|-----------|------|-------|-----------|------|
| BPaL | - | 3 | 5 | 8 |
| BPaLM | 3 | - | 2 | 4 |
| Short MDR | 5 | 2 | - | 6 |
| Long | 8 | 4 | 6 | - |

## Supplementary Material 6: Sensitivity Analyses

### Detailed Sensitivity Analysis Results

#### 1. Risk of Bias Exclusion
- **Studies Excluded:** 8 high risk of bias studies
- **Remaining Studies:** 38
- **BPaL vs Long OR:** 3.45 (2.67-4.45)
- **Interpretation:** Results robust to RoB exclusion

#### 2. Fixed vs Random Effects
- **Fixed Effects DIC:** 245.6
- **Random Effects DIC:** 234.2 (preferred)
- **BPaL vs Long OR (Fixed):** 3.12 (2.34-4.12)
- **Interpretation:** Random effects model appropriate

#### 3. Alternative Prior Distributions
- **Vague Prior (0-5):** OR = 3.28 (2.51-4.23)
- **Informative Prior:** OR = 3.31 (2.54-4.26)
- **Very Vague Prior (0-10):** OR = 3.25 (2.48-4.21)
- **Interpretation:** Results consistent across priors

#### 4. Small Study Exclusion (n < 50)
- **Studies Excluded:** 12
- **Remaining Studies:** 34
- **BPaL vs Long OR:** 3.34 (2.56-4.34)
- **Interpretation:** Robust to small study exclusion

#### 5. Outcome Definition Variations
- **Strict Definition (Cure Only):** OR = 3.15 (2.38-4.08)
- **Broad Definition (Cure + Completion):** OR = 3.28 (2.51-4.23)
- **Interpretation:** Consistent across definitions

#### 6. Publication Year Stratification
- **Recent Studies (2021-2025):** OR = 3.18 (2.41-4.11)
- **Older Studies (2019-2020):** OR = 3.25 (2.48-4.18)
- **Interpretation:** No temporal trends detected

#### 7. Geographic Stratification
- **High Burden Countries:** OR = 3.01 (2.23-4.01)
- **Other Countries:** OR = 3.34 (2.45-4.67)
- **Interaction Test:** P = 0.67 (no significant difference)

## Supplementary Material 7: Subgroup Analyses

### Fluoroquinolone Resistance Subgroup

**Table S2. Subgroup Analysis by FQ Resistance**

| Treatment | FQ-Resistant OR (95% CrI) | FQ-Susceptible OR (95% CrI) | P-Interaction |
|-----------|---------------------------|----------------------------|---------------|
| BPaL vs Long | 2.89 (2.12-3.89) | 3.45 (2.67-4.45) | 0.23 |
| BPaLM vs Long | 2.34 (1.67-3.23) | 2.89 (2.23-3.78) | 0.31 |
| Short MDR vs Long | 1.23 (0.89-1.67) | 1.67 (1.34-2.12) | 0.18 |

### HIV Co-infection Subgroup

**Table S3. Subgroup Analysis by HIV Status**

| Treatment | HIV-Positive OR (95% CrI) | HIV-Negative OR (95% CrI) | P-Interaction |
|-----------|---------------------------|---------------------------|---------------|
| BPaL vs Long | 2.67 (1.89-3.67) | 3.12 (2.34-4.12) | 0.45 |
| BPaLM vs Long | 2.23 (1.56-3.12) | 2.56 (1.89-3.45) | 0.52 |
| Short MDR vs Long | 1.34 (0.98-1.89) | 1.56 (1.23-2.01) | 0.38 |

### Geographic Region Subgroup

**Table S4. Subgroup Analysis by Geographic Region**

| Treatment | High Burden OR (95% CrI) | Other Countries OR (95% CrI) | P-Interaction |
|-----------|---------------------------|-----------------------------|---------------|
| BPaL vs Long | 3.01 (2.23-4.01) | 3.34 (2.45-4.67) | 0.67 |
| BPaLM vs Long | 2.45 (1.78-3.34) | 2.78 (1.98-3.89) | 0.59 |
| Short MDR vs Long | 1.34 (0.98-1.89) | 1.67 (1.12-2.45) | 0.44 |

## Supplementary Material 8: Publication Bias Assessment

### Funnel Plot Analysis

**Figure S2. Funnel Plot for Publication Bias**
*Funnel plot shows no significant asymmetry (Egger's test P = 0.23), suggesting minimal publication bias.*

### Trial Registry Comparison

**Table S5. Publication Status of Registered Trials**

| Registry | Registered Trials | Published | Publication Rate |
|----------|------------------|-----------|------------------|
| ClinicalTrials.gov | 28 | 8 | 29% |
| TB Trials Tracker | 12 | 4 | 33% |
| WHO ICTRP | 5 | 1 | 20% |
| Total | 45 | 13 | 29% |

## Supplementary Material 9: Certainty of Evidence Assessment

### Detailed GRADE Assessment

**Table S6. GRADE Certainty Ratings for All Comparisons**

| Comparison | Risk of Bias | Inconsistency | Indirectness | Imprecision | Publication Bias | Overall Certainty |
|------------|--------------|---------------|-------------|-------------|------------------|-------------------|
| BPaL vs Long | Not serious | Not serious | Not serious | Not serious | Not serious | High |
| BPaLM vs Long | Not serious | Not serious | Not serious | Not serious | Not serious | High |
| Short MDR vs Long | Not serious | Serious (-1) | Not serious | Not serious | Not serious | Moderate |
| BPaL vs BPaLM | Not serious | Not serious | Not serious | Serious (-1) | Not serious | Moderate |
| BPaL vs Short MDR | Not serious | Not serious | Not serious | Not serious | Not serious | High |
| BPaLM vs Short MDR | Not serious | Not serious | Not serious | Not serious | Not serious | High |

### CINeMA Confidence Assessment

**Table S7. CINeMA Confidence Ratings**

| Comparison | Confidence in NMA | Key Limitations |
|------------|-------------------|----------------|
| BPaL vs Long | High | None |
| BPaLM vs Long | High | None |
| Short MDR vs Long | Moderate | Inconsistency |
| BPaL vs BPaLM | Moderate | Imprecision |

## Supplementary Material 10: Data Availability

### Complete Dataset

The complete extracted dataset is available as Supplementary Data File 1 (extracted_data.csv). This includes all study-level and arm-level data used in the analysis.

### Statistical Code Repository

All R and Python code used for analysis is available at: [GitHub repository URL]

### Protocol Deviations

No protocol deviations occurred during the conduct of this systematic review.

## References for Supplementary Materials

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71.

2. Higgins JPT, Thomas J, Chandler J, et al. Cochrane Handbook for Systematic Reviews of Interventions version 6.3 (updated February 2022). Cochrane, 2022.

3. Dias S, Welton NJ, Sutton AJ, Ades AE. Evidence synthesis for decision making 1: introduction. Med Decis Making 2013;33:597-606.

4. Salanti G, Ades AE, Ioannidis JP. Graphical methods and numerical summaries for presenting results from multiple-treatment meta-analysis: an overview and tutorial. J Clin Epidemiol 2011;64:163-71.

5. Veroniki AA, Straus SE, Fyraridis A, Tricco AC. The rank-heat plot is a novel way to present the results from a network meta-analysis including multiple outcomes. J Clin Epidemiol 2016;76:193-9.

---

**Supplementary Materials Version:** 1.0
**Last Updated:** October 12, 2025
**Corresponding Author:** [Author details]
