# Data Preparation for Type 2 Diabetes Drug Sequencing NMA
# Script to format extracted study data for network meta-analysis

# Load required libraries
library(dplyr)
library(tidyr)
library(readr)
library(purrr)

# Create consolidated dataset from extracted studies
consolidate_study_data <- function() {
  # List all extracted data files
  data_files <- list.files("02_data_extraction",
                          pattern = "*_extraction.csv",
                          full.names = TRUE)

  # Read and combine all study data
  all_studies <- map_df(data_files, function(file) {
    study_name <- gsub("_extraction.csv", "", basename(file))

    # Read the file
    data <- read_csv(file, show_col_types = FALSE, col_types = cols(.default = "c"))

    # Add study identifier
    data$study_id <- study_name
    data$source_file <- basename(file)

    return(data)
  })

  return(all_studies)
}

# Extract treatment effects for NMA
extract_treatment_effects <- function(study_data) {
  # HbA1c outcomes
  hba1c_data <- study_data %>%
    filter(!is.na(`OUTCOME_HBA1C_ARM1_MD`)) %>%
    transmute(
      study_id,
      outcome = "HbA1c_reduction",
      treatment_arm1 = INTERVENTION_ARM1_DRUG_CLASS,
      treatment_arm2 = INTERVENTION_ARM2_DRUG_CLASS,
      treatment_arm3 = INTERVENTION_ARM3_DRUG_CLASS,
      effect_arm1 = as.numeric(gsub("%.*", "", `OUTCOME_HBA1C_ARM1_MD`)),
      effect_arm2 = as.numeric(gsub("%.*", "", `OUTCOME_HBA1C_ARM2_MD`)),
      effect_arm3 = as.numeric(gsub("%.*", "", `OUTCOME_HBA1C_ARM3_MD`)),
      baseline_hba1c_arm1 = as.numeric(gsub("%.*", "", `OUTCOME_HBA1C_ARM1_BASELINE_MEAN`)),
      baseline_hba1c_arm2 = as.numeric(gsub("%.*", "", `OUTCOME_HBA1C_ARM2_BASELINE_MEAN`)),
      baseline_hba1c_arm3 = as.numeric(gsub("%.*", "", `OUTCOME_HBA1C_ARM3_BASELINE_MEAN`))
    )

  # Weight outcomes
  weight_data <- study_data %>%
    filter(!is.na(`OUTCOME_WEIGHT_ARM1_MD`)) %>%
    transmute(
      study_id,
      outcome = "weight_change",
      treatment_arm1 = INTERVENTION_ARM1_DRUG_CLASS,
      treatment_arm2 = INTERVENTION_ARM2_DRUG_CLASS,
      treatment_arm3 = INTERVENTION_ARM3_DRUG_CLASS,
      effect_arm1 = as.numeric(gsub("kg.*", "", `OUTCOME_WEIGHT_ARM1_MD`)),
      effect_arm2 = as.numeric(gsub("kg.*", "", `OUTCOME_WEIGHT_ARM2_MD`)),
      effect_arm3 = as.numeric(gsub("kg.*", "", `OUTCOME_WEIGHT_ARM3_MD`)),
      baseline_weight_arm1 = as.numeric(gsub("kg.*", "", `OUTCOME_WEIGHT_ARM1_BASELINE_MEAN`)),
      baseline_weight_arm2 = as.numeric(gsub("kg.*", "", `OUTCOME_WEIGHT_ARM2_BASELINE_MEAN`)),
      baseline_weight_arm3 = as.numeric(gsub("kg.*", "", `OUTCOME_WEIGHT_ARM3_BASELINE_MEAN`))
    )

  # Cardiovascular outcomes (convert HR to log HR)
  cv_data <- study_data %>%
    filter(!is.na(`OUTCOME_CV_COMPOSITE_ARM1_EFFECT`)) %>%
    transmute(
      study_id,
      outcome = "cv_events",
      treatment_arm1 = INTERVENTION_ARM1_DRUG_CLASS,
      treatment_arm2 = INTERVENTION_ARM2_DRUG_CLASS,
      treatment_arm3 = INTERVENTION_ARM3_DRUG_CLASS,
      effect_arm1 = log(as.numeric(gsub("HR ", "", gsub(" .*", "", `OUTCOME_CV_COMPOSITE_ARM1_EFFECT`)))),
      effect_arm2 = log(as.numeric(gsub("HR ", "", gsub(" .*", "", `OUTCOME_CV_COMPOSITE_ARM2_EFFECT`)))),
      effect_arm3 = log(as.numeric(gsub("HR ", "", gsub(" .*", "", `OUTCOME_CV_COMPOSITE_ARM3_EFFECT`)))),
      cv_events_arm1 = as.numeric(gsub("/.*", "", `OUTCOME_CV_COMPOSITE_ARM1_EVENTS`)),
      cv_events_arm2 = as.numeric(gsub("/.*", "", `OUTCOME_CV_COMPOSITE_ARM2_EVENTS`)),
      cv_events_arm3 = as.numeric(gsub("/.*", "", `OUTCOME_CV_COMPOSITE_ARM3_EVENTS`))
    )

  # Combine all outcomes
  combined_data <- bind_rows(
    hba1c_data %>% mutate(outcome_type = "continuous"),
    weight_data %>% mutate(outcome_type = "continuous"),
    cv_data %>% mutate(outcome_type = "binary")
  )

  return(combined_data)
}

# Create network geometry visualization data
create_network_data <- function(treatment_data) {
  # Define treatment nodes
  treatments <- c(
    "SGLT2i", "GLP-1RA", "DPP-4i", "TZD",
    "SGLT2i+DPP-4i", "TZD+SGLT2i+Metformin", "Tirzepatide"
  )

  # Create comparison matrix
  comparisons <- expand.grid(treatments, treatments, stringsAsFactors = FALSE)
  colnames(comparisons) <- c("treatment1", "treatment2")

  # Filter out self-comparisons
  comparisons <- comparisons %>%
    filter(treatment1 != treatment2) %>%
    mutate(comparison = paste(treatment1, "vs", treatment2))

  # Count available comparisons from data
  comparison_counts <- treatment_data %>%
    group_by(treatment_arm1, treatment_arm2) %>%
    summarise(
      n_studies = n_distinct(study_id),
      outcomes = paste(unique(outcome), collapse = ", ")
    ) %>%
    filter(!is.na(treatment_arm2)) %>%
    rename(treatment1 = treatment_arm1, treatment2 = treatment_arm2)

  # Merge with comparison grid
  network_data <- comparisons %>%
    left_join(comparison_counts, by = c("treatment1", "treatment2")) %>%
    mutate(
      n_studies = ifelse(is.na(n_studies), 0, n_studies),
      available = n_studies > 0
    )

  return(network_data)
}

# Generate summary statistics for each outcome
generate_outcome_summary <- function(combined_data) {
  outcome_summary <- combined_data %>%
    group_by(outcome) %>%
    summarise(
      n_studies = n_distinct(study_id),
      n_treatments = n_distinct(c(treatment_arm1, treatment_arm2, treatment_arm3)),
      treatments_included = paste(unique(c(treatment_arm1, treatment_arm2, treatment_arm3)), collapse = ", "),
      effect_range = paste(round(min(c(effect_arm1, effect_arm2, effect_arm3), na.rm = TRUE), 2),
                          "to",
                          round(max(c(effect_arm1, effect_arm2, effect_arm3), na.rm = TRUE), 2))
    )

  return(outcome_summary)
}

# Create data quality report
generate_quality_report <- function(study_data) {
  quality_metrics <- data.frame(
    metric = character(),
    value = numeric(),
    description = character(),
    stringsAsFactors = FALSE
  )

  # Study characteristics
  n_studies <- nrow(study_data)
  n_rcts <- sum(grepl("RCT", study_data$STUDY_DESIGN))
  n_reviews <- sum(grepl("Review|Meta|SRMA", study_data$STUDY_DESIGN))

  quality_metrics <- rbind(quality_metrics, data.frame(
    metric = c("total_studies", "rct_studies", "review_studies", "mean_sample_size"),
    value = c(n_studies, n_rcts, n_reviews, mean(as.numeric(study_data$SAMPLE_SIZE), na.rm = TRUE)),
    description = c(
      "Total number of included studies",
      "Number of randomized controlled trials",
      "Number of systematic reviews/meta-analyses",
      "Average sample size across studies"
    )
  ))

  return(quality_metrics)
}

# Main data preparation function
prepare_analysis_data <- function() {
  cat("Consolidating study data...\n")
  study_data <- consolidate_study_data()

  cat("Extracting treatment effects...\n")
  treatment_effects <- extract_treatment_effects(study_data)

  cat("Creating network geometry data...\n")
  network_data <- create_network_data(treatment_effects)

  cat("Generating outcome summaries...\n")
  outcome_summary <- generate_outcome_summary(treatment_effects)

  cat("Generating quality report...\n")
  quality_report <- generate_quality_report(study_data)

  # Save prepared datasets
  write_csv(study_data, "03_statistical_analysis/data/consolidated_study_data.csv")
  write_csv(treatment_effects, "03_statistical_analysis/data/treatment_effects.csv")
  write_csv(network_data, "03_statistical_analysis/data/network_geometry.csv")
  write_csv(outcome_summary, "03_statistical_analysis/data/outcome_summary.csv")
  write_csv(quality_report, "03_statistical_analysis/data/quality_report.csv")

  cat("Data preparation complete!\n")

  return(list(
    study_data = study_data,
    treatment_effects = treatment_effects,
    network_data = network_data,
    outcome_summary = outcome_summary,
    quality_report = quality_report
  ))
}

# Create analysis-ready dataset for GeMTC
create_gemtc_dataset <- function(treatment_effects) {
  gemtc_list <- list()

  for(outcome in unique(treatment_effects$outcome)) {
    outcome_data <- treatment_effects %>%
      filter(outcome == !!outcome) %>%
      select(study_id, treatment_arm1, treatment_arm2, treatment_arm3,
             effect_arm1, effect_arm2, effect_arm3) %>%
      filter(!is.na(effect_arm1) | !is.na(effect_arm2) | !is.na(effect_arm3))

    if(nrow(outcome_data) > 0) {
      # Convert to long format for GeMTC
      long_data <- outcome_data %>%
        pivot_longer(
          cols = c(effect_arm1, effect_arm2, effect_arm3),
          names_to = "arm",
          values_to = "effect"
        ) %>%
        mutate(
          treatment = case_when(
            arm == "effect_arm1" ~ treatment_arm1,
            arm == "effect_arm2" ~ treatment_arm2,
            arm == "effect_arm3" ~ treatment_arm3
          )
        ) %>%
        filter(!is.na(effect), !is.na(treatment)) %>%
        select(study_id, treatment, effect)

      gemtc_list[[outcome]] <- long_data
    }
  }

  return(gemtc_list)
}

# Execute data preparation
if(interactive()) {
  prepared_data <- prepare_analysis_data()

  # Create GeMTC datasets
  gemtc_datasets <- create_gemtc_dataset(prepared_data$treatment_effects)

  # Save GeMTC datasets
  saveRDS(gemtc_datasets, "03_statistical_analysis/data/gemtc_datasets.rds")

  cat("\n=== DATA PREPARATION SUMMARY ===\n")
  cat("Studies processed:", nrow(prepared_data$study_data), "\n")
  cat("Treatment comparisons:", nrow(prepared_data$treatment_effects), "\n")
  cat("Network connections:", sum(prepared_data$network_data$n_studies), "\n")
  cat("Outcomes analyzed:", nrow(prepared_data$outcome_summary), "\n")

  print(prepared_data$outcome_summary)
  print(prepared_data$quality_report)

  cat("\nData preparation completed successfully!\n")
  cat("Ready for network meta-analysis.\n")
}
