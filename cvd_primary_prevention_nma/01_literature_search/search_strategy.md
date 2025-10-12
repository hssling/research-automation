# Literature Search Strategy: CVD Primary Prevention Network Meta-Analysis

## Search Strategy Development

### Search Team
- **Lead Search Strategist**: Dr Priya Sharma, MD, PhD
- **Information Specialist**: Dr Michael Chen, MD
- **Technical Support**: Automated Research Systems Team

### Search Strategy Version
- **Version**: 1.0
- **Date**: October 12, 2025
- **Previous Versions**: None

## Database Selection Rationale

### Primary Databases
1. **PubMed/MEDLINE** - Primary biomedical literature source
2. **Embase** - Comprehensive drug and device coverage
3. **Cochrane CENTRAL** - High-quality controlled trials
4. **Web of Science** - Multidisciplinary coverage with citation tracking

### Secondary Databases
1. **Scopus** - Alternative to Web of Science
2. **CINAHL** - Nursing and allied health literature
3. **ClinicalTrials.gov** - Ongoing and completed trials
4. **WHO ICTRP** - International trial registry

### Grey Literature Sources
1. **Conference Proceedings**: AHA, ESC, ACC, ADA, ASN
2. **Regulatory Documents**: FDA, EMA, PMDA submissions
3. **Dissertation Databases**: ProQuest, EThOS
4. **Preprint Servers**: medRxiv, bioRxiv, SSRN

## Search Terms Development

### Population Search Terms

#### Primary Prevention Terms
- "primary prevention"[tiab]
- "high-risk"[tiab]
- "elevated risk"[tiab]
- "cardiovascular risk"[tiab]
- "CVD risk"[tiab]
- "ASCVD risk"[tiab]

#### Risk Factor Terms
- "diabetes"[tiab]
- "diabetes mellitus"[tiab]
- "type 2 diabetes"[tiab]
- "chronic kidney disease"[tiab]
- "CKD"[tiab]
- "renal insufficiency"[tiab]
- "hypertension"[tiab]
- "dyslipidemia"[tiab]
- "hypercholesterolemia"[tiab]

#### Risk Assessment Terms
- "ASCVD risk score"[tiab]
- "Framingham risk score"[tiab]
- "pooled cohort equation"[tiab]
- "risk stratification"[tiab]
- "risk assessment"[tiab]

### Intervention Search Terms

#### Statin Therapy
- "statin"[tiab]
- "atorvastatin"[tiab]
- "rosuvastatin"[tiab]
- "simvastatin"[tiab]
- "pravastatin"[tiab]
- "fluvastatin"[tiab]
- "lovastatin"[tiab]
- "pitavastatin"[tiab]

#### Non-Statin Lipid Therapy
- "ezetimibe"[tiab]
- "PCSK9 inhibitor"[tiab]
- "evolocumab"[tiab]
- "alirocumab"[tiab]
- "inclisiran"[tiab]
- "bempedoic acid"[tiab]

#### Anti-hypertensive Therapy
- "ACE inhibitor"[tiab]
- "angiotensin receptor blocker"[tiab]
- "calcium channel blocker"[tiab]
- "diuretic"[tiab]
- "beta blocker"[tiab]
- "ARB"[tiab]
- "ACEI"[tiab]
- "CCB"[tiab]

#### Anti-platelet Therapy
- "aspirin"[tiab]
- "antiplatelet"[tiab]
- "clopidogrel"[tiab]
- "ticagrelor"[tiab]
- "prasugrel"[tiab]

#### Combination Therapy
- "polypill"[tiab]
- "fixed dose combination"[tiab]
- "combination therapy"[tiab]
- "dual therapy"[tiab]
- "triple therapy"[tiab]

#### Lifestyle Interventions
- "lifestyle intervention"[tiab]
- "lifestyle modification"[tiab]
- "dietary intervention"[tiab]
- "exercise intervention"[tiab]
- "weight management"[tiab]
- "smoking cessation"[tiab]
- "behavioral intervention"[tiab]

### Outcome Search Terms

#### Mortality Outcomes
- "all-cause mortality"[tiab]
- "cardiovascular mortality"[tiab]
- "cardiovascular death"[tiab]
- "total mortality"[tiab]
- "overall mortality"[tiab]

#### Cardiovascular Events
- "MACE"[tiab]
- "major adverse cardiovascular events"[tiab]
- "myocardial infarction"[tiab]
- "heart attack"[tiab]
- "stroke"[tiab]
- "cerebrovascular accident"[tiab]
- "revascularization"[tiab]
- "PCI"[tiab]
- "CABG"[tiab]
- "coronary artery bypass"[tiab]
- "percutaneous coronary intervention"[tiab]

#### Safety Outcomes
- "adverse events"[tiab]
- "serious adverse events"[tiab]
- "myopathy"[tiab]
- "rhabdomyolysis"[tiab]
- "liver dysfunction"[tiab]
- "new onset diabetes"[tiab]
- "bleeding"[tiab]
- "major bleeding"[tiab]

### Study Design Terms

#### Clinical Trial Terms
- "randomized controlled trial"[pt]
- "controlled clinical trial"[pt]
- "randomized"[tiab]
- "clinical trial"[tiab]
- "trial"[tiab]
- "RCT"[tiab]

#### Observational Study Terms (if applicable)
- "cohort study"[tiab]
- "prospective study"[tiab]
- "retrospective study"[tiab]
- "observational study"[tiab]

## Complete Search Strategies

### PubMed/MEDLINE Search Strategy

#### Search 1: Primary Prevention + Statins
```sql
("primary prevention"[tiab] OR "high-risk"[tiab] OR "elevated risk"[tiab] OR "cardiovascular risk"[tiab] OR "ASCVD risk"[tiab] OR diabetes[tiab] OR "chronic kidney disease"[tiab] OR "CKD"[tiab]) AND
(statin[tiab] OR atorvastatin[tiab] OR rosuvastatin[tiab] OR simvastatin[tiab] OR pravastatin[tiab] OR fluvastatin[tiab] OR lovastatin[tiab] OR pitavastatin[tiab]) AND
("all-cause mortality"[tiab] OR "cardiovascular mortality"[tiab] OR MACE[tiab] OR "myocardial infarction"[tiab] OR stroke[tiab] OR "major adverse cardiovascular events"[tiab]) AND
("randomized controlled trial"[pt] OR "controlled clinical trial"[pt] OR randomized[tiab] OR "clinical trial"[tiab])
```

#### Search 2: Primary Prevention + PCSK9 Inhibitors
```sql
("primary prevention"[tiab] OR "high-risk"[tiab] OR "elevated risk"[tiab] OR "cardiovascular risk"[tiab] OR "ASCVD risk"[tiab] OR diabetes[tiab] OR "chronic kidney disease"[tiab] OR "CKD"[tiab]) AND
("PCSK9 inhibitor"[tiab] OR evolocumab[tiab] OR alirocumab[tiab] OR inclisiran[tiab]) AND
("all-cause mortality"[tiab] OR "cardiovascular mortality"[tiab] OR MACE[tiab] OR "myocardial infarction"[tiab] OR stroke[tiab]) AND
("randomized controlled trial"[pt] OR "controlled clinical trial"[pt] OR randomized[tiab] OR "clinical trial"[tiab])
```

#### Search 3: Primary Prevention + Lifestyle Interventions
```sql
("primary prevention"[tiab] OR "high-risk"[tiab] OR "elevated risk"[tiab] OR "cardiovascular risk"[tiab] OR "ASCVD risk"[tiab] OR diabetes[tiab] OR "chronic kidney disease"[tiab] OR "CKD"[tiab]) AND
("lifestyle intervention"[tiab] OR "lifestyle modification"[tiab] OR "dietary intervention"[tiab] OR "exercise intervention"[tiab] OR "Mediterranean diet"[tiab] OR "DASH diet"[tiab] OR "weight management"[tiab]) AND
("all-cause mortality"[tiab] OR "cardiovascular mortality"[tiab] OR MACE[tiab] OR "myocardial infarction"[tiab] OR stroke[tiab]) AND
("randomized controlled trial"[pt] OR "controlled clinical trial"[pt] OR randomized[tiab] OR "clinical trial"[tiab])
```

#### Search 4: Primary Prevention + Polypills
```sql
("primary prevention"[tiab] OR "high-risk"[tiab] OR "elevated risk"[tiab] OR "cardiovascular risk"[tiab] OR "ASCVD risk"[tiab] OR diabetes[tiab] OR "chronic kidney disease"[tiab] OR "CKD"[tiab]) AND
(polypill[tiab] OR "fixed dose combination"[tiab] OR "combination therapy"[tiab]) AND
("all-cause mortality"[tiab] OR "cardiovascular mortality"[tiab] OR MACE[tiab] OR "myocardial infarction"[tiab] OR stroke[tiab]) AND
("randomized controlled trial"[pt] OR "controlled clinical trial"[pt] OR randomized[tiab] OR "clinical trial"[tiab])
```

### Embase Search Strategy

#### Search 1: Primary Prevention + All Interventions
```sql
('primary prevention':ti,ab OR 'high risk':ti,ab OR 'elevated risk':ti,ab OR 'cardiovascular risk':ti,ab OR 'ASCVD risk':ti,ab OR diabetes:ti,ab OR 'chronic kidney disease':ti,ab OR 'CKD':ti,ab) AND
(statin:ti,ab OR atorvastatin:ti,ab OR rosuvastatin:ti,ab OR ezetimibe:ti,ab OR 'PCSK9 inhibitor':ti,ab OR evolocumab:ti,ab OR alirocumab:ti,ab OR polypill:ti,ab OR 'lifestyle intervention':ti,ab) AND
('all cause mortality':ti,ab OR 'cardiovascular mortality':ti,ab OR MACE:ti,ab OR 'myocardial infarction':ti,ab OR stroke:ti,ab) AND
(randomized controlled trial:it OR 'controlled clinical trial':it OR randomized:ti,ab OR 'clinical trial':ti,ab)
```

### ClinicalTrials.gov Search Strategy

#### Basic Search
- **Condition**: "cardiovascular disease" OR "diabetes" OR "chronic kidney disease"
- **Intervention**: statin OR ezetimibe OR PCSK9 OR evolocumab OR alirocumab OR polypill OR lifestyle OR exercise OR diet
- **Outcome Measures**: mortality OR MACE OR myocardial infarction OR stroke
- **Study Type**: Interventional Studies
- **Status**: Completed, Active, not recruiting
- **Phase**: Phase 2, Phase 3, Phase 4

#### Advanced Search
```sql
SEARCH: (cardiovascular OR diabetes OR kidney) AND (statin OR ezetimibe OR PCSK9 OR polypill OR lifestyle) AND (mortality OR MACE OR infarction OR stroke) | INTERVENTIONAL | PHASE:2 OR PHASE:3 OR PHASE:4
```

### Web of Science Search Strategy

#### Topic Search
```sql
TS=("primary prevention" OR "high-risk" OR "cardiovascular risk" OR diabetes OR "chronic kidney disease") AND
TS=(statin OR atorvastatin OR rosuvastatin OR ezetimibe OR PCSK9 OR evolocumab OR alirocumab OR polypill OR "lifestyle intervention") AND
TS=(mortality OR MACE OR "myocardial infarction" OR stroke) AND
TS=(randomized OR "clinical trial" OR RCT)
```

## Search Validation and Testing

### Search Strategy Validation
1. **Sensitivity Testing**: Ensure known relevant studies are captured
2. **Specificity Testing**: Minimize irrelevant results
3. **Database Comparison**: Cross-validate results across databases

### Known Relevant Studies for Validation
1. **JUPITER Trial**: Rosuvastatin for primary prevention
2. **HOPE-3 Trial**: Polypill for primary prevention
3. **FOURIER Trial**: Evolocumab for primary prevention
4. **ODYSSEY OUTCOMES**: Alirocumab for primary prevention
5. **TIPS-3 Trial**: Polypill strategy

### Search Syntax Optimization
- **Boolean Operators**: AND, OR, NOT used appropriately
- **Truncation**: Use of * for word variants
- **Proximity Operators**: NEAR, ADJ for phrase searching
- **Field Tags**: Title, abstract, MeSH terms

## Search Execution Plan

### Initial Search Execution
- **Date Range**: 1990 - Present (statin era)
- **Language**: English (primary), with multilingual abstract screening
- **Update Schedule**: Monthly updates for new publications

### Search Results Management
1. **Deduplication**: Automated removal of duplicate records
2. **Screening**: Two-stage process (title/abstract, full-text)
3. **Documentation**: Complete audit trail of search decisions

### Search Results Export
- **Format**: RIS, EndNote, CSV, JSON
- **Fields**: All available metadata
- **Frequency**: Weekly exports during active searching

## Quality Assurance

### Search Quality Metrics
- **Recall**: Percentage of known relevant studies found
- **Precision**: Percentage of retrieved studies that are relevant
- **Number Needed to Read**: Average studies to find one relevant

### Peer Review of Search Strategy
- **PRESS Checklist**: Peer Review of Electronic Search Strategies
- **Search Strategy Review**: Independent review by information specialist
- **Documentation**: Complete transparency in search methods

## Updates and Amendments

### Search Strategy Updates
- **Monthly Review**: Assess need for new search terms
- **Annual Comprehensive Review**: Complete strategy reassessment
- **Emerging Interventions**: Add new drugs/therapies as they become available

### Version Control
- **Version 1.0**: Initial search strategy (October 12, 2025)
- **Future Versions**: Documented changes with rationale

## Documentation Requirements

### Search Report Components
1. **Search Strategy**: Complete syntax for each database
2. **Search Dates**: Execution dates and update schedule
3. **Results Summary**: Number of hits per database
4. **Validation Results**: Sensitivity and specificity metrics
5. **PRISMA-S Checklist**: Reporting standards compliance

### Supplementary Files
1. **Search Strategy Appendix**: Detailed database-specific strategies
2. **Search Validation Report**: Methods and results of validation
3. **Update Log**: Record of strategy modifications

## References

1. **PRESS Guideline**: McGowan J, Sampson M, Salzwedel DM, et al. PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement. J Clin Epidemiol 2016;75:40-6.
2. **PRISMA-S**: Rethlefsen ML, Kirtley S, Waffenschmidt S, et al. PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews. Syst Rev 2021;10(1):39.
3. **Cochrane Handbook**: Higgins JPT, Thomas J, Chandler J, et al. Cochrane Handbook for Systematic Reviews of Interventions version 6.3. Cochrane, 2022.

## Contact Information

**Search Strategy Coordinator**: Dr Priya Sharma
**Email**: priya.sharma@cvd-prevention-nma.org
**Institution**: Shridevi Institute of Medical Sciences and Research Hospital, Tumakuru

---

**Search Strategy Word Count**: 1,847
**Tables**: 0
**Figures**: 0
**References**: 3
