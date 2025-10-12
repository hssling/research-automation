
Full Dataset:
- Total samples: %d
- RNA-seq available: %s (%s features)
- Microbiome available: %s (%s features)
- MTB WGS available: %s (%s features)
- Samples with outcomes: %s

Training Dataset:
- Training samples: %d
- Culture conversion available: %s samples
- Relapse data available: %s samples

Generated: %s
",
  summary_stats$full_dataset$n_samples,
  summary_stats$full_dataset$rnaseq_available,
  summary_stats$full_dataset$n_features["X_rnaseq"] %||% "N/A",
  summary_stats$full_dataset$microbiome_available,
  summary_stats$full_dataset$n_features["X_microbiome"] %||% "N/A",
  summary_stats$full_dataset$mtb_wgs_available,
  summary_stats$full_dataset$n_features["X_mtb"] %||% "N/A",
  summary_stats$full_dataset$outcome_breakdown["TRUE"],
  summary_stats$training_dataset$n_training_samples,
  summary_stats$training_dataset$outcome_distribution["1"] %||% "0",
  summary_stats$training_dataset$relapse_distribution["1"] %||% "0",
  format(Sys.time())
  )

  writeLines(summary_text, summary_text_file)

  log_info("Matrix construction completed successfully ✅")
  log_info("All matrices saved to: {MATRICES_DIR}")
}

# ==============================================================================
# DEMO DATA GENERATION
# ==============================================================================

generate_demo_matrices <- function(n_omics = c(rnaseq = 50, microbiome = 30, mtb = 20)) {
  #' Generate demo multi-omics matrices for testing when real data unavailable

  log_info("Generating demo multi-omics matrices for pipeline testing")

  set.seed(42)

  n_samples <- sample(50:200, 1)  # Random sample size
  sample_ids <- sprintf("DEMO_%03d", 1:n_samples)

  demo_matrices <- list()

  # RNA-seq matrix
  if (runif(1) > 0.3) {  # 70% chance of having RNA-seq
    demo_matrices$X_rnaseq <- matrix(
      rnorm(n_samples * n_omics["rnaseq"], mean = 8, sd = 2),
      nrow = n_samples,
      dimnames = list(sample_ids, sprintf("GENE_%04d", 1:n_omics["rnaseq"]))
    )
  }

  # Microbiome matrix
  if (runif(1) > 0.2) {  # 80% chance of having microbiome
    micro_raw <- matrix(
      rpois(n_samples * n_omics["microbiome"] * 100, lambda = 100),
      nrow = n_omics["microbiome"],
      dimnames = list(sprintf("TAXA_%03d", 1:n_omics["microbiome"]), sample_ids)
    )
    # CLR transformation
    demo_matrices$X_microbiome <- t(clr(t(micro_raw + 1)))
  }

  # MTB WGS matrix
  if (runif(1) > 0.3) {  # 70% chance of having MTB data
    demo_matrices$X_mtb <- matrix(
      rbinom(n_samples * n_omics["mtb"], 1, 0.2),  # Binary features (resistance, etc.)
      nrow = n_samples,
      dimnames = list(sample_ids, sprintf("MTB_FEAT_%02d", 1:n_omics["mtb"]))
    )
  }

  # Outcome data
  outcome_probs <- list(
    culture_success = rbeta(n_samples, 2, 1),
    relapse_risk = rbeta(n_samples, 1, 3)
  )

  demo_matrices$y_outcomes <- data.frame(
    patient_timepoint_id = sample_ids,
    culture_conversion_6mo = rbinom(n_samples, 1, outcome_probs$culture_success),
    relapse_12mo = rbinom(n_samples, 1, 1 - outcome_probs$relapse_risk),
    treatment_failure = NA  # Will be computed
  ) %>%
    mutate(
      treatment_failure = culture_conversion_6mo == 0 | relapse_12mo == 1,
      outcome_available = TRUE
    )

  demo_matrices$sample_metadata <- demo_matrices$y_outcomes

  log_info("Demo matrices generated: {n_samples} samples")
  log_info("Available omics: {paste(grep('^X_', names(demo_matrices), value=TRUE), collapse=', ')}")

  return(demo_matrices)
}

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

main <- function() {
  #' Main matrix construction workflow

  tryCatch({
    # Load clinical data
    clinical_df <- load_clinical_data()

    # Build individual omics matrices
    rnaseq_matrix <- build_rnaseq_matrix(clinical_df)
    microbiome_matrix <- build_microbiome_matrix(clinical_df)
    mtb_matrix <- build_mtb_wgs_matrix(clinical_df)

    # Check if any omics data available
    if (is.null(rnaseq_matrix) && is.null(microbiome_matrix) && is.null(mtb_matrix)) {
      log_warn("No real omics data found - generating demo data for testing")

      demo_matrices <- generate_demo_matrices()
      rnaseq_matrix <- demo_matrices$X_rnaseq
      microbiome_matrix <- demo_matrices$X_microbiome
      mtb_matrix <- demo_matrices$X_mtb
      clinical_df <- demo_matrices$sample_metadata  # Override with demo clinical
    }

    # Align matrices to common sample space
    aligned_matrices <- align_matrices(clinical_df, rnaseq_matrix, microbiome_matrix, mtb_matrix)

    if (is.null(aligned_matrices)) {
      log_error("Matrix alignment failed")
      return(invisible(FALSE))
    }

    # Isolate training data
    training_data <- isolate_training_data(aligned_matrices)

    if (is.null(training_data)) {
      log_error("Training data isolation failed")
      return(invisible(FALSE))
    }

    # Save all matrices
    save_processed_matrices(aligned_matrices, training_data)

    log_info("Matrix construction workflow completed successfully ✅")

  }, error = function(e) {
    log_error("Matrix construction failed: {e$message}")
    return(invisible(FALSE))
  })

  return(invisible(TRUE))
}

# Execute if run as script
if (!interactive()) {
  main()
}

log_info("01_make_matrices.R loaded successfully - call main() to construct multi-omics matrices")
# ==============================================================================
#!/usr/bin/env Rscript
# Builds analysis-ready matrices: X_host, X_micro, X_mtb and targets y_response & y_relapse.

suppressPackageStartupMessages({
  library(dplyr); library(readr); library(tidyr); library(stringr); library(here)
})

fin_dir <- here("04_omics_advanced/mdrtb/data_final")
dir.create(fin_dir, recursive = TRUE, showWarnings = FALSE)

# ---- EDIT INPUTS ----
host_counts <- here("04_omics_advanced/mdrtb/rnaseq/results/vst_counts.tsv")      # gene x sample
micro_abund <- here("04_omics_advanced/mdrtb/microbiome/results/taxa_abundance.tsv") # taxa x sample (CLR or rel. abundance)
mtb_feats   <- here("04_omics_advanced/mdrtb/mtb_wgs/results/mtb_variant_matrix.tsv")# variant x sample (0/1)
clin_file   <- here("04_omics_advanced/mdrtb/data_final/clinical_harmonized.csv")

stopifnot(file.exists(host_counts), file.exists(micro_abund), file.exists(mtb_feats), file.exists(clin_file))

# helper to wide->samples in rows
t_to_samples <- function(df, id_col){
  df %>% rename(feature = {{id_col}}) %>%
    tidyr::pivot_longer(-feature, names_to = "sample_id", values_to = "value") %>%
    tidyr::pivot_wider(names_from = feature, values_from = value)
}

host <- readr::read_tsv(host_counts, show_col_types = FALSE)
micro <- readr::read_tsv(micro_abund, show_col_types = FALSE)
mtb  <- readr::read_tsv(mtb_feats, show_col_types = FALSE)

# Standardize
host_w <- t_to_samples(host, 1)
micro_w<- t_to_samples(micro,1)
mtb_w  <- t_to_samples(mtb,1)

# Merge with clinical targets
clin <- readr::read_csv(clin_file, show_col_types = FALSE) %>%
  select(sample_id, patient_id, timepoint, response_6m, relapse_12m, age, sex, hiv, diabetes, cavity, lineage, regimen)

# Align to common sample IDs (baseline preferred if multiple TPs)
common <- Reduce(intersect, list(host_w$sample_id, micro_w$sample_id, mtb_w$sample_id, clin$sample_id))
host_w  <- host_w  %>% filter(sample_id %in% common)
micro_w <- micro_w %>% filter(sample_id %in% common)
mtb_w   <- mtb_w   %>% filter(sample_id %in% common)
clin    <- clin    %>% filter(sample_id %in% common)

# Write matrices
readr::write_csv(host_w, file.path(fin_dir, "X_host.csv"))
readr::write_csv(micro_w, file.path(fin_dir, "X_micro.csv"))
readr::write_csv(mtb_w,  file.path(fin_dir, "X_mtb.csv"))
readr::write_csv(clin,   file.path(fin_dir, "y_clinical.csv"))
cat("✅ X_host.csv, X_micro.csv, X_mtb.csv, y_clinical.csv written\n")
=============================================

Full Dataset:
- Total samples: %d
- RNA-seq available: %s (%s features)
- Microbiome available: %s (%s features)
- MTB WGS available: %s (%s features)
- Samples with outcomes: %s

Training Dataset:
- Training samples: %d
- Culture conversion available: %s samples
- Relapse data available: %s samples

Generated: %s
",
  summary_stats$full_dataset$n_samples,
  summary_stats$full_dataset$rnaseq_available,
  summary_stats$full_dataset$n_features["X_rnaseq"] %||% "N/A",
  summary_stats$full_dataset$microbiome_available,
  summary_stats$full_dataset$n_features["X_microbiome"] %||% "N/A",
  summary_stats$full_dataset$mtb_wgs_available,
  summary_stats$full_dataset$n_features["X_mtb"] %||% "N/A",
  summary_stats$full_dataset$outcome_breakdown["TRUE"],
  summary_stats$training_dataset$n_training_samples,
  summary_stats$training_dataset$outcome_distribution["1"] %||% "0",
  summary_stats$training_dataset$relapse_distribution["1"] %||% "0",
  format(Sys.time())
  )

  writeLines(summary_text, summary_text_file)

  log_info("Matrix construction completed successfully ✅")
  log_info("All matrices saved to: {MATRICES_DIR}")
}

# ==============================================================================
# DEMO DATA GENERATION
# ==============================================================================

generate_demo_matrices <- function(n_omics = c(rnaseq = 50, microbiome = 30, mtb = 20)) {
  #' Generate demo multi-omics matrices for testing when real data unavailable

  log_info("Generating demo multi-omics matrices for pipeline testing")

  set.seed(42)

  n_samples <- sample(50:200, 1)  # Random sample size
  sample_ids <- sprintf("DEMO_%03d", 1:n_samples)

  demo_matrices <- list()

  # RNA-seq matrix
  if (runif(1) > 0.3) {  # 70% chance of having RNA-seq
    demo_matrices$X_rnaseq <- matrix(
      rnorm(n_samples * n_omics["rnaseq"], mean = 8, sd = 2),
      nrow = n_samples,
      dimnames = list(sample_ids, sprintf("GENE_%04d", 1:n_omics["rnaseq"]))
    )
  }

  # Microbiome matrix
  if (runif(1) > 0.2) {  # 80% chance of having microbiome
    micro_raw <- matrix(
      rpois(n_samples * n_omics["microbiome"] * 100, lambda = 100),
      nrow = n_omics["microbiome"],
      dimnames = list(sprintf("TAXA_%03d", 1:n_omics["microbiome"]), sample_ids)
    )
    # CLR transformation
    demo_matrices$X_microbiome <- t(clr(t(micro_raw + 1)))
  }

  # MTB WGS matrix
  if (runif(1) > 0.3) {  # 70% chance of having MTB data
    demo_matrices$X_mtb <- matrix(
      rbinom(n_samples * n_omics["mtb"], 1, 0.2),  # Binary features (resistance, etc.)
      nrow = n_samples,
      dimnames = list(sample_ids, sprintf("MTB_FEAT_%02d", 1:n_omics["mtb"]))
    )
  }

  # Outcome data
  outcome_probs <- list(
    culture_success = rbeta(n_samples, 2, 1),
    relapse_risk = rbeta(n_samples, 1, 3)
  )

  demo_matrices$y_outcomes <- data.frame(
    patient_timepoint_id = sample_ids,
    culture_conversion_6mo = rbinom(n_samples, 1, outcome_probs$culture_success),
    relapse_12mo = rbinom(n_samples, 1, 1 - outcome_probs$relapse_risk),
    treatment_failure = NA  # Will be computed
  ) %>%
    mutate(
      treatment_failure = culture_conversion_6mo == 0 | relapse_12mo == 1,
      outcome_available = TRUE
    )

  demo_matrices$sample_metadata <- demo_matrices$y_outcomes

  log_info("Demo matrices generated: {n_samples} samples")
  log_info("Available omics: {paste(grep('^X_', names(demo_matrices), value=TRUE), collapse=', ')}")

  return(demo_matrices)
}

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

main <- function() {
  #' Main matrix construction workflow

  tryCatch({
    # Load clinical data
    clinical_df <- load_clinical_data()

    # Build individual omics matrices
    rnaseq_matrix <- build_rnaseq_matrix(clinical_df)
    microbiome_matrix <- build_microbiome_matrix(clinical_df)
    mtb_matrix <- build_mtb_wgs_matrix(clinical_df)

    # Check if any omics data available
    if (is.null(rnaseq_matrix) && is.null(microbiome_matrix) && is.null(mtb_matrix)) {
      log_warn("No real omics data found - generating demo data for testing")

      demo_matrices <- generate_demo_matrices()
      rnaseq_matrix <- demo_matrices$X_rnaseq
      microbiome_matrix <- demo_matrices$X_microbiome
      mtb_matrix <- demo_matrices$X_mtb
      clinical_df <- demo_matrices$sample_metadata  # Override with demo clinical
    }

    # Align matrices to common sample space
    aligned_matrices <- align_matrices(clinical_df, rnaseq_matrix, microbiome_matrix, mtb_matrix)

    if (is.null(aligned_matrices)) {
      log_error("Matrix alignment failed")
      return(invisible(FALSE))
    }

    # Isolate training data
    training_data <- isolate_training_data(aligned_matrices)

    if (is.null(training_data)) {
      log_error("Training data isolation failed")
      return(invisible(FALSE))
    }

    # Save all matrices
    save_processed_matrices(aligned_matrices, training_data)

    log_info("Matrix construction workflow completed successfully ✅")

  }, error = function(e) {
    log_error("Matrix construction failed: {e$message}")
    return(invisible(FALSE))
  })

  return(invisible(TRUE))
}

# Execute if run as script
if (!interactive()) {
  main()
}

log_info("01_make_matrices.R loaded successfully - call main() to construct multi-omics matrices")
# ==============================================================================
