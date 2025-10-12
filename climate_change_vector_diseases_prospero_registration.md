# PROSPERO Registration Protocol

**Registration Number:** CRD42024356789

## **Climate Change and Vector-Borne Diseases in South Asia**

---

## **Protocol Registration Information**

| **Item** | **Entry**
|---------|---------
| **Registration Date** | March 15, 2025
| **Last Updated** | March 20, 2025
| **Review Due Date** | March 2025
| **Stage of Review** | Started

---

## **Review Question**

**Primary Research Question:** Are rising average temperatures and rainfall variability associated with malaria and dengue incidence across South Asian countries?

**Secondary Research Questions:**
1. What is the threshold effect of temperature on vector-borne disease transmission?
2. What are the lagged effects of climate variables on disease incidence?
3. What is the population attributable fraction of climate change to vector-borne diseases?

---

## **Eligibility Criteria**

### **Inclusion Criteria:**
- **Population:** South Asian countries (Afghanistan, Bangladesh, Bhutan, India, Maldives, Nepal, Pakistan, Sri Lanka)
- **Intervention/Exposure:** Long-term climate change trends (mean temperature, maximum temperature, rainfall variability, humidity)
- **Comparator:** Pre-climate change baselines and non-affected periods
- **Outcome:** Malaria incidence (confirmed cases), dengue fever incidence (confirmed cases), dengue hemorrhagic fever incidence
- **Language:** English

### **Exclusion Criteria:**
- Studies with less than 12 months of observation
- Countries with less than 80% data completeness
- Experimental studies or non-ecological designs
- Non-South Asian countries

---

## **Study Selection Process**

### **Stage 1: Title and Abstract Screening**
- **Process:** Independent screening by two reviewers
- **Criteria:** Relevance to climate change and vector-borne diseases in South Asia
- **Conflict Resolution:** Third reviewer arbitration

### **Stage 2: Full-Text Assessment**
- **Process:** Independent full-text review by two reviewers
- **Secondary Screening:** Quality assessment and data extraction
- **Quality Assessment:** Cochrane Effective Practice and Organization of Care Group criteria

---

## **Data Collection Process**

### **Primary Data Sources:**

#### **Climate Data:**
- **WorldClim v2.1:** Historical climate data (2015-2025)
- **CRU-TS4.06:** Monthly temperature and precipitation (2005-2015)
- **Satellite-derived Variables:** NDVI for vegetation monitoring

#### **Disease Data:**
- **WHO Global Malaria Programme:** Annual malaria incidence reports
- **WHO Dengue Surveillance:** Monthly dengue incidence data
- **National Health Information Systems:** Country-level reporting

#### **Confounding Variables:**
- **Socioeconomic:** GDP per capita, poverty rates, healthcare access
- **Vector Control:** ITN usage, IRS coverage, larval surveillance
- **Population Dynamics:** Urbanization rates, age structure, mobility

---

## **Data Items**

### **Climate Exposure Variables:**
1. **Temperature Metrics:**
   - Monthly average temperature (°C)
   - Monthly maximum temperature (°C)
   - Monthly minimum temperature (°C)
   - Temperature variability (standard deviation)
   - Heatwave frequency (days ≥35°C)

2. **Precipitation Variables:**
   - Monthly total rainfall (mm)
   - Rainfall variability (coefficient of variation)
   - Extreme rainfall events (≥100mm/day)
   - Drought frequency (monthly rainfall <10mm)

3. **Humidity and Environmental:**
   - Relative humidity (%)
   - Urban population density
   - Vegetation indices (NDVI)

### **Disease Outcome Measures:**
1. **Malaria Outcomes:**
   - Laboratory-confirmed malaria cases per 100,000 population
   - Malaria incidence rate (all species)
   - Age-standardized malaria rates

2. **Dengue Outcomes:**
   - Dengue fever cases per 100,000 population
   - Dengue hemorrhagic fever cases
   - Dengue mortality rate

### **Confounding/Effect Modifier Variables:**
1. **Healthcare Access:** Physician density, hospital beds per capita
2. **Vector Control:** Insecticide-treated net usage, indoor residual spraying
3. **Socioeconomic:** Poverty rate, GDP per capita, literacy rate
4. **Demographic:** Population density, urbanization rate, age distribution

---

## **Outcomes and Prioritization**

### **Primary Outcomes:**
1. **Malaria Incidence Rate:** Confirmed malaria cases per 100,000 population
2. **Dengue Incidence Rate:** Confirmed dengue cases per 100,000 population
3. **Climate Attributable Fraction:** Percentage of disease burden attributable to climate change

### **Secondary Outcomes:**
1. **Lagged Climate Effects:** Effects of climate variables at 1-6 month lags
2. **Threshold Effects:** Non-linear relationships between temperature and disease incidence
3. **Spatial Heterogeneity:** Country-level differences in climate-disease relationships
4. **Economic Impact:** Healthcare costs attributable to climate change

---

## **Risk of Bias Assessment**

### **Items to be Assessed:**
1. **Ecological Study Bias:** Risk of ecological fallacy
2. **Measurement Bias:** Accuracy of climate and disease data
3. **Confounding Bias:** Control of socioeconomic and healthcare factors
4. **Publication Bias:** Selectively available climate-disease studies

### **Quality Assessment Tools:**
- **Cochrane Handbook:** Risk of bias assessment for observational studies
- **GRADE Framework:** Strength of evidence assessment
- **Joanna Briggs Institute:** Critical appraisal checklist for prevalence studies

---

## **Strategy for Data Synthesis**

### **Synthesis Methods:**
1. **Primary Analysis:** Generalized Estimating Equations (GEE) for longitudinal data
2. **Climate Attribution:** Population attributable fraction calculations
3. **Effect Modification:** Stratified analysis by socioeconomic status
4. **Sensitivity Analysis:** Alternative model specifications

### **Statistical Software:**
- **R Statistical Environment:** Primary analysis platform
- **STATA/MP:** Alternative statistical modeling
- **Python Ecosystem:** Data visualization and geospatial analysis

### **Meta-Analytical Approach:**
- **Random Effects Model:** Assuming heterogeneity between countries
- **Subgroup Analysis:** By income level, climate zone, disease endemicity
- **Meta-Regression:** Investigation of effect modification
- **Publication Bias Assessment:** Funnel plots, Egger's test

---

## **Data Management and Analysis Plan**

### **Data Processing:**
1. **Standardization:** Age-standardized rates using WHO world population
2. **Missing Data:** Multiple imputation for climate data gaps
3. **Outlier Treatment:** Winsorization for extreme values
4. **Spatial Alignment:** Geographical interpolation for climate variables

### **Analysis Plan:**
1. **Descriptive Analysis:** Trends in climate variables and disease incidence (2005-2025)
2. **Correlation Analysis:** Bivariate relationships between climate and disease variables
3. **Regression Analysis:** Multivariate models with fixed and random effects
4. **Attribution Analysis:** Quantifying climate change contribution to disease burden

---

## **Ethics Approval**

### **Ethical Approval Status:**
**Approved** - Research Ethics Review Committee, World Health Organization

**Approval Reference:** EK-2025-045

**Approval Date:** March 10, 2025

### **Ethical Considerations:**
- **Data Privacy:** All data sources are public health surveillance datasets
- **Individual Consent:** Not applicable (aggregate ecological data)
- **Data Confidentiality:** No individual patient identifiers used
- **Research Integrity:** Transparency in data sources and methods

---

## **Declarations**

### **Funding:**
This study is funded by the World Health Organization Department of Environment, Climate Change and Health (UCH)

### **Role of Funders:**
- **Sponsor:** World Health Organization
- **Sponsor Contact:** uch@who.int
- **Role:** Study design, data collection, analysis, reporting, publication submission

### **Conflicts of Interest:**
No conflicts of interest declared by any members of the research team

### **Dissemination Plans:**
- **Primary Publication:** Nature Climate Change (target journal)
- **Policy Briefs:** WHO publication for health ministry use
- **Technical Report:** Detailed methodology and results for researchers
- **Public Communication:** WHO website and South Asian health ministry materials

---

## **Protocol Amendments**

**Version 1.0** - Original protocol (March 15, 2025)
- Primary objectives and inclusion criteria established
- Data sources and analysis methods specified

**Version 1.1** - Updated protocol (March 20, 2025)
- Additional climate variables included
- Spatiotemporal analysis methods expanded
- Economic impact assessment added

---

**End of PROSPERO Registration Protocol**
