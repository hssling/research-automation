# Living Review Protocol: Periodic Auto-Updation of Evidence

## Overview

This living systematic review implements automated periodic updates to maintain the currency of evidence in the drug-resistant tuberculosis network meta-analysis. The system automatically searches for new literature, extracts relevant data, updates analyses, and notifies stakeholders of significant changes.

## Objectives

1. **Automated Literature Surveillance**: Continuously monitor bibliographic databases for new relevant studies
2. **Incremental Data Extraction**: Automatically extract data from newly identified studies
3. **Dynamic Analysis Updates**: Re-run statistical analyses with new data
4. **Change Detection**: Identify significant changes in treatment effects or conclusions
5. **Stakeholder Notification**: Alert researchers and clinicians of important updates
6. **Quality Assurance**: Maintain methodological rigor in automated processes

## System Architecture

### Core Components

1. **Literature Surveillance Module** (`scripts/auto_search.py`)
   - Automated database querying
   - Duplicate detection
   - Study eligibility screening

2. **Data Extraction Module** (`scripts/auto_extraction.py`)
   - Automated PDF processing
   - Structured data extraction
   - Quality assessment

3. **Analysis Update Module** (`scripts/auto_analysis.py`)
   - Incremental NMA updates
   - Statistical testing for significant changes
   - Results visualization updates

4. **Scheduler Module** (`scripts/scheduler.py`)
   - Cron job management
   - Update frequency configuration
   - Error handling and recovery

5. **Notification Module** (`scripts/notifications.py`)
   - Email alerts for stakeholders
   - Dashboard updates
   - Change summary generation

## Update Schedule

### Standard Schedule
- **Literature Search**: Weekly (every Monday 2 AM)
- **Data Extraction**: Daily for new studies (6 AM)
- **Analysis Update**: Bi-weekly (1st and 15th of month, 3 AM)
- **Full Review**: Quarterly (1st day of quarter, 4 AM)

### Trigger-Based Updates
- **High-Impact Studies**: Immediate update for studies with >500 participants
- **Regulatory Changes**: Immediate update for guideline changes
- **Safety Alerts**: Immediate update for drug safety concerns

## Methodological Framework

### Literature Search Strategy
```markdown
**Databases Searched:**
- PubMed/MEDLINE (Primary)
- Embase
- Cochrane CENTRAL
- Web of Science Core Collection
- ClinicalTrials.gov
- WHO ICTRP

**Search Frequency:** Weekly
**Date Range:** Previous week from last search
**Language:** English (primary), with multilingual abstract screening
```

### Study Eligibility Criteria (Automated)
1. **Population**: Adults/adolescents with bacteriologically confirmed MDR/RR-TB
2. **Interventions**: BPaL, BPaLM, short MDR regimens, individualized long regimens
3. **Outcomes**: Treatment success, relapse, serious adverse events
4. **Study Design**: RCTs, prospective observational studies, retrospective studies
5. **Sample Size**: ≥10 participants per treatment arm

### Data Extraction Fields (Automated)
- Study metadata (authors, year, journal, DOI)
- Participant characteristics (N, age, sex, HIV status, resistance pattern)
- Intervention details (regimen composition, duration, dosing)
- Outcome data (success rates, relapse rates, adverse events)
- Study quality indicators (risk of bias, funding source)

## Quality Assurance

### Automated Quality Checks
1. **Study Eligibility Verification**: Machine learning classifier (95% accuracy)
2. **Data Extraction Validation**: Double extraction with reconciliation
3. **Statistical Integrity**: Automated heterogeneity and inconsistency testing
4. **Clinical Relevance**: Automated assessment of applicability

### Human Oversight
- **Monthly Review**: Manual verification of 10% random sample
- **Significant Changes**: Human review of all major finding changes
- **System Updates**: Quarterly review of automation algorithms

## Change Detection Algorithm

### Statistical Significance
- **Treatment Effects**: Bayesian posterior probability >95% for meaningful change
- **Ranking Changes**: SUCRA value changes >10 points
- **Heterogeneity**: I² changes >25%

### Clinical Significance
- **Success Rate Changes**: >5% absolute change in treatment success
- **Safety Signals**: New adverse events with incidence >2%
- **Subgroup Effects**: New significant interactions

## Output Products

### Automated Updates
1. **Updated Analysis Files**: Revised statistical outputs
2. **Change Summary Reports**: Structured summaries of updates
3. **Visualization Updates**: Refreshed forest plots and rankings
4. **Dashboard Updates**: Real-time evidence displays

### Notification Products
1. **Stakeholder Alerts**: Email notifications for significant changes
2. **Clinical Updates**: Summary for practicing clinicians
3. **Policy Briefs**: Updates for guideline developers
4. **Research Summaries**: Updates for academic audiences

## Integration with Existing Systems

### Dashboard Integration
- Real-time evidence display
- Interactive change tracking
- Stakeholder communication portal

### Publication Integration
- Automatic manuscript updates
- Version control for living document
- Citation management for dynamic references

## Ethical Considerations

### Transparency
- Clear documentation of automated processes
- Public access to update algorithms
- Disclosure of automation limitations

### Data Privacy
- Secure handling of personal data
- Compliance with data protection regulations
- Transparent data usage policies

### Accountability
- Clear attribution of automated contributions
- Human responsibility for final decisions
- Audit trails for all automated processes

## Performance Metrics

### System Performance
- **Search Sensitivity**: >95% recall of eligible studies
- **Extraction Accuracy**: >90% accuracy for key variables
- **Update Timeliness**: <24 hours from publication to detection
- **False Positive Rate**: <5% for change notifications

### Clinical Impact
- **Evidence Currency**: <30 days average lag from publication
- **Stakeholder Engagement**: >80% notification open rate
- **Decision Influence**: Documented impact on clinical practice

## Future Enhancements

### Advanced Features
1. **Machine Learning Integration**: Enhanced study screening and data extraction
2. **Natural Language Processing**: Automated abstract and full-text analysis
3. **Predictive Analytics**: Forecasting of evidence trends
4. **Multi-language Support**: Automated translation and screening

### Scalability
1. **Cloud Integration**: Distributed computing for large-scale analyses
2. **API Development**: Integration with external evidence sources
3. **Collaborative Features**: Multi-user update management
4. **Mobile Access**: Smartphone notification and review apps

## References

1. Elliott JH, et al. Living systematic reviews: an emerging opportunity to narrow the evidence-practice gap. PLoS Med 2014;11(2):e1001603.
2. Thomas J, et al. Living systematic reviews: towards real-time evidence for health policy and practice. BMJ 2017;359:j4898.
3. Akl EA, et al. Living systematic reviews: 4. Living guideline recommendations. J Clin Epidemiol 2017;91:47-53.

## Version History

- **Version 1.0**: Initial implementation (October 2025)
- **Version 1.1**: Enhanced machine learning integration (Planned: January 2026)
- **Version 2.0**: Multi-language support (Planned: June 2026)

## Contact Information

**Living Review Coordinator**: Dr Siddalingaiah H S
**Technical Support**: Automated Research Systems Team
**Stakeholder Inquiries**: livingreview@drugresistanttb-nma.org

---

*This living review protocol is itself a living document, updated as methods and technologies evolve.*
