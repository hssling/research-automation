# Type 2 Diabetes Drug Sequencing: A Network Meta-Analysis Protocol

## Registration and Version Control
- **Protocol Version**: 1.0
- **Date**: October 12, 2025
- **PROSPERO Registration**: TBD
- **OSF Registration**: TBD
- **Version Control**: Git repository for all analysis code and documentation

## 1. Title
Network Meta-Analysis of Drug Class Sequencing for Optimizing Glycemic Control, Cardiovascular, and Renal Outcomes in Type 2 Diabetes Mellitus

## 2. Background and Rationale

### Clinical Background
Type 2 diabetes mellitus (T2DM) affects over 500 million adults worldwide and is associated with significant morbidity and mortality, particularly from cardiovascular and renal complications. The choice of optimal drug sequencing after metformin failure or in treatment-naïve patients remains controversial despite numerous clinical trials.

### Evidence Gaps
- Limited direct head-to-head comparisons between drug classes
- Uncertainty about optimal sequencing strategies
- Need for comprehensive evaluation across multiple patient-important outcomes
- Lack of evidence synthesis considering baseline patient characteristics

### Rationale for Network Meta-Analysis
The rich network of cardiovascular outcome trials (CVOTs) and comparative effectiveness studies provides an opportunity to indirectly compare multiple drug classes and combinations through network meta-analysis (NMA) to inform clinical decision-making.

## 3. Research Objectives

### Primary Objective
To compare the efficacy and safety of diabetes drug classes and combinations for optimizing patient-important outcomes in adults with T2DM.

### Secondary Objectives
- To rank drug classes by comparative effectiveness across multiple outcomes
- To identify optimal sequencing strategies based on patient baseline characteristics
- To assess heterogeneity and consistency in treatment effects
- To evaluate the quality of evidence supporting different treatment strategies

## 4. Methods

### Study Design
Bayesian network meta-analysis with hierarchical modeling incorporating multi-outcome analysis and meta-regression for moderator effects.

### Eligibility Criteria

#### Population
- Adults (≥18 years) with T2DM
- On metformin monotherapy or treatment-naïve
- Mixed populations acceptable if ≥80% have T2DM

#### Interventions
**Drug Classes:**
- SGLT2 inhibitors (SGLT2i)
- GLP-1 receptor agonists (GLP-1RA)
- DPP-4 inhibitors (DPP-4i)
- Thiazolidinediones (TZD)
- Basal insulin
- Prandial insulin
- Dual therapy combinations
- Triple therapy combinations

#### Comparators
- Placebo
- Active comparators from specified drug classes
- Standard care or metformin monotherapy

#### Outcomes
**Primary:**
- Composite cardiovascular outcomes (MACE-3: CV death, MI, stroke)
- eGFR decline ≥40% from baseline
- End-stage kidney disease (ESKD)
- Severe hypoglycemia

**Secondary:**
- HbA1c change from baseline (%)
- Weight change from baseline (kg)
- Individual CV events (MI, stroke, CV death, HF hospitalization)
- All-cause mortality

#### Study Designs
- Randomized controlled trials (RCTs)
- Cluster RCTs with appropriate analysis
- Large observational studies (n ≥500) for long-term outcomes

### Information Sources
- **Electronic Databases:** PubMed, CENTRAL, Embase, Web of Science
- **Trial Registries:** ClinicalTrials.gov, EU Clinical Trials Register
- **Regulatory Sources:** FDA/EMA documents, clinical study reports
- **Grey Literature:** Conference abstracts, theses, regulatory reports

### Search Strategy
Comprehensive search strategy developed according to PRESS guidelines with database-specific adaptations (see separate search strategy document).

### Study Selection Process
1. **Deduplication** using EndNote or Covidence
2. **Title/abstract screening** by two independent reviewers
3. **Full-text review** by two independent reviewers
4. **Discrepancy resolution** through discussion or third reviewer arbitration

### Data Extraction
**Standardized Forms:**
- Study characteristics (design, sample size, follow-up)
- Population characteristics (age, sex, BMI, diabetes duration, comorbidities)
- Intervention details (drug, dose, frequency, background therapy)
- Outcome data (effect sizes, confidence intervals, time points)
- Risk of bias assessments

**Double Extraction:** All data extracted independently by two reviewers with reconciliation of discrepancies.

### Risk of Bias Assessment
- **RCTs:** Cochrane Risk of Bias 2.0 tool
- **Observational Studies:** ROBINS-I tool
- **Overall Quality:** GRADE approach for NMA

### Statistical Analysis Plan

#### Network Meta-Analysis Model
**Bayesian Hierarchical Model:**
- Random effects model accounting for multi-arm trials
- Hierarchical modeling for multi-outcome analysis
- Markov Chain Monte Carlo (MCMC) estimation using JAGS or Stan

#### Effect Measures
- **Binary Outcomes:** Odds ratios (OR) with 95% credible intervals (CrI)
- **Continuous Outcomes:** Mean differences (MD) with 95% CrI
- **Time-to-Event:** Hazard ratios (HR) with 95% CrI

#### Heterogeneity Assessment
- Global heterogeneity (τ²)
- Local inconsistency (node-splitting approach)
- Design-by-treatment interaction

#### Moderator Analysis
**Pre-specified Moderators:**
- Baseline ASCVD status
- Baseline CKD stage
- Baseline heart failure
- Baseline BMI category
- Diabetes duration
- Age category

#### Sensitivity Analyses
- Fixed-effect vs random-effects models
- Exclusion of high risk-of-bias studies
- Exclusion of observational studies
- Alternative outcome definitions
- Different follow-up time points

#### Ranking Analysis
- Surface under the cumulative ranking curve (SUCRA)
- Mean rank probabilities
- Rank heat plots

### Quality Assurance

#### Data Management
- Standardized coding manual
- Double data entry with verification
- Database validation checks
- Audit trail for all changes

#### Analysis Validation
- Reproducible analysis scripts
- Code review by independent statistician
- Sensitivity analysis for robustness
- Comparison with published NMAs

#### Reporting Standards
- PRISMA-NMA extension
- GRADE assessment for evidence quality
- Complete statistical code availability
- Protocol registration and publication

## 5. Ethics and Dissemination

### Ethics
This study uses only published aggregate data and does not require ethical approval.

### Dissemination Plan
- **Primary Publication:** High-impact medical journal
- **Secondary Publications:** Methodology papers, subgroup analyses
- **Conference Presentations:** ADA, EASD, ACC, ASN meetings
- **Knowledge Translation:** Clinical practice guidelines, decision aids
- **Data Sharing:** Complete dataset and analysis code on OSF

## 6. Project Timeline

### Phase 1: Setup (Weeks 1-2)
- [ ] Finalize protocol and registration
- [ ] Develop search strategy and data extraction forms
- [ ] Set up analysis environment and databases

### Phase 2: Literature Search (Weeks 3-8)
- [ ] Execute comprehensive literature search
- [ ] Screen titles and abstracts (target: 5,000-10,000 articles)
- [ ] Full-text review (target: 200-400 articles)
- [ ] Data extraction and validation

### Phase 3: Analysis (Weeks 9-16)
- [ ] Prepare data for NMA
- [ ] Conduct primary analyses
- [ ] Perform sensitivity analyses
- [ ] Generate results visualizations

### Phase 4: Interpretation (Weeks 17-20)
- [ ] Interpret findings in clinical context
- [ ] Assess evidence quality (GRADE)
- [ ] Draft results sections
- [ ] Internal peer review

### Phase 5: Manuscript Preparation (Weeks 21-26)
- [ ] Write complete manuscript
- [ ] Generate figures and tables
- [ ] Prepare supplementary materials
- [ ] External peer review

### Phase 6: Submission and Revision (Weeks 27-32)
- [ ] Journal submission
- [ ] Address reviewer comments
- [ ] Final manuscript preparation
- [ ] Publication and dissemination

## 7. Project Team and Responsibilities

### Principal Investigators
- **Lead Investigator:** [Name], MD, PhD - Clinical expertise, interpretation
- **Co-Investigator:** [Name], PhD - Statistical analysis, methodology
- **Co-Investigator:** [Name], MD - Clinical interpretation, guidelines

### Research Staff
- **Project Coordinator:** Literature search, data management
- **Research Assistants:** Data extraction, quality assessment
- **Statistician:** Analysis execution, code development
- **Librarian:** Search strategy development, grey literature

### Advisory Committee
- **Clinical Experts:** Endocrinology, Cardiology, Nephrology
- **Methodology Experts:** NMA specialists, systematic review experts
- **Patient Partners:** Lived experience perspective

## 8. Funding and Resources

### Required Resources
- **Software:** R, JAGS/Stan, RevMan, EndNote/Covidence
- **Databases:** Access to PubMed, Embase, Web of Science
- **Personnel:** 2 FTE research staff for 6 months
- **Computing:** High-performance computing for Bayesian analysis

### Potential Funding Sources
- **Government:** NIH, PCORI, CIHR
- **Foundation:** ADA, JDRF, AHA
- **Industry:** Unrestricted grants from pharmaceutical companies
- **Institutional:** University research funds

## 9. Risk Assessment and Mitigation

### Potential Risks
- **Publication Bias:** Mitigate with comprehensive search, funnel plots
- **Heterogeneity:** Use random-effects models, meta-regression
- **Inconsistency:** Node-splitting analysis, design-by-treatment interaction
- **Sparse Networks:** Careful interpretation, sensitivity analysis
- **Outdated Evidence:** Regular search updates, living review consideration

### Contingency Plans
- Insufficient studies for certain comparisons
- High heterogeneity requiring network meta-regression
- Missing outcome data requiring imputation strategies
- Delays in literature search or analysis

## 10. Amendments to Protocol

Any substantial changes to this protocol will be:
- Documented with rationale and date
- Registered with PROSPERO/OSF
- Reported transparently in publications
- Approved by advisory committee

## References

1. Higgins JPT, et al. Cochrane Handbook for Systematic Reviews of Interventions. 2023.
2. Hutton B, et al. The PRISMA Extension Statement for Reporting of Systematic Reviews Incorporating Network Meta-analyses. Ann Intern Med. 2015.
3. Puhan MA, et al. A GRADE Working Group approach for rating the quality of treatment effect estimates from network meta-analysis. BMJ. 2014.
4. Dias S, et al. Checking consistency in mixed treatment comparison meta-analysis. Stat Med. 2010.

---

**Protocol Contact:**
[Lead Investigator Name]
[Institution]
[Email]
[Phone]

**Last Updated:** October 12, 2025
**Version:** 1.0
