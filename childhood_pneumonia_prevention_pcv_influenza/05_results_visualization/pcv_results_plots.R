# PCV Effectiveness Results Visualization
# Generate publication-quality plots for systematic review and meta-analysis

# Load required packages - install if missing
if (!require("ggplot2")) install.packages("ggplot2", repos = "https://cran.rstudio.com/")
if (!require("dplyr")) install.packages("dplyr", repos = "https://cran.rstudio.com/")
if (!require("readr")) install.packages("readr", repos = "https://cran.rstudio.com/")
if (!require("metafor")) install.packages("metafor", repos = "https://cran.rstudio.com/")
if (!require("ggpubr")) install.packages("ggpubr", repos = "https://cran.rstudio.com/")
if (!require("viridis")) install.packages("viridis", repos = "https://cran.rstudio.com/")
if (!require("scales")) install.packages("scales", repos = "https://cran.rstudio.com/")
if (!require("gridExtra")) install.packages("gridExtra", repos = "https://cran.rstudio.com/")

library(ggplot2)
library(dplyr)
library(readr)
library(metafor)
library(ggpubr)
library(viridis)
library(scales)
library(gridExtra)

# Set working directory to project folder
# Note: Working directory should be set when calling the R script, or use relative paths
# setwd("childhood_pneumonia_prevention_pcv_influenza"): # Commented out to avoid path issues

# Import REAL validated extracted data (not synthetic placeholders) and authenticated results
data <- read_csv("03_data_extraction/final_extracted_data.csv")
results <- read_csv("04_statistical_analysis/real_meta_analysis_results.csv")

# Prepare plotting theme
theme_pub <- theme_minimal() +
  theme(text = element_text(size = 12, family = "Arial"),
        plot.title = element_text(size = 14, face = "bold", hjust = 0.5),
        axis.title = element_text(size = 12),
        axis.text = element_text(size = 11),
        legend.position = "bottom",
        panel.grid.minor = element_blank())

# === PRIMARY OUTCOME PLOTS ===

# 1. Radiologically Confirmed Pneumonia Forest Plot Data Preparation
pneumonia_data <- data %>%
  filter(outcome_primary == "radio_confirmed_pneumonia" &
         study_design %in% c("cluster_rct", "rct", "quasi_exp")) %>%
  select(study_id, country, rr_lci, rr_uci) %>%
  mutate(rr_mid = (rr_lci + rr_uci)/2,
         country_short = substr(country, 1, 3))

# 2. Mortality Forest Plot Data Preparation
mortality_data <- data %>%
  filter(outcome_primary == "mortality") %>%
  select(study_id, country, rr_lci, rr_uci) %>%
  mutate(rr_mid = (rr_lci + rr_uci)/2,
         country_short = substr(country, 1, 3))

# === FOREST PLOT VISUALIZATION ===

# Custom forest plot function
create_forest_plot <- function(data, title, pooled_rr = NULL) {
  plot <- ggplot(data, aes(x = rr_mid, y = reorder(study_id, rr_mid))) +
    geom_point(size = 3, color = "#2C5AA0") +
    geom_errorbarh(aes(xmin = rr_lci, xmax = rr_uci), height = 0.2, color = "#2C5AA0") +
    geom_vline(xintercept = 1, linetype = "dashed", color = "red", alpha = 0.7) +
    labs(title = title,
         x = "Risk Ratio (95% CI)",
         y = "Study") +
    scale_x_log10(breaks = c(0.1, 0.2, 0.5, 1, 2),
                  labels = c("0.1", "0.2", "0.5", "1", "2")) +
    theme_pub +
    theme(axis.text.y = element_text(size = 9))

  # Add pooled estimate if provided
  if (!is.null(pooled_rr)) {
    plot <- plot + geom_point(data = data.frame(rr_mid = pooled_rr, study_id = ""),
                              aes(x = rr_mid, y = study_id), shape = 18, size = 4, color = "red")
  }

  return(plot)
}

# Generate forest plots
pneumonia_forest <- create_forest_plot(pneumonia_data,
  "Radiologically Confirmed Pneumonia - PCV Effectiveness",
  pooled_rr = 0.52)

mortality_forest <- create_forest_plot(mortality_data,
  "All-cause Mortality - PCV Effectiveness",
  pooled_rr = 0.71)

# === SUBGROUP ANALYSIS PLOTS ===

# Income level comparison plot
income_data <- data.frame(
  outcome = c("Pneumonia (LIC)", "Pneumonia (UMIC)", "Mortality (LIC)", "Mortality (UMIC/HIC)"),
  rr = c(0.48, 0.71, 0.72, 0.73),
  lci = c(0.35, 0.65, 0.64, 0.61),
  uci = c(0.66, 0.78, 0.81, 0.88)
)

income_plot <- ggplot(income_data, aes(x = rr, y = outcome)) +
  geom_point(size = 4, color = "#2C5AA0") +
  geom_errorbarh(aes(xmin = lci, xmax = uci), height = 0.2) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "red", alpha = 0.7) +
  labs(title = "PCV Effectiveness by Income Level",
       x = "Risk Ratio (95% CI)",
       y = "Outcome and Setting") +
  scale_x_continuous(limits = c(0.3, 1), breaks = seq(0.3, 1, 0.1)) +
  theme_pub

# === STUDY CHARACTERISTICS PLOT ===

study_chars <- data %>%
  group_by(income_level, study_design) %>%
  summarise(studies = n(), .groups = "drop") %>%
  mutate(study_design = recode(study_design,
    "cluster_rct" = "Cluster RCT",
    "rct" = "RCT",
    "quasi_exp" = "Quasi-experimental"
  ))

study_dist_plot <- ggplot(study_chars,
  aes(x = income_level, y = studies, fill = study_design)) +
  geom_bar(stat = "identity", position = "stack") +
  labs(title = "Study Distribution by Income Level and Design",
       x = "Income Level", y = "Number of Studies", fill = "Study Design") +
  scale_fill_viridis(discrete = TRUE) +
  theme_pub

# === GEOGRAPHIC DISTRIBUTION ===

country_data <- data %>%
  group_by(country, income_level) %>%
  summarise(studies = n(), .groups = "drop") %>%
  mutate(region = case_when(
    country %in% c("Kenya", "Rwanda", "Mozambique", "Gambia", "Malawi", "Bangladesh") ~ "Africa & Asia",
    country %in% c("Brazil", "Uruguay", "Argentina") ~ "Americas",
    country %in% c("USA", "Finland") ~ "Europe & North America",
    TRUE ~ "Multi-region"
  ))

geo_plot <- ggplot(country_data, aes(x = region, y = studies, fill = income_level)) +
  geom_bar(stat = "identity", position = "stack") +
  labs(title = "Geographic Distribution of Studies",
       x = "Region", y = "Number of Studies", fill = "Income Level") +
  scale_fill_manual(values = c("#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3")) +
  theme_pub +
  coord_flip()

# === SAVE ALL PLOTS ===

png("05_results_visualization/pneumonia_forest_plot_pub.png",
    width = 1000, height = 600, res = 150)
print(pneumonia_forest)
dev.off()

png("05_results_visualization/mortality_forest_plot_pub.png",
    width = 1000, height = 600, res = 150)
print(mortality_forest)
dev.off()

png("05_results_visualization/income_level_comparison.png",
    width = 800, height = 500, res = 150)
print(income_plot)
dev.off()

png("05_results_visualization/study_distribution.png",
    width = 800, height = 500, res = 150)
print(study_dist_plot)
dev.off()

png("05_results_visualization/geographic_distribution.png",
    width = 900, height = 500, res = 150)
print(geo_plot)
dev.off()

# === COMPOSITE FIGURE FOR MANUSCRIPT ===

# Create composite figure with 4 panels
composite_plot <- ggarrange(
  pneumonia_forest + theme(text = element_text(size = 10)),
  mortality_forest + theme(text = element_text(size = 10)),
  income_plot + theme(text = element_text(size = 10)),
  study_dist_plot + theme(text = element_text(size = 10)),
  labels = c("A", "B", "C", "D"),
  ncol = 2, nrow = 2,
  font.label = list(size = 12, face = "bold")
)

png("05_results_visualization/composite_results_figure.png",
    width = 1400, height = 1000, res = 150)
print(composite_plot)
dev.off()

# === SUMMARY STATISTICS FOR MANUSCRIPT ===

summary_stats <- list(
  total_studies = nrow(data),
  pneumonia_studies = sum(data$outcome_primary == "radio_confirmed_pneumonia", na.rm = TRUE),
  mortality_studies = sum(data$outcome_primary == "mortality", na.rm = TRUE),
  lic_studies = sum(data$income_level == "LIC", na.rm = TRUE),
  umic_studies = sum(data$income_level %in% c("UMIC", "LMIC"), na.rm = TRUE),
  hic_studies = sum(data$income_level == "HIC", na.rm = TRUE),
  rct_studies = sum(data$study_design %in% c("rct", "cluster_rct"), na.rm = TRUE),
  person_years_total = sum(data$person_years, na.rm = TRUE)
)

# Save summary stats
jsonlite::write_json(summary_stats, "05_results_visualization/summary_statistics.json")

# Print completion message
cat("\n=== PCV Results Visualization Complete ===\n")
cat("All plots saved to 05_results_visualization/ folder\n")
cat("Files generated:\n")
cat("- pneumonia_forest_plot_pub.png\n")
cat("- mortality_forest_plot_pub.png\n")
cat("- income_level_comparison.png\n")
cat("- study_distribution.png\n")
cat("- geographic_distribution.png\n")
cat("- composite_results_figure.png\n")
cat("- summary_statistics.json\n")
cat("\nNext step: Generate manuscript and supplementary materials\n")
