# Statistical Analysis Plan for Drug-Resistant Tuberculosis NMA

## 1. Introduction

### 1.1 Study Objectives
This statistical analysis plan (SAP) details the analysis of data from a systematic review and network meta-analysis comparing BPaL/BPaLM regimens versus alternative treatments for drug-resistant tuberculosis.

### 1.2 Analysis Scope
- **Primary Analysis:** Bayesian random-effects network meta-analysis
- **Component Analysis:** Component network meta-analysis for drug effects
- **Sensitivity Analyses:** Comprehensive robustness assessment
- **Subgroup Analyses:** Predefined subgroup investigations

## 2. Data Description

### 2.1 Data Sources
- **Primary Data:** Extracted data from included studies
- **Data Format:** CSV files with study-level and arm-level data
- **Key Variables:**
  - Study identifiers (study_id, title, authors, year)
  - Treatment arms (treatment_name, sample_size, responders)
  - Outcome measures (treatment_success, relapse, adverse_events)
  - Study characteristics (design, country, risk_of_bias)

### 2.2 Data Structure
```
Study_ID | Treatment | Responders | Sample_Size | Outcome_Type | Study_Year | Country
Study001 | BPaL      | 45         | 50          | Success      | 2020       | South Africa
Study001 | Short_MDR | 38         | 50          | Success      | 2020       | South Africa
Study002 | BPaLM     | 89         | 100         | Success      | 2021       | Multiple
```

## 3. Analysis Populations

### 3.1 Intention-to-Treat Population
- **Definition:** All patients randomized/assigned to treatment arms
- **Handling Missing Data:** Available case analysis as primary approach
- **Sensitivity Analysis:** Multiple imputation for missing outcomes

### 3.2 Per-Protocol Population
- **Definition:** Patients completing treatment according to protocol
- **Use:** Sensitivity analysis for treatment success outcomes
- **Exclusions:** Major protocol violations, loss to follow-up

## 4. Outcome Measures

### 4.1 Primary Outcomes

#### Treatment Success
- **Measure:** Dichotomous (success vs failure)
- **Definition:** WHO criteria (cure + treatment completion)
- **Time Point:** End of treatment
- **Analysis:** Network meta-analysis of proportions

#### Relapse
- **Measure:** Dichotomous (relapse vs no relapse)
- **Definition:** Bacteriological recurrence within 12 months
- **Time Point:** 12 months post-treatment
- **Analysis:** Time-to-event analysis if sufficient data

#### Serious Adverse Events
- **Measure:** Dichotomous (SAE vs no SAE)
- **Definition:** CTCAE Grade 3-4 or treatment discontinuation
- **Time Point:** Throughout treatment period
- **Analysis:** Per-patient analysis (accounting for multiple events)

### 4.2 Secondary Outcomes

#### Sputum Culture Conversion
- **Measure:** Dichotomous (converted vs not converted)
- **Definition:** First negative culture
- **Time Point:** 2 months (8 weeks)
- **Analysis:** Network meta-analysis of proportions

#### Treatment Discontinuation
- **Measure:** Dichotomous (discontinued vs completed)
- **Definition:** Permanent discontinuation due to adverse events
- **Time Point:** Throughout treatment period
- **Analysis:** Network meta-analysis of proportions

## 5. Statistical Methods

### 5.1 Network Meta-Analysis

#### Model Specification
```r
# Random-effects NMA model
model <- mtc.model(network,
                  type = "consistency",
                  likelihood = "binom",
                  link = "logit",
                  linearModel = "random",
                  n.chain = 4,
                  n.adapt = 10000,
                  n.iter = 50000,
                  thin = 10)
```

#### Convergence Criteria
- Gelman-Rubin statistic (R̂) < 1.1 for all parameters
- Effective sample size > 100 per chain
- Monte Carlo standard error < 5% of posterior SD

### 5.2 Component Network Meta-Analysis

#### Component Definition
- **Bedaquiline:** Present in BPaL, BPaLM
- **Pretomanid:** Present in BPaL, BPaLM
- **Linezolid:** Present in BPaL, BPaLM
- **Moxifloxacin:** Present in BPaLM, Short_MDR
- **Short Backbone:** Present in Short_MDR
- **Long Backbone:** Present in Long_Individualized

#### Interaction Terms
- BDQ × Pa, BDQ × LZD, Pa × LZD (first-order interactions)
- Higher-order interactions if model fit suggests

### 5.3 Heterogeneity Assessment

#### Between-Study Variance
- **Estimation:** τ² from random-effects model
- **Interpretation:**
  - τ² < 0.04: Low heterogeneity
  - 0.04 ≤ τ² ≤ 0.16: Moderate heterogeneity
  - τ² > 0.16: High heterogeneity

#### Inconsistency Detection
- **Node-Splitting:** Compare direct and indirect evidence
- **DIC Comparison:** Consistency vs inconsistency models
- **Threshold:** P < 0.10 for significant inconsistency

### 5.4 Ranking Analysis

#### SUCRA Calculation
- **Formula:** SUCRA_k = (1/K) × Σ_{j≠k} P(rank_k ≤ rank_j)
- **Interpretation:** 100% = always best, 0% = always worst
- **Visualization:** SUCRA bar plots and rank heat plots

## 6. Sensitivity Analyses

### 6.1 Primary Sensitivity Analyses

#### 1. Risk of Bias Exclusion
```r
# Exclude high risk of bias studies
low_rob_data <- subset(data, risk_of_bias != "High")
# Refit NMA model
```

#### 2. Fixed vs Random Effects
```r
# Compare model fit
model_fixed <- mtc.model(network, linearModel = "fixed")
model_random <- mtc.model(network, linearModel = "random")
# Compare DIC values
```

#### 3. Alternative Priors
```r
# Test different heterogeneity priors
vague_prior <- mtc.hy.prior("std.dev", "dunif", 0, 5)
informative_prior <- mtc.hy.prior("std.dev", "dhnorm", 0, 0.322^2)
```

#### 4. Small Study Exclusion
```r
# Exclude studies with n < 50 per arm
large_studies <- subset(data, sample_size >= 50)
```

### 6.2 Secondary Sensitivity Analyses

#### 1. Outcome Definition Variations
- Strict definition (cure only) vs broad definition (cure + completion)
- Different time points for culture conversion

#### 2. Geographic Stratification
- High TB burden countries vs other countries
- Regional subgroup analyses

#### 3. Publication Year Effects
- Stratify by median publication year
- Meta-regression for temporal trends

## 7. Subgroup Analyses

### 7.1 Predefined Subgroups

#### Fluoroquinolone Resistance
- **Subgroups:** FQ-resistant vs FQ-susceptible
- **Analysis:** Separate NMA models for each subgroup
- **Interaction Test:** Test for subgroup differences

#### HIV Co-infection
- **Subgroups:** HIV-positive vs HIV-negative
- **Analysis:** Subgroup-specific NMA if sufficient data
- **Covariate:** HIV prevalence as meta-regression covariate

#### Geographic Region
- **Definition:** WHO high TB burden countries vs others
- **Analysis:** Meta-regression with region as covariate

#### Study Design
- **Subgroups:** RCTs vs observational studies
- **Analysis:** Separate analyses with comparison of results

### 7.2 Subgroup Analysis Methods

#### Separate Models
```r
# For each subgroup level
subgroup_data <- subset(data, subgroup_variable == level)
subgroup_network <- mtc.network(data.ab = subgroup_data)
subgroup_model <- mtc.model(subgroup_network, ...)
```

#### Meta-Regression
```r
# Continuous covariates
meta_reg_model <- mtc.model(network,
                           linearModel = "random",
                           regressor = list(coefficient = "shared"))
```

## 8. Missing Data Handling

### 8.1 Primary Approach
- **Available Case Analysis:** Use observed data only
- **Reporting:** Document missing data patterns by study and outcome

### 8.2 Sensitivity Analysis
- **Multiple Imputation:** If missing data > 10% for key outcomes
- **Worst-Case Scenario:** Assume poor outcomes for missing data
- **Best-Case Scenario:** Assume good outcomes for missing data

## 9. Model Validation

### 9.1 Convergence Assessment
- **Gelman-Rubin Diagnostic:** R̂ < 1.1 for all parameters
- **Autocorrelation:** Review autocorrelation plots
- **Effective Sample Size:** n_eff > 100 per chain

### 9.2 Model Fit Assessment
- **Deviance Information Criterion (DIC):** Compare alternative models
- **Posterior Predictive Checks:** Compare observed vs replicated data
- **Leverage Plots:** Identify influential studies

### 9.3 Software Validation
- **Cross-Software Comparison:** Validate key results in STATA
- **Manual Calculations:** Verify simple pairwise comparisons
- **Code Review:** Statistical review of all analysis code

## 10. Presentation of Results

### 10.1 Effect Measures
- **Odds Ratios:** Primary effect measure for dichotomous outcomes
- **Credible Intervals:** 95% CrI for all estimates
- **Probability Statements:** P(best), P(better than reference)

### 10.2 League Table Format
```
Comparison          OR (95% CrI)        Interpretation
BPaL vs BPaLM       1.23 (0.89-1.67)    No significant difference
BPaL vs Short MDR   2.45 (1.78-3.12)    Significantly favors BPaL
BPaL vs Long        3.21 (2.45-4.18)    Significantly favors BPaL
```

### 10.3 Visualization Standards
- **Forest Plots:** Treatment effects with confidence intervals
- **Network Graphs:** Study connectivity and evidence flow
- **SUCRA Plots:** Treatment ranking visualizations
- **Component Effects:** Forest plots of individual drug effects

## 11. Interpretation Guidelines

### 11.1 Clinical Significance
- **Minimal Important Difference:** OR > 1.5 or OR < 0.67
- **Context:** Consider baseline risk and absolute effects
- **Trade-offs:** Balance efficacy vs safety outcomes

### 11.2 Statistical Significance
- **Bayesian Interpretation:** Based on posterior probabilities
- **Thresholds:** P > 0.975 for beneficial, P < 0.025 for harmful
- **Credible Intervals:** Exclude null value for significance

### 11.3 Certainty Assessment
- **GRADE for NMA:** Rate confidence in each comparison
- **CINeMA Framework:** Structured assessment of NMA confidence
- **Limitations:** Downgrade for bias, inconsistency, imprecision

## 12. Quality Assurance

### 12.1 Analysis Documentation
- **Analysis Log:** Record all analysis decisions and rationale
- **Code Comments:** Comprehensive documentation of all scripts
- **Version Control:** Track changes to analysis code and data

### 12.2 Result Verification
- **Double Programming:** Key analyses programmed independently
- **Cross-Checking:** Manual verification of critical calculations
- **Peer Review:** Statistical review before finalizing results

### 12.3 Reproducibility
- **Random Seeds:** Set seeds for reproducible MCMC sampling
- **Data Versioning:** Track versions of analysis datasets
- **Software Versions:** Document all software and package versions

## 13. Timeline

### 13.1 Analysis Milestones
- **Data Preparation:** Complete by Week 2
- **Model Development:** Complete by Week 4
- **Primary Analysis:** Complete by Week 6
- **Sensitivity Analyses:** Complete by Week 8
- **Final Report:** Complete by Week 10

### 13.2 Quality Gates
- **Interim Review:** Preliminary results reviewed at Week 6
- **Final Review:** Complete analysis reviewed before manuscript
- **External Review:** Consider external statistical consultation

## 14. References

1. Higgins JPT, Thomas J, Chandler J, et al. Cochrane Handbook for Systematic Reviews of Interventions. 2nd Edition. Chichester (UK): John Wiley & Sons, 2019.

2. Dias S, Welton NJ, Sutton AJ, Ades AE. Evidence synthesis for decision making 1: introduction. Med Decis Making. 2013;33(5):597-606.

3. Salanti G, Ades AE, Ioannidis JP. Graphical methods and numerical summaries for presenting results from multiple-treatment meta-analysis: an overview and tutorial. J Clin Epidemiol. 2011;64(2):163-171.

4. Veroniki AA, Straus SE, Fyraridis A, Tricco AC. The rank-heat plot is a novel way to present the results from a network meta-analysis including multiple outcomes. J Clin Epidemiol. 2016;76:193-199.

## 15. Amendments

### 15.1 Protocol Amendments
Any deviations from this SAP will be:
- Documented with rationale
- Approved by study statistician
- Reported in final publication

### 15.2 Version History
- **Version 1.0:** Initial SAP (October 12, 2025)
- **Amendments:** None to date

---

**SAP Status:** Final
**Effective Date:** October 12, 2025
**Prepared by:** [Statistician Name], PhD
**Approved by:** [Principal Investigator Name], MD, PhD
