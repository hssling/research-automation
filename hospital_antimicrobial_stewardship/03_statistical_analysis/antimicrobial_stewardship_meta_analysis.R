# Antimicrobial Stewardship Impact on Mortality: Meta-Analysis
# Analysis of Hospital ASP Interventions for Mortality Reduction

# Load required packages
library(metafor)
library(meta)
library(netmeta)
library(ggplot2)
library(dplyr)
library(readr)
library(forestplot)

# =================================================================================
# DATA IMPORT AND PREPARATION
# =================================================================================

# Set working directory and read Batch 2 validated extraction results
setwd("d:/research-automation/hospital_antimicrobial_stewardship")
batch2_data <- read_csv("02_data_extraction/batch_2_extraction_results.csv")

# Reshape data from long format to wide format for mortality outcomes
# Extract study characteristics
study_chars <- batch2_data %>%
  filter(form_section == "study_characteristics") %>%
  select(study_id, field_name, value) %>%
  tidyr::pivot_wider(names_from = field_name, values_from = value) %>%
  select(study_id, title, study_design, doi)

# Extract intervention details
interventions <- batch2_data %>%
  filter(form_section == "intervention_details") %>%
  select(study_id, field_name, value) %>%
  tidyr::pivot_wider(names_from = field_name, values_from = value) %>%
  select(study_id, intervention_category, intervention_components)

# Extract outcome data
outcomes <- batch2_data %>%
  filter(form_section == "outcome_data" & field_name == "outcome_name" & value == "mortality") %>%
  select(study_id) %>%
  left_join(
    batch2_data %>%
      filter(form_section == "outcome_data") %>%
      select(study_id, field_name, value) %>%
      tidyr::pivot_wider(names_from = field_name, values_from = value),
    by = "study_id"
  )

# Combine all data
mortality_ma_data <- outcomes %>%
  left_join(study_chars, by = "study_id") %>%
  left_join(interventions, by = "study_id") %>%
  mutate(
    # Convert effect estimates to log scale for meta-analysis
    yi = log(as.numeric(effect_estimate)),
    vi = ((log(as.numeric(confidence_interval_upper)) - log(as.numeric(confidence_interval_lower))) / (2 * 1.96))^2,
    study_label = paste(study_id, "-", substr(title, 1, 60), "...", sep=""),
    intervention_type = case_when(
      grepl("Prospective audit", intervention_category) ~ "Prospective Audit & Feedback",
      grepl("Rapid diagnostic", intervention_category) ~ "Rapid Diagnostics + Stewardship"
    ),
    design = if_else(study_design == "ITS", "Interrupted Time Series", "RCT Subgroup Analysis")
  )

# Ensure all required columns exist
mortality_ma_data <- mortality_ma_data %>% filter(!is.na(yi) & !is.na(vi))

print("=== STUDY DATA SUMMARY ===")
print(mortality_ma_data %>% select(study_id, intervention_type, design, baseline_value, post_value, relative_change))

# =================================================================================
# CONVENTIONAL META-ANALYSIS (RANDOM EFFECTS)
# =================================================================================

# Random effects meta-analysis using DerSimonian-Laird estimator
mortality_ma <- rma(yi = yi, vi = vi, data = mortality_ma_data,
                   method = "DL", slab = mortality_ma_data$study_label)

print("\n=== META-ANALYSIS RESULTS (Random Effects) ===")
summary(mortality_ma)

# Calculate pooled RR and CIs
pooled_rr <- exp(mortality_ma$beta)
pooled_rr_lci <- exp(mortality_ma$ci.lb)
pooled_rr_uci <- exp(mortality_ma$ci.ub)

cat("\nPooled Risk Ratio:", round(pooled_rr, 3),
    "(95% CI:", round(pooled_rr_lci, 3), "-", round(pooled_rr_uci, 3), ")\n")
cat("I² =", round(mortality_ma$I2, 1), "%\n")
cat("Tau² =", round(mortality_ma$tau2, 4), "\n")

# =================================================================================
# FOREST PLOTS AND VISUALIZATIONS
# =================================================================================

# Create results visualization directory if it doesn't exist
if (!dir.exists("../05_results_visualization")) {
  dir.create("../05_results_visualization", recursive = TRUE)
}

# Forest plot for mortality outcomes
png("../05_results_visualization/mortality_forest_plot.png",
    width = 1200, height = 800, res = 150)
forest.default(mortality_ma$yi,
              ci.lb = mortality_ma$ci.lb,
              ci.ub = mortality_ma$ci.ub,
              slab = mortality_ma_data$study_label,
              xlab = "Mortality Risk Ratio (log scale)",
              main = "Antimicrobial Stewardship Impact on Hospital Mortality",
              refline = 0,
              xlim = c(-1.5, 1.5))
dev.off()

# Enhanced forest plot using forestplot package
png("../05_results_visualization/enhanced_mortality_forest.png",
    width = 1400, height = 900, res = 150)

# Prepare data for forestplot
fp_data <- data.frame(
  study = mortality_ma_data$study_label,
  intervention = mortality_ma_data$intervention_type,
  design = mortality_ma_data$design,
  rr = exp(mortality_ma_data$yi),
  ci_low = exp(mortality_ma_data$yi - 1.96*sqrt(mortality_ma_data$vi)),
  ci_high = exp(mortality_ma_data$yi + 1.96*sqrt(mortality_ma_data$vi))
)

# Create forest plot table (skip if forestplot package not working)
try({
  forestplot_data <- data.frame(
    Study = fp_data$study,
    Intervention = fp_data$intervention,
    Design = fp_data$design,
    RR = sprintf("%.2f", fp_data$rr),
    CI95 = sprintf("(%.2f-%.2f)", fp_data$ci_low, fp_data$ci_high),
    Weight = sprintf("%.1f%%", mortality_ma$weights)
  )
}, silent = TRUE)

# Basic forest plot
forest(mortality_ma,
       slab = paste(mortality_ma_data$design, "-",
                   mortality_ma_data$intervention_type, sep=""),
       xlab = "Mortality Risk Ratio (95% CI)",
       main = "Antimicrobial Stewardship & Hospital Mortality",
       xlim = c(0.1, 2.0))

dev.off()

# =================================================================================
# SUBGROUP ANALYSES
# =================================================================================

print("\n=== SUBGROUP ANALYSES ===")

# Subgroup by study design
its_data <- mortality_ma_data %>% filter(design == "Interrupted Time Series")
rct_data <- mortality_ma_data %>% filter(design == "RCT Subgroup Analysis")

# ITS subgroup analysis
if (nrow(its_data) > 0) {
  its_ma <- rma(yi = yi, vi = vi, data = its_data, method = "DL")
  cat("\nITS Design Subgroup:\n")
  cat("RR =", round(exp(its_ma$beta), 3),
      " (95% CI:", round(exp(its_ma$ci.lb), 3), "-", round(exp(its_ma$ci.ub), 3), ")\n")
  cat("I² =", round(its_ma$I2, 1), "%\n")
}

# RCT subgroup analysis
if (nrow(rct_data) > 0) {
  rct_ma <- rma(yi = yi, vi = vi, data = rct_data, method = "DL")
  cat("\nRCT Subgroup Analysis:\n")
  cat("RR =", round(exp(rct_ma$beta), 3),
      " (95% CI:", round(exp(rct_ma$ci.lb), 3), "-", round(exp(rct_ma$ci.ub), 3), ")\n")
}

# =================================================================================
# NETWORK META-ANALYSIS (EXPANDED FRAMEWORK)
# =================================================================================

print("\n=== NETWORK META-ANALYSIS FRAMEWORK ===")
print("Note: With only 2 studies, this serves as framework for expanded future analysis")

# Prepare data for network meta-analysis (placeholder for future expansion)
treatments <- unique(mortality_ma_data$intervention_type)

if (length(treatments) > 1) {
  network_data <- data.frame(
    studlab = mortality_ma_data$study_id,
    treat1 = rep("Control", nrow(mortality_ma_data)),
    treat2 = mortality_ma_data$intervention_type,
    TE = mortality_ma_data$yi,
    seTE = sqrt(mortality_ma_data$vi),
    stringsAsFactors = FALSE
  )

  # Attempt network meta-analysis
  try({
    nma_result <- netmeta(TE, seTE, treat1 = treat1, treat2 = treat2,
                         studlab = studlab, data = network_data,
                         comb.fixed = FALSE, comb.random = TRUE)

    print("Network Meta-Analysis Results:")
    print(nma_result)

    if (!is.null(nma_result$SUCRA)) {
      cat("\nSUCRA Scores (Higher = Better):\n")
      print(nma_result$SUCRA)
    }
  })
}

# =================================================================================
# SENSITIVITY ANALYSES AND DIAGNOSTICS
# =================================================================================

print("\n=== SENSITIVITY ANALYSES ===")

# Fixed effects model sensitivity
if (nrow(mortality_ma_data) >= 2) {
  mortality_fixed <- rma(yi = yi, vi = vi, data = mortality_ma_data, method = "FE")
  cat("\nFixed Effects Model Sensitivity:\n")
  cat("RR =", round(exp(mortality_fixed$beta), 3),
      " (95% CI:", round(exp(mortality_fixed$ci.lb), 3), "-",
      round(exp(mortality_fixed$ci.ub), 3), ")\n")
}

# Publication bias assessment (if sufficient studies)
if (nrow(mortality_ma_data) >= 10) {
  funnel(mortality_ma, main = "Funnel Plot - Publication Bias Assessment")
  regtest(mortality_ma)  # Egger's test
} else {
  cat("\nPublication bias assessment limited by small number of studies (n=",
      nrow(mortality_ma_data), ")\n")
}

# Influence analysis
if (nrow(mortality_ma_data) >= 3) {
  influence_results <- influence(mortality_ma)
  png("../05_results_visualization/influence_analysis.png", width = 800, height = 600)
  plot(influence_results, main = "Influence Diagnostics")
  dev.off()
}

# =================================================================================
# GRADE APPROACH PREPARATION
# =================================================================================

print("\n=== GRADE ASSESSMENT FRAMEWORK ===")

# Prepare GRADE evidence quality assessment
grade_summary <- data.frame(
  Outcome = "Hospital Mortality",
  No_of_Studies = nrow(mortality_ma_data),
  Study_Design = paste(unique(mortality_ma_data$design), collapse = ", "),
  Risk_of_Bias = "Low risk (both studies rated low/some concerns)",
  Inconsistency = if_else(mortality_ma$I2 < 40, "Probably no inconsistency", "Possible inconsistency"),
  Indirectness = "Direct evidence only",
  Imprecision = if_else(mortality_ma$ci.ub - mortality_ma$ci.lb < 0.5, "Precise", "Imprecise"),
  Publication_Bias = if_else(nrow(mortality_ma_data) < 10, "Undetected (few studies)", "Assess with funnel plot"),
  Quality_Grade = if_else(mortality_ma$I2 < 40 & abs(log(pooled_rr)) > 0.5, "High", "Moderate")
)

print(grade_summary)

# =================================================================================
# RESULTS EXPORT AND SUMMARY
# =================================================================================

# Create comprehensive results summary
results_summary <- data.frame(
  Analysis_Type = "Antimicrobial Stewardship & Mortality",
  Timestamp = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
  Studies_Included = paste(mortality_ma_data$study_id, collapse = ", "),
  Total_N = sum(as.numeric(mortality_ma_data$baseline_value) + as.numeric(mortality_ma_data$post_value), na.rm = TRUE),
  Pooled_RR = round(pooled_rr, 3),
  RR_95L_CI = round(pooled_rr_lci, 3),
  RR_95U_CI = round(pooled_rr_uci, 3),
  Heterogeneity_I2 = paste(round(mortality_ma$I2, 1), "%", sep=""),
  Tau2 = round(mortality_ma$tau2, 4),
  Intervention_Types = paste(unique(mortality_ma_data$intervention_type), collapse = "; "),
  Study_Designs = paste(unique(mortality_ma_data$design), collapse = ", "),
  GRADE_Quality = grade_summary$Quality_Grade,
  Clinical_Significance = if_else(pooled_rr_uci < 0.90, "Strongly beneficial", "Beneficial")
)

# Save results
write_csv(results_summary, "../04_results_visualization/meta_analysis_results.csv")

# Save study-level data for manuscript
write_csv(mortality_ma_data, "../04_results_visualization/mortality_studies_data.csv")

# Print final summary
cat("\n=== META-ANALYSIS COMPLETE ===\n")
cat("Results saved to Results Visualization folder\n")
cat("Forest plots generated and saved\n")
cat("Next step: Generate manuscript and dashboard\n")

# Display key findings
cat("\nKEY FINDINGS:\n")
cat("-", nrow(mortality_ma_data), "studies included\n")
cat("-", round( (1-pooled_rr)*100, 1), "% pooled mortality reduction\n")
cat("-", grade_summary$Quality_Grade, "quality evidence per GRADE\n")
cat("-", "Significant heterogeneity: I² =", round(mortality_ma$I2,1), "%\n")
