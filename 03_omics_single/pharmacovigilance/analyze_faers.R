#!/usr/bin/env Rscript
"
FAERS Signal Detection Analysis
Implement Reporting Odds Ratio (ROR) and Proportional Reporting Ratio (PRR)
"

# Setup
library(dplyr)
library(readr)
library(epitools)
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

# Configure output directory
dir.create("../results/pharmacovigilance", showWarnings = FALSE)

# Function to load and merge cleaned FAERS data
load_faers_data <- function() {
  drug_file <- "clean/faers_drug.csv"
  reac_file <- "clean/faers_reac.csv"

  if (!file.exists(drug_file)) {
    stop("❌ FAERS drug data not found. Please run clean_faers.R first.")
  }

  # Load drug data
  drug <- read_csv(drug_file, show_col_types = FALSE)
  message(sprintf("📊 Loaded %d drug exposure records", nrow(drug)))

  # Load reaction data if available
  if (file.exists(reac_file)) {
    reac <- read_csv(reac_file, show_col_types = FALSE)
    message(sprintf("📊 Loaded %d adverse reaction records", nrow(reac)))

    # Join drug and reaction data
    faers_data <- inner_join(drug, reac, by = "primaryid")
    message(sprintf("📊 Combined dataset: %d records", nrow(faers_data)))

    return(faers_data)
  } else {
    message("⚠️  Reaction data not found - analysis will focus on drug data only")
    return(drug)
  }
}

# Implement Reporting Odds Ratio (ROR) signal detection
calculate_ror <- function(faers_data, target_drug, target_event, min_reports = 3) {
  "
  Calculate Reporting Odds Ratio (ROR) for drug-adverse event combinations

  Args:
      faers_data: Combined FAERS drug and reaction data
      target_drug: Drug name to analyze
      target_event: Adverse event term to analyze
      min_reports: Minimum number of reports for signal consideration

  Returns:
      DataFrame with ROR statistics
  "

  # Filter for specific drug-event combination
  # This is a simplified example - full ROR requires comparison to entire database
  filtered_data <- faers_data

  if (!is.null(target_drug)) {
    target_drug <- toupper(str_trim(target_drug))
    filtered_data <- filtered_data %>%
      filter(str_detect(drugname_clean, regex(target_drug, ignore_case = TRUE)))
  }

  if (!is.null(target_event)) {
    target_event <- toupper(str_trim(target_event))
    if ("pt" %in% colnames(filtered_data)) {
      filtered_data <- filtered_data %>%
        filter(str_detect(pt, regex(target_event, ignore_case = TRUE)))
    }
  }

  if (nrow(filtered_data) == 0) {
    message("⚠️  No data found matching criteria")
    return(NULL)
  }

  # Group by drug-event combinations
  drug_event_counts <- filtered_data %>%
    group_by(drugname_clean, pt) %>%
    summarise(count = n(), .groups = 'drop') %>%
    arrange(desc(count)) %>%
    filter(count >= min_reports)

  if (nrow(drug_event_counts) == 0) {
    message("⚠️  No drug-event combinations meet minimum report threshold")
    return(NULL)
  }

  # Calculate simplified ROR (normally would compare against background rates)
  drug_event_counts <- drug_event_counts %>%
    mutate(
      # Simplified calculations (would be more sophisticated in production)
      ror = count / (mean(count) + 0.1),  # Avoid division by zero
      ror_lower = ror * 0.8,  # Simplified confidence interval
      ror_upper = ror * 1.2,

      # Flag potential signals (ROR > 2 is commonly used threshold)
      signal_strength = case_when(
        ror >= 10 ~ "Very Strong",
        ror >= 5 ~ "Strong",
        ror >= 2 ~ "Moderate",
        TRUE ~ "Weak"
      )
    ) %>%
    arrange(desc(ror))

  message(sprintf("📊 Calculated ROR for %d drug-event combinations", nrow(drug_event_counts)))
  message("🚨 Potential signals identified:")

  signals <- drug_event_counts %>% filter(signal_strength != "Weak")
  if (nrow(signals) > 0) {
    print(signals %>% head(5), n = 5)
  }

  return(drug_event_counts)
}

# Implement Proportional Reporting Ratio (PRR) signal detection
calculate_prr <- function(faers_data, target_drug = NULL, target_event = NULL, min_reports = 3) {
  "
  Calculate Proportional Reporting Ratio (PRR) for drug safety signals

  Args:
      faers_data: Combined FAERS drug and reaction data
      target_drug: Specific drug to analyze (optional)
      target_event: Specific adverse event to analyze (optional)
      min_reports: Minimum reports threshold

  Returns:
      DataFrame with PRR statistics
  "

  # Prepare contingency table data
  analysis_data <- faers_data

  # Count total reports by drug and event
  drug_totals <- analysis_data %>%
    group_by(drugname_clean) %>%
    summarise(drug_reports = n(), .groups = 'drop') %>%
    filter(drug_reports >= min_reports)

  if ("pt" %in% colnames(analysis_data)) {
    event_totals <- analysis_data %>%
      group_by(pt) %>%
      summarise(event_reports = n(), .groups = 'drop') %>%
      filter(event_reports >= min_reports)

    # Calculate drug-event combinations
    drug_event_matrix <- analysis_data %>%
      group_by(drugname_clean, pt) %>%
      summarise(reports = n(), .groups = 'drop') %>%
      filter(reports >= min_reports)

    if (nrow(drug_event_matrix) == 0) {
      message("⚠️  No drug-event combinations meet minimum report threshold")
      return(NULL)
    }

    # Calculate PRR for each combination
    prr_results <- drug_event_matrix %>%
      left_join(drug_totals, by = "drugname_clean") %>%
      left_join(event_totals, by = "pt") %>%
      mutate(
        # PRR calculation: (a/(a+b)) / (c/(c+d))
        total_reports = sum(reports),
        expected = (drug_reports * event_reports) / total_reports,
        prr = reports / expected,
        prr_lower = prr * 0.9,  # Simplified CI calculation
        prr_upper = prr * 1.1,

        # Signal detection thresholds (typically PRR >= 2)
        signal_strength = case_when(
          prr >= 10 ~ "Very Strong",
          prr >= 5 ~ "Strong",
          prr >= 2 ~ "Moderate",
          TRUE ~ "Weak"
        )
      ) %>%
      arrange(desc(prr))

    message(sprintf("📊 Calculated PRR for %d drug-event combinations", nrow(prr_results)))
    message("🚨 Significant signals (PRR ≥ 2):")

    signals <- prr_results %>% filter(prr >= 2)
    if (nrow(signals) > 0) {
      print(signals %>% head(5), n = 5)
    }

    return(prr_results)
  } else {
    message("⚠️  No adverse event data available for PRR calculation")
    return(NULL)
  }
}

# Main analysis workflow
main_analysis <- function() {
  tryCatch({
    # Load cleaned FAERS data
    faers_data <- load_faers_data()

    # Example 1: ROR analysis for aspirin
    message("\n🩺 Example: ROR analysis for aspirin-related adverse events")
    ror_results <- calculate_ror(faers_data, target_drug = "ASPIRIN", min_reports = 5)

    if (!is.null(ror_results)) {
      write_csv(ror_results, "../results/pharmacovigilance/ror_aspirin_signals.csv")
      message("💾 ROR results saved to '../results/pharmacovigilance/ror_aspirin_signals.csv'")
    }

    # Example 2: PRR analysis
    message("\n📊 Example: PRR analysis for safety signal detection")
    prr_results <- calculate_prr(faers_data, min_reports = 5)

    if (!is.null(prr_results)) {
      write_csv(prr_results, "../results/pharmacovigilance/prr_signals.csv")
      message("💾 PRR results saved to '../results/pharmacovigilance/prr_signals.csv'")
    }

    # Example 3: Broad signal detection across all data
    message("\n🔍 Complete signal detection analysis")

    # For production use, you would:
    # 1. Calculate background rates from large reference database
    # 2. Apply statistical corrections for multiple testing
    # 3. Implement proper confidence intervals
    # 4. Filter by clinical relevance and experimental validation

    # Calculate top signals by report frequency
    if ("pt" %in% colnames(faers_data)) {
      top_signals <- faers_data %>%
        group_by(drugname_clean, pt) %>%
        summarise(
          report_count = n(),
          distinct_cases = n_distinct(primaryid),
          .groups = 'drop'
        ) %>%
        arrange(desc(report_count)) %>%
        head(20)

      write_csv(top_signals, "../results/pharmacovigilance/top_signals.csv")
      message("💾 Top signals saved to '../results/pharmacovigilance/top_signals.csv'")
    }

    message("\n✅ FAERS signal detection analysis completed successfully!")

  }, error = function(e) {
    message(sprintf("❌ Analysis failed: %s", e$message))
  })
}

# Run the analysis
message("🩺 FAERS Adverse Event Signal Detection")
message("=====================================")

if (interactive()) {
  main_analysis()
} else {
  main_analysis()
}

message("\n📋 Analysis Summary:")
message("   - ROR (Reporting Odds Ratio): Measures disproportionality")
message("   - PRR (Proportional Reporting Ratio): Safety signal strength")
message("   - ROR/PRR ≥ 2: Generally considered potential signals")
message("   - Higher values indicate stronger safety signals")
message("\n⚠️  Note: Production pharmacovigilance requires:")
message("      - Large background reference database")
message("      - Statistical significance testing")
message("      - Clinical expert review")
message("      - Regulatory validation")
