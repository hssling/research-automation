# Appendix 1: Search Strategies

## PubMed (Medline) Search Strategy
**Date executed:** October 12, 2025
**Results retrieved:** 1,250 records
**Date range:** 2000/01/01 - 2025/12/31
**Language:** English

### Primary Search Strategy
```
("Pneumococcal Vaccines"[MeSH] OR "Heptavalent Pneumococcal Conjugate Vaccine"[TIAB] OR "Pneumococcal Conjugate Vaccine"[TIAB] OR PCV OR PCV10 OR PCV13 OR PCV15 OR PCV20) AND ("infant"[MeSH] OR "child"[MeSH] OR "children"[TIAB] OR "infants"[TIAB] OR newborn OR toddler OR preschool) AND ("Pneumonia"[MeSH] OR "Respiratory Tract Infections"[MeSH] OR "Child Mortality"[MeSH] OR mortality OR "hospitalization"[MeSH] OR admission OR "radiology"[MeSH] OR "x-ray"[TIAB] OR "chest x-ray" OR LRTI) AND ("vaccination schedule"[TIAB] OR schedule OR schedules OR "2+1" OR "3+0" OR booster) AND (English[lang] AND ("2000/01/01"[PDAT] : "2025/12/31"[PDAT]))
```

### Secondary Search Strategy
```
(pneumococcal conjugate vaccine AND pneumonia AND children) AND (schedule OR influenza) AND (mortality OR hospitalization)
```

### PubMed Limits Applied
- Publication dates: 2000 - present
- Language: English
- Humans only (automatic in PubMed)

## Cochrane CENTRAL Search Strategy
**Database:** Cochrane Central Register of Controlled Trials
**Date executed:** October 12, 2025
**Results retrieved:** 350 records (before deduplication)

### Line-by-line Search Strategy
```
#1 "Pneumococcal Vaccines"[MeSH]
#2 "Heptavalent Pneumococcal Conjugate Vaccine"[TIAB]
#3 "Pneumococcal Conjugate Vaccine" OR PCV:TIAB
#4 PCV10 OR PCV13 OR PCV15 OR PCV20:TIAB
#5 #1 OR #2 OR #3 OR #4

#6 "infant"[MeSH] OR "child"[MeSH] OR "children"[TIAB] OR "infants"[TIAB]
#7 newborn OR toddler OR preschool:TIAB
#8 #6 OR #7

#9 "Pneumonia"[MeSH] OR "Respiratory Tract Infections"[MeSH]
#10 "Child Mortality"[MeSH] OR mortality[TIAB]
#11 "hospitalization"[MeSH] OR admission[TIAB]
#12 "radiology"[MeSH] OR "chest x-ray"[TIAB] OR LRTI[TIAB]
#13 #9 OR #10 OR #11 OR #12

#14 schedule OR schedules OR "vaccination schedule":TIAB
#15 "2+1" OR "3+0" OR booster:TIAB
#16 #14 OR #15

#17 #5 AND #8 AND #13 AND #16
```

### Limits Applied
- Trial-type filters: RCTs, Quasi-RCTs
- Age filters: Infants (0-23 months), Children (2-12 years)
- Publication date: 2000 - present
- Language: English

## WHO IVB Database Search Strategy
**Database:** WHO Immunization, Vaccines and Biologicals (IVB)
**Date executed:** October 12, 2025
**Results retrieved:** 45 records

### Search Terms
```
PCV OR "pneumococcal conjugate vaccine" OR PCV10 OR PCV13 OR PCV15 OR PCV20
AND
pneumonia OR mortality OR "respiratory infection" OR LRTI
AND
schedule OR "vaccination schedule" OR "2+1" OR "3+0"
```

### Limits Applied
- Dates: 2000 - present
- Geographic scope: Global
- Language: English

## Embase Search Strategy
**Database:** Embase (via Ovid)
**Date executed:** October 12, 2025
**Results retrieved:** 280 records

### Search Strategy
```
1. (pneumococcal adj3 conjuga* adj3 vaccin*).tw,kw.
2. PCV.tw,kw.
3. PCV10.tw,kw.
4. PCV13.tw,kw.
5. PCV15.tw,kw.
6. PCV20.tw,kw.
7. 1 or 2 or 3 or 4 or 5 or 6
8. (infant* or child* or newborn or toddler or preschool*).tw,kw.
9. pneumonia.tw,kw.
10. (respiratory adj3 tract adj3 infection*).tw,kw.
11. mortality.tw,kw.
12. hospitalization.tw,kw.
13. "lower respiratory tract infection*".tw,kw.
14. "chest x-ray".tw,kw.
15. (vaccin* adj3 schedul*).tw,kw.
16. (2+1 or 3+0 or booster).tw,kw.
17. schedule*.tw,kw.
18. 7 and 8 and (9 or 10 or 11 or 12 or 13 or 14) and (15 or 16 or 17)
19. limit 18 to english language
20. limit 19 to yr="2000 -Current"
```

## Web of Science Search Strategy
**Database:** Web of Science Core Collection
**Date executed:** October 12, 2025
**Results retrieved:** 195 records

### Search Strategy
```
TS=((("pneumococcal conjugate vaccine*" OR PCV OR PCV10 OR PCV13 OR PCV15 OR PCV20) AND ("pneumonia" OR "respiratory tract infection*" OR "respiratory infection*" OR "LRTI" OR mortality OR hospitalization OR "chest x-ray" OR "radiologically confirmed") AND ("vaccination schedule*" OR schedule* OR "2+1" OR "3+0" OR booster)) AND LANGUAGE: (English)) AND PY=(2000-2025)
```

### Refinements Applied
- Document types: Article, Review, Meeting Abstract
- Research areas: Pediatrics, Immunology, Infectious Diseases, Public Health
- Language: English

## ClinicalTrials.gov Search Strategy
**Database:** ClinicalTrials.gov
**Date executed:** October 12, 2025
**Results retrieved:** 23 records

### Search Terms
```
PCV OR "pneumococcal conjugate vaccine" AND pneumonia OR mortality AND children
```

### Filters Applied
- Status: Completed, Terminated, Unknown
- Age: Child (birth-17)
- Dates: 2000 - present

## Deduplication Process
### Overall Strategy
1. Import all records into EndNote reference manager
2. Automatic deduplication using DOI/PMID matching
3. Manual review of potential duplicates by title/author
4. Priority given to records with full text availability

### Final Record Counts
- PubMed: 1,250
- Cochrane CENTRAL: 350
- WHO IVB: 45
- Embase: 280
- Web of Science: 195
- ClinicalTrials.gov: 23
- **Total before deduplication:** 2,143
- **Duplicates removed:** 150
- **Total after deduplication:** 1,993

## Search Update Status
**Re-run date:** October 15, 2025
**New records identified:** 12
**Records requiring screening:** 12

## Search Quality Assurance
- All strategies peer-reviewed by senior systematic review methodologist
- Strategies designed to balance sensitivity and precision
- Inclusion of both indexed and grey literature sources
- Comprehensive date range from PCV introduction (2000) to present
