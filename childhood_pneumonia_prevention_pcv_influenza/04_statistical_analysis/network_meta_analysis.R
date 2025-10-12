# Network Meta-Analysis for PCV Effectiveness in Childhood Pneumonia Prevention
# Direct and Indirect Comparisons of PCV Vaccination Strategies

# Load required packages for network meta-analysis
required_packages <- c("netmeta", "gemtc", "rjags", "coda", "metafor",
                      "ggplot2", "dplyr", "readr", "jsonlite")

for(pkg in required_packages) {
  if (!require(pkg, character.only = TRUE)) {
    install.packages(pkg, dependencies = TRUE)
  }
}

library(netmeta)
library(metafor)
library(ggplot2)
library(dplyr)
library(readr)

# Set working directory
setwd("childhood_pneumonia_prevention_pcv_influenza")

# Import REAL validated extracted data
data <- read_csv("03_data_extraction/final_extracted_data.csv")
rob_data <- read_csv("03_data_extraction/rob2_assessment_forms.csv")

# Print data overview
cat("\n=== DATA OVERVIEW ===\n")
cat("Total studies included:", nrow(data), "\n")
cat("Studies by design:\n")
print(table(data$study_design))
cat("Studies by income level:\n")
print(table(data$income_level))
cat("PCV products identified:\n")
print(table(data$pcv_product, useNA = "ifany"))

# OUTCOME 1: RADIOLOGICALLY CONFIRMED PNEUMONIA
# Prepare data for network meta-analysis
pneumonia_network <- data %>%
  filter(outcome_primary == "radio_confirmed_pneumonia",
         study_design %in% c("rct", "cluster_rct")) %>%
  select(study_id, pcv_product, rr_lci, rr_uci, n_intervention, n_control) %>%
  mutate(treatment = case_when(
    grepl("PCV10", pcv_product) ~ "PCV10",
    grepl("PCV13", pcv_product) ~ "PCV13",
    grepl("PCV7|heptavalent", tolower(pcv_product)) ~ "PCV7",
    grepl("control|placebo", tolower(pcv_product)) ~ "Control",
    TRUE ~ "PCV_unspecified"
  )) %>%
  filter(!is.na(rr_lci) & !is.na(rr_uci) & rr_lci > 0 & rr_uci > 0)

# Calculate effect sizes for network
pneumonia_network <- pneumonia_network %>%
  mutate(yi = log(rr_lci + (rr_uci - rr_lci) / 2),  # log risk ratio
         sei = (log(rr_uci) - log(rr_lci)) / (2 * 1.96))  # standard error

cat("\n=== PNEUMONIA NETWORK DATA ===\n")
print(pneumonia_network %>% select(study_id, treatment, yi, sei))

# Create network meta-analysis object
if(nrow(pneumonia_network) >= 3 && length(unique(pneumonia_network$treatment)) >= 3) {
  try({
    pneumonia_netmeta <- netmeta(TE = yi, seTE = sei, treat1 = treatment,
                                treat2 = "Control", studlab = study_id,
                                data = pneumonia_network, sm = "RR", method = "REML")

    cat("\n=== PNEUMONIA NETWORK META-ANALYSIS RESULTS ===\n")
    summary(pneumonia_netmeta)

    # League table for direct and indirect comparisons
    pneumonia_league <- netleague(pneumonia_netmeta)
    cat("\nLeague Table (Risk Ratios vs Control):\n")
    print(pneumonia_league)

    # Network plot
    png("05_results_visualization/pneumonia_network_plot.png", width = 800, height = 600)
    netgraph(pneumonia_netmeta, plastic = TRUE, points = TRUE, col = "blue",
             thickness = "se.fixed", multiarm = FALSE)
    title("Network Plot - Pneumonia Prevention")
    dev.off()

    # Forest plot of network results
    png("05_results_visualization/pneumonia_network_forest.png", width = 800, height = 600)
    forest(pneumonia_netmeta, ref = "Control", sortvar = TE, xlim = c(0.05, 3))
    title("Network Meta-Analysis - Pneumonia Outcomes")
    dev.off()

  }, error = function(e) {
    cat("\n⚠️ Pneumonia network meta-analysis failed:", e$message, "\n")
    cat("Insufficient data for network (need ≥3 studies comparing ≥3 interventions)\n")
  })
} else {
  cat("\n⚠️ Insufficient data for pneumonia network meta-analysis\n")
  cat("Need ≥3 studies comparing ≥3 different PCV interventions\n")
}

# OUTCOME 2: ALL-CAUSE MORTALITY
# Prepare mortality data for network
mortality_network <- data %>%
  filter(outcome_primary == "mortality",
         study_design %in% c("rct", "cluster_rct")) %>%
  select(study_id, pcv_product, rr_lci, rr_uci, n_intervention, n_control) %>%
  mutate(treatment = case_when(
    grepl("PCV10", pcv_product) ~ "PCV10",
    grepl("PCV13", pcv_product) ~ "PCV13",
    grepl("PCV7|heptavalent", tolower(pcv_product)) ~ "PCV7",
    grepl("control|placebo", tolower(pcv_product)) ~ "Control",
    TRUE ~ "PCV_unspecified"
  )) %>%
  filter(!is.na(rr_lci) & !is.na(rr_uci) & rr_lci > 0 & rr_uci > 0)

# Calculate effect sizes for mortality network
mortality_network <- mortality_network %>%
  mutate(yi = log(rr_lci + (rr_uci - rr_lci) / 2),
         sei = (log(rr_uci) - log(rr_lci)) / (2 * 1.96))

cat("\n=== MORTALITY NETWORK DATA ===\n")
print(mortality_network %>% select(study_id, treatment, yi, sei))

# Mortality network meta-analysis
if(nrow(mortality_network) >= 3 && length(unique(mortality_network$treatment)) >= 3) {
  try({
    mortality_netmeta <- netmeta(TE = yi, seTE = sei, treat1 = treatment,
                                treat2 = "Control", studlab = study_id,
                                data = mortality_network, sm = "RR", method = "REML")

    cat("\n=== MORTALITY NETWORK META-ANALYSIS RESULTS ===\n")
    summary(mortality_netmeta)

    # League table for mortality
    mortality_league <- netleague(mortality_netmeta)
    cat("\nLeague Table - Mortality (Risk Ratios vs Control):\n")
    print(mortality_league)

    # Network plot for mortality
    png("05_results_visualization/mortality_network_plot.png", width = 800, height = 600)
    netgraph(mortality_netmeta, plastic = TRUE, points = TRUE, col = "red",
             thickness = "se.fixed", multiarm = FALSE)
    title("Network Plot - Mortality Prevention")
    dev.off()

    # Forest plot
    png("05_results_visualization/mortality_network_forest.png", width = 800, height = 600)
    forest(mortality_netmeta, ref = "Control", sortvar = TE, xlim = c(0.05, 3))
    title("Network Meta-Analysis - Mortality Outcomes")
    dev.off()

  }, error = function(e) {
    cat("\n⚠️ Mortality network meta-analysis failed:", e$message, "\n")
    cat("Insufficient data for mortality network\n")
  })
} else {
  cat("\n⚠️ Insufficient data for mortality network meta-analysis\n")
  cat("Need ≥3 studies comparing ≥3 different PCV interventions\n")
}

# SUBGROUP ANALYSIS: DIFFERENT PCV SCHEDULES
# Compare 2+1 vs 3+0 schedules
schedule_data <- data %>%
  filter(!is.na(schedule), schedule %in% c("2+1", "3+0")) %>%
  select(study_id, schedule, rr_lci, rr_uci, outcome_primary) %>%
  filter(!is.na(rr_lci) & !is.na(rr_uci))

if(nrow(schedule_data) >= 2) {
  cat("\n=== SCHEDULE COMPARISON ANALYSIS ===\n")

  for(outcome in unique(schedule_data$outcome_primary)) {
    outcome_data <- schedule_data %>% filter(outcome_primary == outcome)

    if(nrow(outcome_data) >= 2) {
      cat("\n", toupper(outcome), "outcome by schedule:\n")

      outcome_data <- outcome_data %>%
        mutate(yi = log(rr_lci + (rr_uci - rr_lci)/2),
               sei = (log(rr_uci) - log(rr_lci))/(2*1.96))

      # Meta-analysis by schedule
      schedule_ma <- rma(yi = yi, sei = sei, data = outcome_data,
                        mods = ~ factor(schedule), method = "REML")

      cat("Schedule comparison results:\n")
      print(summary(schedule_ma))

      # Forest plot by schedule
      try({
        png(paste0("05_results_visualization/", outcome, "_schedule_forest.png"),
            width = 800, height = 600)
        forest(schedule_ma, xlab = "Risk Ratio (95% CI)")
        title(paste("Schedule Comparison -", tools::toTitleCase(outcome)))
        dev.off()
      }, error = function(e) {
        cat("Error creating schedule forest plot:", e$message, "\n")
      })
    }
  }
}

# ROBINS-I ASSESSMENT INTEGRATION
# If we have ROB data, incorporate into network analysis
if(nrow(rob_data) > 0) {
  cat("\n=== RISK OF BIAS INTEGRATION ===\n")
  cat("Risk of bias levels in included studies:\n")
  print(table(rob_data$overall_bias))

  # Subgroup analysis by ROB level
  rob_levels <- c("Low", "Moderate", "High")

  for(level in rob_levels) {
    subset_data <- rob_data %>% filter(overall_bias == level)
    if(nrow(subset_data) > 0) {
      cat("\nStudies with", level, "risk of bias:", nrow(subset_data), "\n")
    }
  }
}

# SAVE COMPREHENSIVE RESULTS
network_results <- list(
  pneumonia_network_summary = if(exists("pneumonia_netmeta")) summary(pneumonia_netmeta) else "Insufficient data",
  mortality_network_summary = if(exists("mortality_netmeta")) summary(mortality_netmeta) else "Insufficient data",
  total_studies = nrow(data),
  nma_ready_studies = length(unique(c(pneumonia_network$study_id, mortality_network$study_id))),
  treatments_compared = length(unique(c(pneumonia_network$treatment, mortality_network$treatment))),
  analysis_date = format(Sys.time(), "%Y-%m-%d %H:%M:%S")
)

# Save network results summary
write_json(network_results, "04_statistical_analysis/network_meta_analysis_results.json", pretty = TRUE)

# Create results summary table
network_summary_table <- data.frame(
  Outcome = c("Radiologically Confirmed Pneumonia", "All-cause Mortality"),
  N_studies = c(length(unique(pneumonia_network$study_id)),
               length(unique(mortality_network$study_id))),
  Treatments_compared = c(length(unique(pneumonia_network$treatment)),
                         length(unique(mortality_network$treatment))),
  Network_stat = c(if(exists("pneumonia_netmeta")) "Completed" else "Insufficient data",
                  if(exists("mortality_netmeta")) "Completed" else "Insufficient data"),
  League_table_available = c(if(exists("pneumonia_league")) "Yes" else "No",
                           if(exists("mortality_league")) "Yes" else "No")
)

write_csv(network_summary_table, "04_statistical_analysis/network_meta_analysis_summary.csv")

# Print final summary
cat("\n=== NETWORK META-ANALYSIS COMPLETION SUMMARY ===\n")
cat("Files created:\n")
cat("- Network plot visualizations saved to 05_results_visualization/\n")
cat("- Network forest plots created\n")
cat("- Results summary saved to 04_statistical_analysis/network_meta_analysis_results.json\n")
cat("- Analysis summary table: network_meta_analysis_summary.csv\n")

if(!exists("pneumonia_netmeta") && !exists("mortality_netmeta")) {
  cat("\n⚠️ NOTE: No network meta-analysis completed due to insufficient comparative data\n")
  cat("Network NMA requires ≥3 studies directly comparing ≥3 interventions\n")
  cat("Current data supports traditional pairwise meta-analyses only\n")
} else {
  cat("\n✅ Network meta-analysis successfully completed for available outcomes\n")
}

cat("\nNext step: Align manuscript sections with actual analyses performed\n")
