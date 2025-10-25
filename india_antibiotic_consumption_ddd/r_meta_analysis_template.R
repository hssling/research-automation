# =======================================================================================
# Antibiotic Consumption in India: DDD-Based Meta-Analysis & Network Meta-Analysis (NMA)
# =======================================================================================
# Template for R-based meta-analysis of antibiotic consumption data (DDD/DID metrics)
# Based on WHO ATC/DDD methodology & AWaRe classification

# Required packages ----
install.packages(c("meta", "metafor", "netmeta", "dmetar", "openxlsx", "ggplot2", "ggpubr"))
library(meta)
library(metafor)
library(netmeta)
library(dmetar)
library(openxlsx)
library(ggplot2)
library(ggpubr)

# Set working directory ----
setwd("D:/research-automation/india_antibiotic_consumption_ddd")

# ==============================================================================
# DATA IMPORT & PREPARATION
# ==============================================================================

# Import dummy/example data (replace with your actual extracted data)
# Expected columns: study_id, year, region, setting, population, total_ddd, days_observed, did_value, se, awa_cat, antibiotic_class
data <- read.xlsx("data/antibiotic_ddd_study_data.xlsx", sheet = 1)  # Replace with your data file

# Data cleaning ----
data$region <- factor(data$region, levels = c("North India", "South India", "East India", "West India", "Northeast India"))
data$setting <- factor(data$setting, levels = c("Public Hospital", "Private Hospital", "Pharmacy", "Community"))
data$awa_cat <- factor(data$awa_cat, levels = c("Access", "Watch", "Reserve"))
data$antibiotic_class <- factor(data$antibiotic_class)  # e.g., "β-lactams", "Fluoroquinolones", etc.

# Visualization of data distribution ----
ggplot(data, aes(x = did_value, fill = region)) +
  geom_histogram(alpha = 0.7, position = "identity") +
  theme_minimal() +
  labs(title = "Distribution of DID Values by Region", x = "DID (DDD/1,000 inhabitants/day)", y = "Frequency")

# AWaRe distribution pie chart ----
awa_summary <- table(data$awa_cat)
pie(awa_summary, main = "Distribution of Antibiotic Consumption by AWaRe Category",
    labels = paste(names(awa_summary), "\n", awa_summary, sep = ""))

# ==============================================================================
# META-ANALYSIS: Pooled DID Estimates
# ==============================================================================

# Overall random-effects meta-analysis ----
ma_overall <- metacont(n.e = population,  # Number of inhabitants
                       mean.e = did_value,  # DID from study
                       sd.e = se,  # Standard error
                       studlab = study_id,
                       data = data,
                       sm = "MD",  # Mean difference (for pooled DID)
                       method.tau = "REML",  # Restricted maximum likelihood
                       hakn = TRUE)  # Knapp-Hartung adjustment

# Display results ----
summary(ma_overall)
forest(ma_overall, main = "Pooled DID: Antibiotic Consumption in India")

# Heterogeneity assessment ----
print(paste("I² =", round(ma_overall$I2, 2), "%"))
print(paste("τ² =", round(ma_overall$tau2, 4)))
print("Cochran Q p-value =", ma_overall$Q.pval)

# Publication bias assessment ----
funnel(ma_overall, main = "Funnel Plot for DID Estimates")
egger_test <- metabias(ma_overall, method.bias = "Egger")
print(egger_test)

# ==============================================================================
# SUBGROUP ANALYSES
# ==============================================================================

# By region ----
ma_region <- metacont(n.e = population,
                      mean.e = did_value,
                      sd.e = se,
                      studlab = study_id,
                      byvar = region,
                      data = data,
                      sm = "MD",
                      method.tau = "REML",
                      hakn = TRUE)

forest(ma_region, main = "DID by Region")

# By setting (Public vs Private) ----
ma_setting <- metacont(n.e = population,
                       mean.e = did_value,
                       sd.e = se,
                       studlab = study_id,
                       byvar = setting,
                       data = data,
                       sm = "MD",
                       method.tau = "REML",
                       hakn = TRUE)

forest(ma_setting, main = "DID by Healthcare Setting")

# By AWaRe category ----
ma_aware <- metacont(n.e = population,
                     mean.e = did_value,
                     sd.e = se,
                     studlab = study_id,
                     byvar = awa_cat,
                     data = data,
                     sm = "MD",
                     method.tau = "REML",
                     hakn = TRUE)

forest(ma_aware, main = "DID by AWaRe Category")

# ==============================================================================
# META-REGRESSION
# ==============================================================================

# Meta-regression for temporal trends ----
mr_year <- metareg(ma_overall, ~ year, method.tau = "REML")
summary(mr_year)
bubble(mr_year, main = "Bubble Plot: DID vs Publication Year")

# Meta-regression for policy phases (e.g., pre/post Schedule H1 policy) ----
# Create policy variable: 0 = pre-policy, 1 = post-policy
data$policy_phase <- ifelse(data$year >= 2014, 1, 0)  # Example: Schedule H1 in 2013-14
mr_policy <- metareg(ma_overall, ~ policy_phase, method.tau = "REML")
summary(mr_policy)

# Multi-predictor meta-regression ----
mr_multi <- metareg(ma_overall, ~ year + region + setting, method.tau = "REML")
summary(mr_multi)

# ==============================================================================
# NETWORK META-ANALYSIS (NMA) FOR ANTIBIOTIC CLASSES
# ==============================================================================

# Prepare NMA data (if multiple antibiotic classes compared in same studies) ----
# Assuming pairwise comparisons between antibiotic classes within studies
nma_data <- data.frame(
  study = data$study_id,
  treatment = data$antibiotic_class,
  mean = data$did_value,
  se = data$se
)

# Run NMA ----
nma_result <- netmeta(TE = nma_result$TE,  # Treatment effects
                      seTE = nma_result$seTE,
                      treat1 = nma_result$treat1,
                      treat2 = nma_result$treat2,
                      studlab = nma_result$studlab,
                      data = nma_result,
                      sm = "MD",
                      method.tau = "REML")

# NMA results ----
summary(nma_result)
netrank(nma_result, small.values = "bad")  # Ranking by consumption (higher DID = more use)

# Surface Under the Cumulative Ranking (SUCRA) values ----
sucra_nma <- netrank(nma_result, rank = "SUCRA")
print(sucra_nma)

# Network plot ----
netgraph(nma_result, plastic = TRUE, thickness = "number.of.studies",
         main = "Network of Antibiotic Classes Compared by DID")

# Forest plot of NMA results ----
forest(nma_result, main = "Network Meta-Analysis: Antibiotic Classes")

# ==============================================================================
# EXPORT RESULTS
# ==============================================================================

# Save forest plot ----
png("output/did_forest_plot.png", width = 800, height = 600)
forest(ma_overall)
dev.off()

# Save subgroup analysis ----
png("output/did_region_subgroup.png", width = 800, height = 600)
forest(ma_region)
dev.off()

# Export summary statistics ----
results_summary <- data.frame(
  Analysis = c("Overall DID", "DID by Region (North)", "DID by Region (South)", "DID by Region (East)",
               "DID by Region (West)", "DID by Region (Northeast)",
               "Public Setting DID", "Private Setting DID", "Community Setting DID"),
  Pooled_DID = c(round(ma_overall$TE.random, 2), round(ma_region$TE.common.w, 2)[1:5],
                 round(ma_setting$TE.common.w, 2)[1:3]),
  SE = c(round(ma_overall$seTE.random, 3), round(ma_region$seTE.common.w, 3)[1:5],
         round(ma_setting$seTE.common.w, 3)[1:3]),
  CI_Lower = c(round(ma_overall$lower.random, 2), round(ma_region$lower.common.w, 2)[1:5],
               round(ma_setting$lower.common.w, 2)[1:3]),
  CI_Upper = c(round(ma_overall$upper.random, 2), round(ma_region$upper.common.w, 2)[1:5],
               round(ma_setting$upper.common.w, 2)[1:3]),
  I2 = c(round(ma_overall$I2 * 100, 1), round(ma_region$I2.w * 100, 1)[1:5],
         round(ma_setting$I2.w * 100, 1)[1:3]),
  p_value = c(round(ma_overall$pval.random, 4), round(ma_region$pval.common.w, 4)[1:5],
              round(ma_setting$pval.common.w, 4)[1:3])
)

write.xlsx(results_summary, "output/meta_analysis_results_summary.xlsx")

# Export AWaRe distribution ----
awa_table <- data.frame(
  Category = names(awa_summary),
  Count = as.numeric(awa_summary),
  Percentage = round(as.numeric(awa_summary) / sum(awa_summary) * 100, 2)
)
write.xlsx(awa_table, "output/aware_distribution.xlsx")

# ==============================================================================
# ADDITIONAL VISUALIZATIONS
# ==============================================================================

# Bubble plot for meta-regression ----
ggbubb <- ggplot(data, aes(x = year, y = did_value, size = population, color = region)) +
  geom_point(alpha = 0.7) +
  scale_size(range = c(1, 10)) +
  theme_minimal() +
  labs(title = "DID Trends Over Time by Region",
       x = "Publication Year", y = "DID (DDD/1,000 inhabitants/day)",
       size = "Population Size", color = "Region")
ggsave("output/did_temporal_trends.png", ggbubb, width = 10, height = 6)

# ==============================================================================
# END OF SCRIPT
# ==============================================================================

# Notes:
# 1. Replace dummy data references with your actual dataset
# 2. Adjust variable names as needed to match your data extraction form
# 3. Ensure SE calculation if not directly available (SE = SD/sqrt(n) or from CI)
# 4. For NMA, ensure data is in contrast format with multiple treatments per study
# 5. Run sensitivity analyses for robustness (e.g., fixed vs random effects)
# 6. Consult statistical expert for complex interactions or missing data imputation
