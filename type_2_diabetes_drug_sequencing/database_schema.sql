-- Type 2 Diabetes Drug Sequencing Research Project Database Schema
-- Comprehensive schema for network meta-analysis of diabetes medications

-- Main studies table
CREATE TABLE studies (
    study_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pmid TEXT UNIQUE,
    nct_id TEXT,
    title TEXT NOT NULL,
    authors TEXT,
    journal TEXT,
    publication_year INTEGER,
    study_design TEXT CHECK (study_design IN ('RCT', 'Observational', 'Meta-analysis')),
    phase TEXT CHECK (phase IN ('Phase 2', 'Phase 3', 'Phase 4', 'Not applicable')),
    country TEXT,
    multicenter BOOLEAN DEFAULT 0,
    sample_size INTEGER,
    follow_up_months REAL,
    funding_source TEXT,
    registration TEXT,
    full_text_available BOOLEAN DEFAULT 0,
    inclusion_criteria TEXT,
    exclusion_criteria TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interventions table (for multi-arm studies)
CREATE TABLE interventions (
    intervention_id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_id INTEGER NOT NULL,
    arm_name TEXT NOT NULL,
    drug_class TEXT NOT NULL CHECK (drug_class IN ('SGLT2i', 'GLP-1RA', 'DPP-4i', 'TZD', 'Basal insulin', 'Prandial insulin', 'Dual therapy', 'Triple therapy', 'Placebo', 'Standard care')),
    specific_drug TEXT,
    dose TEXT,
    frequency TEXT,
    background_therapy TEXT,
    treatment_duration_months REAL,
    participants_randomized INTEGER,
    participants_completed INTEGER,
    FOREIGN KEY (study_id) REFERENCES studies(study_id) ON DELETE CASCADE
);

-- Baseline characteristics table
CREATE TABLE baseline_characteristics (
    characteristic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_id INTEGER NOT NULL,
    intervention_id INTEGER,
    characteristic_type TEXT NOT NULL,
    characteristic_name TEXT NOT NULL,
    mean_value REAL,
    sd_value REAL,
    median_value REAL,
    q1_value REAL,
    q3_value REAL,
    min_value REAL,
    max_value REAL,
    n_participants INTEGER,
    percentage_value REAL,
    reported_units TEXT,
    FOREIGN KEY (study_id) REFERENCES studies(study_id) ON DELETE CASCADE,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id) ON DELETE CASCADE
);

-- Outcome measures table
CREATE TABLE outcome_measures (
    outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_id INTEGER NOT NULL,
    intervention_id INTEGER,
    outcome_type TEXT NOT NULL CHECK (outcome_type IN ('HbA1c', 'CV_composite', 'eGFR_decline', 'ESKD', 'Hypoglycemia_severe', 'Weight_change', 'MACE', 'MI', 'Stroke', 'CV_death', 'All_cause_death')),
    timepoint_months INTEGER NOT NULL,
    outcome_measure TEXT NOT NULL,
    n_events INTEGER,
    n_participants INTEGER,
    effect_size REAL,
    confidence_interval_lower REAL,
    confidence_interval_upper REAL,
    p_value REAL,
    statistical_test TEXT,
    adjustment_factors TEXT,
    FOREIGN KEY (study_id) REFERENCES studies(study_id) ON DELETE CASCADE,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id) ON DELETE CASCADE
);

-- Moderator variables table
CREATE TABLE moderator_variables (
    moderator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_id INTEGER NOT NULL,
    intervention_id INTEGER,
    moderator_type TEXT NOT NULL CHECK (moderator_type IN ('ASCVD', 'CKD', 'HF', 'BMI', 'Diabetes_duration', 'Age', 'Sex', 'Race_ethnicity')),
    category_value TEXT,
    mean_value REAL,
    sd_value REAL,
    n_participants INTEGER,
    FOREIGN KEY (study_id) REFERENCES studies(study_id) ON DELETE CASCADE,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id) ON DELETE CASCADE
);

-- Risk of bias assessment
CREATE TABLE risk_of_bias (
    bias_id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_id INTEGER NOT NULL,
    domain TEXT NOT NULL CHECK (domain IN ('Random_sequence', 'Allocation_concealment', 'Blinding_participants', 'Blinding_outcome', 'Incomplete_data', 'Selective_reporting', 'Other_bias')),
    risk_level TEXT CHECK (risk_level IN ('Low', 'Unclear', 'High')),
    supporting_text TEXT,
    assessor_name TEXT,
    assessment_date DATE,
    FOREIGN KEY (study_id) REFERENCES studies(study_id) ON DELETE CASCADE
);

-- Data extraction tracking
CREATE TABLE data_extraction (
    extraction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_id INTEGER NOT NULL,
    extractor_name TEXT NOT NULL,
    extraction_date DATE NOT NULL,
    verification_status TEXT CHECK (verification_status IN ('Pending', 'Verified', 'Needs_revision')),
    verifier_name TEXT,
    verification_date DATE,
    notes TEXT,
    FOREIGN KEY (study_id) REFERENCES studies(study_id) ON DELETE CASCADE
);

-- Literature search results
CREATE TABLE literature_search (
    search_id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_date DATE NOT NULL,
    database_name TEXT NOT NULL CHECK (database_name IN ('PubMed', 'CENTRAL', 'ClinicalTrials.gov', 'Embase', 'Web_of_Science')),
    search_strategy TEXT NOT NULL,
    total_results INTEGER,
    included_results INTEGER,
    excluded_results INTEGER,
    search_notes TEXT
);

-- Study screening and selection
CREATE TABLE study_screening (
    screening_id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_id INTEGER,
    pmid TEXT,
    title TEXT,
    abstract TEXT,
    screening_stage TEXT CHECK (screening_stage IN ('Title_abstract', 'Full_text')),
    inclusion_status TEXT CHECK (inclusion_status IN ('Include', 'Exclude', 'Uncertain')),
    exclusion_reason TEXT,
    screener_name TEXT NOT NULL,
    screening_date DATE NOT NULL,
    kappa_agreement REAL,
    FOREIGN KEY (study_id) REFERENCES studies(study_id) ON DELETE SET NULL
);

-- Network meta-analysis results
CREATE TABLE nma_results (
    nma_id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_type TEXT NOT NULL,
    outcome_measure TEXT NOT NULL,
    comparison_intervention1 TEXT NOT NULL,
    comparison_intervention2 TEXT NOT NULL,
    effect_size REAL,
    confidence_interval_lower REAL,
    confidence_interval_upper REAL,
    p_value REAL,
    heterogeneity_i2 REAL,
    tau_squared REAL,
    rank_probability REAL,
    surface_under_cumulative_ranking REAL,
    analysis_date DATE NOT NULL,
    analysis_software TEXT,
    model_specifications TEXT
);

-- Create indexes for better performance
CREATE INDEX idx_studies_pmid ON studies(pmid);
CREATE INDEX idx_studies_year ON studies(publication_year);
CREATE INDEX idx_interventions_study ON interventions(study_id);
CREATE INDEX idx_interventions_drug_class ON interventions(drug_class);
CREATE INDEX idx_outcome_measures_study ON outcome_measures(study_id);
CREATE INDEX idx_outcome_measures_type ON outcome_measures(outcome_type);
CREATE INDEX idx_baseline_characteristics_study ON baseline_characteristics(study_id);
CREATE INDEX idx_moderator_variables_study ON moderator_variables(study_id);
CREATE INDEX idx_risk_of_bias_study ON risk_of_bias(study_id);
CREATE INDEX idx_data_extraction_study ON data_extraction(study_id);
CREATE INDEX idx_study_screening_pmid ON study_screening(pmid);
CREATE INDEX idx_nma_results_outcome ON nma_results(outcome_measure);

-- Create views for common queries
CREATE VIEW study_summary AS
SELECT
    s.study_id,
    s.pmid,
    s.title,
    s.authors,
    s.publication_year,
    s.study_design,
    s.sample_size,
    COUNT(DISTINCT i.intervention_id) as num_arms,
    GROUP_CONCAT(DISTINCT i.drug_class) as drug_classes
FROM studies s
LEFT JOIN interventions i ON s.study_id = i.study_id
GROUP BY s.study_id;

CREATE VIEW intervention_summary AS
SELECT
    i.intervention_id,
    i.study_id,
    s.title,
    i.arm_name,
    i.drug_class,
    i.specific_drug,
    i.participants_randomized,
    COUNT(DISTINCT om.outcome_id) as num_outcomes
FROM interventions i
JOIN studies s ON i.study_id = s.study_id
LEFT JOIN outcome_measures om ON i.intervention_id = om.intervention_id
GROUP BY i.intervention_id;
