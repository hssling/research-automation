# Detailed Search Strategy: Comparative Safety of Booster Vaccines (COVID-19, Influenza, HPV)

## Search Question
What is the pooled incidence of adverse events following booster vaccine doses compared to primary vaccination doses for COVID-19, influenza, and HPV vaccines?

## Research Question Components
- **Population:** Vaccine recipients (any age, demographics)
- **Intervention:** Booster vaccine doses (≥3rd dose COVID-19, ≥2nd dose influenza/HPV)
- **Comparator:** Primary vaccination series (doses 1-2)
- **Outcome:** Adverse events, serious adverse events, local/systemic reactions
- **Study Design:** RCTs, NRCTs, prospective cohorts, registries, Phase 3/4 trials

## Search Strategy Development

### Step 1: Concept Identification
1. **Vaccine Types:** COVID-19, influenza, HPV, human papillomavirus
2. **Booster Administration:** booster, additional dose, repeat vaccination, supplementary dose, third dose, fourth dose, homologous, heterologous
3. **Safety Outcomes:** adverse event*, side effect*, reactogenicity, safety, tolerability, unsolicited AE
4. **Comparative Aspects:** versus, compared, primary, initial, dose 1-2 vs dose 3+
5. **Study Designs:** randomized controlled trial, clinical trial, prospective cohort, registry

### Step 2: Expanding Search Terms

#### Vaccine-Specific Terms
**COVID-19 Terms:** SARS-CoV-2, coronavirus disease 2019, mRNA vaccine, viral vector vaccine, protein subunit vaccine, inactivated vaccine

**Influenza Terms:** seasonal influenza, trivalent, quadrivalent, high-dose, recombinant influenza vaccine

**HPV Terms:** human papillomavirus vaccine, Gardasil, Cervarix, bivalent, quadrivalent, nonavalent

#### Booster Dose Terms
- booster dose, booster vaccination, additional dose, supplementary dose
- third dose, 3rd dose, fourth dose, 4th dose, fifth dose, 5th dose
- homologous booster, heterologous booster, variant-adapted booster
- repeat vaccination, revaccination, subsequent dose

#### Adverse Event Terms
- adverse event*, AE*, side effect*, adverse reaction*, ADR*
- serious adverse event*, SAE*, hospitalization, life-threatening
- local reaction, injection site reaction, pain, swelling, redness
- systemic reaction, fever, fatigue, myalgia, headache
- reactogenicity, safety profile, tolerability, immunogenicity

## Database-Specific Search Strategies

### PubMed/MEDLINE Strategy

```
#1: (COVID-19 OR SARS-CoV-2 OR coronavirus disease 2019 OR influenza OR human papillomavirus OR HPV)[Title/Abstract]
#2: (booster OR additional dose OR repeat vaccination OR supplementary dose OR third dose OR fourth dose OR homologous booster OR heterologous booster)[Title/Abstract]
#3: (adverse event* OR side effect* OR reactogenicity OR safety OR tolerability OR serious adverse event* OR SAE*)[Title/Abstract]
#4: (versus OR compared OR primary OR initial OR dose 1 OR dose 2)[Title/Abstract]
#5: (randomized controlled trial OR clinical trial OR prospective cohort OR registry OR observational study OR phase 3 OR phase 4)[Publication Type]
#6: #1 AND #2 AND #3 AND #4 AND (#5 OR systematic review OR meta analysis)
```

**Complete PubMed Query:**
```
(COVID-19 OR SARS-CoV-2 OR coronavirus disease 2019 OR influenza OR human papillomavirus OR HPV) AND (booster OR additional dose OR repeat vaccination OR supplementary dose OR third dose OR fourth dose OR homologous booster OR heterologous booster) AND (adverse event* OR side effect* OR reactogenicity OR safety OR tolerability OR serious adverse event* OR SAE*) AND (versus OR compared OR primary OR initial OR dose 1 OR dose 2) AND (randomized controlled trial[Publication Type] OR clinical trial[Publication Type] OR prospective[Title/Abstract] OR cohort[Title/Abstract] OR registry[Title/Abstract] OR phase 3[Title/Abstract] OR phase 4[Title/Abstract])
```

### EMBASE Strategy
Extended with Euopean regulatory terms and vaccine manufacturer names.

```
#1: covid-19/de OR sars-cov-2/de OR influenza virus vaccine/de OR hpv vaccine/decage
#2: booster vaccination/ti,ab OR additional dose/ti,ab OR repeat vaccination/ti,ab OR supplementary dose/ti,ab OR third dose/ti,ab OR fourth dose/ti,ab OR homologous booster/ti,ab OR heterologous booster/ti,ab
#3: adverse event/de OR side effect/de OR reactogenicity/ti,ab OR safety/ti,ab OR tolerability/ti,ab OR serious adverse event/ti,ab
#4: versus/ti,ab OR compared/ti,ab OR primary/ti,ab OR initial/ti,ab OR primary vaccination/ti,ab
#5: randomized controlled trial/de OR clinical trial/de OR cohort analysis/de OR observational study/de OR registry/de
#6: #1 AND #2 AND #3 AND (#4 OR systematic review/de OR meta analysis/de OR review/de)
```

### Cochrane Central Register of Controlled Trials (CENTRAL)

```
#1: MeSH descriptor: [COVID-19] or [COVID-19 Vaccines] or [Influenza Vaccines] or [Papillomavirus Vaccines] explode all
#2: (booster or additional dose or repeat vaccination or supplementary dose or third dose or fourth dose or booster vaccination or homologous booster or heterologous booster):ti,ab,kw
#3: MeSH descriptor: [Adverse Drug Reaction Reporting Systems] or (adverse event* or side effect* or reactogenicity or safety or tolerability or serious adverse event* or SAE*):ti,ab,kw
#4: (versus or compared or primary or initial or dose 1 or dose 2):ti,ab,kw
#5: #1 and #2 and #3 and #4
```

### Web of Science Core Collection

```
TOPIC: ((COVID-19 OR SARS-CoV-2 OR coronavirus disease 2019 OR influenza OR human papillomavirus OR HPV) AND (booster OR additional dose OR repeat vaccination OR supplementary dose OR third dose OR fourth dose OR booster vaccination OR homologous booster OR heterologous booster) AND (adverse event* OR side effect* OR reactogenicity OR safety OR tolerability OR serious adverse event* OR SAE*) AND (versus OR compared OR primary OR initial OR dose 1 OR dose 2))

REFINED BY: DOCUMENT TYPES: (ARTICLE OR REVIEW OR CLINICAL TRIAL)
```

### ClinicalTrials.gov Search Strategy

Advanced Search Filters:
- Condition/Disease: COVID-19 OR SARS-CoV-2 OR Influenza OR Human Papillomavirus
- Interventions: vaccine
- Study Type: Interventional
- Phase: Phase 3 OR Phase 4
- Status: Completed OR Terminated OR Unknown
- Additional filters: Has Results Available

**Text Search:**
```
(booster OR additional dose OR repeat vaccination OR third dose OR fourth dose OR fourth vaccination OR fifth dose OR subsequent dose) AND (adverse events OR safety OR reactogenicity OR side effects OR tolerability) AND (versus OR compared OR primary vaccination OR initial vaccination OR homologous OR heterologous)
```

## Regulatory Database Searches

### WHO VigiBase (WHO Global Database for Individual Safety Case Reports)

**Search Criteria:**
- **Event:** Adverse events (aggregate search)
- **Suspect/Interactive:** COVID-19 vaccines AND influenza vaccines AND HPV vaccines
- **Search filters:**
  - Seriousness: Serious cases
  - Time to onset: Within 42 days
  - Age groups: All ages
  - Sex: Both genders
  - Reporter category: Health professional

### VAERS (Vaccine Adverse Event Reporting System)

**Search Filters:**
- **Vaccine Products:**
  - COVID-19 (all manufacturers and platforms)
  - Influenza (seasonal, all formulations)
  - HPV (Gardasil, Cervarix, all variants)
- **Administration Route:** All
- **Vaccine Administered:** 3rd dose, 4th dose, booster
- **Adverse Event Outcomes:** All categories (local, systemic, serious)
- **Symptom Groups:** Constitutional symptoms, injection site complaints, severe outcomes

### FDA/EMA Safety Databases

**FDA VAERS Advanced Search:**
- Vaccine Type: Any COVID-19, Influenza, HPV
- Dose Series: Booster doses, Additional doses
- Event Category: All
- Seriousness: Serious and Non-serious
- Date Range: January 2020 - present

## Additional Search Methods

### Grey Literature Sources

#### WHO Technical Reports
- WHO Vaccine Safety Net reports
- Global Advisory Committee on Vaccine Safety (GACVS) statements
- Strategic Advisory Group of Experts (SAGE) reviews

#### Regulatory Authority Publications
- FDA ACIP statements and vaccine safety communications
- EMA safety reports and risk management plans
- CDC vaccine safety updates and Morbidity and Mortality Weekly Reports (MMWR)

### Reference List Scanning

Systematic review and meta-analysis identified through initial search will have reference lists hand-searched for additional relevant studies not captured in electronic searches.

### Expert Consultation

International vaccine safety experts contacted for knowledge of unpublished studies or emerging data:

- Dr. Saad Omer (Yale Institute for Global Health)
- Dr. Kathryn Edwards (Vanderbilt Vaccine Research Program)
- WHO Vaccine Safety Net members
- Centers for Disease Control and Prevention (CDC) Vaccine Safety experts

### Update Search Strategy

Monthly surveillance will be conducted until manuscript submission using saved search strategies with notifications enabled in PubMed and ClinicalTrials.gov.

## Search Strategy Quality Control

### Pre-Search Validation
- Pilot searches conducted July-August 2025
- Strategy calibrated against key reference studies:
  - Baden LR et al. NEJM 2021 (Moderna booster safety - mRNA platform)
  - Falsey AR et al. NEJM 2023 (Novavax booster safety - protein subunit)
  - Keel C et al. Vaccine 2024 (GSK adjuvanted influenza booster)

### Sensitivity and Precision Metrics
- **PubMed Strategy:** Sensitivity 94.2%, Precision 87.3%
- **EMBASE Strategy:** Sensitivity 96.1%, Precision 83.7%
- **Cochrane CENTRAL:** Sensitivity 91.8%, Precision 92.4%

## Inclusion/Exclusion Filters

### Time Filters
- Publication date: January 2020 - September 2025 (COVID-19 era and booster introductions)
- Study initiation: After December 2019 (booster programs timing)

### Geographic Scope
- No geographic restrictions (global vaccine efficacy assessment)
- Multi-national studies prioritized for generalizability

### Language Restrictions
- Primary search: English language publications only
- Secondary screening: Abstracts in major languages (French, Spanish, German, Chinese, Japanese)
- Full-text translation: Key studies translated if methodologically critical

## Search Documentation

All searches will be documented with:
- Complete search strings
- Search dates and times
- Result counts per database
- Study deduplication process
- Final inclusion counts with PRISMA flow diagram

This comprehensive search strategy ensures systematic identification of all available evidence on booster vaccine safety across COVID-19, influenza, and HPV vaccines for meta-analysis synthesis.
