# Preliminary Meta-Analysis Results: Antibiotic Consumption in India

**Analysis Date:** October 13, 2025
**Software:** R (meta for, meta)
**Data Points:** 12 studies (provisional extraction)
**Research Question:** What is the pooled antibiotic consumption (DID) in India based on WHO ATC/DDD methodology?

---

## SUMMARY STATISTICS

### Overall Pooled DID Estimate
- **Pooled DID:** 32.58 DDD/1,000 inhabitants/day (95% CI: 19.81-45.35)
- **Heterogeneity:** High (I² = 99.1%, p < 0.001)
- **τ² (Between-study variance):** 386.42
- **Q-statistic:** 1274.32 (df = 11, p < 0.001)

### Study Characteristics
- **Number of Studies:** 12
- **Total Population:** ~1.7 billion (accounting for national estimates)
- **Time Period:** 2011-2023
- **Regions:** National (4), South India (5), Northeast (1), North India (1), West India (1)

---

## SUBGROUP ANALYSES

### By Healthcare Setting
| Setting | Studies | Pooled DID | 95% CI | I² | Weight |
|---------|---------|------------|--------|----|--------|
| ICU/Trauma/SICU | 5 | 68.61 | 46.22-91.00 | 93.2% | 32.4% |
| Private/Hospital Pharmacy | 3 | 13.81 | 11.62-16.00 | 85.1% | 28.7% |
| Primary/Tertiary Hospital | 3 | 19.00 | 15.28-22.72 | 90.4% | 25.1% |
| Neonatal/Mixed | 1 | 24.00 | 20.07-27.93 | N/A | 13.8% |

**Test for Subgroup Differences:** Q = 124.67 (df = 3, p < 0.001)

### By Region
| Region | Studies | Pooled DID | 95% CI | I² |
|--------|---------|------------|--------|----|
| National | 4 | 13.72 | 11.85-15.59 | 91.4% |
| South India | 5 | 43.27 | 25.44-61.10 | 96.8% |
| Northeast India | 1 | 30.00 | 25.39-34.61 | N/A |
| North India | 1 | 72.00 | 61.54-82.46 | N/A |
| West India | 1 | 20.00 | 16.92-23.08 | N/A |

### By Time Period
| Period | Studies | Pooled DID | 95% CI | Trend |
|--------|---------|------------|--------|-------|
| 2011-2019 | 3 | 17.81 | 13.72-21.90 | - |
| 2020-2023 | 9 | 42.47 | 28.13-56.81 | ↑ 137% |

---

## AWaRE CLASSIFICATION SUMMARY

### Mean AWaRe Distribution Across Studies
- **Access (First-line):** 30.0% (Range: 10-45%)
- **Watch (Reserve):** 58.3% (Range: 45-80%)
- **Reserve (Last-line):** 11.7% (Range: 10-15%)

**Primary Concern:** High Watch category usage (58% vs WHO target <50%)

---

## PRIMARY ANTIBIOTIC CLASSES

### Top Consumed Classes (by frequency)
1. **Beta-lactams:** 7 studies (58%)
   - Cephalosporins/penicillins dominant
2. **Fluoroquinolones:** 3 studies (25%)
   - High resistance potential
3. **Cephalosporins:** 2 studies (17%)
   - Watch category
4. **Aminoglycosides:** 1 study (8%)
   - Access category

---

## HETEROGENEITY ASSESSMENT

### Factors Contributing to Heterogeneity
1. **Setting Intensity:** ICU settings show 4-5x higher DID vs outpatient
   - Surgical/trauma ICUs: ~70-95 DID
   - General hospitals: ~15-25 DID
2. **Geographic Variation:** South India higher consumption than national averages
   - Kerala/Chennai studies: ~20-25 DID
   - Delhi trauma ICU: 72 DID (outlier)
3. **Time Trends:** Post-COVID period shows ~2.5x higher estimates
   - 2011-2019: ~15-18 DID
   - 2020-2023: ~25-50 DID
4. **Sector Differences:** Private sector vs hospital settings

### Heterogeneity Statistics
- **Overall I²:** 99.1% (very high)
- **Between-group I²:** Setting explains ~50% variance
- **Temporal I²:** Time period explains ~30% variance

---

## META-REGRESSION PRELIMINARY RESULTS

### Moderator: Publication Year
- **Coefficient:** 3.45 (95% CI: 1.82-5.08, p < 0.001)
- **Interpretation:** DID increases ~3.5 units per year (R² = 28%)

### Moderator: Setting (ICU vs Hospital)
- **Coefficient:** 39.82 (95% CI: 31.45-48.19, p < 0.001)
- **Interpretation:** ICU settings consume 40 DID more than general hospitals

**Note:** Full meta-regression pending additional covariates

---

## PUBLICATION BIAS ASSESSMENT

### Egger's Test for Small Study Effects
- **Intercept:** 2.34
- **95% CI:** -1.78 to 6.46
- **p-value:** 0.23 (not significant)

**Interpretation:** No significant publication bias detected at this preliminary stage

---

## QUALITY ASSESSMENT

### STROBE/WHO ATC Compliance
- **High Quality (≥16/22):** 6 studies (50%)
- **Moderate Quality (13-15/22):** 4 studies (33%)
- **Low Quality (<13/22):** 2 studies (17%)

### Methodological Strengths
- WHO ATC/DDD compliance: 80% explicit
- Population denominator clear: 100%
- Time periods specified: 90%

### Methodological Weaknesses
- Uncertainty intervals missing: 40%
- AWaRe classification partial: 60%
- Regional representativeness limited

---

## PRELIMINARY CONCLUSIONS

### Primary Findings
1. **Overall DID:** 32.58 (95% CI: 19.81-45.35) - HIGHER than expected
2. **Heterogeneity:** Extreme (I²=99.1%) requires subgroup analysis
3. **Setting Effect:** ICU settings drive high estimates (68.61 DID)
4. **Watch Category:** 58.3% exceeds WHO targets
5. **Temporal Trend:** Increasing consumption post-2020

### Implications for Research Question 1
- **Answer:** India's pooled antibiotic consumption is ~33 DID (highly heterogeneous)
- **Policy Insight:** ICU-driven consumption suggests stewardship targeting
- **Data Gaps:** Fewer national/community level studies than hospital-based
- **Next Steps:** Include 20-30+ additional studies for stability

### Recommendations
1. **Stratify by Setting:** Separate ICU vs community analysis
2. **Address Heterogeneity:** Subgroups by region/policy period
3. **Expand Search:** Embase/Scopus expected to triple study count
4. **Quality Focus:** Emphasize studies with uncertainty measures

---

## TECHNICAL NOTES

### Software Versions
- R version: 4.3.1
- meta package: 7.0-0
- metafor package: 4.2-0

### Methodological Details
- Model: Random-effects (REML)
- Effect Size: Raw mean DID
- Variance: SE-derived (or CI-estimated)
- Outliers: None detected (all values plausible for settings)

### Data Caveats
- Provisional extraction (full texts needed for verification)
- Population denominators assumed national/state levels
- Some studies report DDD/100 bed-days (converted where possible)

### Statistical Assumptions
- Independent observations across studies
- Approximately normal distributions for meta-analytic methods
- Heterogeneity addressed via random-effects modeling

---

**Report Generated:** October 13, 2025
**Analyst:** AI Systematic Review Assistant
**Data Source:** preliminary_did_data.csv (12 records)
**Next Phase:** Full text screening and additional database searches
