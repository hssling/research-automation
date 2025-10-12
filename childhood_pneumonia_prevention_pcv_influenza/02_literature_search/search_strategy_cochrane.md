# Cochrane CENTRAL Search Strategy: PCV Effectiveness Studies

## Search Strategy Details
**Search Date:** October 12, 2025
**Database:** Cochrane Central Register of Controlled Trials (CENTRAL)
**Date Range:** 2000 - present
**Language:** English

## Primary Search Strategy

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

## Secondary Search Strategy (Broader capture)

```
(pneumococcal conjugate vaccine OR PCV) AND (infants OR children OR preschool) AND (pneumonia OR "respiratory infection" OR mortality OR hospitalization OR "lower respiratory tract infection") AND (schedule OR influenza) AND (randomized OR trial OR systematic review OR meta-analysis)
```

## Filters Applied
- Trial-type filters: Randomized Controlled Trials, Quasi-Randomized Studies
- Age filters: Infants (0 to 23 months), Children (2 to 12 years)
- Publication date: 2000 - present
- Language: English

## Expected Results from CENTRAL
- Published RCTs not yet indexed in PubMed
- Conference abstracts and proceedings
- Trials published in non-Index Medicus journals
- Cluster randomized trials
- Quasi-experimental designs
- Economic evaluations with clinical outcomes

## Manual Review Criteria
**High Priority for Full-Text Review:**
- Trials comparing 2+1 vs 3+0 schedules
- Studies with radiologically confirmed pneumonia outcomes
- Multi-country evaluations
- Cluster randomized trials from LMICs
- Studies with influenza co-administration

**Medium Priority:**
- Vaccine effectiveness studies (pre-post design)
- Observational cohort studies with strong design
- Cost-effectiveness analyses with epidemiological data

**Low Priority / Exclude:**
- Laboratory immunogenicity studies only
- Single-arm vaccine trials
- Modeling studies without empirical data
- Safety surveillance only

## Export Strategy
- Export all records to EndNote/Reference Manager
- Export format: RIS or BibTeX
- Include abstracts and keywords
- Flag duplicates for removal

## Integration with PubMed Results
1. Import CENTRAL records
2. Merge with PubMed references
3. Remove exact duplicates
4. Conduct duplicate screening for similar studies
5. Create single master reference database

---

**Next Steps:**
1. Execute CENTRAL search via Cochrane Library
2. Export results in standard format
3. Merge with PubMed results
4. Begin title/abstract screening
5. Track PRISMA flow diagram metrics
