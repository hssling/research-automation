# Data Extraction Forms and Guidelines
## Childhood Pneumonia Prevention Systematic Review

## Overview
Data extraction will be performed by two independent reviewers using standardized forms. All extractions will be cross-verified and discrepancies resolved by arbitration.

## Study Characteristics Extraction Form

### Basic Study Information
- **Study ID:** [Auto-generated unique identifier]
- **Author:** [Lead author surname, year]
- **Publication Year:** [Year of publication]
- **Journal:** [Full journal name]
- **DOI/PMID:** [Digital Object Identifier and/or PubMed ID]
- **Funding Source:** [Industry/ government/ NGO/ self-funded]
- **Conflict of Interest:** [Declared conflicts]

### Study Design
- **Design Type:**
  - [ ] Individual RCTs
  - [ ] Cluster RCTs
  - [ ] Quasi-experimental (pre-post)
  - [ ] Interrupted time series
  - [ ] Controlled before-after
  - [ ] Population cohort
  - [ ] Other: ________
- **Total Sample Size:** [Total number of subjects]
- **Unit of Randomization:**
  - [ ] Individual
  - [ ] Cluster (specify: ________)
- **Follow-up Duration:** [Time period from intervention to outcome]

### Geographic and Setting Information
- **Country/Countries:** [List all countries]
- **WHO Region:** [List all WHO regions: AFR/ AMR/ EMR/ EUR/ SEAR/ WPR]
- **Income Classification:**
  - [ ] Low-income countries (LICs)
  - [ ] Middle-income countries (MICs) - Lower/Upper
  - [ ] High-income countries (HICs)
- **Urban/Rural:** [Predominantly urban/rural/mixed]

### Population Characteristics
- **Target Population:** [Children under 5/6-9 years/mixed]
- **Age Range:** [Mean age/age range in months/years]
- **Sex Distribution:** [Male % / Female %]
- **HIV Status:** [HIV-exposed % / HIV-unexposed % / Unknown]
- **Malnutrition:** [Prevalence of moderate/severe malnutrition %]

### Intervention Details
- **PCV Product:**
  - [ ] PCV7
  - [ ] PCV10
  - [ ] PCV13
  - [ ] PCV15
  - [ ] PCV20
  - [ ] Mixed/Other
- **PCV Schedule:**
  - [ ] 2+1 (2 infant doses + booster)
  - [ ] 3+0 (3 infant doses, no booster)
  - [ ] 3+1 (3 infant doses + booster)
  - [ ] Catch-up program
  - [ ] Other: ________
- **Dose Timing:** [Specific ages in months for each dose]
- **Vaccine Coverage Achieved:** [Actual vs planned coverage %]

### Co-interventions
- **Influenza Vaccination:**
  - [ ] Seasonal influenza vaccine co-administered
  - [ ] Separate influenza vaccination program
  - [ ] No influenza vaccine
- **Type:** [Live attenuated/Inactivated/TIV]
- **Schedule:** [Annual/seasonal timing]

### Outcome Measures
**Primary Outcomes:**
1. **Radiologically Confirmed Pneumonia**
   - Numerator (events): ________
   - Denominator (person-years): ________
   - Incidence rate per 1000 child-years: ________
   - Risk Ratio (95% CI): ________

2. **All-cause LRTI Hospitalizations**
   - Numerator (events): ________
   - Denominator (person-years): ________
   - Incidence rate per 1000 child-years: ________
   - Risk Ratio (95% CI): ________

3. **All-cause Mortality**
   - Numerator (deaths): ________
   - Denominator (population): ________
   - Mortality rate per 1000 child-years: ________
   - Risk Ratio (95% CI): ________

**Secondary Outcomes:**
1. **Clinical Pneumonia Episodes**
   - Definition used: ________
   - Numerator/Denominator: ________
   - Effect measure: ________

2. **Serotype-specific Pneumonia**
   - Vaccine serotypes: ________
   - Non-vaccine serotypes: ________
   - Rate ratios: ________

### Statistical Methods
- **Effect Measures:** [RR/OR/HR/Incidence rate ratio]
- **Confounders Adjusted For:** [List variables]
- **Matching Used:** [Yes/No - method: ________]
- **Propensity Scores:** [Yes/No - method: ________]

### Risk of Bias Assessment (Cochrane RoB 2.0 for RCTs)
- **Overall Risk:** [Low/Moderate/High/Critical]
- **Domain 1 - Randomization:** [Low/High/Unclear]
- **Domain 2 - Deviations:** [Low/High/Unclear]
- **Domain 3 - Missing Data:** [Low/High/Unclear]
- **Domain 4 - Measurement:** [Low/High/Unclear]
- **Domain 5 - Selection:** [Low/High/Unclear]

### Risk of Bias Assessment (ROBINS-I for Non-RCTs)
- **Overall Risk:** [Low/Moderate/Serious/Critical/No Information]
- **Confounding:** [Low/Moderate/Serious/Critical]
- **Selection:** [Low/Moderate/Serious/Critical]
- **Intervention:** [Low/Moderate/Serious/Critical]
- **Missing Data:** [Low/Moderate/Serious/Critical]
- **Measurement:** [Low/Moderate/Serious/Critical]
- **Reporting:** [Low/Moderate/Serious/Critical]

### GRADE Assessment
- **Certainty Level:** [High/Moderate/Low/Very Low]
- **Reasons for Downgrading:**
  - [ ] Risk of bias
  - [ ] Indirectness
  - [ ] Inconsistency
  - [ ] Imprecision
  - [ ] Publication bias

---

## Quality Control Checklist

### Completeness Check
- [ ] All form fields completed
- [ ] Data logically consistent
- [ ] Effect estimates correctly calculated
- [ ] Units properly reported

### Cross-verification
- [ ] Two reviewers extracted data independently
- [ ] Percentage agreement calculated (>90% required)
- [ ] Discrepancies resolved by third reviewer
- [ ] Final dataset imported to analysis software

### Data Integrity
- [ ] No transcription errors
- [ ] Appropriate rounding applied
- [ ] Confidence intervals correctly reported
- [ ] Missing data clearly marked

---

## Data Dictionary

### Variable Naming Convention
- Study characteristics: `study_*`
- Population: `pop_*`
- Intervention: `int_*`
- Outcomes: `out_*`
- Quality: `qual_*`

### File Structure
```
03_data_extraction/
├── forms/
│   ├── study_characteristics.csv
│   ├── interventions.csv
│   └── outcomes.csv
├── raw_data/
│   ├── extracted_data_combined.csv
│   └── quality_assessments.csv
└── analysis_ready/
    ├── pairwise_data.csv
    └── network_data.csv
