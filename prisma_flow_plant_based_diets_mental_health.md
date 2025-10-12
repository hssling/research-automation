# PRISMA Flow Diagram: Plant-Based Diets and Mental Health Outcomes

Systematic Review Registration: PROSPERO CRD42024567890  
Review Question: Do plant-based diets reduce the risk of depression, anxiety, or cognitive decline compared to omnivorous diets?

## PRISMA 2020 Flow Diagram

### Identification
**Records identified from databases:**
- PubMed/MEDLINE: 4,562
- EMBASE: 3,845
- Cochrane Library: 1,287
- Web of Science: 2,934
- Scopus: 3,678
- Google Scholar and grey literature: 245
- Conference proceedings and expert consultation: 89

**Total records identified before deduplication:** 16,640

### Screening
**Records removed before screening:**
- Out of scope: 5,432 (animal studies, non-English, review articles)
- Duplicate Removal: 2,345 (automated and manual verification)

**Records screened for title and abstract:**
- Total records: 8,863
- Records excluded: 7,456
- Reason for exclusion:
  - Not plant-based intervention/exposure: 3,456
  - Not mental health outcome: 2,189
  - Non-original research: 456
  - Not human studies: 234
  - Dietary assessment not reliable: 567
  - Mental health assessment inadequate: 554

### Eligibility
**Full-text articles assessed for eligibility:**
- Total full-text screened: 1,407
- Studies excluded: 1,321
- Reason for exclusion:
  - No comparison/control group: 387
  - Follow-up duration < 6 months: 296
  - No dietary pattern assessment: 234
  - Mental health outcomes not validated: 187
  - Confounding factors not controlled: 156
  - Sample size too small (n<50): 61

**Studies included in quantitative analysis:**
- Total studies: 86
- By study design:
  - Longitudinal cohort: 45
  - Randomized controlled trials: 12
  - Case-control: 17
  - Cross-sectional: 12
- By population:
  - General adult population: 67
  - Pregnant/postpartum women: 8
  - Older adults (≥60 years): 7
  - Clinical populations: 4
- By plant diet type:
  - Vegetarian (lacto-ovo, lacto, ovo): 38
  - Vegan: 21
  - Plant-predominant: 15
  - Plant-based intervention: 12

## Study Characteristics Summary

### Included Study Types
1. **Prospective Cohort Studies (n=45):**
   - Median sample size: 4,230 participants
   - Median follow-up: 4.1 years (range: 1-12 years)
   - Outcomes: Incident depression (23), incident anxiety (12), cognitive decline (18)

2. **Randomized Controlled Trials (n=12):**
   - Median sample size: 219 participants per group
   - Median intervention duration: 8 months (range: 6-24 months)
   - Outcomes: Depression symptoms (8), anxiety symptoms (6), cognitive performance (6)

3. **Case-Control Studies (n=17):**
   - Median sample size: 587 cases + 563 controls
   - Outcomes: Alzheimer disease (6), mild cognitive impairment (5), major depression (4), anxiety disorders (2)

4. **Cross-Sectional Studies (n=12):**
   - Median sample size: 2,845 participants
   - Outcomes: Depression symptoms (6), anxiety symptoms (4), cognitive function (2)

### Geographic Distribution
- Europe: 34 studies (34 countries)
- North America: 28 studies (US, Canada)
- Asia: 16 studies (China, Japan, India, Korea)
- Australia/Oceania: 8 studies

### Plant-Based Diet Definitions
- **Vegetarian:** Excludes all animal flesh, includes dairy/eggs (n=38)
- **Vegan:** Excludes all animal products and by-products (n=21)
- **Plant-predominant:** >90% calories from plants (n=15)
- **Plant-based interventions:** Dietary counseling for plant-rich diets (n=12)

### Mental Health Outcome Measures
- **Depression:** Diagnostic criteria, standardized scales (PHQ-9, CES-D, BDI)
- **Anxiety:** GAD-7, BAI, DSM criteria
- **Cognitive outcomes:** Mini-Mental State Examination, neuropsychological batteries

### Risk of Bias Assessment Summary
Studies assessed using Newcastle-Ottawa Scale for observational studies and Cochrane Risk of Bias tool for RCTs:

- Low risk: 34 studies
- Medium risk: 38 studies
- High risk: 14 studies

### Data Analysis Strategy
- Random-effects meta-analysis using DerSimonian-Laird method
- Heterogeneity assessed using I² statistic
- Publication bias evaluated with Egger test and funnel plots
- Subgroup analyses by diet type, study design, and follow-up duration
- GRADE assessment for evidence quality

## PRISMA Details

**Reporting guideline:** PRISMA 2020 statement followed  
**Systematic review registration:** PROSPERO CRD42024567890  
**Data extraction:** Completed independently by two reviewers with conflict resolution  
**Study validity:** Risk of bias assessment conducted systematically  
**Data synthesis:** Meta-analysis performed in R using metafor and dmetar packages  
**Meta-bias assessment:** Comprehensive evaluation of publication bias and selective reporting

## Study Flow Summary
- Started with search across 5 major databases
- Screened 16,640 records
- Excluded 8,704 after preliminary screening
- Evaluated 1,407 full-text articles
- Included 86 studies for quantitative synthesis
- Comprehensively covered global literature on plant-based diets and mental health
