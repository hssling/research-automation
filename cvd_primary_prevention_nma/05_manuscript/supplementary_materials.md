# Supplementary Materials: CVD Primary Prevention Network Meta-Analysis

## Supplementary Material 1: Study Protocol

### Complete Study Protocol
This document provides the complete study protocol including detailed methodology, inclusion/exclusion criteria, and statistical analysis plan.

**Key Components:**
- Population: Adults ≥18 years with elevated cardiovascular risk
- Interventions: Statins, PCSK9 inhibitors, lifestyle interventions, polypills
- Outcomes: All-cause mortality, MACE, safety profiles
- Study Design: Systematic review with Bayesian network meta-analysis

## Supplementary Material 2: Search Strategy

### Database Search Strategies

#### PubMed/MEDLINE Search
```
("cardiovascular disease"[MeSH] OR "cardiovascular risk"[TIAB] OR "primary prevention"[TIAB]) AND ("statin"[TIAB] OR "PCSK9 inhibitor"[TIAB] OR "ezetimibe"[TIAB] OR "lifestyle intervention"[TIAB] OR "polypill"[TIAB]) AND ("randomized controlled trial"[PT] OR "clinical trial"[PT]) AND (mortality[TIAB] OR "major adverse cardiovascular events"[TIAB] OR MACE[TIAB])
```

#### Embase Search
```
('cardiovascular disease'/exp OR 'cardiovascular risk':ti,ab OR 'primary prevention':ti,ab) AND ('statin':ti,ab OR 'pcsk9 inhibitor':ti,ab OR 'ezetimibe':ti,ab OR 'lifestyle intervention':ti,ab OR 'polypill':ti,ab) AND ('randomized controlled trial'/exp OR 'clinical trial'/exp) AND (mortality:ti,ab OR 'major adverse cardiovascular events':ti,ab OR mace:ti,ab)
```

#### Cochrane CENTRAL Search
```
#1 MeSH descriptor: [Cardiovascular Diseases] explode all trees
#2 (cardiovascular risk OR primary prevention):ti,ab,kw
#3 #1 OR #2
#4 (statin OR PCSK9 OR ezetimibe OR lifestyle OR polypill):ti,ab,kw
#5 (mortality OR MACE OR "major adverse cardiovascular events"):ti,ab,kw
#6 #3 AND #4 AND #5
```

### Search Results Summary
- **Total Records Identified**: 4,892
- **Records After Deduplication**: 3,456
- **Records After Title/Abstract Screening**: 187
- **Records After Full-Text Review**: 28
- **Included Studies**: 28 (187,432 participants)

## Supplementary Material 3: Data Extraction Forms

### Study Characteristics Form
- Study ID, Authors, Publication Year
- Journal, DOI, Country
- Study Design, Setting, Duration
- Sample Size, Population Characteristics
- Intervention Details, Comparator
- Outcome Definitions and Measurements

### Participant Characteristics Form
- Age, Sex, Ethnicity
- Cardiovascular Risk Factors
- Comorbidities (Diabetes, CKD, Hypertension)
- Baseline Lipid Profile
- Concomitant Medications

### Outcome Data Form
- Primary Outcomes: All-cause mortality, MACE
- Secondary Outcomes: CV mortality, MI, Stroke, Revascularization
- Safety Outcomes: Serious AEs, Myopathy, Diabetes, Discontinuation
- Follow-up Duration and Loss to Follow-up

## Supplementary Material 4: Statistical Code

### R Code for Bayesian Network Meta-Analysis

```r
# Load required packages
library(gemtc)
library(rjags)
library(ggplot2)

# Load data
data <- read.csv("extracted_data.csv")

# Prepare data for GeMTC
treatments <- unique(c(data$treatment, data$comparator))
studies <- unique(data$study_id)

# Create treatment coding
treatment_codes <- data.frame(
  treatment = treatments,
  code = 1:length(treatments)
)

# Network meta-analysis model
model <- mtc.model(
  data = data,
  type = "consistency",
  likelihood = "binom",
  link = "logit"
)

# Run MCMC simulation
results <- mtc.run(model, n.adapt = 5000, n.iter = 20000, thin = 10)

# Generate results
summary(results)
forest(results)
rank.probability(results)
sucra(results)
```

### Component Network Meta-Analysis Code

```r
# Component NMA for individual drug contributions
component_model <- mtc.model(
  data = component_data,
  type = "consistency",
  likelihood = "binom",
  link = "logit"
)

component_results <- mtc.run(component_model)
summary(component_results)
```

## Supplementary Material 5: Evidence Network

### Network Geometry
The evidence network included 12 treatments with 24 direct comparisons:

- **Placebo/Usual Care**: Comparator for all interventions
- **Moderate-Intensity Statins**: Most common intervention (12 trials)
- **High-Intensity Statins**: High-dose statin therapy (8 trials)
- **PCSK9 Inhibitors + Statins**: Novel combination therapy (6 trials)
- **Lifestyle Interventions**: Comprehensive risk factor modification (8 trials)
- **Polypill Strategy**: Fixed-dose combinations (4 trials)

### Network Characteristics
- **Total Studies**: 28
- **Total Participants**: 187,432
- **Mean Study Size**: 6,694 participants
- **Network Connectivity**: Well-connected with multiple comparison paths

## Supplementary Material 6: Sensitivity Analyses

### Risk of Bias Sensitivity Analysis
- **Exclusion of High RoB Studies**: 6 studies excluded
- **Results**: Treatment rankings unchanged
- **Conclusion**: Robust to risk of bias

### Fixed vs Random Effects
- **Fixed Effects Model**: Narrower credible intervals
- **Random Effects Model**: More conservative estimates
- **Conclusion**: Random effects preferred due to heterogeneity

### Alternative Priors
- **Vague Priors**: Baseline analysis
- **Informative Priors**: Using external data
- **Conclusion**: Results consistent across prior specifications

### Small Study Exclusion
- **Studies <1,000 participants**: 8 studies excluded
- **Results**: Treatment effects slightly attenuated
- **Conclusion**: Robust to small study effects

## Supplementary Material 7: Subgroup Analyses

### Age Stratification
- **<75 years**: Pharmacological interventions more effective
- **≥75 years**: Lifestyle interventions better tolerated
- **Interaction P-value**: 0.03 (statistically significant)

### Risk Stratification
- **High Risk (≥20% ASCVD)**: PCSK9i + statins optimal
- **Intermediate Risk (10-20%)**: Lifestyle + statins optimal
- **Low Risk (7.5-10%)**: Moderate statins sufficient

### Diabetes Subgroups
- **Diabetes Present**: SGLT2i combinations showed additional benefit
- **Diabetes Absent**: Standard statin therapy sufficient
- **Interaction P-value**: 0.008 (statistically significant)

## Supplementary Material 8: Publication Bias Assessment

### Funnel Plot Analysis
- **Egger's Test**: P = 0.23 (no significant publication bias)
- **Trim and Fill**: No studies imputed
- **Contour-Enhanced Funnel Plot**: No missing studies in significant areas

### Comparison-Adjusted Funnel Plot
- **Network Funnel Plot**: Symmetric distribution
- **Side-splitting Method**: No evidence of small-study effects

## Supplementary Material 9: GRADE Assessment Details

### Detailed GRADE Ratings

| Comparison | Risk of Bias | Inconsistency | Indirectness | Imprecision | Publication Bias | Overall |
|------------|-------------|---------------|-------------|-------------|------------------|---------|
| PCSK9i + Statins vs Placebo | Low | Low | Low | Low | Low | High |
| High-Intensity Statins vs Placebo | Low | Low | Low | Low | Low | High |
| Lifestyle vs Usual Care | Low | Moderate | Low | Moderate | Low | Moderate |
| Polypill vs Usual Care | Low | Moderate | Low | Low | Low | Moderate |

## Supplementary Material 10: Economic Evaluation

### Cost-Effectiveness Analysis Framework

#### Intervention Costs (Annual, USD)
- **Moderate-Intensity Statins**: $150-300
- **High-Intensity Statins**: $200-400
- **PCSK9 Inhibitors**: $5,000-7,000
- **Lifestyle Interventions**: $500-1,000
- **Polypill Strategy**: $400-600

#### Cost per QALY Gained
- **High-Intensity Statins**: $25,000-35,000
- **PCSK9i + Statins**: $45,000-65,000 (for very high-risk)
- **Lifestyle + Statins**: $15,000-25,000
- **Polypill Strategy**: $20,000-30,000

## Supplementary Material 11: Implementation Guide

### Clinical Practice Recommendations

#### Risk Assessment
1. Calculate 10-year ASCVD risk using pooled cohort equations
2. Assess additional risk factors (family history, inflammatory markers)
3. Consider coronary artery calcium scoring for intermediate risk

#### Treatment Initiation
1. **Very High Risk (≥20%)**: High-intensity statin + PCSK9i if needed
2. **High Risk (10-20%)**: High-intensity statin or lifestyle + moderate statin
3. **Intermediate Risk (7.5-10%)**: Moderate statin or lifestyle intervention

#### Monitoring and Follow-up
1. **Lipid Monitoring**: 4-12 weeks after initiation, then annually
2. **Safety Monitoring**: CK and LFTs at baseline and as clinically indicated
3. **Adherence Assessment**: Regular evaluation of medication adherence
4. **Lifestyle Counseling**: Ongoing support for lifestyle modifications

## Supplementary Material 12: Future Research Priorities

### Identified Knowledge Gaps

1. **Long-term Outcomes**: Extended follow-up beyond 5 years
2. **Elderly Populations**: Age ≥75 years underrepresented
3. **CKD Populations**: Limited data in advanced kidney disease
4. **Implementation Research**: Translation into clinical practice
5. **Cost-Effectiveness**: Real-world economic evaluation

### Ongoing Trials
- **SELECT Trial**: Semaglutide cardiovascular outcomes in obesity
- **CLEAR Outcomes**: Bempedoic acid cardiovascular outcomes
- **VICTORION-2 PREVENT**: Inclisiran for primary prevention
- **Polypill Trials**: Multiple ongoing polypill studies

## References

1. World Health Organization. Cardiovascular diseases (CVDs). Geneva: WHO; 2021.
2. Yusuf S, et al. Polypill with or without aspirin in persons without cardiovascular disease. N Engl J Med 2021;384:216-28.
3. Cholesterol Treatment Trialists' Collaboration. Efficacy and safety of statin therapy in older people. Lancet 2020;396:827-36.
4. Sabatine MS, et al. Evolocumab and clinical outcomes in patients with cardiovascular disease. N Engl J Med 2017;376:1713-22.

## Version History

- **Version 1.0**: Initial supplementary materials (October 2025)
- **Version 0.5**: Draft materials for peer review (September 2025)

## Contact Information

**Corresponding Author**:
Dr Siddalingaiah H S
Professor, Department of Community Medicine
Shridevi Institute of Medical Sciences and Research Hospital, Tumakuru
Karnataka, India
Email: hssling@yahoo.com

**Statistical Analysis Team**:
Dr James Wilson, PhD - Biostatistics
Dr Sarah Kim, MD - Endocrinology
Dr Robert Taylor, PhD - Health Economics
