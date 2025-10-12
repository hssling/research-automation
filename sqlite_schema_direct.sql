-- =============================================
-- RESEARCH AUTOMATION PLATFORM - SQLITE SCHEMA
-- Direct SQLite version for immediate deployment
-- =============================================

-- =============================================
-- USER MANAGEMENT & AUTHENTICATION
-- =============================================

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    institution TEXT,
    research_field TEXT DEFAULT 'other',
    role TEXT DEFAULT 'researcher',
    api_key TEXT UNIQUE,

    email_verified INTEGER DEFAULT 0,
    two_factor_enabled INTEGER DEFAULT 0,
    account_status TEXT DEFAULT 'pending_verification',

    profile_picture_url TEXT,
    bio TEXT,
    orcid_id TEXT,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT,

    UNIQUE(email)
);

CREATE TABLE user_expertise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    expertise_area TEXT NOT NULL,
    proficiency_level TEXT DEFAULT 'intermediate',

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, expertise_area)
);

-- =============================================
-- RESEARCH PROJECT MANAGEMENT
-- =============================================

CREATE TABLE research_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    research_question TEXT NOT NULL,

    methodology TEXT NOT NULL,
    status TEXT DEFAULT 'planning_phase',

    owner_id INTEGER NOT NULL,
    funding_source TEXT,
    grant_number TEXT,
    clinical_trial_number TEXT,

    target_population TEXT,
    intervention TEXT,
    comparator TEXT,
    outcome_measures TEXT,

    prisma_registered INTEGER DEFAULT 0,
    prospero_registration_number TEXT,

    start_date TEXT,
    target_completion_date TEXT,
    actual_completion_date TEXT,

    visibility TEXT DEFAULT 'private',
    repository_url TEXT,
    preprint_url TEXT,

    keywords TEXT,
    research_tags TEXT,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE project_collaborators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role TEXT DEFAULT 'co_author',
    permissions TEXT,

    invited_at TEXT DEFAULT CURRENT_TIMESTAMP,
    joined_at TEXT,
    last_accessed TEXT,

    UNIQUE(project_id, user_id),
    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- =============================================
-- LITERATURE MANAGEMENT SYSTEM
-- =============================================

CREATE TABLE literature_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pubmed_id TEXT UNIQUE,
    doi TEXT UNIQUE,
    pmcid TEXT,

    title TEXT NOT NULL,
    abstract TEXT,
    authors TEXT, -- JSON string for author array
    journal TEXT,
    publication_year INTEGER,
    volume TEXT,
    issue TEXT,
    pages TEXT,

    study_type TEXT DEFAULT 'other',
    study_design TEXT,
    population TEXT,
    intervention TEXT,
    comparator TEXT,
    outcomes TEXT,

    keywords TEXT,
    mesh_terms TEXT,

    full_text_url TEXT,
    pdf_url TEXT,

    citation_count INTEGER DEFAULT 0,
    altmetric_score REAL,
    quality_score REAL DEFAULT 0.0,

    date_added TEXT DEFAULT CURRENT_TIMESTAMP,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(pubmed_id, doi)
);

CREATE TABLE literature_searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    search_name TEXT NOT NULL,
    search_description TEXT,
    search_strategy TEXT,

    databases_searched TEXT,
    search_dates TEXT,
    inclusion_criteria TEXT,
    exclusion_criteria TEXT,

    total_records_found INTEGER DEFAULT 0,
    duplicates_removed INTEGER DEFAULT 0,
    total_screened_title_abstract INTEGER DEFAULT 0,
    total_screened_full_text INTEGER DEFAULT 0,
    total_included INTEGER DEFAULT 0,

    search_date TEXT DEFAULT CURRENT_TIMESTAMP,
    executed_by INTEGER NOT NULL,

    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (executed_by) REFERENCES users(id)
);

CREATE TABLE search_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    inclusion_status TEXT DEFAULT 'pending',
    exclusion_reason TEXT,
    exclusion_criteria_failing TEXT,

    screening_stage TEXT DEFAULT 'title_abstract',
    screened_by INTEGER,
    screened_at TEXT DEFAULT CURRENT_TIMESTAMP,

    is_duplicate INTEGER DEFAULT 0,
    duplicate_of_id INTEGER,

    UNIQUE(search_id, article_id),
    FOREIGN KEY (search_id) REFERENCES literature_searches(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES literature_articles(id),
    FOREIGN KEY (screened_by) REFERENCES users(id),
    FOREIGN KEY (duplicate_of_id) REFERENCES search_results(id)
);

-- =============================================
-- DATA EXTRACTION SYSTEM
-- =============================================

CREATE TABLE extraction_forms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    form_type TEXT DEFAULT 'systematic_review',
    form_schema TEXT,
    field_dependencies TEXT,

    created_by INTEGER NOT NULL,
    is_template INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,

    usage_count INTEGER DEFAULT 0,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE extracted_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    extraction_form_id INTEGER NOT NULL,

    data_values TEXT,
    extraction_notes TEXT,

    extracted_by INTEGER NOT NULL,
    extracted_at TEXT DEFAULT CURRENT_TIMESTAMP,

    extraction_status TEXT DEFAULT 'draft',
    validation_status TEXT DEFAULT 'pending',
    validation_notes TEXT,
    validated_by INTEGER,
    validated_at TEXT,

    version_number INTEGER DEFAULT 1,
    is_latest_version INTEGER DEFAULT 1,

    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES literature_articles(id),
    FOREIGN KEY (extraction_form_id) REFERENCES extraction_forms(id),
    FOREIGN KEY (extracted_by) REFERENCES users(id),
    FOREIGN KEY (validated_by) REFERENCES users(id)
);

-- =============================================
-- QUALITY ASSESSMENT
-- =============================================

CREATE TABLE quality_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,

    assessment_tool TEXT,
    assessment_data TEXT,
    overall_risk_of_bias TEXT DEFAULT 'unclear',

    assessed_by INTEGER NOT NULL,
    assessed_at TEXT DEFAULT CURRENT_TIMESTAMP,

    version INTEGER DEFAULT 1,
    is_final_assessment INTEGER DEFAULT 0,

    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES literature_articles(id),
    FOREIGN KEY (assessed_by) REFERENCES users(id)
);

-- =============================================
-- META-ANALYSIS ENGINE
-- =============================================

CREATE TABLE meta_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    analysis_name TEXT NOT NULL,
    analysis_description TEXT,

    effect_measure TEXT NOT NULL,
    analysis_model TEXT DEFAULT 'random_effects',
    heterogeneity_estimator TEXT DEFAULT 'dersimonian_laird',

    inclusion_criteria TEXT,
    exclusion_criteria TEXT,
    subgroup_definitions TEXT,

    risk_of_bias_integration INTEGER DEFAULT 1,
    sensitivity_analyses_planned TEXT,

    status TEXT DEFAULT 'configuring',
    created_by INTEGER NOT NULL,
    started_at TEXT,
    completed_at TEXT,
    execution_time_seconds INTEGER,

    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE meta_analysis_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,

    overall_effect REAL,
    effect_se REAL,
    effect_ci_lower REAL,
    effect_ci_upper REAL,

    z_statistic REAL,
    p_value REAL,

    heterogeneity_i2 REAL,
    heterogeneity_q REAL,
    heterogeneity_p_value REAL,
    between_study_variance REAL,

    prediction_interval_lower REAL,
    prediction_interval_upper REAL,

    total_studies INTEGER,
    total_participants INTEGER,
    studies_excluded_outliers INTEGER DEFAULT 0,

    forest_plot_url TEXT,
    funnel_plot_url TEXT,
    galbraith_plot_url TEXT,

    results_json TEXT,

    model_convergence INTEGER DEFAULT 1,
    model_warnings TEXT,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (analysis_id) REFERENCES meta_analyses(id) ON DELETE CASCADE
);

-- =============================================
-- MANUSCRIPT MANAGEMENT
-- =============================================

CREATE TABLE manuscripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,

    manuscript_type TEXT NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT,
    keywords TEXT,

    target_journal TEXT,
    submission_deadline TEXT,

    prisma_checklist_completed INTEGER DEFAULT 0,
    prisma_checklist_data TEXT,

    introduction_content TEXT,
    methods_content TEXT,
    results_content TEXT,
    discussion_content TEXT,
    conclusion_content TEXT,
    references_content TEXT,

    word_count INTEGER DEFAULT 0,
    table_count INTEGER DEFAULT 0,
    figure_count INTEGER DEFAULT 0,

    status TEXT DEFAULT 'draft',
    created_by INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE manuscript_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manuscript_id INTEGER NOT NULL,

    version_number INTEGER NOT NULL,
    version_name TEXT,
    version_description TEXT,

    content_snapshot TEXT,
    abstract_snapshot TEXT,
    keywords_snapshot TEXT,

    ai_assisted INTEGER DEFAULT 0,
    ai_model_used TEXT,
    ai_generation_prompt TEXT,
    human_revisions INTEGER DEFAULT 0,

    created_by INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (manuscript_id) REFERENCES manuscripts(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- =============================================
-- API MANAGEMENT
-- =============================================

CREATE TABLE api_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token_name TEXT NOT NULL,
    token_hash TEXT UNIQUE NOT NULL,
    permissions TEXT,
    expires_at TEXT,
    last_used TEXT,
    is_active INTEGER DEFAULT 1,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_type TEXT DEFAULT 'user_action',
    user_id INTEGER,
    project_id INTEGER,
    action TEXT,
    description TEXT,
    metadata TEXT,
    ip_address TEXT,
    user_agent TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE SET NULL
);

-- =============================================
-- INDEXES FOR PERFORMANCE
-- =============================================

CREATE INDEX idx_users_email_status ON users(email, account_status);
CREATE INDEX idx_projects_status_methodology ON research_projects(status, methodology);
CREATE INDEX idx_projects_owner_dates ON research_projects(owner_id, start_date, target_completion_date);
CREATE INDEX idx_articles_pubmed_doi ON literature_articles(pubmed_id, doi);
CREATE INDEX idx_articles_year_type ON literature_articles(publication_year, study_type);
CREATE INDEX idx_searches_project_date ON literature_searches(project_id, search_date);
