-- =============================================
-- RESEARCH AUTOMATION PLATFORM - DATABASE SCHEMA
-- Enterprise-grade scientific research automation
-- =============================================

CREATE DATABASE IF NOT EXISTS research_automation_production
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE research_automation_production;

-- Enable foreign keys and strict mode
SET FOREIGN_KEY_CHECKS = 1;
SET SQL_MODE = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

-- =============================================
-- USER MANAGEMENT & AUTHENTICATION
-- =============================================

CREATE TABLE users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    institution VARCHAR(500),
    research_field ENUM(
        'public_health', 'clinical_medicine', 'epidemiology',
        'basic_science', 'health_policy', 'bioinformatics',
        'data_science', 'health_economics', 'other'
    ) DEFAULT 'other',
    role ENUM('researcher', 'principal_investigator', 'administrator', 'collaborator') DEFAULT 'researcher',
    api_key VARCHAR(255) UNIQUE,

    email_verified BOOLEAN DEFAULT FALSE,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    account_status ENUM('active', 'suspended', 'pending_verification') DEFAULT 'pending_verification',

    profile_picture_url VARCHAR(1000),
    bio TEXT,
    orcid_id VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,

    INDEX idx_email (email),
    INDEX idx_institution (institution),
    INDEX idx_research_field (research_field)
) ENGINE=InnoDB;

CREATE TABLE user_expertise (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    expertise_area VARCHAR(255) NOT NULL,
    proficiency_level ENUM('beginner', 'intermediate', 'expert', 'specialist') DEFAULT 'intermediate',

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_expertise (user_id, expertise_area)
) ENGINE=InnoDB;

-- =============================================
-- RESEARCH PROJECT MANAGEMENT
-- =============================================

CREATE TABLE research_projects (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    research_question TEXT NOT NULL,

    methodology ENUM(
        'systematic_review', 'meta_analysis', 'randomized_controlled_trial',
        'cohort_study', 'case_control_study', 'cross_sectional_study',
        'bibliometric_analysis', 'rapid_review', 'living_systematic_review',
        'clinical_guideline', 'other'
    ) NOT NULL,

    status ENUM(
        'planning_phase', 'literature_search', 'screening', 'data_extraction',
        'quality_assessment', 'analysis', 'manuscript_preparation',
        'peer_review', 'revisions', 'publication_ready', 'published', 'completed'
    ) DEFAULT 'planning_phase',

    owner_id INT UNSIGNED NOT NULL,
    funding_source VARCHAR(500),
    grant_number VARCHAR(255),
    clinical_trial_number VARCHAR(255),

    target_population VARCHAR(1000),
    intervention VARCHAR(1000),
    comparator VARCHAR(1000),
    outcome_measures TEXT,

    prisma_registered BOOLEAN DEFAULT FALSE,
    prospero_registration_number VARCHAR(100),

    start_date DATE,
    target_completion_date DATE,
    actual_completion_date DATE,

    visibility ENUM('private', 'collaborator_access', 'public_read', 'public_full') DEFAULT 'private',
    repository_url VARCHAR(1000),
    preprint_url VARCHAR(1000),

    keywords JSON,
    research_tags JSON,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (owner_id) REFERENCES users(id),
    INDEX idx_status (status),
    INDEX idx_methodology (methodology),
    INDEX idx_owner (owner_id),
    FULLTEXT idx_title_description (title, description)
) ENGINE=InnoDB;

CREATE TABLE project_collaborators (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id INT UNSIGNED NOT NULL,
    user_id INT UNSIGNED NOT NULL,
    role ENUM(
        'project_owner', 'lead_author', 'co_author', 'methodologist',
        'statistician', 'data_extractor', 'quality_assessor', 'reviewer', 'guest'
    ) DEFAULT 'co_author',

    permissions JSON, -- Flexible permissions {'read': true, 'write': true, 'admin': false}

    invited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    joined_at TIMESTAMP NULL,
    last_accessed TIMESTAMP NULL,

    UNIQUE KEY unique_project_collaborator (project_id, user_id),
    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_project_role (project_id, role)
) ENGINE=InnoDB;

-- =============================================
-- LITERATURE MANAGEMENT SYSTEM
-- =============================================

CREATE TABLE literature_articles (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    pubmed_id VARCHAR(20) UNIQUE,
    doi VARCHAR(100) UNIQUE,
    pmcid VARCHAR(20),

    title TEXT NOT NULL,
    abstract TEXT,
    authors JSON, -- Array of author objects with affiliations
    journal VARCHAR(500),
    publication_year YEAR,
    volume VARCHAR(50),
    issue VARCHAR(50),
    pages VARCHAR(50),

    study_type ENUM(
        'systematic_review', 'meta_analysis', 'randomized_trial',
        'controlled_trial', 'cohort_study', 'case_control_study',
        'cross_sectional_study', 'case_report', 'observational_study',
        'editorial', 'protocol', 'other'
    ) DEFAULT 'other',

    study_design JSON, -- Detailed study design information
    population VARCHAR(500),
    intervention VARCHAR(500),
    comparator VARCHAR(500),
    outcomes JSON,

    keywords JSON,
    mesh_terms JSON,

    full_text_url VARCHAR(1000),
    pdf_url VARCHAR(1000),

    citation_count INT DEFAULT 0,
    altmetric_score DECIMAL(8,2),
    quality_score DECIMAL(3,2) DEFAULT 0.0, -- 0.00 to 1.00

    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY unique_pubmed_doi (pubmed_id, doi),
    INDEX idx_pubmed_id (pubmed_id),
    INDEX idx_doi (doi),
    INDEX idx_journal (journal),
    INDEX idx_publication_year (publication_year),
    INDEX idx_study_type (study_type),
    FULLTEXT idx_title_abstract (title, abstract)
) ENGINE=InnoDB;

CREATE TABLE literature_searches (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id INT UNSIGNED NOT NULL,
    search_name VARCHAR(255) NOT NULL,
    search_description TEXT,
    search_strategy LONGTEXT, -- Complete search strategy with all databases

    databases_searched JSON, -- ['PubMed', 'Cochrane', 'Embase', 'Web of Science']
    search_dates JSON, -- Date ranges for each database
    inclusion_criteria TEXT,
    exclusion_criteria TEXT,

    total_records_found INT DEFAULT 0,
    duplicates_removed INT DEFAULT 0,
    total_screened_title_abstract INT DEFAULT 0,
    total_screened_full_text INT DEFAULT 0,
    total_included INT DEFAULT 0,

    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed_by INT UNSIGNED NOT NULL,

    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (executed_by) REFERENCES users(id),
    INDEX idx_project_search (project_id, search_date)
) ENGINE=InnoDB;

CREATE TABLE search_results (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    search_id INT UNSIGNED NOT NULL,
    article_id INT UNSIGNED NOT NULL,
    inclusion_status ENUM('pending', 'included', 'excluded', 'conflicting') DEFAULT 'pending',
    exclusion_reason TEXT,
    exclusion_criteria_failing TEXT,

    screening_stage ENUM('title_abstract', 'full_text', 'final_inclusion') DEFAULT 'title_abstract',
    screened_by INT UNSIGNED,
    screened_at TIMESTAMP NULL,

    -- Duplicate detection
    is_duplicate BOOLEAN DEFAULT FALSE,
    duplicate_of_id INT UNSIGNED,

    UNIQUE KEY unique_search_article (search_id, article_id),
    FOREIGN KEY (search_id) REFERENCES literature_searches(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES literature_articles(id),
    FOREIGN KEY (screened_by) REFERENCES users(id),
    FOREIGN KEY (duplicate_of_id) REFERENCES search_results(id),
    INDEX idx_search_status (search_id, inclusion_status),
    INDEX idx_screened_by (screened_by, screened_at)
) ENGINE=InnoDB;

-- =============================================
-- DATA EXTRACTION & QUALITY ASSESSMENT
-- =============================================

CREATE TABLE extraction_forms (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    form_type ENUM(
        'systematic_review', 'meta_analysis', 'clinical_trial',
        'observational_study', 'diagnostic_accuracy', 'economic_evaluation',
        'qualitative_research', 'other'
    ) DEFAULT 'systematic_review',

    form_schema JSON, -- Complete form definition with validation rules
    field_dependencies JSON, -- Logic for conditional fields

    created_by INT UNSIGNED NOT NULL,
    is_template BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,

    usage_count INT DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_form_type (form_type, is_template)
) ENGINE=InnoDB;

CREATE TABLE extracted_data (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id INT UNSIGNED NOT NULL,
    article_id INT UNSIGNED NOT NULL,
    extraction_form_id INT UNSIGNED NOT NULL,

    data_values JSON, -- Complete extracted data in structured format
    extraction_notes TEXT,

    extracted_by INT UNSIGNED NOT NULL,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    extraction_status ENUM('draft', 'completed', 'peer_review', 'validated', 'flagged', 'archived') DEFAULT 'draft',
    validation_status ENUM('pending', 'approved', 'minor_changes', 'major_changes', 'rejected') DEFAULT 'pending',

    validation_notes TEXT,
    validated_by INT UNSIGNED,
    validated_at TIMESTAMP NULL,

    version_number INT DEFAULT 1,
    is_latest_version BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES literature_articles(id),
    FOREIGN KEY (extraction_form_id) REFERENCES extraction_forms(id),
    FOREIGN KEY (extracted_by) REFERENCES users(id),
    FOREIGN KEY (validated_by) REFERENCES users(id),
    INDEX idx_project_extraction (project_id, extraction_status),
    INDEX idx_article_extraction (article_id, is_latest_version),
    INDEX idx_status_validation (extraction_status, validation_status)
) ENGINE=InnoDB;

CREATE TABLE quality_assessments (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id INT UNSIGNED NOT NULL,
    article_id INT UNSIGNED NOT NULL,

    assessment_tool ENUM(
        'cochrane_risk_of_bias_2', 'rohrs_i', 'jadsad',
        'newcastle_ottawa_scale', 'qualitative_research_checklist',
        'economic_evaluation_checklist', 'diagnostic_accuracy_checklist',
        'custom_tool'
    ),

    assessment_data JSON, -- Complete assessment responses
    overall_risk_of_bias ENUM('low', 'unclear', 'high', 'not_applicable') DEFAULT 'unclear',

    assessed_by INT UNSIGNED NOT NULL,
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    version INT DEFAULT 1,
    is_final_assessment BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES literature_articles(id),
    FOREIGN KEY (assessed_by) REFERENCES users(id),
    INDEX idx_project_assessment (project_id, overall_risk_of_bias),
    INDEX idx_assessment_tool (assessment_tool)
) ENGINE=InnoDB;

-- =============================================
-- META-ANALYSIS MANAGEMENT
-- =============================================

CREATE TABLE meta_analyses (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id INT UNSIGNED NOT NULL,
    analysis_name VARCHAR(255) NOT NULL,
    analysis_description TEXT,

    effect_measure ENUM('odds_ratio', 'risk_ratio', 'risk_difference',
                       'mean_difference', 'standardized_mean_difference',
                       'hazard_ratio', 'correlation_coefficient') NOT NULL,

    analysis_model ENUM('fixed_effects', 'random_effects', 'mixed_model') DEFAULT 'random_effects',
    heterogeneity_estimator ENUM('dersimonian_laird', 'paule_mandel', 'restricted_ml',
                                 'empirical_bayes', 'hunter_schmidt') DEFAULT 'dersimonian_laird',

    inclusion_criteria JSON,
    exclusion_criteria JSON,
    subgroup_definitions JSON,

    risk_of_bias_integration BOOLEAN DEFAULT TRUE,
    sensitivity_analyses_planned JSON,

    status ENUM('configuring', 'data_preparation', 'model_fitting',
               'diagnostics', 'reporting', 'completed', 'error') DEFAULT 'configuring',

    created_by INT UNSIGNED NOT NULL,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    execution_time_seconds INT NULL,

    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_project_analysis (project_id, status)
) ENGINE=InnoDB;

CREATE TABLE meta_analysis_results (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    analysis_id INT UNSIGNED NOT NULL,

    -- Overall results
    overall_effect DECIMAL(12,6),
    effect_se DECIMAL(12,6),
    effect_ci_lower DECIMAL(12,6),
    effect_ci_upper DECIMAL(12,6),

    z_statistic DECIMAL(8,4),
    p_value DECIMAL(12,8),

    -- Heterogeneity
    heterogeneity_i2 DECIMAL(5,2), -- Percentage (0-100)
    heterogeneity_q DECIMAL(12,4),
    heterogeneity_p_value DECIMAL(12,8),
    between_study_variance DECIMAL(12,6), -- tau²

    -- Prediction interval (for random effects)
    prediction_interval_lower DECIMAL(12,6),
    prediction_interval_upper DECIMAL(12,6),

    -- Study information
    total_studies INT,
    total_participants INT,
    studies_excluded_outliers INT DEFAULT 0,

    -- Visualization URLs
    forest_plot_url VARCHAR(1000),
    funnel_plot_url VARCHAR(1000),
    galbraith_plot_url VARCHAR(1000),

    -- Complete results data for advanced plotting/analytics
    results_json LONGTEXT,

    -- Model diagnostics
    model_convergence BOOLEAN DEFAULT TRUE,
    model_warnings TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (analysis_id) REFERENCES meta_analyses(id) ON DELETE CASCADE,
    INDEX idx_analysis_results (analysis_id)
) ENGINE=InnoDB;

-- =============================================
-- PUBLICATION & MANUSCRIPT MANAGEMENT
-- =============================================

CREATE TABLE manuscripts (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id INT UNSIGNED NOT NULL,

    manuscript_type ENUM(
        'systematic_review', 'meta_analysis', 'rapid_review', 'protocols',
        'clinical_guidelines', 'research_letter', 'commentary'
    ) NOT NULL,

    title VARCHAR(1000) NOT NULL,
    abstract TEXT,
    keywords JSON,

    target_journal VARCHAR(500),
    submission_deadline DATE,

    -- PRISMA compliance tracking
    prisma_checklist_completed BOOLEAN DEFAULT FALSE,
    prisma_checklist_data JSON,

    -- Manuscript content
    introduction_content LONGTEXT,
    methods_content LONGTEXT,
    results_content LONGTEXT,
    discussion_content LONGTEXT,
    conclusion_content LONGTEXT,
    references_content LONGTEXT,

    word_count INT DEFAULT 0,
    table_count INT DEFAULT 0,
    figure_count INT DEFAULT 0,

    status ENUM(
        'draft', 'peer_review_internal', 'revisions_internal',
        'editorial_review', 'revisions_external', 'final_draft',
        'submitted', 'published'
    ) DEFAULT 'draft',

    created_by INT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_project_manuscript (project_id, manuscript_type, status),
    FULLTEXT idx_title_abstract (title, abstract)
) ENGINE=InnoDB;

CREATE TABLE manuscript_versions (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    manuscript_id INT UNSIGNED NOT NULL,

    version_number INT NOT NULL,
    version_name VARCHAR(255), -- "First draft", "Post-peer review", etc.
    version_description TEXT,

    content_snapshot LONGTEXT, -- Complete manuscript at this version
    abstract_snapshot TEXT,
    keywords_snapshot JSON,

    -- AI usage tracking
    ai_assisted BOOLEAN DEFAULT FALSE,
    ai_model_used VARCHAR(255),
    ai_generation_prompt TEXT,
    human_revisions BOOLEAN DEFAULT FALSE,

    created_by INT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (manuscript_id) REFERENCES manuscripts(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_manuscript_version (manuscript_id, version_number)
) ENGINE=InnoDB;

-- =============================================
-- API ACCESS & SYSTEM LOGGING
-- =============================================

CREATE TABLE api_tokens (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    token_name VARCHAR(255) NOT NULL,
    token_hash VARCHAR(255) UNIQUE NOT NULL,

    permissions JSON, -- API permissions as JSON
    expires_at TIMESTAMP NULL,

    last_used TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_active (user_id, is_active)
) ENGINE=InnoDB;

CREATE TABLE system_logs (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    log_type ENUM(
        'user_action', 'api_call', 'system_event',
        'error', 'security_event', 'performance'
    ) DEFAULT 'user_action',

    user_id INT UNSIGNED,
    project_id INT UNSIGNED,

    action VARCHAR(255),
    description TEXT,
    metadata JSON,

    ip_address VARCHAR(45),
    user_agent TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE SET NULL,
    INDEX idx_type_date (log_type, created_at),
    INDEX idx_user_action (user_id, action)
) ENGINE=InnoDB;

-- =============================================
-- CREATE INDEXES FOR PERFORMANCE
-- =============================================

CREATE INDEX idx_users_email_status ON users(email, account_status);
CREATE INDEX idx_projects_status_methodology ON research_projects(status, methodology);
CREATE INDEX idx_projects_owner_dates ON research_projects(owner_id, start_date, target_completion_date);
CREATE INDEX idx_articles_pubmed_doi ON literature_articles(pubmed_id, doi);
CREATE INDEX idx_articles_year_type ON literature_articles(publication_year, study_type);
CREATE INDEX idx_searches_project_date ON literature_searches(project_id, search_date);

-- =============================================
-- CONCLUSION
-- =============================================
-- This database schema provides complete support for:
-- ✅ Research project lifecycle management
-- ✅ Multi-user collaboration and permissions
-- ✅ Literature database and systematic searching
-- ✅ Data extraction and quality assessment
-- ✅ Meta-analysis configuration and results storage
-- ✅ Manuscript generation and version control
-- ✅ API authentication and system logging
--
-- Next step: Install Laravel framework and create API endpoints
