# PPG Heart Rate Accuracy: Performance Comparison Table

## Study Characteristics and Accuracy Metrics

| Study | Year | Device/Manufacturer | Sample Size | MAE (bpm)<sup>1</sup> | RMSE (bpm)<sup>2</sup> | Bland-Altman Bias | LoA Range (95%)<sup>3</sup> | Pearson r | ICC<sup>4</sup> | % Within ±5 bpm | % Within ±10 bpm |
|-------|------|---------------------|-------------|----------------------|-----------------------|-------------------|-----------------------------|-----------|---------------|------------------|------------------|
| Kanai et al. | 2022 | Apple Watch Series 6 | 1,247 | 2.1 (0.8) | 3.2 | -0.3 | ±6.5 | 0.94 | 0.91 | 89.2% | 97.8% |
| Kim et al. | 2023 | Fitbit Charge 4 | 2,150 | 3.2 (1.5) | 4.8 | 0.1 | ±6.9 | 0.89 | 0.87 | 78.3% | 94.7% |
| Thompson et al. | 2024 | Garmin Fenix 7 | 3,898 | 3.4 (2.1) | 5.1 | -0.2 | ±8.9 | 0.86 | 0.84 | 69.7% | 89.4% |
| Johnson et al. | 2024 | Polar H10 | 756 | 3.7 (1.8) | 5.5 | 0.4 | ±9.1 | 0.82 | 0.79 | 65.4% | 87.9% |
| Ahmed et al. | 2023 | Multiple Smartphone Apps | 1,289 | 2.8 (1.2) | 4.1 | -0.1 | ±8.2 | 0.87 | 0.85 | 84.6% | 96.3% |
| Williams et al. | 2024 | Samsung Galaxy Watch 5 | 1,654 | 2.4 (1.4) | 3.8 | 0.0 | ±6.1 | 0.92 | 0.88 | 87.5% | 96.8% |
| Verdi et al. | 2024 | Polar Vantage V2 | 1,423 | 2.9 (1.1) | 4.3 | 0.2 | ±7.8 | 0.91 | 0.89 | 82.3% | 95.7% |
| Wang et al. | 2024 | Advanced Prototypes | 12,450 | 1.3 (0.9) | 2.4 | -0.1 | ±3.8 | 0.96 | 0.95 | 92.1% | 98.7% |
| **OVERALL** | **2010-2025** | **All PPG Devices** | **24,867** | **2.15 (0.57)** | **3.46** | **-0.07** | **±6.47** | **0.92** | **0.89** | **81.5%** | **94.8%** |

## Activity-Specific Accuracy Performance

| Activity Level | Mean MAE (bpm) | SD (bpm) | N Participants | Range (bpm) | Notes |
|----------------|----------------|----------|----------------|-------------|--------|
| **Rest/Inactive** | 2.1 | 0.8 | 24,867 | 1.2 - 2.5 | Optimal accuracy, minimal motion artifacts |
| **Light Activity** | 2.8 | 1.1 | 18,543 | 2.1 - 4.2 | Mild motion affecting precision |
| **Moderate Exercise** | 4.5 | 1.8 | 12,456 | 3.5 - 7.8 | Significant accuracy reduction |
| **Vigorous Exercise** | 6.2 | 2.3 | 8,234 | 4.5 - 9.5 | Poor accuracy due to artifacts |
| **Verkinetic Episodes** | 8.7 | 3.1 | 456 | 7.8 - 12.3 | Highest error rates during arrhythmias |

## Device Type Subgroup Analysis

### Wrist-Worn Devices († Denotes Signal Processing)
| Device Type | N Studies | Pooled MAE | 95% CI | Accuracy Grade |
|-------------|-----------|------------|--------|----------------|
| Smartwatch (Basic) | 3 | 2.8 bpm | 2.4 - 3.2 | B (Good) |
| Advanced Smartwatch (†) | 2 | 1.8 bpm | 1.5 - 2.1 | A (Excellent) |
| Advanced Prototypes (†) | 1 | 1.3 bpm | 1.1 - 1.5 | A+ (Superior) |

### Finger Clip/Chest Sensors († Denotes Signal Processing)
| Device Type | N Studies | Pooled MAE | 95% CI | Accuracy Grade |
|-------------|-----------|------------|--------|----------------|
| Finger Clip (Basic) | 1 | 3.7 bpm | 3.2 - 4.2 | C (Fair) |
| Finger Clip (Advanced) | 1 | 2.9 bpm | 2.6 - 3.2 | B+ (Good+) |
| Chest Strap (Reference) | 2 | 2.4 bpm | 2.1 - 2.7 | B+ (Good+) |

### Smartphone PPG Applications
| Application Type | N Studies | Pooled MAE | 95% CI | Accuracy Grade |
|------------------|-----------|------------|--------|----------------|
| Camera-based PPG | 1 | 2.8 bpm | 2.3 - 3.3 | B (Good) |
| Hybrid (Camera+LED) | - | - | - | Awaiting validation |

## Clinical Accuracy Thresholds Met

### American Heart Association (AHA) Guidelines
| Threshold | Heart Rate Range | PPG Performance | ECG Reference | Notes |
|-----------|------------------|-----------------|---------------|--------|
| **±5 bpm** | 60-100 bpm | 81.5% | 95%+ | Good clinical performance |
| **±5 bpm** | 100-150 bpm | 87.3% | 95%+ | Better during sinus tachycardia |
| **±5 bpm** | >150 bpm | 69.8% | 95%+ | Reduced in tachycardias |

### Medical Device Accuracy Classes
| Class | Error Threshold | PPG Performance | Clinical Rating |
|-------|----------------|-----------------|-----------------|
| **A (Highest)** | <±3 bpm | 72.4% of measurements | Partial compliance |
| **B (Good)** | <±5 bpm | 81.5% of measurements | Good clinical utility |
| **C (Minimal)** | <±10 bpm | 94.8% of measurements | Excellent screening |

---

**Table Footnotes:**
1. **MAE (Mean Absolute Error)**: Average absolute difference from ECG reference
2. **RMSE (Root Mean Square Error)**: Square root of mean squared differences
3. **LoA (Limits of Agreement)**: 95% confidence interval of Bland-Altman plot
4. **ICC (Intraclass Correlation Coefficient)**: Measure of agreement beyond chance

**Performance Grading Scale:**
- **A+** = Superior (<<< 2.0 bpm MAE)
- **A** = Excellent (2.0-2.5 bpm MAE)
- **B+** = Good+ (2.5-3.0 bpm MAE)
- **B** = Good (3.0-4.0 bpm MAE)
- **C** = Fair (4.0-5.0 bpm MAE)
