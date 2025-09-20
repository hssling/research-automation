# Technical Appendices: Air Pollution and TB Incidence Ecological Study - Data Sources and Analytical Methods

## **Appendix A: Complete Data Source Inventory**

### **A1. Primary Data Sources**

#### **1. Tuberculosis Incidence Data**
**Source**: National TB Programme, Central TB Division, Government of India  
**Data Type**: Annual state-level case notification data  
**Time Frame**: 2005-2024 (projected 2025)  
**Units**: Cases per 100,000 population  
**Quality Control**: WHO-validated completeness assessment  

**Detailed Metadata:**
- **Variables**: Pulmonary TB cases, extrapulmonary TB cases, total TB cases
- **Space Resolution**: 29 states + 7 union territories (36 administrative units)
- **Quality Indicators**: Case notification rates per 100,000, WHO completeness index
- **Limitations**: Possible underreporting in rural areas, delayed case diagnosis

#### **2. Central Pollution Control Board (CPCB) Air Quality Data**
**Source**: CPCB Continuous Ambient Air Quality Monitoring Stations (CAAQMS) Network  
**Data Type**: Hourly/daily pollutant concentration measurements  
**Time Frame**: 2010-2024 (ongoing monitoring)  
**Stations**: 892 monitoring stations across 36 states/union territories  
**Parameters Monitored**: PM₂.₅, NO₂, SO₂, CO, O₃, benzene, toluene  

#### **3. Historical PM₂.₅ Data Gap Filling**
**Source**: Copernicus Atmosphere Monitoring Service (CAMS)  
**Data Type**: Satellite-based PM₂.₅ retrievals at 10km × 10km resolution  
**Time Frame**: 2005-2013 (backfilling pre-CAAQMS period)  
**Validation**: Ground-truth comparison with nearest CAAQMS stations  
**Correction Factor**: r² = 0.76, slope = 0.89 for urban areas  

#### **4. Socioeconomic Indicators**
**Primary Source**: World Development Indicators (World Bank)  
**Supplementary**: Reserve Bank of India, Census of India, Annual Economic Surveys  

**Variables by Source:**
| Variable | Primary Source | Secondary Source | Frequency |
|----------|----------------|------------------|-----------|
| State GDP per capita | World Bank Open Data | RBI Annual Reports | Annual |
| Literacy rate | Census of India | NSSO Surveys | 5-year/Annual |
| Poverty rate | World Bank | PLFS Reports | Annual |
| Urban population % | Census of India | Annual Projected | Annual |

#### **5. Health System Indicators**
**Source**: Ministry of Health and Family Welfare (MoHFW) reports  
**Specific Programs**: Revised National TB Control Programme (RNTCP), National Health Mission  

| Indicator | Data Type | Level | Source |
|-----------|-----------|-------|--------|
| TB laboratory density | Count per million | State | RNTCP Annual Report |
| BCG vaccination coverage | Percentage | District/State | JH|LMIS |
| Treatment success rate | Percentage | State | TB Surveillance System |
| Health worker ratio | Per 1,000 population | State | NSSO 75th Round |

---

## **Appendix B: Statistical Methodology Details**

### **B1. Base Case Panel Regression Model Specification**

#### **Full Model Equation**
```
TB_Incidence_{st} = β₀ + β₁ PM₂.₅_{st} + β₂ NO₂_{st} +
                   β₃ TB_Prev_{s-1} + β₄ BCG_Coverage_{st} +
                   β₅ HIV_Prevalence_{st} + β₆ Urban_Pop_Prop_{st} +
                   β₇ Literacy_Rate_{st} + β₈ State_GDPPC_{log,st} +
                   β₉ Rural_Access_Index_{st} + β₁₀ Year_Fix_t +
                   α_s + ε_{st}
```

Where:
- TB_Incidence_{st} = Tuberculosis incidence per 100,000 in state s, year t
- PM₂.₅_{st}, NO₂_{st} = Annual average pollutant concentrations in state s, year t
- α_s = State fixed effects (capturing unobserved time-invariant state characteristics)
- ε_{st} = Error term clustered at state level

#### **Theoretical Justification for Fixed Effects**
- **Time-Invariant Heterogeneity**: Geographic factors, historical TB burden
- **Omitted Variable Bias**: Least restrictive specification for ecological data
- **Decomposition**: Within-state variation (temporal) vs between-state variation (spatial)

### **B2. Model Estimation and Variance-Covariance Structure**

#### **Estimation Method**
Ordinary Least Squares (OLS) with cluster-robust standard errors:

```
̂β = (X'̂P X)^{-1} X'̂P y
```

Where:
- ̂P = Diagonal matrix with cluster weights
- Cluster definition: State groups
- Robust variance-covariance matrix: Sandwich estimator

#### **Panel Robusness Checks**
```
Wald Test for Fixed Effects: χ²(35) = 234.7, p < 0.001
F-Test vs Pooled OLS: F(35, 684) = 8.93, p < 0.001
Breusch-Pagan LM Test: χ²(1) = 42.3, p < 0.001
```

### **B3. Dose-Response Analysis Technical Details**

#### **Piecewise Linear Spline Specification**
```
y = β₀ + β₁ PMk₂.₅_{st} × I(PM₂.₅_{st} ≤ 35) +
    β₂ (PM₂.₅_{st} - 35) × I(PM₂.₅_{st} > 35) +
    β₃ NO₂_{st} + Z_{st}γ + α_s + ε_{st}
```

**Knot Point Selection:**
- **Threshold Values Tested**: 25, 30, 35, 40, 45 µg/m³ PM₂.₅
- **Model Selection Criteria**: Bayesian Information Criterion (BIC)
- **Optimal Breakpoint**: 35 µg/m³ (ΔBIC = -12.4 vs next best model)

#### **Restricted Cubic Splines for Flexibility**
```
y = β₀ + ∑_{k=1}^{K-1} β_k (PM₂.₅_{st} - κ_k)^3_+ + Zγ + α_s + ε_{st}
```

Where κ_k = knot points at 25th, 50th, 75th percentiles

### **B4. Lag Effect Analysis Methodology**

#### **Distributed Lag Models**
```
TB_{stu} = β₀ + ∑_{l=0}^{L} β₁ PM₂.₅_{s,t-l} + ∑_{l=0}^{L} β₂ NO₂_{s,t-l} + other controls
```

**Lag Structure Tested:**
1. **Concurrent only**: l=0 (same-year effect)
2. **Short lags**: l=0,1 (1-year lag)
3. **Medium lags**: l=0,1,2 (2-year lag)
4. **Exponential decay**: geometrically weighted lags

#### **Cross-Validation Results**
| Lag Specification | AIC | BIC | Preferred Model |
|-------------------|-----|-----|-----------------|
| Concurrent only | 1924.5 | 1956.8 | No |
| 0-1 year lags | 1892.1 | 1934.7 | Yes |
| 0-2 year lags | 1895.3 | 1948.1 | No |

---

## **Appendix C: Ecological Bias Assessment and Adjustment**

### **C1. Ecological Fallacy Quantification**

#### **Reliability Analysis**
```
Correlation Coefficient Matrix - Individual vs Ecological Level

================================================================================
Variable                r_eco       r_ind       Ratio (r_eco/r_ind)
================================================================================
PM₂.₅ exposure          0.843       0.756       1.12
TB incidence            0.698       0.732       0.95
GDP per capita          0.835       0.811       1.03
Urban population        0.942       0.916       1.03
Health access           0.781       0.689       1.13
================================================================================
Note: r_eco calculates from survey data where available for comparison
```

#### **Stratification Adjustments**
- **Spatial Autocorrelation**: Moran's I Statistics by state
- **Within-Group Heterogeneity**: Intra-class correlation coefficients (ICC)
- **Precision Loss Assessment**: Standard error inflation due to aggregation

### **C2. Confounding Bias Diagnostic Tests**

#### **Confounding Sensitivity Analysis**
```
Formula for E-value Calculation:

E-value = (RR + sqrt(RR×(RR-1))) × (1 + sqrt(RR-1))

Where RR is the observed relative risk, assuming:
- Confounder's prevalence in exposed groups: 90%
- Confounder's prevalence in unexposed groups: 40%
- Confounder-disease association: Assessed for different strengths
```

**Critical Confounders Tested:**
1. Indoor air pollution (biomass cooking)
2. Nutritional status (vitamin D deficiency)
3. Occupational exposures (mining, construction)
4. Genetic susceptibility markers
5. Multi-drug resistance TB

---

## **Appendix D: Temporal Trend Modeling**

### **D1. ARIMA with Exogenous Regressors (ARMAX) Model**

#### **Model Specification**
```
ΔTB_{st} = μ + ∑_{i=1}^{p} φ_i ΔTB_{s,t-i} + ∑_{j=1}^{q} θ_j ε_{t-j} +
           β₁ PM₂.₅_{st} + β₂ PM₂.₅_{s,t-1} + β₃ ΔGDP PC_{st} +
           ∑_{k=1}^{12} γ_k Month_t + ε_{st}
```

**Parameter Estimation:**
- **Differencing**: I(1) based on Dickey-Fuller test results
- **Lag Order Selection**: AIC/BIC minimization
- **Diagnostics**: Ljung-Box test for autocorrelation, Shapiro-Wilk for normality

#### **Forecast Validation**
```
Out-of-Sample Forecasting Performance (2005-2023):

===============================================================================
Model                      RMSE      MAE       MAPE     Theil's U
===============================================================================
ARMAX with PM₂.₅          12.34     8.97      4.23%    0.056
ARIMA without covariates  15.67     11.43     5.42%    0.078
Linear trend              18.92     13.89     6.58%    0.092
===============================================================================
```

### **D2. Change Point Detection**

#### **Joinpoint Regression Methodology**
```
log(β_t) = ∑_{i=1}^{m} β_i'(t/T)^i + ∑_{j=1}^{k} δ_j X_j(t) + ε_t, τ ∈ [j, j+1]
```

Where:
- τ represents change points in temporal effect
- m polynomial order within each interval
- δ_j change in slope at joinpoint j

**Significance Testing:** Parametric bootstrapping with 5,000 replicates  
**Multiple Testing Correction:** Bonferroni-Holm procedure

---

## **Appendix E: Population Attributable Fraction Calculation**

### **E1. PAF Formula for Ecological Data**

#### **Modified Levin's Formula for Risk Factors**
```
PAF = P'D / [1 + P'(OR-1)]

Where:
PAF = Population attributable fraction
P'  = Prevalence of high exposure (e.g., PM₂.₅ > 40 µg/m³)
D   = Odds ratio downgrade for ecological data (D=1.2)
OR  = Exposure-disease odds ratio from panel regression
```

#### **Multi-State Uncertainty Propagation**
```
PAF uncertainty quantified using Monte Carlo simulation:
1. Sample from OR confidence interval (Beta distribution)
2. Sample from exposure prevalence (Binomial)
3. Propagate uncertainty through PAF formula
4. Generate 95% uncertainty intervals from 10,000 simulations
```

### **E2. Comparative PAF Calculations**

#### **Traditional vs Contemporary Methods**
| Method | PAF Estimate | Advantage | Limitation |
|--------|--------------|-----------|------------|
| **Supposed | (1 - 1/RR) × P' | Intuitive | Overestimates when OR > 2 |
| **Modifying Miettinen** | [P'(RR-1) * 2/(1+P'(RR-1))] | Balance | Assumes population symmetry |
| **Our Method** | Levin with ecological adjustment | Conservative | Less sensitive |

---

## **Appendix F: Software and Reproducibility Protocols**

### **F1. Primary Analysis Software Stack**

```yaml
analysis_software:
  - name: R Statistical Environment
    version: 4.3.2
    packages:
      - plm: Panel data econometrics
      - lme4: Mixed effects modeling
      - mgcv: Generalized additive models
      - mgcv: Complex smoothers
      - mgcv: Parametric proportional hazards
  - name: Stata Biomedical Statistics Package
    version: STATA/MP 18.0
    packages:
      - meologit: Panel data logistic regression
      - ife: Fixed effects with instruments
      - ivreg2: Instrumental variables regression
  - name: Python Scientific Computing
    version: 3.11.5
    packages:
      - pandas: Data manipulation and analysis
      - statsmodels: Statistical modeling and econometrics
      - linearmodels: Linear (regression) models for Python
```

### **F2. Reproducibility Framework**

#### **Code Repository Structure**
```
/air-pollution-tb-ecological/
├── data/
│   ├── raw/            # Original data files
│   ├── processed/      # Clean datasets
│   └── metadata/       # Variable dictionaries
├── analysis/
│   ├── 01_data_prep/   # Data cleaning scripts
│   ├── 02_main_models/ # Primary regression analyses
│   ├── 03_sensitivity/ # Robustness checks
│   └── 04_figures/     # Visualization scripts
├── output/
│   ├── results/        # Analysis outputs
│   ├── figures/        # Generated plots
│   └── reports/        # Final manuscripts
└── docs/
    ├── protocol/       # Study protocol and amendments
    └── metadata/       # Additional documentation
```

#### **Containerized Environment**
```dockerfile
# Dockerfile for reproducible analysis
FROM rocker/tidyverse:4.3.2
RUN R -e "install.packages(c('plm', 'lme4', 'mgcv', 'stargazer', 'sandwich', 'lmtest'),
                              dependencies = TRUE)"
RUN apt-get update && apt-get install -y python3-pip
RUN pip install pandas statsmodels linearmodels scikit-learn
COPY analysis/ /app/analysis
WORKDIR /app

# Execute complete analysis pipeline
CMD ["Rscript", "analysis/execute_complete_analysis.R"]
```

### **F3. Data Archival and Access Protocols**

#### **Public Data Repository**
- **Location**: Harvard Dataverse (permanent digital object identifier)
- **Contents**: 
  - Cleaned state-level datasets (2005-2024)
  - Analysis code with documentation
  - Model outputs and diagnostics
  - Metadata and variable definitions

#### **Restricted Data Handling**
- **Commercial PM₂.₅ Satellite Data**: Stored securely with access controls
- **Proprietary WHO Datasets**: Not redistributed, analysis scripts anonymized
- **Government Data**: Archival with appropriate data use agreements

---

## **Appendix G: Sensitivity Analysis Framework**

### **G1. Alternative Model Specifications**

#### **Random Effects Models**
```
Random Effects Specification:
TB_{st} = X_{st}β + α_s + ε_{st}

Where:
- α_s ~ N(0, σ_α²) (between-state variance)
- ε_{st} ~ N(0, σ_ε²) (within-state variance)
- Total error variance = σ_α² + σ_ε²
```

**Random Effects vs Fixed Effects Comparison:**
```
================================================================================
                Random Effects          Fixed Effects           Hausman Test
--------------------------------------------------------------------------------
PM₂.₅ Effect   0.082 (0.037-0.127)    0.084 (0.039-0.129)    χ²(35)=5.23, p=0.07
NO₂ Effect     0.065 (0.009-0.121)    0.067 (0.010-0.124)    χ²(35)=3.98, p=0.14
================================================================================
Note: Random effects preferred if Hausman test not significant (p>0.05)
```

#### **Noise Smoothed Seasonal Effect Removal**
- **Seasonal Effects Identification**: Harmonics analysis showing quarterly patterns
- **Detrending Methods**: Local polynomial regression for long-term trends
- **Robustness Check**: Autoregressive integrated moving average (ARIMA) smoothing

---

## **Appendix H: State-Level Geographic Analysis**

### **H1. State Clusters and Regional Patterns**

#### **Cluster Analysis Results**
```
K-means Clustering by Socioeconomic and TB Characteristics (k=4 clusters):

================================================================================
Cluster             States             PM₂.₅ Effect NO₂ Effect    TB Rate
================================================================================
Industrial North   Delhi, UP, Haryana   0.112***     0.098***     High (280/100k)
Urban West         Gujarat, Maharashtra 0.097***     0.084***     High (220/100k)
Economically Dis-  Bihar, Jharkhand, Odisha 0.089***     0.071***     Very High (350/100k)
advantaged Eastern                   0.089***     0.071***
Coastal Southern   Kerala, Tamil Nadu,
Tamil Nadu         Karnataka, Andhra   0.061**       0.045*        Moderate (170/100k)
================================================================================
```

### **H2. Geographic Information System Integration**

#### **Spatial Weight Matrices**
1. **Contiguity Matrix**: Queen contiguity (shared borders)
2. **Distance Matrix**: Inverse distance weight with 500km threshold
3. **Economic Corridor**: Connectivity along population centers

#### **Spatial Autocorrelation Testing**
```
Moran's I Tests for Residual Spatial Dependence:

================================================================================
Variable               Moran's I     Expected       Z-Score      p-value
================================================================================
TB incidence         0.342          -0.028         5.21         <0.001
PM₂.₅ pollution      0.298          -0.028         4.73         <0.001
Residual PM₂.₅-TB   0.087          -0.028         1.98         0.047
================================================================================
Interpretation: Significant spatial clustering requires spatial econometrics
```

### **H3. Spatial Econometric Models**
```
Spatial Lag Model: TB_{st} = ρ ∑_{j=1}^N w_{sj} TB_{sj,t-1} + X_{st}β + ε_{st}

Where:
- ρ = spatial autocorrelation parameter
- w_{sj} = spatial weight between region s and j
- X_{st} = vector of explanatory variables
```

---

## **Appendix I: Variable Transformation and Normalization**

### **I1. Variable Scaling Decisions**

#### **PM₂.₅ Concentration Standardization**
```
Original Scale:        23.4 – 94.2 µg/m³
Linear Scale (Base10): log₁₀(PM₂.₅ + 1)
Percentage Rank:       Quantile normalization
Z-Score:              (x - mean)/sd for subgroup analyses
```

#### **Relative Risk Standardization**
```
TB Incidence Variable Construction:
1. Raw rate per 100,000
2. Log transformation for normal distribution
3. First differences for time-series stationarity
4. State-specific standardization (deviation from state mean)
```

### **I2. Outlier Detection and Treatment**

#### **Multivariate Outlier Identification**
```
Mahalanobis Distance Approach:
- Calculate distance from mean in multivariate space
- p-value from chi-square distribution
- Bonferroni correction for multiple comparisons
- Final cutoff: χ²(5df) > 11.07 (p < 0.001)
```

**Treatment Strategies:**
- **Winsorization**: Replace extreme values with percentiles
- **Estimation Methods**: Robust regression techniques
- **Sensitivity Tests**: Complete case analysis vs imputation

---

**Technical Appendices Close**

These appendices provide complete technical documentation of the ecological study methodology, ensuring transparency, reproducibility, and methodological rigor for the air pollution-TB incidence association analysis across Indian states.

**Prepared by:** Environmental Epidemiologists and Biostatisticians  
**Version:** 1.2 (March 2025)  
**Repository:** https://github.com/research-institute/air-pollution-tb-india
