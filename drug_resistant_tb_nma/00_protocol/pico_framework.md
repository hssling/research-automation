# PICO Framework for Drug-Resistant Tuberculosis NMA

## Population (P)

### Inclusion Criteria
- **Age:** Adults and adolescents ≥10 years old
- **Disease:** Bacteriologically confirmed tuberculosis with:
  - Multidrug resistance (MDR-TB): Resistance to at least isoniazid and rifampicin
  - Rifampicin resistance (RR-TB): Resistance to rifampicin (with or without isoniazid resistance)
- **Drug Resistance Pattern:**
  - With or without fluoroquinolone resistance
  - With or without second-line injectable resistance
  - Mono-resistance, poly-resistance, MDR-TB, or pre-XDR/XDR-TB
- **HIV Status:** HIV-positive or HIV-negative patients
  - If HIV-positive: Must be on appropriate antiretroviral therapy
- **Diagnostic Confirmation:** Microbiological confirmation required (culture, molecular tests)
- **Treatment History:** New or previously treated cases

### Exclusion Criteria
- **Age:** Children <10 years old (different pharmacokinetics and limited data)
- **Disease:** Drug-sensitive tuberculosis
- **Comorbidities:** Severe comorbidities that contraindicate study drugs
- **Pregnancy:** Pregnant or breastfeeding women (limited safety data)
- **Extrapolmonary TB:** Isolated extrapulmonary disease without pulmonary involvement

## Interventions (I) and Comparators (C)

### Intervention 1: BPaL Regimen
**Components:**
- Bedaquiline (BDQ): 400mg daily for 2 weeks, then 200mg three times per week for 22 weeks
- Pretomanid (Pa): 200mg daily for 26 weeks
- Linezolid (LZD): 600mg daily for 26 weeks (or reduced dose in some protocols)

**Duration:** 26 weeks (6 months)
**Administration:** All oral medications

### Intervention 2: BPaLM Regimen
**Components:**
- Bedaquiline (BDQ): 400mg daily for 2 weeks, then 200mg three times per week for 8 weeks
- Pretomanid (Pa): 200mg daily for 8 weeks
- Linezolid (LZD): 600mg daily for 8 weeks
- Moxifloxacin (MFX): 400mg daily for 8 weeks

**Duration:** 8 weeks (2 months)
**Administration:** All oral medications

### Comparator 1: Short MDR Regimen
**Components (WHO-recommended):**
- Intensive phase (4-6 months): Kanamycin + moxifloxacin + prothionamide + clofazimine + high-dose isoniazid + pyridoxine + ethambutol
- Continuation phase (5 months): Moxifloxacin + clofazimine + prothionamide + ethambutol

**Duration:** 9-11 months total
**Administration:** Mix of oral and injectable drugs

### Comparator 2: Individualized Long Regimens
**Components:** Customized based on drug susceptibility testing
- Typically includes 4-6 drugs from: bedaquiline, delamanid, linezolid, clofazimine, cycloserine, fluoroquinolones, second-line injectable drugs, prothionamide, ethambutol, high-dose isoniazid, pyridoxine

**Duration:** 18-24 months
**Administration:** Mix of oral and injectable drugs

## Outcomes (O)

### Primary Outcomes

#### 1. Treatment Success
**Definition:** Proportion of patients achieving cure or treatment completion
- **Cure:** Sustained sputum culture conversion with no evidence of failure
- **Treatment Completion:** Completed treatment according to protocol without evidence of failure but no microbiological confirmation of cure

**Time Point:** End of treatment
**Measurement:** WHO definitions and criteria
**Importance:** Primary efficacy endpoint for TB treatment

#### 2. Relapse Rate
**Definition:** Recurrent TB disease within 12 months after treatment completion
**Time Point:** 12 months post-treatment
**Measurement:** Bacteriological confirmation of recurrent disease
**Importance:** Key indicator of treatment durability

#### 3. Serious Adverse Events (SAEs)
**Definition:** Adverse events requiring treatment discontinuation or hospitalization

**Specific SAEs of Interest:**
- **Peripheral Neuropathy:** Linezolid-related toxicity
  - Definition: Grade 2+ neuropathy (interfering with activities of daily living)
  - Measurement: Clinical assessment, nerve conduction studies if available

- **Myelosuppression:**
  - Anemia: Hemoglobin <8 g/dL or requiring transfusion
  - Thrombocytopenia: Platelets <50,000/μL or requiring intervention
  - Neutropenia: ANC <1000/μL

- **QTc Prolongation:**
  - QTc >500ms on ECG
  - QTc prolongation requiring treatment discontinuation
  - Arrhythmic events (torsades de pointes, ventricular tachycardia)

**Time Point:** Throughout treatment and follow-up
**Measurement:** CTCAE criteria, laboratory monitoring, ECG monitoring
**Importance:** Primary safety endpoint

### Secondary Outcomes

#### 1. Sputum Culture Conversion
**Definition:** Time to first negative sputum culture
**Time Point:** 2 months (8 weeks) after treatment initiation
**Measurement:** Liquid culture or molecular methods
**Importance:** Early bacteriological response indicator

#### 2. Treatment Discontinuation
**Definition:** Permanent discontinuation of any study drug due to adverse events
**Time Point:** Throughout treatment period
**Measurement:** Protocol-defined criteria
**Importance:** Treatment tolerability indicator

#### 3. Mortality
**Definition:**
- All-cause mortality
- TB-related mortality
**Time Point:** End of treatment and 12-month follow-up
**Measurement:** Vital status assessment
**Importance:** Critical clinical outcome

#### 4. Acquired Drug Resistance
**Definition:** Development of additional drug resistance during treatment
**Time Point:** End of treatment
**Measurement:** Drug susceptibility testing
**Importance:** Treatment failure indicator

## Outcome Hierarchy and Prioritization

### Primary Outcome Hierarchy
1. **Treatment Success** (highest priority - definitive efficacy measure)
2. **Relapse Rate** (critical for long-term efficacy assessment)
3. **Serious Adverse Events** (essential for safety evaluation)

### Safety Outcome Hierarchy
1. **QTc Prolongation** (cardiac safety - potentially life-threatening)
2. **Myelosuppression** (hematological toxicity - can be severe)
3. **Peripheral Neuropathy** (neurological toxicity - impacts quality of life)

## Measurement Methods and Timing

### Efficacy Outcomes
- **Bacteriological:** Monthly sputum cultures during treatment, quarterly during follow-up
- **Clinical:** Monthly clinical assessment during treatment
- **Definition Standardization:** WHO definitions for TB treatment outcomes

### Safety Outcomes
- **Laboratory Monitoring:**
  - Complete blood count: Weekly for first 8 weeks, then monthly
  - Liver function tests: Monthly
  - Renal function: Monthly
  - ECG: Baseline, week 2, month 1, then monthly

- **Clinical Monitoring:**
  - Neuropathy assessment: Monthly using standardized scales
  - Visual acuity and color vision: Monthly (ethambutol optic neuritis)
  - Psychiatric symptoms: Monthly (cycloserine, fluoroquinolones)

### Follow-up Schedule
- **During Treatment:** Monthly assessments
- **End of Treatment:** Comprehensive evaluation
- **Post-Treatment:** 6, 12, 18, 24 months follow-up

## Outcome Assessment Challenges and Solutions

### Challenge 1: Outcome Definition Variability
**Problem:** Different studies may use varying definitions for "cure" and "treatment completion"
**Solution:** Standardize using WHO definitions; sensitivity analysis excluding studies with non-standard definitions

### Challenge 2: Loss to Follow-up
**Problem:** High loss to follow-up in TB studies may bias results
**Solution:** Intention-to-treat analysis; assess loss to follow-up as outcome; sensitivity analysis assuming different outcomes for lost patients

### Challenge 3: Competing Risks
**Problem:** Mortality may compete with treatment success/failure assessment
**Solution:** Competing risk analysis for mortality; composite outcomes where appropriate

## Statistical Considerations for Outcomes

### Dichotomous Outcomes
- Treatment success, relapse, mortality, adverse events
- Analysis: Odds ratios, risk ratios, risk differences
- Consideration: Zero events in some arms

### Time-to-Event Outcomes
- Time to sputum conversion, time to relapse
- Analysis: Hazard ratios, median time to event
- Consideration: Censoring, competing risks

### Continuous Outcomes
- QTc interval changes, hematological parameters
- Analysis: Mean differences, standardized mean differences
- Consideration: Baseline adjustment, repeated measures

## Outcome-Specific Analysis Plans

### Treatment Success
- Primary analysis: Network meta-analysis of proportions
- Subgroup analysis: By drug resistance pattern, HIV status
- Sensitivity analysis: By study design, risk of bias

### Relapse Rate
- Analysis: Time-to-relapse using Kaplan-Meier methods
- Consideration: Requires long-term follow-up data
- Competing risk: Death during follow-up period

### Serious Adverse Events
- Analysis: Per-patient incidence (some patients may experience multiple events)
- Timing: Early vs late adverse events
- Attribution: Definitely related, probably related, possibly related

## References for Outcome Definitions
1. WHO. Definitions and reporting framework for tuberculosis – 2013 revision (updated December 2014)
2. Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0
3. International Conference on Harmonisation (ICH) E2A Guideline for Clinical Safety Data Management

---

**Document Version:** 1.0
**Last Updated:** October 12, 2025
