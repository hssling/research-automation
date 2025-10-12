# Protocol: Physical Activity Modalities and Cognitive Reserve in Aging - Network Meta-Analysis

## PROSPERO Registration
PROSPERO Registration Number: [To be assigned upon submission]

## Research Question
Which type of physical activity (aerobic, resistance, mind-body like yoga/tai chi) most effectively enhances cognitive reserve and delays dementia onset in adults over 60?

## Objectives
1. To conduct a systematic review and network meta-analysis comparing the effectiveness of different physical activity modalities on cognitive reserve in adults aged ≥60 years
2. To rank the effectiveness of aerobic exercise, resistance training, and mind-body exercises (yoga, tai chi) for cognitive reserve enhancement and dementia prevention
3. To assess the relative effectiveness of these interventions using indirect comparisons where direct head-to-head trials are limited

## Background
Cognitive reserve refers to the brain's resilience to neuropathological damage and the effectiveness of compensatory mechanisms. Physical activity has been associated with cognitive benefits in aging populations, but different exercise modalities may have varying effects on cognitive reserve. While individual studies have examined specific exercise types, there is no comprehensive synthesis comparing all three major modalities. Network meta-analysis will allow ranking of these interventions and indirect comparisons.

## Methods

### Inclusion Criteria
1. **Population**: Adults aged ≥60 years, community-dwelling, without diagnosed dementia at baseline
2. **Interventions**: Aerobic exercise, resistance training, mind-body exercises (yoga, tai chi), or combinations thereof
3. **Controls**: Sedentary control groups, usual care, or active control groups
4. **Outcomes**: Measures of cognitive reserve (composite cognitive scores, executive function, global cognition) or dementia prevention (incidence of dementia, cognitive decline)
5. **Study Design**: Randomized controlled trials (RCTs), cluster RCTs, quasi-experimental studies with pre/post measurements
6. **Duration**: Intervention duration ≥12 weeks
7. **Language**: English studies only

### Exclusion Criteria
1. Pharmacological interventions
2. Mixed-age populations (mean age <60)
3. Studies with diagnosed dementia patients at baseline
4. Animal studies
5. Reviews, case reports, cross-sectional studies, or observational studies

### Search Strategy
Databases: PubMed, EMBASE, Cochrane Central Register of Controlled Trials (CENTRAL), PsycINFO, and Web of Science

Search terms will combine:
- Population: ("aged" OR "elderly" OR "older adult" OR "senior")
- Intervention: ("physical activity" OR "exercise" OR aerobic OR resistance OR "strength training" OR yoga OR tai OR chi OR "tai chi")
- Outcome: ("cognitive reserve" OR cognition OR "cognitive function" OR dementia OR "cognitive decline")
- Study type: (RCT OR randomized OR controlled)

### Study Selection Process
1. Title/abstract screening by two independent reviewers
2. Full-text screening by two independent reviewers
3. Resolution of disagreements by consensus with third reviewer

### Data Extraction
Data will include:
- Study characteristics (design, duration, sample size)
- Population demographics (age, sex, baseline cognitive status)
- Intervention details (type, intensity, frequency, duration)
- Outcome measures and results
- Risk of bias assessments

### Risk of Bias Assessment
Using Cochrane Risk of Bias 2.0 tool for RCTs and ROBINS-I for non-randomized studies.

### Data Synthesis
1. Conventional pair-wise meta-analysis using random-effects model
2. Network meta-analysis using Bayesian framework (geMTC package in R) for ranking interventions
3. Sensitivity analyses for study quality
4. Assessment of transitivity, consistency, and heterogeneity

### Software
- Review management: Covidence or Rayyan
- Statistical analysis: R (metafor, netmeta, gemtc packages)
- Network plots: GraphViz

### Timeline
- Protocol submission: Month 1
- Literature search: Month 2
- Screening/Analysis: Months 3-5
- Manuscript preparation: Months 6-8
- Submission: Month 9

## Ethics and Dissemination
This systematic review does not require ethical approval as it involves secondary analysis of published data.

Findings will be disseminated through:
1. Publication in a peer-reviewed journal
2. Conference presentations
3. Online repositories (OSF or Zenodo)

## Corresponding Author
[Researcher Name]
[Institution]
[Email]

## Protocol Amendments
Any amendments to this protocol will be documented and reported with rationale.
