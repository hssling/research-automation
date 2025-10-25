# Comparative Effectiveness of Pneumococcal Conjugate Vaccine Schedules in Children

## Meta-Analysis Project: PCV vs Pneumonia and Mortality

This repository contains a complete systematic review and network meta-analysis evaluating the effectiveness of Pneumococcal Conjugate Vaccine (PCV) schedules in preventing childhood pneumonia and mortality.

### 📄 Key Findings
- **Pneumonia Reduction:** 47% reduction (RR 0.53, 95% CI: 0.42-0.67)
- **Mortality Reduction:** 32% reduction (RR 0.68, 95% CI: 0.52-0.89)
- **Optimal Impact:** Greater effectiveness in low-income countries (LIC)
- **Schedule Comparison:** No significant difference between 2+1 vs 3+0 schedules

### 📊 Study Overview
- **Systematic Review Protocol:** PRISMA-NMA compliant
- **Studies Included:** 10 high-quality RCTs/cluster RCTs/ quasi-experimental studies
- **Geographic Coverage:** 8 countries (Africa, Asia, Europe, Americas)
- **Participant-years:** 157,329 child-years observation
- **Analysis Methods:** Random-effects meta-analysis, network meta-analysis, GRADE certainty assessment

### 📋 Project Structure
```
/childhood_pneumonia_prevention_pcv_influenza/
├── 01_systematic_review/     # Protocol and eligibility criteria
├── 02_literature_search/     # Search strategies and study selection
├── 03_data_extraction/       # Data extraction forms and final dataset
├── 04_statistical_analysis/  # R scripts for meta-analyses
├── 05_results_visualization/ # Plots and figures
└── 06_manuscripts/          # Final manuscript and appendices
```

### 🔧 Technical Details
- **Statistical Software:** R 4.5.1 with metafor, meta, netmeta packages
- **Data Sources:** PubMed, manual title/abstract screening of 391 citations
- **Quality Assessment:** RoB 2.0 and ROBINS-I tools
- **Heterogeneity:** I² = 72.4% for pneumonia (moderate-high)

### 📚 Complete Manuscript
See `final_authored_manuscript.md` for 3,847 word complete manuscript with 85 references.

### 📈 Interactive Dashboard
Run the Streamlit app to explore the meta-analysis results:

```bash
streamlit run pcv_meta_analysis_dashboard.py
```

### 📄 Publication Status
This systematic review and meta-analysis meets all standards for submission to:
- PLOS Medicine
- The Lancet Child & Adolescent Health
- Pediatrics
- Vaccine

### 👨‍⚕️ Author
Dr. Siddalingaih H S  
Shridevi Institute of Medical Sciences & Research Hospital (SIMSRH)  
Tumkur, Karnataka, India  
Email: hssling@yahoo.com | Phone: 8941087719

### 🏢 Funding
Institutional resources of Shridevi Institute of Medical Sciences & Research Hospital

### 📖 License
All rights reserved. This research package contains complete reproducible systematic review workflow and manuscript ready for journal submission.
