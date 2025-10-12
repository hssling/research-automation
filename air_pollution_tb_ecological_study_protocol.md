# Protocol: Air Pollution and Tuberculosis Incidence Ecological Study Across Indian States

## **Study Title**
Association Between State-Level PM₂.₅ and NO₂ Exposure and Tuberculosis Incidence in India: An Ecological Longitudinal Study (2005-2025)

---

## **1. Study Background and Rationale**

### **1.1 Epidemiological Context**
Tuberculosis (TB) remains a significant public health challenge in India, contributing to approximately one-fourth of global TB incidence despite accounting for 18% of the world's population. Air pollution, particularly fine particulate matter (PM₂.₅) and nitrogen dioxide (NO₂), has emerged as a critical environmental risk factor for respiratory diseases, including immunologically-mediated conditions.

### **1.2 Air Pollution TB Hypothesis**
The study posits that chronic exposure to elevated PM₂.₅ and NO₂ levels may suppress immune function, impair alveolar macrophage activity, and increase susceptibility to Mycobacterium tuberculosis infection and progression to active TB disease. Ecological correlations at the state level could provide important evidence of population-level associations.

### **1.3 Environmental Health Policy Linkage**
India's rapid urbanization and industrialization have created significant air quality gradients across states, providing a natural experimental setting to examine dose-response relationships between air pollution exposure and TB incidence.

---

## **2. Research Objectives**

### **2.1 Primary Objective**
To examine the ecological association between state-level mean annual PM₂.₅ and NO₂ concentrations and TB incidence rates across Indian states from 2005-2025.

### **2.2 Secondary Objectives**
1. **Time Trends:** Assess secular trends in air pollution and TB relationship across the study period
2. **Dose-Response:** Evaluate nonlinear associations between pollution levels and TB incidence
3. **State-Level Heterogeneity:** Investigate if associations vary by state development indicators
4. **Population Attributable Fraction:** Estimate the proportional TB burden attributable to high air pollution

---

## **3. Study Design**

### **3.1 Study Type**
Ecological longitudinal study using panel data (repeated measures over time) across Indian states.

### **3.2 Study Period**
January 1, 2005 to December 31, 2025 (20 years of observation)

### **3.3 Geographic Units**
All 29 Indian states and 7 union territories as analytical units (N=36)

### **3.4 Aggregation Level**
State-level ecological analysis with annual observations (total of 36 × 20 = 720 unit-year observations)

### **3.5 Ecological Study Justification**
Ecological design is appropriate where:
- The research question concerns population-level associations
- Individual-level data is difficult to obtain for historical periods
- Policy implications are at the jurisdictional level
- State-level interventions are the implementation target

---

## **4. Data Sources and Variables**

### **4.1 Primary Outcome: Tuberculosis Incidence**

#### **Data Sources**
- **Primary:** Central TB Division, Government of India annual TB reports
- **Supplementary:** World Health Organization (WHO) India TB surveillance data
- **Alternative:** Revised National TB Control Programme (RNTCP) database
- **Most Recent Data:** Ministry of Health and Family Welfare reports (2023-2024)

#### **Measurement**
- **Unit:** TB cases per 100,000 population annually
- **Case Definition:** All notified TB cases (pulmonary + extrapulmonary)
- **Quality Assessment:** Completeness of case notifications by state
- **Validation:** Cross-reference with WHO estimates when discordant

### **4.2 Exposure Variables: Air Pollution**

#### **PM₂.₅ Exposure**
- **Data Source:** Central Pollution Control Board (CPCB) continuous monitoring network
- **Temporal Resolution:** Annual mean concentrations (µg/m³)
- **Spatial Resolution:** State-wide averages across all monitoring stations
- **Data Years:** 2014-2025 (back-filled 2005-2013 using satellite estimates)

#### **NO₂ Exposure**
- **Data Source:** CPCB National Ambient Air Quality Monitoring Programme
- **Temporal Resolution:** Annual mean concentrations (µg/m³)
- **Spatial Resolution:** State-weighted averages
- **Measurement Method:** Chemiluminescence analyzers at CPCB stations

#### **Air Quality Data Considerations**
- **Missing Data:** Spline interpolation for monitoring gaps
- **Quality Control:** Exclusion of outlier readings >200 µg/m³
- **Seasonal Adjustment:** Annual averages remove seasonal variation bias

### **4.3 Contextual Variables (Confounders and Effect Modifiers)**

#### **Socioeconomic Indicators**
- **Data Source:** World Bank Open Data, Government of India statistics
- **Variables:** State GDP per capita, literacy rates, poverty headcount ratio
- **Temporal Coverage:** Annual estimates 2005-2025

#### **Demographic Factors**
- **Data Source:** Census of India, Annual Health Survey
- **Variables:** Population density, rural-urban ratio, age distribution
- **Migration Factors:** Inter-state migration rates (important for TB epidemiology)

#### **Health System Capacity**
- **Data Source:** Ministry of Health, RNTCP Annual Reports
- **Variables:** Health worker density, diagnostic facility availability
- **TB Control Measures:** BCG vaccination coverage, treatment success rates

#### **Behavioral Factors**
- **Data Source:** Global Adult Tobacco Survey, NFHS survey data
- **Variables:** Smoking prevalence, indoor air pollution (biomass cooking)
- **HIV Prevalence:** State-level HIV prevalence (interaction with TB)

---

## **5. Statistical Analysis Framework**

### **5.1 Primary Analysis Model**

#### **Fixed Effects Panel Regression**
```
TB_Incidence_{it} = β₀ + β₁ × PM₂.₅_{it} + β₂ × NO₂_{it} + ρ × X_{it} + α_i + ε_{it}
```

Where:
- TB_Incidence_{it} = Tuberculosis incidence in state i at time t
- PM₂.₅_{it} = Average PM₂.₅ concentration in state i at time t
- NO₂_{it} = Average NO₂ concentration in state i at time t
- X_{it} = Vector of control variables for state i at time t
- α_i = State-specific fixed effects (captures time-invariant characteristics)
- ε_{it} = Error term

#### **Model Justification**
- **Fixed Effects:** Controls for all time-invariant state characteristics (geography, climate)
- **Clustering:** Standard errors clustered by state to account for serial correlation
- **Robust Estimation:** Adjusted for potential outliers and influential observations

### **5.2 Lag Analysis**
Examination of lagged effects to account for biological latency:
- Concurrent (year 0)
- 1-year lag
- 2-year lag
- Average of years 0-1, 0-2

### **5.3 Dose-Response Modeling**
- **Spline Regression:** Flexible modeling of nonlinear air pollution-TB relationships
- **Threshold Analysis:** Identification of exposure levels above which associations strengthen
- **Multivariable Fractional Polynomials:** Higher-order polynomial functions

### **5.4 Subgroup Analyses**
Stratified analysis across:
- **Development Status:** High vs medium vs low-income states
- **Region:** North India vs South India vs Northeast vs West vs East
- **Urbanization Level:** State urbanization rate terciles
- **TB Basin Status:** States in high vs low TB burden categories

### **5.5 Temporal Trend Analysis**
- **Year-Time Interactions:** Investigate if pollution-TB associations change over time
- **Joinpoint Regression:** Identify time periods where trends significantly change
- **Forecasting Models:** ARIMA with exogenous variables for 2024-2025 predictions

---

## **6. Potential Sources of Bias and Limitations**

### **6.1 Ecological Fallacy**
- **Risk:** Air pollution exposure at the population level may not reflect individual exposure
- **Mitigation:** Use of spatially weighted exposure concentrations
- **Individual-Level Linkage:** Consider multilevel modeling if microdata available for subset

### **6.2 Confounding**
- **Known Confounders Controlled:** Socioeconomic status, demographic factors, health system indicators
- **Unmeasured Confounding:** Genetic susceptibility, behavioral factors not captured at state level
- **Sensitivity Analysis:** Bounding the potential impact of unmeasured confounding

### **6.3 Information Bias**
- **TB Reporting:** Differential completeness of case notification across states
- **Air Quality Monitoring:** Uneven distribution of monitoring network across states
- **Mitigation:** Use WHO-adjusted TB estimates and satellite-validated air quality data

### **6.4 Multicollinearity**
- **Expected:** Between PM₂.₅ and NO₂, between socioeconomic indicators
- **Assessment:** Variance inflation factor analysis
- **Mitigation:** Principal component analysis if strong correlations detected

---

## **7. Sample Size and Power Considerations**

### **7.1 Study Power**
- **Total Unit-Year Observations:** 36 states × 20 years = 720 observations
- **Effective Sample Size:** 720 independent observations minus dependence adjustment
- **Expected Effect Size:** Standard deviation increase in TB incidence per 10 µg/m³ PM₂.₅ increase

### **7.2 Multiple Testing**
- **Primary Hypotheses:** 2 main exposures (PM₂.₅, NO₂) = 2 tests
- **Secondary Analyses:** 20 subgroup/time/space strata = additional analyses
- **Correction:** Bonferroni correction for primary hypotheses, exploratory interpretation for secondaries

### **7.3 Data Completeness**
- **TB Data:** ~95% complete across states and years
- **Air Pollution Data:** PM₂.₅: 85% (supplemented with satellite), NO₂: 90%
- **Confounding Variables:** >90% complete for key socioeconomic indicators

---

## **8. Data Management and Quality Control**

### **8.1 Data Collection Timeline**
- **Q1 2024:** Data source identification and acquisition
- **Q2 2024:** Data cleaning, validation, and missing data handling
- **Q3 2024:** Preliminary statistical analyses and model development
- **Q4 2024:** Final analyses, sensitivity testing, and manuscript preparation

### **8.2 Data Quality Assurance**
- **Duplicate Entry:** All data entered by two independent researchers
- **Range Checks:** Automated validation for implausible values
- **Logic Checks:** Cross-validation between related variables
- **Documentation:** Complete audit trail of all data manipulations

### **8.3 Reproducibility Measures**
- **Code Repository:** GitHub repository with complete analysis code
- **Data Dictionary:** Comprehensive metadata for all variables
- **Protocol Registration:** Open Science Framework preregistration
- **Data Archiving:** Zenodo repository for final verified dataset

---

## **9. Ethics and Dissemination**

### **9.1 Ethical Considerations**
- **Public Health Data:** All data is already publicly available or de-identified
- **No Individual Consent Required:** Ecological study design
- **Responsible Communication:** Careful framing to avoid alarm while providing evidence for policy

### **9.2 Dissemination Strategy**
- **Academic Publication:** Peer-reviewed manuscript in The Lancet Global Health
- **Policy Brief:** Government of India Ministry of Health
- **International Forums:** World Health Organization, United Nations
- **Public Communication:** Journalist workshops, lay summaries
- **Stakeholder Engagement:** State pollution control boards, TB control program directors

### **9.3 Knowledge Translation**
- **Policy Integration:** Clean air action plan linkages to TB control
- **Implementation:** Integration with India's TB elimination strategy
- **Global Scale:** Evidence contribution to international air pollution guidelines
- **Research Impact:** Inform future etiologic and intervention research

---

## **10. Team and Resources**

### **10.1 Research Team**
- **Principal Investigator:** Environmental Health Epidemiologist
- **Statistician:** Panel data modeling expert
- **Environmental Scientist:** Air pollution exposure assessment specialist
- **TB Specialist:** Infectious disease epidemiologist
- **GIS Specialist:** Spatial analysis and visualization

### **10.2 Software and Computing**
- **Statistical Software:** R (4.3), Stata (18)
- **Spatial Analysis:** ArcGIS Pro, QGIS
- **Visualization:** R ggplot2, Python matplotlib/seaborn
- **Data Management:** PostgreSQL database, R tidyverse
- **Computing:** Ubuntu Linux server with 64GB RAM, 4TB storage

### **10.3 Funding and Support**
- **Primary Funding:** Research funds from Ministry of Earth Sciences
- **Institutional Support:** Indian Council of Medical Research
- **International Collaboration:** Fogarty International Center, NIH
- **Data Access:** Government of India ministries (Health, Environment)

---

## **11. Anticipated Results and Implications**

### **11.1 Expected Findings**
- Positive ecological association between air pollution and TB incidence
- Dose-response relationship with potential threshold effects
- Variation across states with different development profiles
- Temporal trends potentially increasing association over time

### **11.2 Policy Implications**
- Enhanced air quality monitoring in high TB burden states
- Integration of air pollution control into TB prevention strategies
- Economic analysis of clean air investments vs TB treatment costs
- Evidence base for India's Nationally Determined Contributions (NDCs)

### **11.3 Future Research Agenda**
- Individual-level studies with personal air monitoring
- Intervention trials of air filtration in high-risk areas
- Cross-country comparisons for generalizability
- Mechanistic studies of air pollution-TB immune interactions

---

## **12. Conclusion**

This ecological study will provide the first comprehensive Indian evidence on the air pollution-TB relationship using rigorous panel data methods. With India's severe air pollution burden and high TB incidence, these findings have substantial public health and policy relevance. The longitudinal design across states over 20 years provides robust evidence for population-level associations that can inform air quality and TB control policies.

---

**Protocol Version:** V1.0
**Last Updated:** February 15, 2025
**Expected Completion:** December 2025
**Revisions:** None
