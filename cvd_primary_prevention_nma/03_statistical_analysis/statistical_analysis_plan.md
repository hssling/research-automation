# Statistical Analysis Plan: CVD Primary Prevention Network Meta-Analysis

## Registration
**SAP Version**: 1.0
**Date**: October 12, 2025
**Previous Versions**: None

## Analysis Team
- **Lead Statistician**: Dr James Wilson, PhD
- **Senior Statistician**: Dr Sarah Kim, PhD
- **Statistical Programmer**: Dr Michael Chen, MD
- **Quality Control**: Dr Priya Sharma, MD, PhD

## Overview

This statistical analysis plan (SAP) details the planned analyses for the network meta-analysis comparing pharmacological and lifestyle interventions for primary prevention of cardiovascular disease. The SAP follows established guidelines for network meta-analysis and ensures transparency and reproducibility.

## Analysis Objectives

### Primary Objectives
1. **All-Cause Mortality**: Compare interventions for all-cause mortality reduction
2. **MACE Prevention**: Compare interventions for major adverse cardiovascular events
3. **Safety Assessment**: Compare safety profiles across interventions

### Secondary Objectives
1. **Individual Outcomes**: MI, stroke, revascularization, heart failure
2. **Subgroup Effects**: Age, diabetes, CKD, risk level interactions
3. **Component Effects**: Individual drug contributions
4. **Cost-Effectiveness**: Network meta-regression for economic analysis

## Data Sources and Structure

### Included Studies
- **Expected Range**: 25-40 randomized controlled trials
- **Total Participants**: 150,000-300,000
- **Treatment Arms**: 8-12 different interventions
- **Comparisons**: 15-25 direct comparisons

### Data Format
- **Primary Format**: Arm-level data (preferred)
- **Alternative Format**: Contrast-level data (if arm-level unavailable)
- **Time-to-Event**: Extracted as log hazard ratios with standard errors
- **Dichotomous**: Events and sample sizes per arm

### Missing Data Handling
1. **Contact Authors**: For critical missing information
2. **Statistical Imputation**: Multiple imputation for minor missing data
3. **Sensitivity Analysis**: Assess impact of missing data assumptions

## Statistical Methods

### Network Meta-Analysis Framework

#### Model Specification
**Bayesian Random-Effects NMA Model:**

For dichotomous outcomes:
```
logit(p_ik) = μ_i + δ_ik
δ_ik ~ Normal(θ_ik, σ²_ik)
θ_ik = {
  0 if i = k (reference treatment)
  θ_k if treatment k is compared to i
}
θ_k ~ Normal(0, τ²)
τ ~ Uniform(0, 5)
```

Where:
- `p_ik` = probability of event in arm k of study i
- `μ_i` = study-specific baseline effect
- `δ_ik` = random effect for arm k in study i
- `θ_k` = relative treatment effect for treatment k
- `τ` = between-study heterogeneity

#### Software Implementation
- **Primary Software**: R with GeMTC package
- **Alternative Software**: R with netmeta package
- **Validation Software**: JAGS for Bayesian model verification
- **Sensitivity Analysis**: STATA network meta-analysis routines

#### Convergence Assessment
- **Gelman-Rubin Statistic**: PSRF < 1.1 for all parameters
- **Effective Sample Size**: ESS > 1000 for key parameters
- **Trace Plots**: Visual inspection for convergence
- **Brooks-Gelman Multivariate Statistic**: < 1.2

### Effect Measures

#### Primary Effect Measures
- **Dichotomous Outcomes**: Odds ratios (OR) with 95% credible intervals
- **Time-to-Event Outcomes**: Hazard ratios (HR) with 95% credible intervals
- **Continuous Outcomes**: Mean differences (MD) with 95% credible intervals

#### Treatment Rankings
- **SUCRA Values**: Surface under the cumulative ranking curve
- **Rank Probabilities**: Probability of being best, second-best, etc.
- **Rankograms**: Visual representation of ranking probabilities

### Heterogeneity Assessment

#### Global Heterogeneity
- **τ² Estimation**: Between-study variance with 95% CrI
- **I² Interpretation**:
  - 0-25%: Low heterogeneity
  - 25-50%: Moderate heterogeneity
  - 50-75%: Substantial heterogeneity
  - >75%: Considerable heterogeneity

#### Local Inconsistency
- **Node-Splitting**: Compare direct and indirect evidence
- **Loop-Specific Approach**: Assess inconsistency in closed loops
- **Design Inconsistency**: Compare different study designs

#### Sources of Heterogeneity
1. **Clinical Diversity**: Different populations and settings
2. **Methodological Diversity**: Different study designs and conduct
3. **Statistical Heterogeneity**: Random variation in treatment effects

### Transitivity Assessment

#### Effect Modifiers
1. **Baseline Risk**: ASCVD risk score distribution
2. **Age Distribution**: Mean age and age range
3. **Comorbidities**: Diabetes, CKD prevalence
4. **Intervention Intensity**: Drug doses and lifestyle intensity
5. **Follow-up Duration**: Treatment and follow-up length

#### Transitivity Evaluation
- **Box Plots**: Distribution of effect modifiers across comparisons
- **Statistical Tests**: Chi-square tests for categorical modifiers
- **Visual Assessment**: Side-by-side comparisons of study characteristics

## Network Meta-Regression

### Covariates for Investigation

#### Continuous Covariates
1. **Baseline LDL-C**: Mean LDL-C levels across studies
2. **ASCVD Risk Score**: Mean 10-year risk estimates
3. **Age**: Mean participant age
4. **BMI**: Mean body mass index
5. **Blood Pressure**: Mean systolic/diastolic pressure

#### Categorical Covariates
1. **Diabetes Prevalence**: Percentage with diabetes
2. **CKD Prevalence**: Percentage with chronic kidney disease
3. **Statin Intensity**: High-intensity vs moderate-intensity
4. **Study Design**: RCT vs other designs
5. **Geographic Region**: North America, Europe, Asia, Other

### Meta-Regression Models

#### Univariate Models
```
θ_k = β₀ + β₁ × Covariate_k + ε_k
ε_k ~ Normal(0, τ²)
```

#### Multivariate Models
```
θ_k = β₀ + β₁ × Covariate₁_k + β₂ × Covariate₂_k + ε_k
ε_k ~ Normal(0, τ²)
```

#### Interaction Models
```
θ_k = β₀ + β₁ × Covariate_k + β₂ × Treatment_k + β₃ × Covariate_k × Treatment_k + ε_k
```

### Interpretation of Meta-Regression
- **β Coefficients**: Change in log odds ratio per unit change in covariate
- **95% CrI**: Uncertainty in meta-regression coefficients
- **Model Fit**: DIC comparison between models
- **Residual Heterogeneity**: τ² reduction after covariate adjustment

## Component Network Meta-Analysis

### Drug Components
1. **Statins**: Atorvastatin, rosuvastatin, simvastatin, pravastatin
2. **PCSK9 Inhibitors**: Evolocumab, alirocumab
3. **Ezetimibe**: As monotherapy or add-on
4. **Anti-hypertensives**: ACEI, ARB, CCB, diuretics
5. **Anti-platelet**: Aspirin, other anti-platelet agents
6. **Lifestyle**: Exercise, diet, smoking cessation, weight management

### Additive Component Models
```
θ_k = β₁ × Statin_k + β₂ × PCSK9_k + β₃ × Ezetimibe_k + β₄ × Lifestyle_k + ε_k
```

### Interaction Assessment
- **Synergistic Effects**: Combined effects greater than additive
- **Antagonistic Effects**: Combined effects less than additive
- **Dose-Response**: Effect modification by component intensity

## Subgroup Analyses

### Predefined Subgroups

#### Risk-Based Subgroups
1. **ASCVD Risk <10%**: Lower risk primary prevention
2. **ASCVD Risk 10-20%**: Intermediate risk
3. **ASCVD Risk >20%**: High risk primary prevention

#### Age-Based Subgroups
1. **Age <75 years**: Standard adult population
2. **Age ≥75 years**: Elderly population
3. **Age <55 years**: Younger adults

#### Comorbidity Subgroups
1. **Diabetes Present**: Diabetic population
2. **Diabetes Absent**: Non-diabetic population
3. **CKD Present**: Chronic kidney disease
4. **CKD Absent**: Normal renal function

#### Treatment-Based Subgroups
1. **Statin-Naive**: No prior statin therapy
2. **Statin-Experienced**: Prior statin use
3. **High-Intensity Statin**: Atorvastatin 40-80mg, rosuvastatin 20-40mg
4. **Moderate-Intensity Statin**: Lower doses

### Subgroup Analysis Methods
- **Within-Network**: Separate NMA for each subgroup
- **Interaction Tests**: Statistical tests for subgroup differences
- **Meta-Regression**: Covariate adjustment for subgroup factors

## Sensitivity Analyses

### Primary Sensitivity Analyses
1. **Fixed-Effects Model**: Compare with random-effects results
2. **Alternative Priors**: Different prior distributions for τ
3. **Study Quality**: Exclude high risk of bias studies
4. **Sample Size**: Exclude small studies (<100 participants per arm)
5. **Follow-up Duration**: Stratify by median follow-up time

### Outcome Definition Sensitivity
1. **MACE Variations**: Different composite outcome definitions
2. **Mortality Definitions**: Cardiovascular vs all-cause mortality
3. **Safety Outcomes**: Different adverse event classifications
4. **Time Windows**: Different follow-up periods

### Methodological Sensitivity
1. **Software Comparison**: GeMTC vs netmeta vs STATA
2. **Model Specification**: Different link functions
3. **Imputation Methods**: Different approaches to missing data
4. **Heterogeneity Models**: Alternative heterogeneity distributions

## Publication Bias and Small Study Effects

### Assessment Methods
1. **Funnel Plots**: Visual assessment of small study effects
2. **Contour-Enhanced Funnel Plots**: Distinguish publication bias from heterogeneity
3. **Egger's Test**: Statistical test for funnel plot asymmetry
4. **Trim and Fill**: Adjustment for potential missing studies

### Adjustment Approaches
1. **Selection Models**: Statistical adjustment for publication bias
2. **Regression Models**: Study size as covariate in meta-regression
3. **Sensitivity Analysis**: Assess impact of potential bias

## Certainty of Evidence

### GRADE for Network Meta-Analysis

#### Direct Evidence Rating
- **Risk of Bias**: Study limitations assessment
- **Inconsistency**: Unexplained heterogeneity
- **Indirectness**: Differences in populations/interventions
- **Imprecision**: Wide confidence intervals
- **Publication Bias**: Suspected small study effects

#### Indirect Evidence Rating
- **First-Order Loops**: Single source of indirectness
- **Higher-Order Loops**: Multiple sources of indirectness
- **Network Geometry**: Strength of indirect connections

#### Overall Certainty
- **High**: Further research very unlikely to change confidence
- **Moderate**: Further research likely to impact confidence
- **Low**: Further research very likely to impact confidence
- **Very Low**: Very uncertain about the estimate

## Software and Computing

### Primary Analysis Environment
- **R Version**: 4.0+
- **Required Packages**:
  - GeMTC: Main NMA package
  - netmeta: Alternative NMA package
  - gemtc: GeMTC interface
  - rjags: JAGS interface
  - coda: MCMC diagnostics
  - ggplot2: Visualization
  - metafor: Meta-analysis utilities

### Computing Requirements
- **RAM**: 16GB minimum for large networks
- **Storage**: 50GB for data and results
- **Processing Time**: 4-8 hours for full analysis
- **Parallel Processing**: Multiple cores for faster computation

### Reproducible Analysis
- **R Markdown**: Complete analysis workflow
- **Version Control**: Git for code versioning
- **Docker**: Containerized analysis environment
- **Data Archiving**: Complete dataset preservation

## Data Management

### Data Structure
- **Study-Level Data**: One row per study
- **Arm-Level Data**: One row per treatment arm
- **Contrast-Level Data**: One row per comparison
- **Covariate Data**: Study-level effect modifiers

### Data Validation
- **Range Checks**: Plausible value ranges
- **Consistency Checks**: Internal consistency within studies
- **Completeness Checks**: Missing data identification
- **Quality Checks**: Automated data quality assessment

### Data Security
- **De-identification**: Remove personal identifiers
- **Access Control**: Restricted access to sensitive data
- **Backup**: Regular data backups
- **Archiving**: Long-term data preservation

## Reporting and Presentation

### Analysis Results
1. **Network Geometry**: Evidence network visualization
2. **Treatment Effects**: League tables and forest plots
3. **Ranking Results**: SUCRA values and rankograms
4. **Heterogeneity**: Global and local heterogeneity assessment
5. **Inconsistency**: Node-splitting and heat plots
6. **Meta-Regression**: Covariate effect plots
7. **Component Analysis**: Component effect estimates
8. **Subgroup Analysis**: Subgroup-specific results
9. **Sensitivity Analysis**: Robustness assessment
10. **Publication Bias**: Funnel plots and tests

### Publication-Quality Figures
- **Resolution**: 300 DPI minimum
- **Format**: TIFF or PNG for publications
- **Color Scheme**: Color-blind friendly palettes
- **Font Size**: 12pt minimum for readability
- **Aspect Ratio**: Appropriate for journal formats

### Tables
- **League Tables**: All pairwise comparisons
- **Study Characteristics**: Complete study information
- **Risk of Bias**: Detailed bias assessment
- **GRADE Tables**: Certainty of evidence summaries

## Quality Assurance

### Analysis Validation
1. **Code Review**: Independent review of analysis code
2. **Results Verification**: Double-checking of key results
3. **Software Comparison**: Cross-validation with different software
4. **Sensitivity Analysis**: Comprehensive robustness assessment

### Documentation
1. **Analysis Code**: Complete R scripts with comments
2. **Data Files**: All data in analysis-ready format
3. **Results Files**: All intermediate and final results
4. **Log Files**: Complete analysis logs

### Peer Review
1. **Statistical Review**: Independent statistical review
2. **Clinical Review**: Clinical interpretation validation
3. **Methodological Review**: NMA methodology assessment

## Timeline and Milestones

### Analysis Phases
1. **Phase 1: Data Preparation** (Weeks 1-2)
   - Data cleaning and validation
   - Network geometry assessment
   - Transitivity evaluation

2. **Phase 2: Primary Analysis** (Weeks 3-4)
   - Main NMA models
   - Heterogeneity and inconsistency assessment
   - Treatment ranking analysis

3. **Phase 3: Advanced Analysis** (Weeks 5-6)
   - Meta-regression models
   - Component network meta-analysis
   - Subgroup analyses

4. **Phase 4: Sensitivity Analysis** (Weeks 7-8)
   - Comprehensive sensitivity analyses
   - Publication bias assessment
   - Certainty of evidence rating

5. **Phase 5: Reporting** (Weeks 9-10)
   - Results interpretation
   - Manuscript preparation
   - Supplementary materials

### Quality Gates
1. **Data Quality Gate**: Complete data validation
2. **Analysis Quality Gate**: Convergence and model fit assessment
3. **Results Quality Gate**: Clinical plausibility and consistency
4. **Reporting Quality Gate**: Complete documentation and transparency

## Amendments and Updates

### SAP Amendments
Any changes to the SAP will be:
- Documented with rationale and date
- Approved by senior statistician
- Reported in final publication
- Version controlled

### Version History
- **Version 1.0**: Initial SAP (October 12, 2025)
- **Future Versions**: Documented changes with rationale

## References

1. **GeMTC Package**: van Valkenhoef G, et al. Automating network meta-analysis. Research Synthesis Methods 2012;3(4):285-299.
2. **Netmeta Package**: Rücker G, et al. Network meta-analysis using frequentist methods. R package version 1.2-1. 2020.
3. **Cochrane Handbook**: Higgins JPT, et al. Cochrane Handbook for Systematic Reviews of Interventions version 6.3. 2022.
4. **GRADE for NMA**: Brignardello-Petersen R, et al. Advances in the GRADE approach to rate the certainty in estimates from a network meta-analysis. J Clin Epidemiol 2018;93:36-44.

## Signatures

### Statistical Analysis Team
- **Lead Statistician**: ________________________ Date: ________
- **Senior Statistician**: ________________________ Date: ________
- **Principal Investigator**: ________________________ Date: ________

---

**SAP Version**: 1.0
**Last Updated**: October 12, 2025
**Contact**: Dr James Wilson (james.wilson@cvd-prevention-nma.org)
