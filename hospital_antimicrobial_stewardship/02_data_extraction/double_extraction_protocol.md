# Double Data Extraction Protocol for Hospital Antimicrobial Stewardship

**Date:** October 13, 2025
**Purpose:** Ensure data extraction reliability and validity across all batches

## Background
Double data extraction is a critical quality control step where two independent reviewers extract data from the same studies and compare their results. This protocol provides standardized procedures for the hospital antimicrobial stewardship systematic review.

## Protocol Overview

### 1. Selection Criteria
- **Random Selection:** 20% of studies from each extraction batch (minimum 2 studies per batch)
- **High-Risk Studies:** Automatically include studies with complex interventions or unusual outcomes
- **Priority Studies:** Studies targeting the primary outcomes (mortality, CDI, MDRO)

### 2. Reviewer Assignment
- **Dual Extraction:** Primary reviewer + secondary reviewer (AI-assisted)
- **Third Reviewer:** Senior reviewer available for discrepancies >10%
- **Blind Extraction:** Reviewers work independently without consultation

### 3. Data Extraction Forms
Each reviewer completes all four required forms:
- **Study Characteristics:** Basic study information and design features
- **Intervention Details:** Intervention components, implementation, and comparator
- **Outcome Data:** Effect estimates, statistical methods, and clinical significance
- **Quality Assessment:** Risk of bias evaluation using ITS/QATSO or RoB-2 domains

### 4. Comparison Process

#### Stage 1: Independent Extraction
- Primary reviewer extracts data first
- Secondary reviewer extracts data independently
- Maintain strict separation (no shared protocols during extraction)

#### Stage 2: Data Comparison
- Compare extractions field-by-field
- Calculate percent agreement for each data field
- Flag all discrepancies for reconciliation

#### Stage 3: Discrepancy Resolution
- **Minor Discrepancies (<10% agreement gap):**
  - Discussion between reviewers
  - Consensus agreement documented
  - Final extraction recorded

- **Major Discrepancies (≥10% agreement gap):**
  - Involve third reviewer (senior)
  - Three-person arbitration
  - Documentation of resolution rationale

### 5. Quality Metrics

#### Agreement Thresholds:
- **≥95%:** Excellent reliability - proceed with extraction
- **85-95%:** Good reliability - review discrepancies but proceed
- **75-85%:** Fair reliability - require senior reviewer verification
- **<75%:** Poor reliability - re-extract with enhanced training

#### Key Fields Requiring 100% Agreement:
- Study ID and PMIDs
- Intervention classification (PAF, RDx, CDSS, Education, Combination)
- Statistical model (ITS, regression, etc.)
- Primary outcome measures

### 6. Documentation Requirements

#### Per Study:
- **Double Extraction Log:** Timestamp, reviewer initials, discrepancy flags
- **Resolution Notes:** Rationale for consensus agreements
- **Final Dataset:** Cleaned, agreed-upon extraction

#### Per Batch:
- **Agreement Report:** Overall and field-specific reliability metrics
- **Quality Assessment:** Inter-rater reliability statistics
- **Improvement Actions:** Protocol refinements based on discrepancies

### 7. Timeline
- **Batch Assignment:** Within 24 hours of batch deployment
- **Extraction Completion:** 5-7 days per batch
- **Discrepancy Resolution:** Within 48 hours of comparison
- **Final Dataset Release:** Within 1 week of resolution

### 8. Technology Support
- **Automated Forms:** Standardized CSV templates with validation rules
- **Comparison Scripts:** Automated discrepancy detection
- **Quality Dashboard:** Real-time progress and agreement tracking
- **Audit Trail:** Complete extraction history logging

### 9. Training Requirements
- **Formal Training:** 4-hour training session covering forms and criteria
- **Calibration Exercises:** Practice extractions with known gold-standard studies
- **Competency Assessment:** Pass 90% agreement on calibration studies
- **Ongoing Training:** Monthly refresher sessions

### 10. Best Practices

#### For Reviewers:
- Read full text thoroughly before extraction
- Document uncertainty notes alongside final judgments
- Flag ambiguous information for third reviewer input
- Maintain consistency in interpretation throughout batch

#### For Quality Control:
- Regular calibration exercises ensure consistent application
- Anonymous reviewer feedback improves protocol clarity
- Pattern analysis identifies systematic extraction biases
- Continuous protocol refinement based on real-world application

---

**Implementation Status:** Ready for Batch 1 deployment
**Next Action:** Assign reviewers to Batch 1 studies (50% completion rate = 5 double extractions required)

*Document Created: October 13, 2025*
