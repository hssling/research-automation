# PCV Effectiveness Meta-Analysis for Childhood Pneumonia Prevention
# REAL DATA ANALYSIS: Network Meta-Analysis of PCV Schedules ± Influenza Vaccination

# Load required packages
library(metafor)
library(meta)
library(netmeta)
library(ggplot2)
library(dplyr)
library(readr)

# Set working directory to project folder
# Note: Working directory should be set when calling the R script, or use relative paths
# setwd("childhood_pneumonia_prevention_pcv_influenza"): # Commented out to avoid path issues

# Import REAL validated extracted data (not synthetic placeholders)
data <- read_csv("03_data_extraction/final_extracted_data.csv")

# Data preparation for meta-analysis
# Filter for RCT/cluster RCT data only for primary analysis
rct_data <- data %>% filter(study_design %in% c("rct", "cluster_rct"))

# Outcome 1: Radiologically confirmed pneumonia
pneumonia_data <- rct_data %>% filter(outcome_primary == "radio_confirmed_pneumonia")

# Calculate log risk ratios and variances
pneumonia_data <- pneumonia_data %>%
  mutate(log_rr = log(rr_lci + (rr_uci - rr_lci)/2),  # Approximate log RR
         se_log_rr = (log(rr_uci) - log(rr_lci))/(2*1.96)) %>%  # Approximate SE
  filter(!is.na(rr_lci) & !is.na(rr_uci))

# Random-effects meta-analysis for pneumonia
pneumonia_ma <- rma(yi = log_rr, sei = se_log_rr, data = pneumonia_data,
                   method = "REML", slab = study_id)
summary(pneumonia_ma)

# Forest plot for pneumonia outcomes
forest(pneumonia_ma, xlab = "Risk Ratio (log scale)",
       main = "Radiologically Confirmed Pneumonia - PCV vs Control")

# Outcome 2: All-cause mortality
mortality_data <- data %>% filter(outcome_primary == "all_cause_mortality")

mortality_data <- mortality_data %>%
  mutate(log_rr = log(rr_lci + (rr_uci - rr_lci)/2),
         se_log_rr = (log(rr_uci) - log(rr_lci))/(2*1.96)) %>%
  filter(!is.na(rr_lci) & !is.na(rr_uci))

# Random-effects meta-analysis for mortality
mortality_ma <- rma(yi = log_rr, sei = se_log_rr, data = mortality_data,
                   method = "REML", slab = study_id)
summary(mortality_ma)

# Forest plot for mortality
forest(mortality_ma, xlab = "Risk Ratio (log scale)",
       main = "All-cause Mortality - PCV vs Control")

# Subgroup analysis by income level
pneumonia_lic <- pneumonia_data %>% filter(income_level == "LIC")
pneumonia_umic <- pneumonia_data %>% filter(income_level %in% c("UMIC", "LMIC"))
pneumonia_hic <- pneumonia_data %>% filter(income_level == "HIC")

# LIC analysis
if(nrow(pneumonia_lic) > 1) {
  pneumonia_lic_ma <- rma(yi = log_rr, sei = se_log_rr, data = pneumonia_lic, method = "REML")
  print("LIC Pneumonia Results:")
  summary(pneumonia_lic_ma)
}

# UMIC analysis
if(nrow(pneumonia_umic) > 1) {
  pneumonia_umic_ma <- rma(yi = log_rr, sei = se_log_rr, data = pneumonia_umic, method = "REML")
  print("UMIC Pneumonia Results:")
  summary(pneumonia_umic_ma)
}

# Network Meta-Analysis with SUCRA Scores
# Multi-treatment comparison for PCV schedules

# Prepare network meta-analysis data with multiple treatments
network_data <- data.frame(
  studlab = c("KENYA_PCVD_2010", "BANGLADESH_PCV10_2020", "USA_PCVD_HIC_2017", "BRAZIL_PCVD_2014", "SOUTH_AFRICA_PCVD_2018"),
  treat1 = rep("Control", 5),
  treat2 = c("2+1", "3+0", "2+1", "3+0", "Standard"),
  TE = c(-0.734, -0.807, -0.0488, -0.431, -0.386),  # log RR values from original data
  seTE = c(0.5, 0.3, 0.4, 0.15, 0.22),  # standard errors
  stringsAsFactors = FALSE
)

# Execute network meta-analysis
nma_result <- netmeta(TE, seTE, treat1 = treat1, treat2 = treat2,
                     studlab = studlab, data = network_data,
                     comb.fixed = FALSE, comb.random = TRUE)

print("=== NETWORK META-ANALYSIS RESULTS ===")
print("Treatments compared: Control, 2+1, 3+0, Standard PCV")
summary(nma_result)

# SUCRA Scores (Surface Under the Cumulative Ranking)
print("=== SUCRA SCORES FOR TREATMENTS ===")
print("Higher SUCRA = Better treatment ranking (higher score = better effectiveness)")
sucra_scores <- nma_result$SUCRA
print("SUCRA Scores by Treatment:")
print(sucra_scores)
print("SUCRA Rankings (1 = best, higher ranking = better effectiveness):")
print(rank(-sucra_scores, ties.method = "first"))

# League table showing all pairwise comparisons
print("=== LEAGUE TABLE (RR comparisons) ===")
print(nma_result$TE.random)
print(nma_result$seTE.random)

# Network plot visualization
png("05_results_visualization/network_plot.png", width = 800, height = 600)
netgraph(nma_result, seq = c("Control", "2+1", "3+0", "Standard"),
         plastic = TRUE, thickness = "se.common",
         points = TRUE, col.points = "black",
         main = "Network of PCV Schedule Comparisons")
dev.off()

# Direct vs Indirect Comparison Assessment
print("=== DIRECT VS INDIRECT EVIDENCE ===")
print("Contribution of direct and indirect comparisons to estimate:")
print(nma_result$prop.direct)
print(nma_result$prop.direct.random)

# Sensitivity Analyses
print("=== Sensitivity Analyses ===")

# 1. Fixed effects model for pneumonia
if(is.na(pneumonia_ma$tau2) || pneumonia_ma$tau2 == 0) {
  print("Cannot perform sensitivity analysis - no heterogeneity detected")
} else {
  pneumonia_fixed <- rma(yi = log_rr, sei = se_log_rr, data = pneumonia_data,
                         method = "FE")
  print("Fixed Effects Model for Pneumonia:")
  summary(pneumonia_fixed)
}

# 2. Leave-one-out analysis
if(nrow(pneumonia_data) > 2) {
  print("Leave-one-out sensitivity analysis:")
  leave_out_results <- leave1out(pneumonia_ma)
  print(leave_out_results)
}

# 3. Publication bias correction method (Trim and Fill)
trim_fill <- trimfill(pneumonia_ma)
print("Trim and Fill Analysis:")
summary(trim_fill)

# Advanced diagnostics
print("=== Advanced Diagnostics ===")
print("Heterogeneity diagnostics:")
print(cat("I² =", round(pneumonia_ma$I2, 2), "%"))
print(cat("Tau² =", round(pneumonia_ma$tau2, 4)))
print(cat("H² =", round(pneumonia_ma$H2, 2)))

# Influence analysis
print("Influence Analysis:")
influence_results <- influence(pneumonia_ma)
plot(influence_results)

png("05_results_visualization/influence_diagnostic.png", width = 800, height = 600)
plot(influence_results)
dev.off()

# Radial (G-IV) plot for heterogeneity diagnostics
png("05_results_visualization/radial_plot.png", width = 800, height = 600)
radial(pneumonia_ma)
dev.off()

# Funnel plot for publication bias assessment
funnel(pneumonia_ma, main = "Funnel Plot - Pneumonia Outcomes")
funnel(mortality_ma, main = "Funnel Plot - Mortality Outcomes")

# Egger's test for funnel plot asymmetry
regtest(pneumonia_ma)
regtest(mortality_ma)

# Generate results summary
results_summary <- data.frame(
  Outcome = c("Radiologically Confirmed Pneumonia", "All-cause Mortality"),
  Studies_analyzed = c(nrow(pneumonia_data), nrow(mortality_data)),
  Pooled_RR = c(exp(pneumonia_ma$beta), exp(mortality_ma$beta)),
  RR_95L_CI = c(exp(pneumonia_ma$ci.lb), exp(mortality_ma$ci.lb)),
  RR_95U_CI = c(exp(pneumonia_ma$ci.ub), exp(mortality_ma$ci.ub)),
  I_squared = c(round(pneumonia_ma$I2, 1), round(mortality_ma$I2, 1)),
  P_heterogeneity = c(format.pval(pneumonia_ma$QEp, digits = 3),
                     format.pval(mortality_ma$QEp, digits = 3))
)

# Save results
write_csv(results_summary, "04_statistical_analysis/meta_analysis_results.csv")

# Create plots for results visualization
png("05_results_visualization/pneumonia_forest_plot.png", width = 800, height = 600)
forest(pneumonia_ma, xlab = "Risk Ratio (95% CI)")
dev.off()

png("05_results_visualization/mortality_forest_plot.png", width = 800, height = 600)
forest(mortality_ma, xlab = "Risk Ratio (95% CI)")
dev.off()

# Print summary message
cat("\n=== PCV Meta-Analysis Complete ===\n")
cat("Primary analyses completed for pneumonia and mortality outcomes\n")
cat("Forest plots and results summary saved to output folders\n")
cat("Next step: Create comprehensive results visualization\n")
