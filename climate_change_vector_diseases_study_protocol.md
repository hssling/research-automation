# Detailed Study Protocol

**Climate Change and Vector-Borne Diseases in South Asia: A 20-Year Longitudinal Ecological Study**

---

## **1. TITLE**

**Impact of Climate Change on Malaria and Dengue Transmission in South Asia: A Longitudinal Ecological Analysis (2005-2025)**

---

## **2. BACKGROUND AND RATIONALE**

### **2.1 Public Health Context**

South Asia bears disproportionate burden of vector-borne diseases (VBDs), accounting for approximately 70% of global malaria cases and 50% of dengue cases despite representing only 25% of the world's population. The region faces accelerated climate change impacts, with projected temperature increases of 2.8°C by 2050 and substantial changes in rainfall patterns expected to affect vector biology and disease transmission dynamics.

Vector-borne diseases represent a significant economic burden, with estimated annual costs of $67 billion across South Asia, including direct healthcare costs ($27 billion) and productivity losses ($40 billion).

### **2.2 Epidemiological Rationale**

The temperature-sensitive life cycle of disease vectors creates clear epidemiological pathways linking climate change to enhanced disease transmission:

#### **Malaria Transmission Cycle:**
- **Temperature Optimum:** 25-30°C for Plasmodium falciparum development in Anopheles mosquitoes
- **Vector Biology:** Temperature increases reduce parasite development time from 26 days (20°C) to 13 days (30°C)
- **Vector Survival:** Higher temperatures increase mosquito survival and biting rates
- **Seasonal Extension:** Warmer regions expand transmission seasons

#### **Dengue Transmission Cycle:**
- **Temperature Optimum:** 28-30°C for Aedes aegypti and Aedes albopictus
- **Vector Biology:** Faster viral replication and shorter extrinsic incubation periods
- **Urban Amplification:** Warmer urban environments create persistent transmission reservoirs
- **Geographic Expansion:** Temperature increases enable vector survival in previously temperate regions

### **2.3 Research Gap**

Current evidence on climate change impacts on VBDs in South Asia is fragmented:
- Most studies cover short time periods (<10 years)
- Limited longitudinal designs with monthly resolution
- Insufficient consideration of socioeconomic confounders
- Lack of comprehensive South Asian regional analysis
- Inadequate assessment of indirect climate effects through vector control interventions

---

## **3. RESEARCH OBJECTIVES AND QUESTIONS**

### **3.1 Primary Objective**

To quantify the longitudinal association between climate change variables (temperature, rainfall variability) and vector-borne disease incidence (malaria, dengue) across South Asian countries over a 20-year period (2005-2025).

### **3.2 Primary Research Question**

**Are rising average temperatures and rainfall variability associated with increased malaria and dengue incidence across South Asian countries?**

### **3.3 Secondary Research Questions**

1. **Threshold Effects:** What are the non-linear threshold relationships between temperature and VBD transmission?
2. **Temporal Lag:** What are the distributed lag effects of climate variables on disease incidence?
3. **Regional Variation:** How do climate-disease relationships vary across different South Asian ecological zones?
4. **Attribution Analysis:** What proportion of VBD burden is attributable to climate change?
5. **Effect Modification:** How do socioeconomic factors modify climate-disease associations?
6. **Future Projections:** What are the projected impacts of climate change scenarios on VBD burden?

---

## **4. STUDY DESIGN**

### **4.1 Study Design**

**Longitudinal Ecological Study with Time Series Analysis**

- **Time Frame:** January 2005 - December 2025 (20 years, 240 months)
- **Spatial Scale:** National and sub-national levels (8 South Asian countries)
- **Analytical Framework:** Generalized Estimating Equations (GEE) with lag distributed models
- **Design Strengths:** Comprehensive temporal coverage, ecological validity, statistical power

### **4.2 Study Units**

**Geographical Units:**
- **Country Level:** Primary aggregation (Afghanistan, Bangladesh, India, Nepal, Pakistan, Sri Lanka, Bhutan, Maldives)
- **Sub-National Level:** State/province level analysis where data available
- **Temporal Units:** Monthly observations (climate) and annual observations (disease surveillance)

**Population Definition:**
- All reported malaria and dengue cases in South Asian countries
- Age-standardized incidence rates per 100,000 population
- Laboratory-confirmed and clinically diagnosed cases (as per national surveillance criteria)

---

## **5. INCLUSION AND EXCLUSION CRITERIA**

### **5.1 Inclusion Criteria**
- **Geographic:** All eight South Asian regional cooperation member states
- **Temporal:** Continuous data availability from 2005 onwards
- **Disease Surveillance:** At least 80% case reporting completeness
- **Climate Data Coverage:** Complete meteorological station coverage

### **5.2 Exclusion Criteria**
- Countries with significant data gaps (>20% missing values)
- Months with extreme outliers or data quality issues
- Non-South Asian countries included in sensitivity analyses
- Study periods before 2005 or non-ecological designs

---

## **6. DATA SOURCES AND COLLECTION METHODS**

### **6.1 Primary Climate Data Sources**

#### **Historical Climate Data:**
```r
# Climate Data Acquisition Strategy
climate_data_sources <- list(
  "WorldClim_v2.1" = list(
    format = "GeoTIFF",
    resolution = "30 arc-seconds (~1km)",
    variables = c("tavg", "tmax", "tmin", "prec"),
    temporal_coverage = "2015-2023",
    source_url = "https://worldclim.org/data/worldclim21.html"
  ),
  "CRU_TS4.06" = list(
    format = "NetCDF",
    resolution = "0.5° × 0.5° grid",
    variables = c("tmp", "pre", "wet", "frs"),
    temporal_coverage = "2005-2014",
    source_url = "https://crudata.uea.ac.uk/cru/data/hrg/"
  )
)
```

#### **Climate Variables:**
1. **Temperature Metrics (°C):**
   - Mean monthly temperature (tavg)
   - Maximum monthly temperature (tmax)
   - Minimum monthly temperature (tmin)
   - Temperature variability (standard deviation)
   - Heatwave frequency (days ≥32°C, ≥35°C, ≥38°C)

2. **Precipitation Variables (mm):**
   - Total monthly precipitation (prec)
   - Precipitation variability (coefficient of variation)
   - Number of rainy days (>1mm)
   - Extreme precipitation events (>100mm, >200mm)
   - Drought frequency (consecutive dry days)

3. **Derived Climate Indices:**
   - Standardized Precipitation Index (SPI) for drought assessment
   - Temperature Humidity Index (THI) for thermal stress
   - Palmer Drought Severity Index (PDSI) adaptation

### **6.2 Disease Surveillance Data**

#### **Malaria Data Sources:**
- **World Health Organization Global Malaria Programme**
- **National Malaria Control Programs** (India, Pakistan, Bangladesh)
- **WHO World Malaria Report** annual data
- **Global Health Data Exchange (GHDx)** repository

#### **Dengue Data Sources:**
- **World Health Organization Dengue Surveillance**
- **National Dengue Control Programs**
- **WHO DengueNet** regional reporting system
- **Pan American Health Organization** supplementary data

#### **Data Variables:**
1. **Case Counts:**
   - Confirmed malaria cases (all species)
   - Plasmodium falciparum cases
   - Plasmodium vivax cases
   - Dengue fever cases
   - Dengue hemorrhagic fever cases
   - Dengue mortality

2. **Population Denominators:**
   - Census projections by country and age group
   - WHO age-standardized world population for comparability

3. **Quality Indicators:**
   - Laboratory confirmation rates
   - Passive vs active surveillance proportions
   - Reporting completeness percentages

### **6.3 Confounding and Effect Modifier Variables**

#### **Socioeconomic Variables:**
- GDP per capita (World Bank World Development Indicators)
- Poverty rates (World Bank poverty headcount ratios)
- Healthcare access index (WHO HEACS framework)
- Literacy rates (UNESCO Institute for Statistics)

#### **Vector Control Variables:**
- Insecticide-treated net usage (Roll Back Malaria Partnership)
- Indoor residual spraying coverage (WHO spraying database)
- Larval source management intensity
- Vector surveillance capacity indicators

#### **Demographic Variables:**
- Urbanization rates (World Bank urban population data)
- Population density (Gridded Population of World v4)
- Age structure (WHO themes demographic projections)
- Migration patterns (UN Department of Economic and Social Affairs)

---

## **7. EXPOSURE ASSESSMENT STRATEGY**

### **7.1 Climate Exposure Definition**

#### **Primary Exposure Metrics:**
```r
# Primary Exposure Variables
exposures <- list(
  "Temperature" = list(
    definition = "Monthly average temperature at national level",
    units = "°C",
    optimal_range = "25-30°C for malaria; 28-30°C for dengue",
    measurement = "Station-based interpolation using inverse distance weighting"
  ),
  "Precipitation" = list(
    definition = "Total monthly precipitation with variability",
    units = "mm",
    optimal_range = "100-250mm for vector breeding sites",
    measurement = "Rain gauge calibration and satellite validation"
  )
)
```

#### **Secondary Exposure Metrics:**
1. **Temperature Extremes:** Heatwave frequency and intensity
2. **Drought Indices:** SPI and PDSI for dry season quantification
3. **ENSO Phenomena:** El Niño/La Niña years classification
4. **Humidity Variables:** Dew point and vapor pressure

### **7.2 Exposure Assignment Strategy**

#### **Geographic Assignment:**
1. **National Level:** Population-weighted average of meteorological stations
2. **Sub-National Level:** Administrative boundary averaging
3. **Sensitivity Analysis:** Alternative interpolation methods
4. **Missing Data Handling:** Spatial-temporal imputation algorithms

#### **Temporal Assignment:**
1. **Current Month:** Immediate climate-disease associations
2. **1-Month Lag:** Short-term climate effects
3. **2-6 Month Lag:** Long-term climate memory effects
4. **Seasonal Windows:** 3-month rolling averages

### **7.3 Exposure Validation**

#### **Quality Assurance:**
1. **Instrument Calibration:** Cross-validation with reference stations
2. **Satellite Validation:** MODIS and TRMM comparison datasets
3. **Station Network Assessment:** Completeness and representativeness metrics
4. **Historical Consistency:** Long-term trend validation with reanalysis data

---

## **8. OUTCOME DEFINITION AND MEASUREMENT**

### **8.1 Primary Outcomes**

#### **Malaria Outcomes:**
- **Confirmed Malaria Cases:** Laboratory-confirmed cases per 100,000 population
- **Species-Specific Incidence:** P. falciparum and P. vivax case rates
- **Age-Standardized Rates:** WHO world population standardization

#### **Dengue Outcomes:**
- **Dengue Fever Cases:** Reported dengue cases per 100,000 population
- **Dengue Hemorrhagic Fever:** Severe dengue case rates
- **Dengue Mortality Rate:** Case fatality ratios

### **8.2 Secondary Outcomes**

#### **Composite Outcomes:**
1. **Vector-Borne Disease Index:** Weighted combination of malaria and dengue
2. **Climate-Sensitive Disease Burden:** Age-standardized disability-adjusted life years (DALYs)
3. **Case Fatality Ratios:** Mortality-to-incidence proportions

#### **Effect Modification Outcomes:**
1. **Subgroup Analysis:** By age, sex, urban/rural residence
2. **Economic Stratification:** By income quintile groupings
3. **Socioeconomic Gradient:** Poverty and education interaction terms

### **8.3 Outcome Validation Criteria**

#### **Case Definition Standards:**
1. **Malaria:** WHO expert committee recommended definitions
2. **Dengue:** WHO dengue surveillance guidelines 2016
3. **Severity Classification:** Standard clinical criteria application

#### **Quality Assurance:**
1. **Data Completeness:** Missing value analysis and imputation
2. **Outlier Detection:** Statistical process control methods
3. **Reporting Bias Assessment:** Sensitivity analyses for surveillance improvements

---

## **9. SAMPLE SIZE CALCULATION**

### **9.1 Primary Statistical Power Analysis**

```r
# Power Analysis for Main Effect
power_analysis <- list(
  "Primary_Exposures" = list(
    parameter = "temperature_effect",
    effect_size = 0.15, # Relative risk per °C
    alpha = 0.05,
    power = 0.80,
    expected_n = "1,248 observations (8 countries × 156 months)"
  ),
  "Sample_Size_Calculation" = list(
    formula = "n = (Zα + Zβ)² / (RR - 1)² × prevalence",
    assumptions = "Poisson distribution, baseline risk = 2.5%",
    required_n = "240 months × 8 countries = 1,920 country-months"
  )
)
```

### **9.2 Effect Size Expectations**

Based on existing literature and preliminary data:
- **Temperature Effect:** 12-18% increase per °C (conservative estimate)
- **Precipitation Variability:** 25-35% increase per 50mm standard deviation
- **Minimum Detectable Effect:** 8% relative risk with 80% power

---

## **10. STATISTICAL ANALYSIS FRAMEWORK**

### **10.1 Primary Analytical Approach**

#### **Generalized Estimating Equations (GEE):**
```r
# Primary GEE Model Specification
primary_model <- geeglm(cases ~ temperature + temperature_squared + rain +
                       rain_variability + log_population + gdp_percapita +
                       healthcare_access + year + lagged_cases,
                       data = study_data,
                       id = country,
                       family = poisson,
                       corstr = "ar1")
```

#### **Model Components:**
1. **Non-Linear Effects:** Quadratic terms for temperature thresholds
2. **Interaction Terms:** Socioeconomic effect modification
3. **Seasonal Terms:** Month-of-year indicators
4. **Trend Terms:** Linear and quadratic time trends

### **10.2 Distributed Lag Models**

#### **Lag Structure:**
1. **Immediate Effects:** Current month climate exposure
2. **Short-Term Effects:** 1-3 month lagged climate variables
3. **Medium-Term Effects:** 4-6 month distributed lag structures
4. **Long-Term Effects:** 12-month seasonal rolling averages

### **10.3 Sensitivity Analyses**

#### **Alternative Model Specifications:**
1. **Random Effects Models:** Traditional multilevel approaches
2. **Standard OLS Models:** With robust standard errors
3. **Poisson Regression:** Standard maximum likelihood estimation
4. **Negative Binomial:** For overdispersion in case counts

#### **Robustness Checks:**
1. **Socioeconomic Control:** Alternative poverty and healthcare measures
2. **Vector Control Effects:** INP and IRS coverage adjustments
3. **Reporting Quality:** Surveillance system imputation adjustments
4. **Climate Data Sources:** Alternative temperature and precipitation datasets

### **10.4 Effect Modification Analysis**

#### **Stratified Analysis:**
1. **Economic Status:** GDP per capita subgroups
2. **Vector Control Intensity:** IRS/ITN coverage stratifications
3. **Climate Zones:** Coastal, mountainous, and arid region subgroups
4. **Epidemic Behavior:** Endemic vs epidemic malaria area comparisons

---

## **11. DATA MANAGEMENT AND QUALITY ASSURANCE**

### **11.1 Data Storage and Security**

#### **Secure Database Architecture:**
- **Encrypted Storage:** AES-256 encryption for all datasets
- **Access Logging:** Comprehensive audit trails for data access
- **Regular Backups:** Daily incremental backups with integrity checks
- **Data Destruction:** Secure deletion protocols for sensitive data

### **11.2 Quality Control Protocols**

#### **Data Validation Checks:**
1. **Consistency Checks:** Checksum validation and data completeness
2. **Outlier Detection:** Statistical process control methods
3. **Missing Data Patterns:** Analysis of missing value mechanisms
4. **Cross-Source Validation:** WHO reports vs country data comparison

---

## **12. TIMELINE AND MILESTONES**

### **12.1 Study Timeline**

```mermaid
gantt
    dateFormat YYYY-MM-DD
    title Climate Change Vector Disease Study Timeline

    section Literature Review
    Systematic Search        :done, lit1, 2025-01-01, 2025-02-15
    Quality Assessment       :done, lit2, 2025-02-16, 2025-03-01

    section Data Collection
    WHO Data Acquisition     :done, data1, 2025-01-15, 2025-04-01
    Climate Data Processing  :done, data2, 2025-02-01, 2025-04-15
    Quality Control          :done, data3, 2025-04-01, 2025-05-01

    section Data Analysis
    Primary Modeling         :active, anal1, 2025-03-01, 2025-06-15
    Sensitivity Analysis     :active, anal2, 2025-06-01, 2025-07-15
    Attribution Analysis     :planned, anal3, 2025-07-01, 2025-08-01

    section Publication
    Manuscript Development   :planned, pub1, 2025-08-01, 2025-09-15
    Peer Review Response     :planned, pub2, 2025-09-16, 2025-11-01
    Publication Release      :planned, pub3, 2025-11-01, 2025-12-01
```

---

## **13. DISSEMINATION STRATEGY**

### **13.1 Academic Publications**

#### **Primary Publication Strategy:**
1. **Nature Climate Change:** Target journal for climate-disease interface
2. **Lancet Planetary Health:** Alternative priority journal
3. **PLOS Medicine:** Additional target with broad impact

### **13.2 Policy Dissemination**

#### **WHO Policy Products:**
1. **Technical Briefing:** Climate change adaptation for VBD control
2. **South Asian Action Framework:** Regional cooperation guidelines
3. **Health Ministry Briefs:** Country-specific policy recommendations

### **13.3 Public Outreach**

#### **Communication Products:**
1. **Policy Briefs:** For health ministers and climate negotiators
2. **Infographics:** Visual summaries of key findings
3. **Fact Sheets:** Country-specific risk profiles

---

## **14. ETHICAL CONSIDERATIONS**

### **14.1 Ethical Approval**

**Approved Status:** Research Ethics Review Committee, World Health Organization
**Reference Number:** EK-2025-045
**Date of Approval:** March 10, 2025

### **14.2 Data Privacy and Security**

#### **Privacy Protection Measures:**
- **Aggregate Data Only:** Individual patient data not accessed
- **Anonymous Geographical Units:** Country and district level aggregation
- **Public Domain Sources:** All data from published surveillance systems
- **No Informed Consent Required:** Ecological study design with existing data

---

## **15. MONITORING AND EVALUATION**

### **15.1 Study Monitoring Plan**

#### **Monitoring Indicators:**
1. **Data Quality:** Completeness, accuracy, and timeliness metrics
2. **Timeline Compliance:** Milestone achievement tracking
3. **Resource Utilization:** Budget and personnel allocation monitoring
4. **Communication Effectiveness:** Stakeholder engagement assessment

### **15.2 Quality Assurance Mechanisms**

#### **Independent Review:**
1. **Internal Quality Review:** Research team weekly progress meetings
2. **External Scientific Review:** Expert panel quarterly assessments
3. **Ethical Oversight:** WHO Ethics Committee annual reviews
4. **Data Quality Audit:** Independent statistical verification

### **15.3 Progress Reporting**

#### **Regular Reporting Schedule:**
- **Monthly:** Internal team progress updates
- **Quarterly:** WHO technical advisory group briefing
- **Annually:** WHO Ethics Committee progress report
- **Project-end:** Complete final report and publications

---

## **16. BUDGET AND RESOURCES**

### **16.1 Total Budget Allocation**

| **Budget Category** | **Amount (INR)** | **Amount (USD)** | **% of Total** |
|---------------------|------------------|------------------|----------------|
| **Personnel** | ₹25,00,000 | $30,120 | 25.0% |
| **Data Acquisition** | ₹15,00,000 | $18,072 | 15.0% |
| **Computing Resources** | ₹10,00,000 | $12,048 | 10.0% |
| **Travel & Meetings** | ₹8,00,000 | $9,639 | 8.0% |
| **Publication Charges** | ₹5,00,000 | $6,024 | 5.0% |
| **Contingency** | ₹37,00,000 | $44,579 | 37.0% |
| **Total Budget** | ₹1,00,00,000 | $1,20,482 | 100.0% |

### **16.2 Resources Required**

#### **Human Resources:**
- **Lead Researcher:** PhD Epidemiologist (1.0 FTE)
- **Data Analyst:** MSc Biostatistics (1.0 FTE)
- **Climate Scientist:** MSc Environmental Science (0.5 FTE)
- **Research Assistant:** BS Public Health (0.5 FTE)

#### **Technical Resources:**
- **High-Performance Computing:** Statistical analysis cluster access
- **Data Storage:** Secure cloud hosting with encryption
- **Software Licenses:** R, STATA, Python statistical packages
- **Geospatial Tools:** GIS software and climate data processing

---

## **17. REFERENCE PROTOCOLS**

### **17.1 Citation Standards**

#### **Primary Reporting Standards:**
1. **REPETIR:** Reporting principles for environmental epidemiology studies
2. **STROBE:** Strengthening the reporting of observational studies in epidemiology
3. **PRISMA:** Preferred reporting items for systematic reviews and meta-analyses

### **17.2 Data Citation**

All climate and disease datasets will be cited according to FAIR principles:
- **Unique Digital Object Identifiers (DOIs)** for datasets
- **Zenodo or DataCite** deposition for derived datasets
- **Persistent URLs** for long-term data accessibility

---

**END OF DETAILED STUDY PROTOCOL**

**Climate Change and Vector-Borne Diseases in South Asia Research Study**

**Approved for Implementation: March 2025**
