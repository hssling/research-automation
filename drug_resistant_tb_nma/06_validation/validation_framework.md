# Validation Framework: Drug-Resistant Tuberculosis Network Meta-Analysis

## Overview

This validation framework ensures the quality, reproducibility, and reliability of the network meta-analysis findings. It provides systematic protocols for validating data extraction, statistical analysis, and reporting standards.

## 1. Data Validation Protocols

### 1.1 Double Data Extraction Validation

#### Protocol
- **Primary Extractor**: Senior researcher with TB expertise
- **Secondary Extractor**: Independent researcher without knowledge of primary extraction
- **Validation Criteria**:
  - Agreement on study characteristics ≥95%
  - Agreement on outcome data ≥98%
  - Discrepancy resolution by third reviewer

#### Validation Metrics
```markdown
- Total studies validated: [NUMBER]
- Agreement rate - Study characteristics: [PERCENTAGE]%
- Agreement rate - Outcome data: [PERCENTAGE]%
- Kappa statistic for inter-rater reliability: [VALUE]
```

### 1.2 Data Quality Assessment

#### Completeness Check
- [ ] All required variables extracted
- [ ] Missing data appropriately handled
- [ ] Outliers identified and verified
- [ ] Data entry errors corrected

#### Consistency Validation
- [ ] Treatment definitions standardized
- [ ] Outcome definitions harmonized
- [ ] Time points aligned
- [ ] Population characteristics consistent

## 2. Statistical Analysis Validation

### 2.1 Model Validation

#### Convergence Assessment
- [ ] Gelman-Rubin statistics <1.1 for all parameters
- [ ] Effective sample size >400 for key parameters
- [ ] Monte Carlo error <5% of posterior standard deviation
- [ ] Trace plots show adequate mixing

#### Model Fit Evaluation
- [ ] Deviance Information Criterion (DIC) comparison
- [ ] Posterior predictive checks
- [ ] Leverage plots for influential studies
- [ ] Residual deviance assessment

### 2.2 Heterogeneity and Inconsistency Validation

#### Between-Study Heterogeneity
- [ ] τ² estimation with confidence intervals
- [ ] I² calculation for direct comparisons
- [ ] Meta-regression for heterogeneity sources
- [ ] Subgroup analysis for effect modifiers

#### Inconsistency Assessment
- [ ] Node-splitting method for local inconsistency
- [ ] Global inconsistency via DIC comparison
- [ ] Loop-specific approach for closed loops
- [ ] Heat plots for inconsistency visualization

### 2.3 Sensitivity Analysis Validation

#### Predefined Sensitivity Analyses
- [ ] Risk of bias exclusion analysis
- [ ] Fixed vs random effects comparison
- [ ] Alternative prior distributions
- [ ] Small study exclusion
- [ ] Outcome definition variations
- [ ] Publication year stratification
- [ ] Geographic analysis

#### Validation Criteria
- [ ] All sensitivity analyses completed
- [ ] Results robust across analyses
- [ ] Direction and magnitude of effects consistent
- [ ] Confidence intervals overlapping substantially

## 3. Reporting Quality Validation

### 3.1 PRISMA-NMA Compliance

#### Required Elements
- [ ] Information sources and search strategy
- [ ] Study selection process with reasons for exclusion
- [ ] Data collection process and data items
- [ ] Risk of bias assessment methods
- [ ] Statistical analysis methods
- [ ] Additional analyses (sensitivity, subgroup, etc.)
- [ ] Study characteristics and results synthesis

#### Network Geometry Reporting
- [ ] Network plot with node and edge weights
- [ ] Study distribution across comparisons
- [ ] Evidence contribution matrix
- [ ] Publication bias assessment

### 3.2 GRADE Assessment Validation

#### Certainty Domains
- [ ] Risk of bias assessment
- [ ] Inconsistency evaluation
- [ ] Indirectness consideration
- [ ] Imprecision quantification
- [ ] Publication bias detection

#### Confidence Ratings
- [ ] High/Moderate/Low/Very Low classifications
- [ ] Rationale for downgrading
- [ ] Justification for upgrading (if applicable)
- [ ] Summary of findings table

## 4. Reproducibility Validation

### 4.1 Code Validation

#### Statistical Code Review
- [ ] R scripts independently reviewed
- [ ] Random seed specification for reproducibility
- [ ] Version control for all analysis code
- [ ] Commented code with clear explanations

#### Data Management
- [ ] Raw data preservation
- [ ] Processing steps documented
- [ ] Analysis datasets archived
- [ ] Backup systems in place

### 4.2 External Validation

#### Independent Replication
- [ ] Key analyses replicated by external statistician
- [ ] Results compared with original findings
- [ ] Discrepancies resolved and documented
- [ ] Final agreement on conclusions

#### Peer Review Simulation
- [ ] Internal peer review process
- [ ] Statistical review by independent expert
- [ ] Clinical review by TB specialist
- [ ] Methodological review by epidemiologist

## 5. Publication Bias Validation

### 5.1 Funnel Plot Analysis

#### Asymmetry Assessment
- [ ] Funnel plots for all treatment comparisons
- [ ] Egger's test for small-study effects
- [ ] Trim-and-fill method for bias estimation
- [ ] Contour-enhanced funnel plots

#### Validation Metrics
- [ ] Number of studies potentially missing
- [ ] Impact on pooled effect estimates
- [ ] Publication bias adjustment applied
- [ ] Results interpreted with bias consideration

### 5.2 Search Strategy Validation

#### Completeness Assessment
- [ ] Reference list checking for missed studies
- [ ] Citation tracking for relevant articles
- [ ] Clinical trial registry searches
- [ ] Conference abstract review

## 6. Clinical Relevance Validation

### 6.1 Applicability Assessment

#### Population Relevance
- [ ] Target population clearly defined
- [ ] Inclusion/exclusion criteria appropriate
- [ ] Subgroup analyses for important populations
- [ ] Generalizability assessment

#### Intervention Feasibility
- [ ] Treatment regimens available in target settings
- [ ] Monitoring requirements realistic
- [ ] Cost considerations addressed
- [ ] Implementation barriers identified

### 6.2 Outcome Importance

#### Patient-Centered Outcomes
- [ ] Treatment success as primary outcome
- [ ] Safety outcomes comprehensively assessed
- [ ] Quality of life considerations
- [ ] Long-term outcomes evaluated

## 7. Quality Assurance Timeline

### Pre-Analysis Phase
- [ ] Protocol development and registration
- [ ] Literature search and study selection
- [ ] Data extraction form piloting
- [ ] Training for data extractors

### Analysis Phase
- [ ] Double data extraction completion
- [ ] Statistical analysis validation
- [ ] Sensitivity analysis execution
- [ ] Results interpretation review

### Reporting Phase
- [ ] Manuscript draft review
- [ ] Statistical code audit
- [ ] External validation process
- [ ] Final quality check

## 8. Validation Documentation

### Required Documentation
- [ ] Data extraction validation report
- [ ] Statistical analysis validation report
- [ ] Sensitivity analysis summary
- [ ] Quality assurance checklist
- [ ] Reproducibility statement

### Archival Requirements
- [ ] Raw data files archived
- [ ] Analysis code preserved
- [ ] Validation reports saved
- [ ] Correspondence documented

## 9. Validation Checklist

### Data Quality
- [ ] Double data extraction completed with high agreement
- [ ] Data completeness verified
- [ ] Outliers identified and addressed
- [ ] Missing data handled appropriately

### Statistical Quality
- [ ] Model convergence confirmed
- [ ] Heterogeneity assessed
- [ ] Inconsistency evaluated
- [ ] Sensitivity analyses completed

### Reporting Quality
- [ ] PRISMA-NMA guidelines followed
- [ ] GRADE assessment completed
- [ ] All supplementary materials prepared
- [ ] Code and data sharing planned

### Reproducibility
- [ ] Analysis code documented and shared
- [ ] Random seeds specified
- [ ] External validation completed
- [ ] Independent review conducted

## 10. Validation Outcomes

### Quality Metrics
- **Data Extraction Agreement**: ≥95% for all items
- **Statistical Validation**: All convergence criteria met
- **Reporting Compliance**: 100% PRISMA-NMA items addressed
- **Reproducibility Score**: ≥90% independent replication success

### Validation Status
- **Date of Last Validation**: [DATE]
- **Validation Team**: [NAMES]
- **Overall Quality Rating**: [HIGH/MODERATE/LOW]
- **Reproducibility Confirmed**: [YES/NO]

## 11. Continuous Quality Monitoring

### Post-Publication Validation
- [ ] Reader feedback collection
- [ ] Errata and corrections tracking
- [ ] Citation analysis for impact assessment
- [ ] Update searches for new evidence

### Living Review Framework
- [ ] Annual update searches planned
- [ ] New study incorporation protocol
- [ ] Evidence evolution monitoring
- [ ] Guideline impact assessment

---

**Validation Framework Version**: 1.0
**Last Updated**: October 12, 2025
**Next Review Date**: October 12, 2026

This validation framework ensures the highest standards of research quality and provides transparency in methodology and reporting for the drug-resistant tuberculosis network meta-analysis.
