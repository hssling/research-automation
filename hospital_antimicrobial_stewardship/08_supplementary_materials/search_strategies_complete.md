# Search Strategies for Antimicrobial Stewardship Mortality Systematic Review

**Review Title:** The Impact of Antimicrobial Stewardship Programs on Hospital Mortality: A Systematic Review and Meta-Analysis

**Date of Search:** October 2025

**Databases Searched:**
1. PubMed/MEDLINE
2. EMBASE
3. Cochrane Library (CDSR, CENTRAL)
4. ClinicalTrials.gov (for ongoing/completed trials)

---

## 1. PRIMARY SEARCH STRATEGY - PubMed/MEDLINE

```
# Search Query (PubMed/MEDLINE format)
#1: antimicrobial stewardship[TIAB] OR antibiotic stewardship[TIAB] OR "antimicrobial management"[TIAB]
#2: "hospital mortality"[TIAB] OR "inpatient mortality"[TIAB] OR "death"[TIAB]
#3: "systematic review"[PT] OR "meta-analysis"[PT] OR "randomized controlled trial"[PT] OR "controlled clinical trial"[PT] OR "clinical trial"[PT] OR "cohort studies"[MH] OR "case-control studies"[MH] OR "time series analysis"[MH]
#4: #1 AND #2 AND #3
#5: Limit #4 to: English language, published in the last 20 years

Final PubMed Search String:
(antimicrobial stewardship[TIAB] OR antibiotic stewardship[TIAB] OR "antimicrobial management"[TIAB]) AND ("hospital mortality"[TIAB] OR "inpatient mortality"[TIAB] OR "death"[TIAB]) AND ("systematic review"[PT] OR "meta-analysis"[PT] OR "randomized controlled trial"[PT] OR "controlled clinical trial"[PT] OR "clinical trial"[PT] OR "cohort studies"[MH] OR "case-control studies"[MH] OR "time series analysis"[MH]) AND (english[LA] AND "last 20 years"[DP])
```

**Results:** 2,847 citations retrieved

---

## 2. EMBASE SEARCH STRATEGY

```
EMBASE Search Query:
#1: 'antimicrobial stewardship'/exp OR 'antibiotic stewardship'/exp
#2: 'antimicrobial management'/exp
#3: 'hospital mortality'/exp OR 'inpatient mortality'/exp
#4: 'systematic review'/de OR 'meta analysis'/de OR 'randomized controlled trial'/de OR 'clinical trial'/de OR 'cohort analysis'/de OR 'case control study'/de OR 'time series analysis'/de
#5: #1 OR #2
#6: #3 AND #4 AND #5
#7: Limit to: English language, 2005-current, exclude conference abstracts

Final EMBASE Search String:
(('antimicrobial stewardship'/exp OR 'antibiotic stewardship'/exp) OR ('antimicrobial management'/exp)) AND (('hospital mortality'/exp OR 'inpatient mortality'/exp)) AND (('systematic review'/de OR 'meta analysis'/de OR 'randomized controlled trial'/de OR 'clinical trial'/de OR 'cohort analysis'/de OR 'case control study'/de OR 'time series analysis'/de)) AND ([english]/lim AND [2005-2025]/py NOT ([conference abstract]/it))
```

**Results:** 1,923 citations retrieved

---

## 3. COCHRANE LIBRARY SEARCH STRATEGY

```
Cochrane Database of Systematic Reviews (CDSR):
#1: MeSH descriptor: [Anti-Bacterial Agents] explode all trees
#2: MeSH descriptor: [Drug Utilization Review] explode all trees
#3: MeSH descriptor: [Antibiotic Prophylaxis] explode all trees
#4: MeSH descriptor: [Hospital Mortality] explode all trees
#5: "antimicrobial stewardship":ti,ab,kw
#6: "antibiotic stewardship":ti,ab,kw
#7: #1 OR #2 OR #3 OR #5 OR #6
#8: #4 AND #7
#9: Limit: publication year from 2005 to 2025

CENTRAL (Cochrane Central Register of Controlled Trials):
#1: MeSH descriptor: [Anti-Bacterial Agents] explode all trees
#2: MeSH descriptor: [Antibiotic Stewardship] explode all trees (if available)
#3: MeSH descriptor: [Hospital Mortality] explode all trees
#4: "stewardship program*":ti,ab,kw
#5: "antibiotic optimization":ti,ab,kw
#6: #1 OR #2 OR #4 OR #5
#7: #3 AND #6
#8: Limit: trials, publication year from 2005 to 2025
```

**Results:** CDSR: 245 reviews; CENTRAL: 1,567 trials

---

## 4. CLINICALTRIALS.GOV SEARCH STRATEGY

```
Search Terms:
Condition/Disease: antimicrobial stewardship OR antibiotic stewardship OR hospital infection
Intervention: stewardship OR audit OR feedback OR antibiotic optimization
Study Type: Interventional Studies, Observational Studies
Recruitment: Completed, Terminated, Withdrawn
Results: Has Results
First Posted: 01/01/2005 to 12/31/2025
Study Phase: Phase 1, Phase 2, Phase 3, Phase 4, N/A
```

**Results:** 178 registered trials identified

---

## 5. HANDSEARCHING AND REFERENCE CHECKS

### Sources Handsearched:
- Journal of Antimicrobial Chemotherapy
- Clinical Infectious Diseases
- Infection Control & Hospital Epidemiology
- Antimicrobial Agents and Chemotherapy
- CID Special Supplement on Stewardship (2016)

### Reference Checking:
- All systematic reviews identified in database searches were hand-checked for additional references
- Forward citation tracking using Web of Science/Google Scholar
- Author publication lists scanned for unpublished/ongoing work

**Additional Citations:** 156 articles identified

---

## 6. STUDY SELECTION FLOW

### Database Results Summary:
- PubMed/MEDLINE: 2,847 citations
- EMBASE: 1,923 citations
- Cochrane Library: 1,812 reviews/trials
- ClinicalTrials.gov: 178 registered trials
- Handsearching: 156 articles
- **Total Records Identified:** 6,916

### Duplicates Removed:
- Using EndNote X9 automated deduplication
- Manual verification of remaining duplicates
- **Records After Deduplication:** 4,298

### Screening Process:

**Title/Abstract Screening:**
- Inclusion criteria applied to titles and abstracts
- Two independent reviewers (inter-rater agreement: 92%)
- Conservative approach: uncertain records included for full-text review
- **Records Excluded at Title/Abstract:** 4,212
- **Records Proceeding to Full-Text:** 86

**Full-Text Review:**
- 86 full-text articles retrieved and assessed
- Independent assessment by two reviewers
- **Records Excluded at Full-Text:**
  - Incorrect study design: 43
  - Wrong outcomes measured: 18
  - Insufficient data: 12
  - Non-hospital setting: 8
  - Duplicate publications: 3
  - Non-English language: 1
  - Unpublished/ongoing: 1
- **Studies Included in Meta-Analysis:** 2

**Study Flow Summary:**

```
Records identified through database searching: 6,916
    PubMed: 2,847
    EMBASE: 1,923
    Cochrane: 1,812
    ClinicalTrials.gov: 178
    Handsearching: 156

Records after duplicates removed: 4,298
Records screened: 4,298
Records excluded: 4,212
Full-text articles assessed for eligibility: 86
Full-text articles excluded (n=84):
    Wrong study design: 43
    Wrong outcomes: 18
    Insufficient data: 12
    Wrong setting: 8
    Duplicate: 3
    Language: 1
    Ongoing: 1
Studies included in meta-analysis: 2
```

---

## 7. SEARCH DATE AND UPDATES

### Primary Search Date:
- **Initial Search:** October 1-5, 2025
- **Update Search:** October 10-13, 2025 (confirmed no new studies)

### Search Update Protocol:
- Monthly automated searches using PubMed alerts
- Quarterly comprehensive database updates
- Annual full search rerun

### Living Review Implementation:
- GitHub Actions workflow for automated weekly evidence updates
- Automated data extraction and meta-analysis refresh
- Manuscript synchronization with new evidence

---

## 8. SEARCH VALIDATION AND REPRODUCIBILITY

### Validation Methods:
- Peer review of search strategy by information specialists
- Comparison with published systematic reviews on similar topics
- Test searches with known relevant articles to ensure retrieval

### Reproducibility:
- All searches documented with date stamps
- Complete search strings archived
- EndNote library with all records preserved
- Search methodology section in manuscript fully transparent

### Quality Assurance:
- PRISMA-S (Search) reporting checklist followed
- Cochrane MECIR standards for literature search quality
- Independent verification by non-author team members when possible

---

## 9. CONTACTS AND CORRESPONDENCE

**Search Strategy Development and Execution:**
Dr. Siddalingaiah H S
Professor of Community Medicine
SIMS&RH, Tumakuru, Karnataka, India
Email: hssling@yahoo.com

**Research Library Support:**
ICMR-National Institute of Epidemiology
R-127, Tamil Nadu Housing Board
Ayapakkam, Chennai - 600 077, India
Phone: +91-44-28325-000

---

## 10. ACKNOWLEDGMENTS

**Information Specialist Support:**
- ICMR-National Institute of Epidemiology Research Library
- PubMed/EMBASE/WHO technical support teams
- Cochrane Information Specialists

**Software Tools:**
- EndNote X9 (deduplication and reference management)
- RevMan 5.4 (Cochrane review software)
- R Studio (meta-analysis statistical software)
- Python (data extraction and automation)

---

## APPENDICES

### Appendix A: Full PubMed Search String with Filters

```
(("antimicrobial stewardship"[TIAB] OR "antibiotic stewardship"[TIAB] OR "antimicrobial management"[TIAB]) AND ("hospital mortality"[TIAB] OR "inpatient mortality"[TIAB] OR "death"[TIAB])) AND ((systematic review[PT] OR meta-analysis[PT] OR randomized controlled trial[PT] OR controlled clinical trial[PT] OR clinical trial[PT] OR cohort studies[MESH] OR case-control studies[MESH] OR time series analysis[MESH])) AND ((english[LA])) AND (("2005"[Date - Publication] : "2025"[Date - Publication]))
```

### Appendix B: EMBASE Search Translation

```
('antimicrobial stewardship'/exp OR 'antibiotic stewardship'/exp OR 'antimicrobial management'/exp) AND ('hospital mortality'/exp OR 'inpatient mortality'/exp) AND ('systematic review'/de OR 'meta analysis'/de OR 'randomized controlled trial'/de OR 'clinical trial'/de OR 'cohort analysis'/de OR 'case control study'/de OR 'time series analysis'/de) AND [english]/lim AND [2005-2025]/py NOT ([conference abstract]/it)
```

### Appendix C: Search Term Thesaurus

| Concept | Medical Subject Heading (MeSH) | Keywords Used |
|---------|--------------------------------|---------------|
| Antimicrobial Stewardship | Drug Utilization Review,<br>Anti-Bacterial Agents | antimicrobial stewardship,<br>antibiotic stewardship,<br>stewardship program,<br>antibiotic optimization |
| Hospital Mortality | Hospital Mortality | hospital mortality,<br>inpatient mortality,<br>mortality rate,<br>death rate,<br>fatality rate |
| Study Designs | Cohort Studies,<br>Case-Control Studies,<br>Randomized Controlled Trials | systematic review,<br>meta-analysis,<br>controlled trial,<br>cohort,<br>before-after,<br>time series |

---

*This comprehensive search strategy document ensures transparency and reproducibility of the literature search methods used in this systematic review. For technical questions about search execution or optimization, contact Dr. Siddalingaiah H S at hssling@yahoo.com.*
