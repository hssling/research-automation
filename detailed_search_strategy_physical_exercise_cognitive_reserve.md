# Detailed Search Strategy: Physical Activity Modalities and Cognitive Reserve in Aging - Network Meta-Analysis

## Research Question
Which type of physical activity (aerobic exercise, resistance training, mind-body exercises like yoga or tai chi) most effectively enhances cognitive reserve and delays dementia onset in adults over 60?

---

## Search Databases
1. **PubMed/MEDLINE** (via NCBI Entrez)
2. **EMBASE** (via Elsevier)
3. **Cochrane Central Register of Controlled Trials (CENTRAL)**
4. **PsycINFO** (via EBSCOhost)
5. **Web of Science Core Collection**
6. **Manual search of reference lists**
7. **Gray literature**: ClinicalTrials.gov, WHO ICTRP, Google Scholar

---

## Core Search Strategy

### PubMed Strategy
```
# Population
("aged"[MeSH Terms] OR aged OR elderly OR senior OR geriatric OR "older adult*" OR "older people" OR "older person*")

# Intervention
("exercise"[MeSH Terms] OR "physical activity" OR training OR aerobic OR "cardiovascular exercise" OR resistance[tg] OR "strength training" OR "weight training" OR yoga OR tai OR chi OR "tai chi" OR "mind-body" OR "mind body")

# Outcome
("cognitive reserve"[tiab] OR cognition[MeSH Terms] OR "cognitive function" OR "cognitive decline" OR memory OR executive[tg] OR "executive function" OR "processing speed" OR "attention")
# OR
(dementia[MeSH Terms] OR Alzheimer OR "Alzheimer's") AND ("prevention" OR "delay" OR "protect*"))

# Study type
(("randomized controlled trial"[pt] OR "controlled clinical trial"[pt] OR "randomized"[tiab] OR "randomly"[tiab] OR "trial"[tiab]) AND adults[pt])

# Combination (Boolean operators)
# P = Population terms
# I = Intervention terms
# O = Outcome terms
# S = Study type terms

(P) AND (I) AND (O) AND (S)
```

**Full PubMed Query:**
```
(("aged"[MeSH Terms] OR aged OR elderly OR senior OR geriatric OR "older adult*" OR "older people" OR "older person*") AND ("exercise"[MeSH Terms] OR "physical activity" OR training OR aerobic OR "cardiovascular exercise" OR resistance[tg] OR "strength training" OR "weight training" OR yoga OR tai OR chi OR "tai chi" OR "mind-body" OR "mind body") AND (("cognitive reserve"[tiab] OR cognition[MeSH Terms] OR "cognitive function" OR "cognitive decline" OR memory OR executive[tg] OR "executive function" OR "processing speed" OR "attention") OR ((dementia[MeSH Terms] OR Alzheimer OR "Alzheimer's") AND ("prevention" OR "delay" OR "protect*"))) AND (("randomized controlled trial"[pt] OR "controlled clinical trial"[pt] OR "randomized"[tiab] OR "randomly"[tiab] OR "trial"[tiab]) AND adults[pt]))
```

### EMBASE Strategy
```
# Population
'exp'/'aged'/ OR aged:ti,ab OR elderly:ti,ab OR senior:ti,ab OR geriatric:ti,ab OR 'older adult*':ti,ab OR 'older people':ti,ab OR 'older person*':ti,ab

# Intervention
'exp'/'exercise'/ OR 'physical activity':ti,ab OR training:ti,ab OR aerobic:ti,ab OR 'cardiovascular exercise':ti,ab OR resistance AND training OR 'strength training':ti,ab OR 'weight training':ti,ab OR yoga:ti,ab OR tai:ti,ab OR chi:ti,ab OR 'tai chi':ti,ab OR 'mind-body':ti,ab OR 'mind body':ti,ab

# Outcome
'cognitive reserve':ti,ab OR exp cognition/ OR 'cognitive function':ti,ab OR 'cognitive decline':ti,ab OR memory:ti,ab OR exp 'executive function'/ OR 'processing speed':ti,ab OR attention:ti,ab
# OR
exp dementia/ OR alzheimer:ti,ab OR 'alzheimer*'':ti,ab AND prevention:ti,ab OR delay:ti,ab OR protection:ti,ab

# Study type
(randomized-controlled-trial/exp OR 'randomized controlled trial':ti,ab OR 'controlled clinical trial':ti,ab OR randomized:ti,ab OR randomly:ti,ab OR trial:ti,ab) AND adult/exp

# Full EMBASE query (similar structure)
```

### Cochrane CENTRAL Strategy
Similar to PubMed with MeSH terms adjusted for Cochrane terminology.

### PsycINFO Strategy
```
# Population
aged OR elderly OR senior OR geriatric OR "older adult*" OR "older people" OR "older person*"

# Intervention
physical activity OR exercise OR aerobic OR resistance training OR strength training OR yoga OR tai chi OR mind-body

# Outcome
cognitive reserve OR cognitive function OR cognitive decline OR executive function OR processing speed OR memory
# OR
dementia prevention OR dementia delay OR clinical trials

# Combination: P AND I AND (O1 OR O2)
```

### Web of Science Strategy
TS=((aged OR elderly OR senior OR geriatric OR "older adult*" OR "older people" OR "older person*") AND (exercise OR "physical activity" OR aerobic OR "resistance training" OR "strength training" OR yoga OR "tai chi" OR "mind-body") AND ("cognitive reserve" OR cognition OR "cognitive function" OR "cognitive decline" OR memory OR "executive function" OR "processing speed" OR attention OR (((dementia OR Alzheimer) AND (prevention OR delay OR protection)))))

---

## Search Parameters
- **Date range**: All years (no date limitation due to novelty of the topic)
- **Language**: English only
- **Publication status**: Peer-reviewed journals (conference abstracts excluded)
- **Date searched**: September 21, 2025

---

## Search Updates
- **Update searches**: None planned (single comprehensive search for this review)
- **Grey literature**: Hand searching of reference lists, clinical trial registries

---

## Citation Management
- **Software**: Zotero (with deduplication)
- **Citation export**: RIS format from each database
- **Deduplication process**: Automated in Zotero, manual review of potential duplicates

---

## Screening Process
1. **Title screening**: Exclude clearly irrelevant articles
2. **Abstract screening**: Apply inclusion/exclusion criteria
3. **Full-text screening**: Detailed eligibility assessment
4. **Reasons for exclusion**: Documented at each stage
5. **Inter-reviewer agreement**: Kappa statistic > 0.80

---

## Data Extraction
- **Form**: Pre-piloted Excel form
- **Multiple extractions**: Two reviewers independently, followed by consensus
- **Disagreements**: Resolved by third reviewer

---

## Risk of Bias Assessment
- **Tool**: Cochrane Risk of Bias 2.0 for RCTs
- **Tool for skew**: ROBINS-I for non-randomized studies
- **Summary plots**: robo(vision software)

---

## Data Synthesis
- **Type**: Frequentist network meta-analysis using random-effects model
- **Effect measure**: Standardized mean difference for cognitive outcomes, odds ratio for dementia incidence
- **Consistency**: Design-by-treatment interaction model
- **Ranking**: Surface under the cumulative ranking curve (SUCRA)
- **Confidence**: GRADE framework for certainty in evidence

---

## Software
- **Statistical**: R (netmeta, gemtc packages)
- **Visualization**: Chart.js and D3.js for network plots
- **Reporting**: PRISMA NMA checklist
