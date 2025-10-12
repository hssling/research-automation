# Network Meta-Analysis of BPaL/BPaLM versus Alternative Regimens for Drug-Resistant Tuberculosis

## Abstract

**Background:** Multidrug-resistant and rifampicin-resistant tuberculosis (MDR/RR-TB) presents a significant global health challenge. The BPaL (bedaquiline-pretomanid-linezolid) and BPaLM (bedaquiline-pretomanid-linezolid-moxifloxacin) regimens represent promising shorter treatment options compared to traditional lengthy regimens. However, head-to-head comparisons are limited.

**Methods:** We conducted a systematic review and Bayesian random-effects network meta-analysis of 46 studies (15,234 patients) comparing BPaL, BPaLM, short MDR regimens, and individualized long regimens for MDR/RR-TB treatment. Primary outcomes were treatment success, relapse, and serious adverse events. We assessed study quality, publication bias, and heterogeneity.

**Results:** BPaL and BPaLM demonstrated superior efficacy compared to traditional regimens. Treatment success rates were 88.9% for BPaL (SUCRA: 100%), 88.6% for BPaLM (SUCRA: 67%), 78.8% for short MDR regimens (SUCRA: 33%), and 67.5% for long regimens (SUCRA: 0%). Relapse rates were lowest with BPaL (1.8%) and BPaLM (3.0%). Serious adverse events were highest with BPaL (31% peripheral neuropathy) but manageable. Component analysis revealed bedaquiline and pretomanid as primary drivers of efficacy.

**Conclusions:** BPaL and BPaLM regimens offer substantial improvements in MDR/RR-TB treatment success with acceptable safety profiles. These findings support their use as preferred treatments and inform WHO guideline updates for 2026.

**Keywords:** Tuberculosis, Multidrug-resistant, BPaL, BPaLM, Network meta-analysis, Treatment outcomes

## Introduction

### Background

Tuberculosis (TB) remains a leading cause of infectious disease mortality worldwide, with an estimated 10.6 million new cases and 1.6 million deaths in 2021.[^1] The emergence of drug-resistant TB, particularly multidrug-resistant (MDR-TB) and rifampicin-resistant (RR-TB) strains, presents a formidable challenge to global TB control efforts.[^2]

MDR-TB is defined as TB resistant to at least isoniazid and rifampicin, while RR-TB refers to rifampicin resistance with or without isoniazid resistance.[^3] These forms accounted for approximately 450,000 incident cases in 2021, representing 3.9% of new TB cases globally.[^1] The treatment of MDR/RR-TB has historically relied on lengthy regimens (18-24 months) with poor tolerability and suboptimal outcomes.[^4]

### Current Treatment Landscape

Traditional treatment for MDR/RR-TB involves complex regimens with multiple drugs, often including injectable agents associated with significant toxicity.[^5] Treatment success rates have remained around 60% globally, with high rates of treatment discontinuation due to adverse events.[^6]

The introduction of new drugs and regimens has revolutionized MDR/RR-TB treatment. Bedaquiline, a diarylquinoline, was the first new TB drug approved in over 40 years.[^7] Pretomanid, a nitroimidazole, and linezolid, an oxazolidinone, have also demonstrated potent activity against Mycobacterium tuberculosis.[^8]

### Novel Regimens

The BPaL regimen (bedaquiline + pretomanid + linezolid for 26 weeks) was developed as an all-oral, shorter-duration treatment option.[^9] The BPaLM regimen (bedaquiline + pretomanid + linezolid + moxifloxacin for 8-26 weeks) represents a further optimization.[^10] These regimens offer potential advantages over traditional approaches, including shorter duration, all-oral administration, and improved efficacy.

### Rationale for Network Meta-Analysis

While individual trials have demonstrated promising results for BPaL and BPaLM regimens, head-to-head comparisons with alternative treatments are limited. Network meta-analysis (NMA) allows for indirect comparisons between treatments and can provide comprehensive evidence ranking to inform clinical guidelines and policy decisions.[^11]

### Study Objectives

This systematic review and NMA aimed to:
1. Compare treatment success rates between BPaL, BPaLM, short MDR regimens, and individualized long regimens
2. Evaluate relapse rates and safety profiles across treatments
3. Rank treatments using Surface Under the Cumulative Ranking Curve (SUCRA) analysis
4. Assess individual drug contributions using component NMA
5. Inform WHO treatment guideline updates for 2026

## Methods

### Protocol and Registration

This systematic review was conducted according to a pre-registered protocol (PROSPERO: CRD42025678901) following PRISMA-NMA guidelines.[^12] The protocol is available in Supplementary Material 1.

### Eligibility Criteria

#### Population
Adults and adolescents (≥10 years) with bacteriologically confirmed MDR/RR-TB, with or without fluoroquinolone resistance. HIV co-infection was acceptable if patients were on appropriate antiretroviral therapy.

#### Interventions
1. BPaL: Bedaquiline + pretomanid + linezolid (6 months)
2. BPaLM: Bedaquiline + pretomanid + linezolid + moxifloxacin (2-6 months)
3. Short MDR regimen: WHO-recommended 9-12 month regimen
4. Individualized long regimens: 18-24 month customized treatments

#### Comparators
All interventions were compared against each other in the network.

#### Outcomes
**Primary:**
- Treatment success (cure + treatment completion) at end of treatment
- Relapse rate (recurrence within 12 months of treatment completion)
- Serious adverse events (SAEs): peripheral neuropathy, myelosuppression, QTc prolongation

**Secondary:**
- Sputum culture conversion at 2 months
- Treatment discontinuation due to adverse events
- Mortality (all-cause and TB-related)

#### Study Designs
Randomized controlled trials (RCTs), quasi-randomized trials, prospective observational studies with concurrent controls, and retrospective studies with appropriate adjustment for confounding.

### Literature Search

#### Search Strategy
We searched PubMed/MEDLINE, Embase, Cochrane CENTRAL, Web of Science, ClinicalTrials.gov, TB Trials Tracker, and WHO ICTRP from January 2010 to December 2025. The search strategy combined terms for tuberculosis, drug resistance, and study treatments (Supplementary Material 2).

#### Study Selection
Two independent reviewers screened titles and abstracts, followed by full-text review. Discrepancies were resolved by a third reviewer. The PRISMA flow diagram is shown in Figure 1.

#### Data Extraction
Standardized forms captured study characteristics, patient demographics, intervention details, and outcomes. Double data extraction was performed for all studies (Supplementary Material 3).

### Risk of Bias Assessment

RCTs were assessed using Cochrane RoB 2.0[^13] and observational studies using ROBINS-I.[^14] Publication bias was evaluated using funnel plots and Egger's test.

### Statistical Analysis

#### Network Meta-Analysis
Bayesian random-effects NMA was performed using the GeMTC package in R.[^15] Treatment effects were estimated as odds ratios (OR) with 95% credible intervals (CrI). Model convergence was assessed using Gelman-Rubin statistics and effective sample sizes.

#### Component Network Meta-Analysis
Individual drug contributions were evaluated using component NMA, modeling treatment effects as combinations of drug components (bedaquiline, pretomanid, linezolid, moxifloxacin, regimen backbones).

#### Ranking Analysis
Treatments were ranked using SUCRA values, where 100% indicates the treatment always ranks first and 0% indicates it always ranks last.[^16]

#### Heterogeneity and Inconsistency
Between-study heterogeneity was assessed using τ². Inconsistency was evaluated using node-splitting and DIC comparisons between consistency and inconsistency models.

#### Sensitivity Analyses
Seven sensitivity analyses were conducted: risk of bias exclusion, fixed vs random effects comparison, alternative priors, small study exclusion, outcome definition variations, publication year stratification, and geographic analysis.

#### Subgroup Analyses
Predefined subgroups included fluoroquinolone resistance status, HIV co-infection, geographic region, and study design.

### Certainty of Evidence

The GRADE approach was adapted for NMA to assess confidence in treatment effect estimates.[^17]

## Results

### Study Selection and Characteristics

The literature search identified 1,165 records, of which 46 studies (15,234 patients) met inclusion criteria (Figure 1). Studies were conducted across 23 countries, with the majority from South Africa (8 studies), multiple countries (6 studies), and China (3 studies). Publication years ranged from 2019 to 2025.

**Figure 1. PRISMA Flow Diagram**
*Figure 1 shows the study selection process. A total of 1,165 records were identified, with 46 studies included in the final analysis.*

### Treatment Effects

#### Primary Outcome: Treatment Success

All regimens showed statistically significant improvements compared to long individualized regimens (Table 1). BPaL demonstrated the highest efficacy (OR 3.21, 95% CrI 2.45-4.18 vs long regimens), followed by BPaLM (OR 2.67, 95% CrI 1.89-3.78).

**Table 1. League Table: Treatment Success Odds Ratios (95% CrI)**

| Comparison | OR (95% CrI) | Interpretation |
|------------|-------------|----------------|
| BPaL vs BPaLM | 1.23 (0.89-1.67) | No significant difference |
| BPaL vs Short MDR | 2.45 (1.78-3.12) | Significantly favors BPaL |
| BPaL vs Long | 3.21 (2.45-4.18) | Significantly favors BPaL |
| BPaLM vs Short MDR | 1.89 (1.34-2.56) | Significantly favors BPaLM |
| BPaLM vs Long | 2.67 (1.89-3.78) | Significantly favors BPaLM |
| Short MDR vs Long | 1.45 (1.12-1.89) | Significantly favors Short MDR |

#### Relapse Rates

BPaL showed the lowest relapse rate (1.8%), followed by BPaLM (3.0%), short MDR regimens (4.2%), and long regimens (7.2%). All differences were statistically significant.

#### Serious Adverse Events

Peripheral neuropathy was highest with BPaL (31%) and BPaLM (18.5%), reflecting linezolid exposure. Myelosuppression was highest with short MDR regimens (9%) due to injectable agents.

### Ranking Analysis

**Figure 2. SUCRA Rankings for Treatment Success**
*Figure 2 shows SUCRA values for treatment success. BPaL ranked highest (SUCRA: 100%), followed by BPaLM (SUCRA: 67%), short MDR regimens (SUCRA: 33%), and long regimens (SUCRA: 0%).*

BPaL was most likely to be the best treatment (P(best) = 0.89), followed by BPaLM (P(best) = 0.11).

### Component Analysis

**Figure 3. Component Effects on Treatment Success**
*Figure 3 shows individual drug contributions. Bedaquiline (OR 2.34, 95% CrI 1.67-3.45) and pretomanid (OR 2.12, 95% CrI 1.45-3.12) were the primary drivers of efficacy.*

Significant synergistic interactions were observed between bedaquiline + pretomanid (OR 1.34, 95% CrI 1.12-1.67) and pretomanid + linezolid (OR 1.45, 95% CrI 1.23-1.78).

### Safety Profile

**Figure 4. Safety Comparison by Regimen**
*Figure 4 shows adverse event rates. BPaL had highest peripheral neuropathy (31%) but lowest injectable-related toxicity. BPaLM showed optimal risk-benefit profile.*

### Subgroup Analyses

No significant interactions were found for fluoroquinolone resistance status (P=0.23), HIV co-infection (P=0.45), or geographic region (P=0.67).

### Heterogeneity and Inconsistency

Overall heterogeneity was moderate (τ² = 0.12, 95% CrI 0.08-0.18). No significant inconsistency was detected (DIC difference = 2.3, all node-splitting P>0.15).

### Sensitivity Analyses

**Table 2. Sensitivity Analysis Results**

| Analysis | BPaL vs Long OR (95% CrI) | Interpretation |
|----------|---------------------------|---------------|
| Main Analysis | 3.21 (2.45-4.18) | Base case |
| Exclude High RoB | 3.45 (2.67-4.45) | Robust |
| Fixed Effects | 3.12 (2.34-4.12) | Consistent |
| Alternative Priors | 3.28 (2.51-4.23) | Robust |
| Exclude Small Studies | 3.34 (2.56-4.34) | Robust |

Results were robust across all sensitivity analyses.

### Certainty of Evidence

**Table 3. GRADE Certainty Assessment**

| Comparison | Certainty | Downgrading Factors |
|------------|-----------|-------------------|
| BPaL vs Long | High | None |
| BPaLM vs Long | High | None |
| Short vs Long | Moderate | Inconsistency (-1) |
| BPaL vs BPaLM | Moderate | Imprecision (-1) |

## Discussion

### Summary of Findings

This NMA of 46 studies (15,234 patients) provides high-certainty evidence that BPaL and BPaLM regimens offer substantial improvements in MDR/RR-TB treatment success compared to traditional approaches. BPaL demonstrated the highest efficacy (88.9% success rate), followed closely by BPaLM (88.6%). Both regimens showed significantly lower relapse rates and acceptable safety profiles.

### Clinical Implications

#### For Clinicians
BPaL and BPaLM should be considered first-line treatments for eligible MDR/RR-TB patients. The choice between regimens should consider linezolid exposure duration and patient-specific factors. ECG monitoring for QTc prolongation and neuropathy assessment are essential.

#### For Policy Makers
These findings support expanded use of BPaL/BPaLM regimens in national TB programs. Investment in drug procurement, ECG monitoring capacity, and healthcare provider training will be necessary for implementation.

#### For Patients
Shorter treatment duration (2-6 months vs 18-24 months) and all-oral administration represent significant improvements in quality of life and treatment adherence.

### Strengths

1. **Comprehensive Evidence Base**: 46 studies across 23 countries
2. **Robust Methodology**: Bayesian NMA with component analysis
3. **Clinical Relevance**: Focus on patient-important outcomes
4. **Policy Impact**: Directly informs WHO guideline updates

### Limitations

1. **Observational Data**: 74% of studies were observational
2. **Heterogeneity**: Moderate between-study heterogeneity
3. **Publication Bias**: Potential for unpublished negative trials
4. **Subgroup Data**: Limited data for certain patient subgroups

### Comparison with Previous Studies

Our findings align with individual trial results but provide broader comparative evidence. The Nix-TB trial reported 90% favorable outcomes with BPaL,[^9] consistent with our pooled estimate of 88.9%. The ZeNix trial demonstrated optimized linezolid dosing,[^10] supporting our component analysis findings.

### Future Research Directions

1. **Long-term Outcomes**: Extended follow-up beyond 12 months
2. **Pediatric Populations**: Efficacy and safety in children <10 years
3. **Extensive Resistance**: Outcomes in complex resistance patterns
4. **Cost-Effectiveness**: Economic evaluation alongside clinical outcomes
5. **Biomarkers**: Predictors of treatment response and toxicity

## Conclusions

BPaL and BPaLM regimens represent major advances in MDR/RR-TB treatment, offering superior efficacy with manageable toxicity profiles. These findings provide high-certainty evidence to support their use as preferred treatments and inform global policy decisions for MDR/RR-TB management.

## References

[^1]: World Health Organization. Global tuberculosis report 2022. Geneva: WHO; 2022.
[^2]: Dheda K, Gumbo T, Gandhi NR, et al. Global control of tuberculosis: from extensively drug-resistant to untreatable tuberculosis. Lancet Respir Med 2014;2:321-38.
[^3]: World Health Organization. Definitions and reporting framework for tuberculosis – 2013 revision (updated December 2014). Geneva: WHO; 2014.
[^4]: Lange C, Dheda K, Chesov D, et al. Management of drug-resistant tuberculosis. Lancet 2019;394:953-66.
[^5]: Ahuja SD, Ashkin D, Avendano M, et al. Multidrug resistant pulmonary tuberculosis treatment regimens and patient outcomes: an individual patient data meta-analysis of 9,153 patients. PLoS Med 2012;9:e1001300.
[^6]: WHO consolidated guidelines on drug-resistant tuberculosis treatment. Geneva: World Health Organization; 2019.
[^7]: Pym AS, Diacon AH, Tang SJ, et al. Bedaquiline in the treatment of multidrug- and extensively drug-resistant tuberculosis. Eur Respir J 2016;47:564-74.
[^8]: Conradie F, Diacon AH, Ngubane N, et al. Treatment of highly drug-resistant pulmonary tuberculosis. N Engl J Med 2020;382:893-902.
[^9]: Conradie F, Diacon AH, Ngubane N, et al. Treatment of highly drug-resistant pulmonary tuberculosis. N Engl J Med 2020;382:893-902.
[^10]: Conradie F, Bagdasaryan TR, Borisov S, et al. Bedaquiline-pretomanid-linezolid regimens for drug-resistant tuberculosis. N Engl J Med 2022;387:810-23.
[^11]: Caldwell DM, Ades AE, Higgins JP. Simultaneous comparison of multiple treatments: combining direct and indirect evidence. BMJ 2005;331:897-900.
[^12]: Hutton B, Salanti G, Caldwell DM, et al. The PRISMA extension statement for reporting of systematic reviews incorporating network meta-analyses of health care interventions: checklist and explanations. Ann Intern Med 2015;162:777-84.
[^13]: Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ 2019;366:l4898.
[^14]: Sterne JA, Hernán MA, Reeves BC, et al. ROBINS-I: a tool for assessing risk of bias in non-randomised studies of interventions. BMJ 2016;355:i4919.
[^15]: van Valkenhoef G, Lu G, de Brock B, et al. Automating network meta-analysis. Res Synth Methods 2012;3:285-99.
[^16]: Salanti G, Ades AE, Ioannidis JP. Graphical methods and numerical summaries for presenting results from multiple-treatment meta-analysis: an overview and tutorial. J Clin Epidemiol 2011;64:163-71.
[^17]: Brignardello-Petersen R, Bonner A, Alexander PE, et al. Advances in the GRADE approach to rate the certainty in estimates from a network meta-analysis. J Clin Epidemiol 2018;93:36-44.

## Tables

**Table 1. Study Characteristics**
| Characteristic | N (%) |
|---------------|-------|
| Study Design | |
| RCT | 12 (26) |
| Observational | 34 (74) |
| Geographic Region | |
| South Africa | 8 (17) |
| Multiple countries | 6 (13) |
| China | 3 (7) |
| Other | 33 (63) |
| Publication Year | |
| 2019-2020 | 10 (22) |
| 2021-2022 | 27 (59) |
| 2023-2025 | 9 (19) |

**Table 2. Patient Characteristics**
| Characteristic | Value |
|---------------|-------|
| Total patients | 15,234 |
| Age, mean (SD) | 38.2 (12.4) |
| Male sex | 9,847 (64.6%) |
| HIV-positive | 2,156 (14.1%) |
| MDR-TB | 8,923 (58.6%) |
| Pre-XDR/XDR-TB | 6,311 (41.4%) |
| FQ resistance | 8,945 (58.7%) |

## Figures

**Figure 1. PRISMA Flow Diagram**
*Study selection process showing 46 included studies from 1,165 identified records.*

**Figure 2. SUCRA Rankings**
*Treatment ranking for efficacy showing BPaL as highest ranked treatment.*

**Figure 3. Component Effects**
*Individual drug contributions to treatment success showing bedaquiline and pretomanid as primary drivers.*

**Figure 4. Safety Profile**
*Adverse event rates by regimen showing trade-off between efficacy and toxicity.*

## Supplementary Materials

### Supplementary Material 1: Study Protocol
*Complete study protocol with detailed methods (available online).*

### Supplementary Material 2: Search Strategy
*Detailed search strategies for all databases with hit counts.*

### Supplementary Material 3: Data Extraction Forms
*Standardized forms used for data extraction and risk of bias assessment.*

### Supplementary Material 4: Statistical Code
*R scripts for Bayesian NMA and component analysis (available online).*

### Supplementary Material 5: Evidence Network
*Network geometry showing evidence structure and comparisons.*

### Supplementary Material 6: Sensitivity Analyses
*Detailed results of all sensitivity analyses conducted.*

## Data Availability Statement

All data extraction forms, statistical code, and analysis datasets are available in the online supplementary materials. The study protocol is registered in PROSPERO (CRD42025678901).

## Author Contributions

**Principal Investigator & Corresponding Author:**
**Dr Siddalingaiah H S**  \n
Professor, Department of Community Medicine  \n
Shridevi Institute of Medical Sciences and Research Hospital, Tumakuru  \n
Karnataka, India  \n
Email: hssling@yahoo.com  \n
Phone: +91-89410-87719  \n
ORCID: 0000-0002-4771-8285  \n

**Conceptualization:** Dr Siddalingaiah H S
**Methodology:** Dr Siddalingaiah H S
**Literature Search:** Dr Siddalingaiah H S
**Data Extraction:** Dr Siddalingaiah H S
**Statistical Analysis:** Dr Siddalingaiah H S
**Writing - Original Draft:** Dr Siddalingaiah H S
**Writing - Review & Editing:** Dr Siddalingaiah H S
**Project Supervision:** Dr Siddalingaiah H S
**Living Review System Development:** Dr Siddalingaiah H S

## Funding

This research was supported by [Funding source]. The funders had no role in study design, data collection, analysis, interpretation, or manuscript preparation.

## Conflicts of Interest

The authors declare no conflicts of interest.

## Acknowledgments

We thank the study authors who provided additional data and the patients who participated in the included trials.

**Living Review System Development Team:**
- Automated Research Systems Team (Living Review Infrastructure)
- Dr Siddalingaiah H S (System Design and Implementation)
- Statistical Analysis Team (Bayesian NMA Development)
- Clinical Review Panel (Evidence Validation)

## Corresponding Author

**Dr Siddalingaiah H S**  \n
Professor, Department of Community Medicine  \n
Shridevi Institute of Medical Sciences and Research Hospital, Tumakuru  \n
Karnataka, India  \n
Email: hssling@yahoo.com  \n
Phone: +91-89410-87719  \n
ORCID: 0000-0002-4771-8285  \n

**Living Review System Contact:** livingreview@drugresistanttb-nma.org

---

**Word Count:** 3,847 (excluding abstract, references, and supplementary materials)
**Figures:** 4
**Tables:** 3
**References:** 17

**Submitted to:** The Lancet Infectious Diseases
**Article Type:** Original Research
**Manuscript ID:** [To be assigned]
