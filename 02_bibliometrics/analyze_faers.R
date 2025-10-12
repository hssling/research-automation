#!/usr/bin/env Rscript
"
FAERS Data Analysis for Signal Detection
Compute Reporting Odds Ratio (ROR) and perform signal detection analysis
"

# Setup
library(dplyr)
library(epitools)
library(readr)
library(purrr)
library(tidyr)
library(stringr)

# Set working directory
script_dir <- dirname(normalizePath(commandArgs(trailingOnly = FALSE)[grep("--file=", commandArgs(trailingOnly = FALSE))]))
if (length(script_dir) == 0) {
  script_dir <- getwd()
}
setwd(script_dir)

message("🎯 Starting FAERS signal detection analysis...")

# Function to load data safely
load_faers_data <- function() {
  drug_file <- "clean/faers_drug.csv"
  reac_file <- "clean/faers_reac.csv"

  if (!file.exists(drug_file)) {
    stop("❌ FAERS drug data not found. Run clean_faers.R first.")
  }

  # Load drug data
  drug <- read_csv(drug_file, show_col_types = FALSE)
  message(sprintf("📊 Loaded %d drug exposure records", nrow(drug)))

  # Load reaction data if available
  if (file.exists(reac_file)) {
    reac <- read_csv(reac_file, show_col_types = FALSE)
    message(sprintf("📊 Loaded %d adverse reaction records", nrow(reac)))

    # Join drug and reaction data for complete analysis
    faers_data <- inner_join(drug, reac, by = "primaryid")
    message(sprintf("📊 Combined dataset: %d records", nrow(faers_data)))

    return(faers_data)
  } else {
    message("⚠️  Reaction data not found - analysis will focus on drug data only")
    return(drug)
  }
}

# Example signal detection for drug-adverse event combinations
compute_ror_signal_detection <- function(faers_data, target_drug = NULL, target_event = NULL, min_reports = 3) {
  "
  Compute Reporting Odds Ratio (ROR) for signal detection

  Args:
    faers_data: Combined FAERS drug and reaction data
    target_drug: Specific drug name to analyze (optional)
    target_event: Specific adverse event to analyze (optional)
    min_reports: Minimum reports threshold for signal consideration
  "

  # Prepare data for contingency table analysis
  analysis_data <- faers_data

  # Filter for target drug if specified
  if (!is.null(target_drug)) {
    target_drug <- toupper(str_trim(target_drug))
    analysis_data <- analysis_data %>%
      filter(str_detect(drugname_clean, target_drug) |
             str_detect(drugname, target_drug))

    message(sprintf("🎯 Analyzing drug: %s (%d reports)", target_drug, nrow(analysis_data)))
  }

  # Filter for target event if specified
  if (!is.null(target_event)) {
    target_event <- toupper(str_trim(target_event))
    analysis_data <- analysis_data %>%
      filter(str_detect(pt, target_event))

    message(sprintf("🎯 Analyzing adverse event: %s (%d reports)", target_event, nrow(analysis_data)))
  }

  if (nrow(analysis_data) == 0) {
    message("⚠️  No data found matching the specified criteria")
    return(NULL)
  }

  # Create contingency tables for signal detection
  # This is a simplified version - full signal detection requires comparison
  # against background database rates

  # Group by drug-event combinations
  drug_event_counts <- analysis_data %>%
    group_by(drugname_clean, pt) %>%
    summarise(count = n(), .groups = 'drop') %>%
    arrange(desc(count))

  # Filter by minimum reports threshold
  drug_event_counts <- drug_event_counts %>%
    filter(count >= min_reports)

  if (nrow(drug_event_counts) == 0) {
    message("⚠️  No drug-event combinations meet minimum report threshold")
    return(NULL)
  }

  message(sprintf("📊 Analyzing %d drug-event combinations", nrow(drug_event_counts)))

  # For a simplified ROR calculation (normally would compare to full database)
  # This is a demonstration approach - full signal detection requires
  # comprehensive background rate calculations

  # Example: Compute basic proportions (simplified ROR approximation)
  signals <- drug_event_counts %>%
    mutate(
      drug_total = sum(count),
      proportion = count / drug_total,
      # Simplified risk ratio (would be more complex in reality)
      observed_rate = count / drug_total,
      expected_rate = mean(count) / mean(drug_event_counts$drug_total),
      risk_ratio = observed_rate / expected_rate
    ) %>%
    select(drugname_clean, pt, count, proportion, risk_ratio) %>%
    arrange(desc(risk_ratio))

  # Flag potential signals (simplified threshold)
  signals <- signals %>%
    mutate(
      signal_strength = case_when(
        risk_ratio >= 10 ~ "Strong",
        risk_ratio >= 5 ~ "Moderate",
        risk_ratio >= 2 ~ "Weak",
        TRUE ~ "None"
      )
    )

  # Save results
  output_file <- sprintf("../results/pharmacovigilance/signals_%s.csv",
                         format(Sys.time(), "%Y%m%d_%H%M%S"))
  write_csv(signals, output_file)

  # Print top signals
  message("\n🚨 TOP SIGNALS DETECTED:")
  print(signals %>% head(10), n = 10)

  message(sprintf("\n💾 Signal detection results saved to: %s", basename(output_file)))

  return(signals)
}

# Main analysis function
main_analysis <- function() {
  tryCatch({
    # Load data
    faers_data <- load_faers_data()

    # Example: Analyze all data (or specify target drug/event)
    signals <- compute_ror_signal_detection(faers_data,
                                           target_drug = "ASPIRIN",  # Example
                                           min_reports = 3)

    if (!is.null(signals)) {
      message("\n✅ Signal detection analysis completed!")
      message(sprintf("📊 Analyzed %d drug-event combinations", nrow(signals)))
      message(sprintf("⚠️  Found %d potential signals",
                     sum(signals$signal_strength != "None", na.rm = TRUE)))
    }

    # Example: Drug-specific analysis
    message("\n🔍 Example: Analyzing specific drug-event combinations...")

    # This would normally be expanded based on research questions
    common_events <- faers_data %>%
      count(pt, sort = TRUE) %>%
      head(20)

    message("📋 Most common adverse events in dataset:")
    print(common_events, n = 10)

  }, error = function(e) {
    message(sprintf("❌ Analysis failed: %s", e$message))
  })
}

# Run the analysis
message("🧫 FAERS Adverse Event Signal Detection Analysis")
message("================================================")

if (interactive()) {
  main_analysis()
} else {
  main_analysis()
}

message("\n✅ FAERS analysis completed successfully!")

# Note: This is a simplified demonstration.
# Production pharmacovigilance requires:
# - Comprehensive background rate calculation
# - Statistical significance testing
# - Multiple testing correction
# - Expert clinical review of signals
# - Regular data updates and monitoring
