# Statistical Analysis Protocol for Drug-Resistant Tuberculosis Network Meta-Analysis

## Overview

This document outlines the detailed statistical analysis plan for the network meta-analysis comparing BPaL/BPaLM regimens versus alternative treatments for drug-resistant tuberculosis.

## Analysis Objectives

### Primary Objectives
1. **Estimate relative treatment effects** for all pairwise comparisons between BPaL, BPaLM, short MDR regimens, and individualized long regimens
2. **Rank treatments** using Surface Under the Cumulative Ranking Curve (SUCRA) analysis
3. **Evaluate component effects** using component network meta-analysis to assess individual drug contributions

### Secondary Objectives
1. **Assess heterogeneity** and inconsistency in the treatment network
2. **Conduct sensitivity analyses** to evaluate robustness of findings
3. **Perform subgroup analyses** by resistance patterns and patient characteristics

## Statistical Methods

### 1. Network Meta-Analysis Framework

#### Model Specification
- **Approach:** Bayesian random-effects network meta-analysis
- **Likelihood:** Binomial likelihood for dichotomous outcomes
- **Link Function:** Logit link (equivalent to logistic regression)
- **Effect Measure:** Odds ratios (OR) with 95% credible intervals (CrI)

#### Prior Distributions
- **Treatment Effects:** Vague priors: d_k ~ Normal(0, 1000) for k = 2, ..., K
- **Heterogeneity:** τ ~ Uniform(0, 5) (vague but proper prior)
- **Alternative Prior:** τ ~ Half-Normal(0, 1) (weakly informative)

#### Markov Chain Monte Carlo (MCMC) Settings
- **Number of Chains:** 4 independent chains
- **Burn-in Period:** 10,000 iterations
- **Sampling Iterations:** 50,000 iterations
- **Thinning Interval:** 10 iterations
- **Total Samples:** 20,000 samples per chain (80,000 total)

### 2. Component Network Meta-Analysis

#### Model Structure
Treatments modeled as combinations of components:
- **Bedaquiline (BDQ)**
- **Pretomanid (Pa)**
- **Linezolid (LZD)**
- **Moxifloxacin (MFX)**
- **Short regimen backbone (SHORT)**
- **Long regimen backbone (LONG)**

#### Component Effects Model
```
d_k = Σ β_c * I(component_c in treatment_k) + Σ Σ β_{c1,c2} * I(both in treatment_k)
```

Where:
- β_c = main effect of component c
- β_{c1,c2} = interaction effect between components c1 and c2
- I() = indicator function

### 3. Outcome Definitions and Analysis

#### Primary Outcomes

**Treatment Success:**
- Definition: Cure + treatment completion (WHO definition)
- Analysis: Network meta-analysis of proportions
- Model: Random-effects binomial NMA

**Relapse:**
- Definition: Bacteriological recurrence within 12 months of treatment completion
- Analysis: Time-to-relapse analysis using Kaplan-Meier methods
- Model: Cox proportional hazards NMA (if sufficient data)

**Serious Adverse Events:**
- Definition: CTCAE Grade 3-4 events or requiring treatment discontinuation
- Analysis: Per-patient incidence (accounting for multiple events)
- Model: Random-effects binomial NMA

#### Secondary Outcomes

**Sputum Culture Conversion:**
- Time Point: 2 months (8 weeks)
- Analysis: Network meta-analysis of proportions
- Model: Random-effects binomial NMA

**Treatment Discontinuation:**
- Definition: Permanent discontinuation due to adverse events
- Analysis: Network meta-analysis of proportions
- Model: Random-effects binomial NMA

### 4. Heterogeneity and Inconsistency Assessment

#### Between-Study Heterogeneity
- **Measure:** τ² (variance of random effects)
- **Interpretation:** τ² < 0.04 (low), 0.04-0.16 (moderate), >0.16 (high)
- **Comparison:** I² statistic for direct comparisons

#### Inconsistency Assessment
- **Global Inconsistency:** Comparison of deviance information criterion (DIC) between consistency and inconsistency models
- **Local Inconsistency:** Node-splitting approach for individual comparisons
- **Threshold:** P < 0.10 indicates potential inconsistency

### 5. Ranking Analysis

#### SUCRA Calculation
```
SUCRA_k = (1/K) * Σ_{j≠k} P(rank_k ≤ rank_j)
```

Where:
- K = number of treatments
- P(rank_k ≤ rank_j) = probability that treatment k ranks better than treatment j

#### Interpretation
- SUCRA = 100%: Treatment always ranks first
- SUCRA = 0%: Treatment always ranks last
- SUCRA ≈ 50%: Treatment ranks average

### 6. Subgroup Analyses

#### Predefined Subgroups
1. **Fluoroquinolone Resistance:**
   - Resistant vs susceptible
   - Separate NMA models for each subgroup

2. **HIV Co-infection:**
   - HIV-positive vs HIV-negative
   - Interaction analysis if sufficient data

3. **Geographic Region:**
   - High TB burden countries vs others
   - Meta-regression if sufficient studies

4. **Study Design:**
   - RCTs vs observational studies
   - Separate analyses with comparison

### 7. Sensitivity Analyses

#### Primary Sensitivity Analyses
1. **Risk of Bias:** Exclude high risk of bias studies
2. **Model Specification:** Fixed-effect vs random-effects models
3. **Prior Distributions:** Alternative prior specifications
4. **Small Studies:** Exclude studies with n < 50

#### Secondary Sensitivity Analyses
1. **Outcome Definition:** Alternative definitions of treatment success
2. **Publication Year:** Stratify by publication year
3. **Geographic Region:** Region-specific analyses
4. **Imputation:** Different approaches for missing data

### 8. Meta-Regression

#### Covariates for Investigation
- Publication year (to assess temporal trends)
- Geographic region (high vs low TB burden)
- HIV prevalence in study population
- Proportion with fluoroquinolone resistance
- Study design (RCT vs observational)

#### Model Specification
```
logit(p_ik) = μ_i + θ_k + Σ β_m * x_m + ε_ik
```

Where:
- θ_k = treatment effect for treatment k
- β_m = regression coefficient for covariate m
- x_m = study-level covariate m

### 9. Publication Bias Assessment

#### Methods
1. **Funnel Plot Analysis:** Visual inspection of asymmetry
2. **Egger's Test:** Statistical test for funnel plot asymmetry
3. **Trim and Fill:** Adjustment for potential missing studies
4. **Comparison with Trial Registries:** Assessment of unpublished trials

### 10. Certainty of Evidence Assessment

#### GRADE Approach for NMA
- **Starting Rating:** High for RCTs, Moderate for observational studies
- **Downgrading Factors:**
  - Risk of bias (-1 or -2)
  - Inconsistency (-1)
  - Indirectness (-1)
  - Imprecision (-1)
  - Publication bias (-1)

#### CINeMA Framework
- **Confidence in Network Meta-Analysis**
- **Judgments:** High, Moderate, Low, Very Low confidence

## Software and Implementation

### Primary Software
- **R Statistical Software:** Version 4.2.0 or higher
- **GeMTC Package:** For network meta-analysis
- **rjags Package:** For Bayesian modeling with JAGS
- **gemtc Package:** For GeMTC integration

### Secondary Software
- **JAGS:** Version 4.3.0 or higher (Bayesian engine)
- **STATA:** Version 17 or higher (validation analyses)
- **Python:** For data processing and visualization

### Model Validation
- **Convergence Diagnostics:**
  - Gelman-Rubin statistic (R̂ < 1.1)
  - Effective sample size (n_eff > 100 per chain)
  - Monte Carlo standard error < 5% of posterior standard deviation

- **Model Fit:**
  - Deviance information criterion (DIC)
  - Posterior predictive p-values
  - Comparison of observed vs replicated data

## Data Management

### Data Structure
- **Unit of Analysis:** Treatment arm within study
- **Format:** Long format with one row per treatment arm
- **Variables:** Study ID, treatment, responders, sample size

### Missing Data Handling
- **Primary Approach:** Available case analysis
- **Sensitivity Analysis:** Multiple imputation if appropriate
- **Reporting:** Clear documentation of missing data patterns

### Data Validation
- **Range Checks:** Ensure outcomes between 0 and 1
- **Consistency Checks:** Verify treatment assignments
- **Duplicate Detection:** Identify potential duplicate publications

## Reporting and Presentation

### League Table Format
```
Comparison    OR (95% CrI)    Interpretation
BPaL vs BPaLM 1.23 (0.89-1.67) No difference
BPaL vs Short 2.45 (1.78-3.12) Favors BPaL
...
```

### Visualization Standards
- **Forest Plots:** Treatment effects with 95% CrI
- **Rank Heat Plots:** Toxicity vs efficacy trade-offs
- **Network Graphs:** Study connectivity visualization
- **SUCRA Bar Plots:** Treatment ranking visualization

### Numerical Presentation
- **Odds Ratios:** Report to 2 decimal places
- **Credible Intervals:** Report to appropriate precision
- **Probabilities:** Report as percentages to 1 decimal place

## Quality Assurance

### Analysis Validation
- **Code Review:** All analysis code reviewed by statistician
- **Reproducibility:** Random seed set for reproducible results
- **Version Control:** All scripts maintained in version control system

### Result Verification
- **Cross-Software Validation:** Compare results with STATA if possible
- **Manual Calculations:** Verify simple calculations manually
- **Sensitivity Confirmation:** Ensure sensitivity analyses produce expected changes

## Timeline and Milestones

### Analysis Phases
1. **Data Preparation:** Week 1-2
2. **Model Development:** Week 3-4
3. **Primary Analysis:** Week 5-6
4. **Sensitivity Analyses:** Week 7-8
5. **Report Generation:** Week 9-10

### Quality Checks
- **Interim Review:** Preliminary results reviewed at Week 6
- **Final Review:** Complete analysis reviewed before manuscript writing
- **External Validation:** Consider external statistical review if needed

## References

1. Dias S, Sutton AJ, Ades AE, Welton NJ. Evidence synthesis for decision making 2: a generalized linear modeling framework for pairwise and network meta-analysis of randomized controlled trials. Med Decis Making. 2013;33(5):607-617.

2. Caldwell DM, Ades AE, Higgins JP. Simultaneous comparison of multiple treatments: combining direct and indirect evidence. BMJ. 2005;331(7521):897-900.

3. Welton NJ, Caldwell D, Adamopoulos E, Vedhara K. Mixed treatment comparison with multiple outcomes reported inconsistently across studies. Res Synth Methods. 2012;3(4):354-361.

4. Dias S, Welton NJ, Caldwell DM, Ades AE. Checking consistency in mixed treatment comparison meta-analysis. Stat Med. 2010;29(7-8):932-944.

## Version History

- **Version:** 1.0
- **Date:** October 12, 2025
- **Authors:** [Your Name], Principal Investigator; [Statistician], Co-Investigator
- **Approval:** [Date of approval]

## Amendments

Any deviations from this protocol will be documented with rationale and reported in the final publication.

---

**Protocol Status:** Final
**Effective Date:** October 12, 2025
**Review Date:** Before analysis implementation
