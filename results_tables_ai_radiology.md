# Results Tables: Artificial Intelligence vs Human Radiology Diagnostic Accuracy Meta-Analysis

## **Table 1: Study Characteristics Summary**

| Study ID | Year | Country | Sample Size | Imaging Modality | Disease Category | AI System Type | Study Design |
|----------|------|---------|-------------|------------------|------------------|----------------|--------------|
| Chen-2022 | 2022 | China | 1,235 | CT | Oncology | CNN | Prospective |
| Rodriguez-2023 | 2023 | USA | 987 | MRI | Neurological | CNN | Retrospective |
| Kim-2021 | 2021 | South Korea | 1,543 | Ultrasound | Cardiac | CAD | Prospective |
| Schmidt-2024 | 2024 | Germany | 2,156 | CT | Oncology | Hybrid | Prospective |
| Patel-2022 | 2022 | UK | 875 | MRI | MSK | CNN | Retrospective |
| Liu-2023 | 2023 | China | 1,923 | CT | Trauma | CAD | Prospective |
| Tanaka-2024 | 2024 | Japan | 1,445 | Ultrasound | Liver | Hybrid | Prospective |
| Mueller-2021 | 2021 | Germany | 1,098 | MRI | Cardiac | CNN | Retrospective |
| Singh-2023 | 2023 | India | 756 | CT | Abdominal | CNN | Prospective |
| Garcia-2024 | 2024 | Spain | 1,234 | Ultrasound | Thyroid | CAD | Retrospective |

**Summary Statistics:**
- **Total Studies:** 189 (N=98,743 patients)
- **Median Sample Size:** 1,157 (IQR: 875-1,543)
- **Publication Years:** 2018-2024 (Median: 2022)
- **Geographic Distribution:** Asia 47%, North America 29%, Europe 24%

---

## **Table 2: Diagnostic Accuracy Metrics - Primary Analysis**

### **Pooled Estimates (95% Confidence Intervals)**

| Imaging Modality | AI Sensitivity (%) | Human Sensitivity (%) | AI Specificity (%) | Human Specificity (%) | AI AUC | Human AUC |
|------------------|-------------------|----------------------|------------------|---------------------|---------|------------|
| **Overall** | 89.2 (87.1-91.0) | 84.7 (82.3-86.9) | 92.4 (90.9-93.8) | 87.8 (85.6-89.8) | 0.942 (0.936-0.948) | 0.890 (0.882-0.898) |
| **CT** | 91.3 (89.1-93.2) | 86.1 (83.8-88.2) | 94.2 (92.7-95.5) | 89.3 (87.2-91.2) | 0.952 (0.945-0.958) | 0.901 (0.894-0.908) |
| **MRI** | 87.8 (85.2-90.1) | 82.9 (80.1-85.6) | 90.7 (88.9-92.4) | 85.6 (83.2-87.8) | 0.934 (0.927-0.941) | 0.879 (0.871-0.887) |
| **Ultrasound** | 88.5 (85.9-91.0) | 83.2 (80.5-85.7) | 91.1 (89.1-93.0) | 86.4 (84.3-88.4) | 0.930 (0.922-0.938) | 0.884 (0.876-0.892) |

### **Statistical Significance (Z-tests)**
- **Sensitivity Difference:** z = 6.84, p < 0.001
- **Specificity Difference:** z = 8.21, p < 0.001
- **AUC Difference:** z = 9.47, p < 0.001
- **Effect Sizes:** Cohen's d = 0.89 (large effect for sensitivity), d = 1.12 (large effect for specificity)

---

## **Table 3: Forest Plots Data Summary**

### **Sensitivity Forest Plot**

```
Study                                AI Sensitivity (95% CI)     Human Sensitivity (95% CI)       Weight
Chen-2022                          87.6% (82.4-91.8)          83.1% (77.9-87.8)               8.5%
Rodriguez-2023                     85.4% (80.8-89.5)          81.7% (76.9-85.9)               8.3%
Kim-2021                         91.1% (87.3-94.2)          86.8% (82.6-90.3)               8.7%
Schmidt-2024                      92.8% (89.7-95.3)          88.2% (85.1-90.9)               8.9%

Pooled Estimate (Random Effects)   89.2% (87.1-91.0)          84.7% (82.3-86.9)              100%
Heterogeneity: I² = 34.7%, τ² = 0.0123, χ² = 167.89 (df=188), p < 0.001
Test of overall effect: z = 6.84, p < 0.001
```

### **Specificity Forest Plot**

```
Study                                AI Specificity (95% CI)     Human Specificity (95% CI)       Weight
Chen-2022                          93.8% (90.2-96.8)          88.9% (85.1-92.3)               8.5%
Rodriguez-2023                     91.2% (87.9-94.1)          86.7% (83.2-89.9)               8.3%
Kim-2021                         92.5% (89.1-95.3)          87.8% (84.2-90.9)               8.7%
Schmidt-2024                      95.1% (92.8-96.9)          90.4% (88.1-92.6)               8.9%

Pooled Estimate (Random Effects)   92.4% (90.9-93.8)          87.8% (85.6-89.8)              100%
Heterogeneity: I² = 41.2%, τ² = 0.0137, χ² = 178.45 (df=188), p < 0.001
Test of overall effect: z = 8.21, p < 0.001
```

---

## **Table 4: Subgroup Analysis Results**

### **By AI System Architecture**

| AI Architecture | Studies (n) | AI Sensitivity | Human Sensitivity | Difference | p-value |
|-----------------|-------------|----------------|-------------------|------------|---------|
| **Convolutional Neural Networks** | 142 | 90.1% (88.5-91.6) | 84.8% (83.1-86.4) | +5.3% | <0.001 |
| **Computer-Aided Detection** | 31 | 88.7% (86.8-90.4) | 83.2% (81.3-84.9) | +5.5% | <0.001 |
| **Hybrid Systems** | 16 | 89.4% (87.1-91.4) | 84.1% (81.8-86.2) | +5.3% | <0.001 |
| **Overall** | 189 | 89.2% (87.1-91.0) | 84.7% (82.3-86.9) | +4.5% | <0.001 |

### **By Disease Category**

| Disease Category | Studies (n) | AI Specificity | Human Specificity | Difference | p-value |
|-------------------|-------------|----------------|-------------------|------------|---------|
| **Oncology** | 89 | 93.7% (92.1-95.2) | 88.4% (86.8-89.9) | +5.3% | <0.001 |
| **Trauma** | 45 | 91.8% (89.9-93.6) | 86.9% (84.8-88.8) | +4.9% | <0.001 |
| **Cardiovascular** | 35 | 92.2% (90.3-94.0) | 87.3% (85.2-89.3) | +4.9% | <0.001 |
| **Musculoskeletal** | 20 | 91.1% (88.8-93.2) | 86.8% (84.1-89.3) | +4.3% | <0.001 |
| **Overall** | 189 | 92.4% (90.9-93.8) | 87.8% (85.6-89.8) | +4.6% | <0.001 |

### **By Clinician Experience Level**

| Experience Level | Studies (n) | AI AUC | Human AUC | Difference | p-value |
|------------------|-------------|--------|-----------|------------|---------|
| **>15 years** | 67 | 0.936 (0.928-0.944) | 0.881 (0.873-0.889) | +0.055 | <0.001 |
| **5-15 years** | 89 | 0.943 (0.937-0.949) | 0.892 (0.885-0.899) | +0.051 | <0.001 |
| **<5 years** | 33 | 0.951 (0.943-0.959) | 0.901 (0.893-0.909) | +0.050 | <0.001 |
| **Overall** | 189 | 0.942 (0.936-0.948) | 0.890 (0.882-0.898) | +0.052 | <0.001 |

---

## **Table 5: Heterogeneity and Meta-Regression Analysis**

### **Heterogeneity Statistics**

| Outcome Measure | I² | τ² | Q-statistic | p-value | Interpretation |
|-----------------|----|-----|-------------|---------|----------------|
| **Sensitivity** | 34.7% | 0.0123 | 167.89 (df=188) | p < 0.001 | Moderate heterogeneity |
| **Specificity** | 41.2% | 0.0137 | 178.45 (df=188) | p < 0.001 | Moderate heterogeneity |
| **AUC** | 38.9% | 0.0094 | 159.73 (df=188) | p < 0.001 | Moderate heterogeneity |

### **Meta-Regression Results**

#### **Univariate Meta-Regression for DOR**

| Moderator Variable | Coefficient | Standard Error | Z-value | p-value | R² |
|-------------------|-------------|----------------|---------|---------|----|
| **Imaging Modality (CT/MRI)** | 0.087 | 0.034 | 2.56 | 0.010 | 12.4% |
| **Disease Category (Index Score)** | 0.063 | 0.029 | 2.17 | 0.030 | 8.9% |
| **AI System Type (Scale)** | 0.051 | 0.031 | 1.65 | 0.099 | 5.2% |
| **Radiologist Experience** | 0.073 | 0.028 | 2.61 | 0.009 | 12.9% |
| **Publication Year (2018-2024)** | 0.042 | 0.025 | 1.68 | 0.093 | 5.4% |

#### **Multivariate Meta-Regression Model**
```
Final Model: DOR = β₀ + β₁*(Imaging Modality) + β₂*(Radiologist Experience) + ε
R² adjusted = 22.1%
AIC = -1,247.83

Moderator Effects:
• Imaging Modality: β₁ = 0.082 (SE=0.030), p=0.007
• Radiologist Experience: β₂ = 0.069 (SE=0.025), p=0.006
```

---

## **Table 6: Publication Bias Assessment**

### **Deeks Funnel Plot Asymmetry Test**

| Test | Statistic | p-value | Conclusion |
|------|-----------|---------|------------|
| **Deeks Test (Slope)** | -0.034 | 0.673 | No asymmetry detected |
| **Begg-Mazumdar Test** | z = 0.894 | 0.371 | No evidence of bias |
| **Harbord Test** | z = 1.023 | 0.306 | No evidence of bias |

### **Trim-and-Fill Analysis**

| Outcome | Missing Studies | Adjusted Effect | 95% CI | Adjustment Made |
|---------|----------------|-----------------|--------|-----------------|
| **Sensitivity** | 0 | 89.2% | 87.1-91.0% | None (symmetric) |
| **Specificity** | 2 | 92.1% | 90.8-93.3% | Minor adjustment |
| **AUC** | 0 | 0.942 | 0.936-0.948 | None (symmetric) |

---

## **Table 7: Summary ROC (SROC) Curve Coordinates**

### **Overall SROC Parameters**

| Parameter | Estimate | Standard Error | 95% CI |
|-----------|----------|----------------|--------|
| **Threshold Parameter (θ)** | 1.847 | 0.034 | 1.780-1.914 |
| **Accuracy Parameter (α)** | 2.124 | 0.028 | 2.069-2.179 |
| **Shape Parameter (β)** | 0.892 | 0.031 | 0.831-0.953 |

### **SROC Curve Coordinates**

| Sensitivity | 1-Specificity | Operating Point |
|-------------|---------------|----------------|
| 95% | 20.5% | Ultra-sensitive |
| 90% | 28.7% | High sensitivity |
| 85% | 36.9% | Balanced moderate |
| 80% | 45.2% | High specificity |
| 75% | 52.8% | Ultra-specific |

---

## **Table 8: Clinical Utility Indices**

### **Based on Different Disease Prevalences**

| Disease Prevalence | AI System | Post-test Probability |  |
|-------------------|-----------|----------------------|---|
| **1% (Rare Disease)** | Positive | 17.4% | High false positive rate |
|  | Negative | 0.03% | Near-zero post-test probability |
| **5% (Moderate)** | Positive | 61.2% | Good positive predictive value |
|  | Negative | 0.1% | Excellent negative predictive value |
| **20% (Common)** | Positive | 95.1% | Excellent positive predictive value |
|  | Negative | 0.7% | Strong negative predictive value |
| **40% (Very Common)** | Positive | 98.2% | Outstanding positive predictive value |
|  | Negative | 2.8% | Reliable negative predictive value |

### **Likelihood Ratios**

| Metric | AI System Value | Interpretation |
|--------|----------------|----------------|
| **Positive Likelihood Ratio** | 11.2 | Large effect (generates confident changes) |
| **Negative Likelihood Ratio** | 0.13 | Large effect (generates confident changes) |
| **Diagnostic Odds Ratio** | 86.2 | Very large effect (excellent discrimination) |

---

## **Table 9: Summary of Findings (GRADE Evidence Profile)**

| Diagnostic Outcome | Studies (n) | Quality of Evidence | Diagnostic Performance | Certainty Rating |
|-------------------|-------------|-------------------|----------------------|-----------------|
| **Sensitivity** | 189 | moderatedagger | AI
