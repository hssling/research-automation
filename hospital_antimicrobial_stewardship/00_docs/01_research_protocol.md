# Hospital Antimicrobial Stewardship: A Network Meta-Analysis Protocol

## 1. Background and Rationale

Antimicrobial resistance (AMR) represents one of the most significant global health threats of the 21st century. Hospital antimicrobial stewardship programs (ASPs) are critical interventions designed to optimize antibiotic use, improve patient outcomes, and reduce the emergence of resistant organisms. Despite the proliferation of ASPs, there remains uncertainty about which specific stewardship interventions are most effective for reducing AMR rates, mortality, and antibiotic consumption in acute-care hospital settings.

Previous systematic reviews have examined individual stewardship strategies, but few have employed network meta-analysis (NMA) to simultaneously compare multiple interventions and rank their effectiveness. This study aims to fill this gap by conducting a comprehensive NMA of stewardship models in acute-care hospitals.

## 2. Objectives

### Primary Objective
To rank the comparative effectiveness of different hospital antimicrobial stewardship models for:
- Reducing antimicrobial resistance (AMR) rates
- Reducing mortality
- Reducing antibiotic consumption (measured as days of therapy (DOT) or defined daily doses (DDD) per 1,000 patient-days)

### Secondary Objectives
- To assess the impact of stewardship interventions on Clostridium difficile infection (CDI) rates
- To evaluate the incidence of multidrug-resistant organisms (MDROs)
- To examine potential moderators of treatment effect (ICU vs ward setting, baseline AMR ecology, diagnostic technology availability)

## 3. Methods

### 3.1 Study Design
This will be a systematic review with network meta-analysis (NMA) of randomized controlled trials (RCTs), cluster-randomized controlled trials (cluster-RCTs), and interrupted time series (ITS) studies with multiple arms comparing different antimicrobial stewardship interventions in acute-care hospitals.

### 3.2 Population
Adult patients (≥18 years) in acute-care hospitals, including both general wards and intensive care units (ICUs).

### 3.3 Interventions
We will compare the following stewardship interventions:
1. **Pre-authorization**: Requiring approval before certain antibiotics can be prescribed
2. **Prospective audit and feedback**: Regular review of antibiotic prescriptions with feedback to prescribers
3. **Rapid diagnostic pathways**: Use of rapid diagnostic tests to guide antibiotic therapy
4. **Computerized decision support systems (CDSS) and e-prescribing**: Electronic systems to guide antibiotic prescribing
5. **Education and bundle interventions**: Educational programs, guidelines, and care bundles
6. **Combinations of the above interventions**

Comparisons will be made against usual care (no specific stewardship intervention).

### 3.4 Outcomes

#### Primary Outcomes
- **Mortality**: All-cause mortality (in-hospital or 30-day)
- **CDI incidence**: Clostridium difficile infection rates
- **MDRO incidence**: Incidence of multidrug-resistant organisms (MRSA, VRE, ESBL-producing organisms, CRE)
- **Process measures**: Days of therapy (DOT) or defined daily doses (DDD) per 1,000 patient-days

#### Secondary Outcomes
- **Antibiotic costs**: Economic impact of interventions
- **Length of stay**: Hospital length of stay
- **Adverse events**: Unintended consequences of stewardship interventions

### 3.5 Search Strategy

#### Electronic Databases
- **PubMed/MEDLINE** (via NCBI)
- **CENTRAL** (Cochrane Central Register of Controlled Trials)
- **Embase** (if available)
- **Web of Science**

#### Grey Literature and Other Sources
- **WHO GLASS reports** (for contextual information on AMR epidemiology)
- **PROSPERO** (for ongoing/registered protocols)
- **ClinicalTrials.gov** (for ongoing trials)
- **Conference abstracts** from major infectious diseases meetings

#### Search Terms
We will use a combination of controlled vocabulary (MeSH terms) and free-text terms:

**Population**: "hospital" OR "acute care" OR "inpatient" OR "ICU" OR "intensive care" OR "ward"

**Intervention**: "antimicrobial stewardship" OR "antibiotic stewardship" OR "preauthorization" OR "prior authorization" OR "prospective audit" OR "audit and feedback" OR "rapid diagnostic" OR "CDSS" OR "computerized decision support" OR "e-prescribing" OR "education" OR "guideline" OR "bundle"

**Outcomes**: "mortality" OR "CDI" OR "Clostridium difficile" OR "MDRO" OR "multidrug resistant" OR "MRSA" OR "VRE" OR "ESBL" OR "CRE" OR "antibiotic consumption" OR "DOT" OR "DDD" OR "days of therapy" OR "defined daily dose"

**Study Design**: "randomized controlled trial" OR "RCT" OR "cluster RCT" OR "interrupted time series" OR "ITS" OR "quasi-experimental"

### 3.6 Study Selection

#### Inclusion Criteria
- **Study Design**: RCTs, cluster-RCTs, controlled ITS studies
- **Population**: Adult patients in acute-care hospitals
- **Interventions**: Any of the specified stewardship interventions
- **Comparisons**: Active intervention vs usual care, or head-to-head comparisons
- **Outcomes**: At least one primary outcome reported
- **Publication**: Full-text articles available
- **Language**: English language publications

#### Exclusion Criteria
- **Study Design**: Uncontrolled before-after studies, single-arm studies
- **Population**: Pediatric populations, long-term care facilities, outpatient settings
- **Interventions**: Non-stewardship interventions (e.g., infection control only)
- **Outcomes**: No relevant outcomes reported
- **Publication Type**: Editorials, commentaries, narrative reviews

#### Screening Process
1. Title and abstract screening (two independent reviewers)
2. Full-text review (two independent reviewers)
3. Discrepancies resolved by consensus or third reviewer
4. PRISMA flow diagram will be created

### 3.7 Data Extraction

#### Study Characteristics
- Publication details (authors, year, journal)
- Study design (RCT, cluster-RCT, ITS)
- Setting (country, hospital type, ward vs ICU)
- Sample size and duration
- Baseline AMR ecology

#### Intervention Details
- Specific stewardship components
- Implementation details
- Comparator description
- Co-interventions

#### Outcome Data
- Effect estimates with measures of uncertainty
- Time points of measurement
- Adjustment variables

#### Quality Assessment
- **RCTs/cluster-RCTs**: Cochrane Risk of Bias 2.0 tool
- **ITS studies**: EPOC quality criteria for ITS designs

### 3.8 Risk of Bias Assessment
Two reviewers will independently assess risk of bias. Disagreements will be resolved through discussion or consultation with a third reviewer.

### 3.9 Data Synthesis

#### Conventional Meta-Analysis
- Pairwise meta-analysis for direct comparisons where available
- Random-effects model (DerSimonian-Laird)
- Assessment of heterogeneity (I², τ²)

#### Network Meta-Analysis
- **Design-adjusted NMA**: Accounting for different study designs (RCT vs quasi-experimental)
- **Bayesian framework**: Using Markov Chain Monte Carlo (MCMC) methods
- **Software**: R packages (netmeta, gemtc) or STATA (network command)
- **Model fit**: Comparison of consistency and inconsistency models

#### Assessment of Model Fit and Convergence
- Deviance information criterion (DIC)
- Posterior mean residual deviance
- Brooks-Gelman-Rubin diagnostics
- Effective sample sizes

### 3.10 Assessment of Inconsistency
- Global inconsistency tests
- Node-splitting method for local inconsistency
- Design-by-treatment interaction test

### 3.11 Transitivity Assessment
- Evaluation of effect modifiers across comparisons
- Graphical presentations of study characteristics
- Statistical tests for transitivity violation

### 3.12 Subgroup and Moderator Analyses
- **ICU vs ward setting**
- **Baseline AMR ecology** (high vs low resistance settings)
- **Diagnostic technology availability**
- **Geographic region**
- **Study quality**

### 3.13 Sensitivity Analyses
- Exclusion of high risk-of-bias studies
- Exclusion of quasi-experimental studies
- Different meta-analytic models
- Alternative outcome measures

### 3.14 Ranking of Interventions
- Surface under the cumulative ranking curve (SUCRA)
- P-scores
- Mean ranks

### 3.15 Publication Bias
- Comparison-adjusted funnel plots
- Egger's test for asymmetry
- Contour-enhanced funnel plots

## 4. Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| **Phase 1: Setup** | Month 1 | Protocol development, PROSPERO registration, tool development |
| **Phase 2: Search** | Months 2-3 | Literature search, screening, full-text review |
| **Phase 3: Extraction** | Months 4-5 | Data extraction, quality assessment |
| **Phase 4: Analysis** | Months 6-7 | Statistical analysis, NMA, sensitivity analyses |
| **Phase 5: Writing** | Months 8-9 | Manuscript writing, revision, submission |
| **Phase 6: Publication** | Months 10-12 | Journal submission, peer review, publication |

## 5. Ethical Considerations

This study will use only published data and does not involve primary data collection from human subjects. No ethical approval is required.

## 6. Dissemination Plan

- Publication in a high-impact medical journal
- Presentation at relevant conferences (ECCMID, IDWeek)
- Registration of protocol and results on PROSPERO
- Data sharing through supplementary materials

## 7. References

[References to be added as the review progresses]

## 8. Amendments

Any protocol amendments will be documented with rationale and dated in an appendix.

---

**Protocol Version**: 1.0
**Date**: October 13, 2025
**Principal Investigator**: [To be determined]
**Review Team**: [To be determined]
