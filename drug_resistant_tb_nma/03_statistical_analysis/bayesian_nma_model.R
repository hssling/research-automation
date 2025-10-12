# Bayesian Network Meta-Analysis Model for Drug-Resistant Tuberculosis
# Implements random-effects NMA with component modeling for BPaL/BPaLM vs alternatives

library(gemtc)
library(rjags)
library(ggplot2)
library(ggmcmc)
library(netmeta)
library(readxl)
library(dplyr)
library(tidyr)

# Set seed for reproducibility
set.seed(12345)

# Load and prepare data
load_data <- function() {
  "
  Load extracted data from the systematic review
  Expected format: Study, Treatment, Responders, SampleSize
  "

  # Read the extracted data
  data <- read.csv("drug_resistant_tb_nma/02_data_extraction/extracted_data.csv")

  # Convert to contrast-based format for GeMTC
  # Treatments: A=BPaL, B=BPaLM, C=Short MDR, D=Long Individualized

  return(data)
}

# Prepare data for network meta-analysis
prepare_nma_data <- function(raw_data) {
  "
  Convert raw extracted data to GeMTC format
  "

  # Create treatment coding
  treatments <- c("BPaL", "BPaLM", "Short_MDR", "Long_Individualized")

  # Transform data to arm-based format
  # Each row represents one treatment arm in one study

  nma_data <- data.frame(
    study = character(),
    treatment = character(),
    responders = integer(),
    sampleSize = integer(),
    stringsAsFactors = FALSE
  )

  for (i in 1:nrow(raw_data)) {
    study_id <- raw_data$study_id[i]

    # Add each treatment arm
    for (tx in c("BPaL", "BPaLM", "Short_MDR", "Long_Individualized")) {
      if (!is.na(raw_data[i, paste0(tx, "_success")])) {
        nma_data <- rbind(nma_data, data.frame(
          study = study_id,
          treatment = tx,
          responders = raw_data[i, paste0(tx, "_success")],
          sampleSize = raw_data[i, paste0(tx, "_n")]
        ))
      }
    }
  }

  return(nma_data)
}

# Fit Bayesian NMA model
fit_bayesian_nma <- function(nma_data) {
  "
  Fit random-effects Bayesian NMA model using GeMTC
  "

  # Create network
  network <- mtc.network(data.ab = nma_data)

  # Define model (random effects)
  model <- mtc.model(network,
                    type = "consistency",
                    likelihood = "binom",
                    link = "logit",
                    linearModel = "random",
                    n.chain = 4,
                    n.adapt = 5000,
                    n.iter = 20000,
                    thin = 10)

  # Run MCMC
  results <- mtc.run(model, ma.stat = "OR")

  return(list(network = network, model = model, results = results))
}

# Component network meta-analysis for drug effects
fit_component_nma <- function(nma_data) {
  "
  Component NMA to evaluate individual drug contributions
  Treatments modeled as combinations of components:
  - Bedaquiline (BDQ)
  - Pretomanid (Pa)
  - Linezolid (LZD)
  - Moxifloxacin (MFX)
  - Short regimen backbone (SHORT)
  - Long regimen backbone (LONG)
  "

  # Define treatment compositions
  treatment_compositions <- list(
    "BPaL" = c("BDQ", "Pa", "LZD"),
    "BPaLM" = c("BDQ", "Pa", "LZD", "MFX"),
    "Short_MDR" = c("SHORT"),
    "Long_Individualized" = c("LONG")
  )

  # Create component data
  component_data <- nma_data
  component_data$treatment <- as.character(component_data$treatment)

  # Fit component model
  component_network <- mtc.network(data.ab = component_data)

  # Component model specification would require custom JAGS code
  # This is a simplified version - full implementation needs JAGS model file

  return(component_network)
}

# Generate league table
create_league_table <- function(nma_results) {
  "
  Create league table showing all pairwise comparisons
  "

  # Extract league table from GeMTC results
  league <- relative.effect(nma_results, t1 = c("BPaL", "BPaLM", "Short_MDR"),
                           t2 = c("Long_Individualized"))

  # Format as publication-ready table
  league_table <- data.frame(
    Comparison = rownames(league$summary),
    OR = round(exp(league$summary$logOR), 2),
    lowerCI = round(exp(league$summary$`2.5%`), 2),
    upperCI = round(exp(league$summary$`97.5%`), 2),
    stringsAsFactors = FALSE
  )

  # Add statistical significance
  league_table$Significance <- ifelse(
    league_table$lowerCI > 1, "Favors first",
    ifelse(league_table$upperCI < 1, "Favors second", "No difference")
  )

  return(league_table)
}

# Calculate SUCRA rankings
calculate_sucra <- function(nma_results) {
  "
  Calculate Surface Under the Cumulative Ranking Curve (SUCRA)
  "

  # Extract ranking probabilities
  rank_probs <- rank.probability(nma_results)

  # Calculate SUCRA for each treatment
  sucra_values <- data.frame(
    Treatment = colnames(rank_probs),
    SUCRA = numeric(length(colnames(rank_probs))),
    Rank = numeric(length(colnames(rank_probs)))
  )

  for (i in 1:ncol(rank_probs)) {
    sucra_values$SUCRA[i] <- sum(rank_probs[,i] * (1:nrow(rank_probs))) / nrow(rank_probs)
    sucra_values$Rank[i] <- which.max(rank_probs[,i])
  }

  # Sort by SUCRA value (higher is better)
  sucra_values <- sucra_values[order(-sucra_values$SUCRA), ]

  return(sucra_values)
}

# Create forest plot for network estimates
create_forest_plot <- function(nma_results) {
  "
  Generate forest plot showing network estimates vs direct evidence
  "

  # Extract forest plot data
  forest_data <- forest.mtc(nma_results)

  # Create visualization
  p <- ggplot(forest_data, aes(x = Treatment, y = OR, ymin = lower, ymax = upper)) +
    geom_pointrange() +
    geom_hline(yintercept = 1, linetype = "dashed") +
    coord_flip() +
    theme_minimal() +
    labs(title = "Network Meta-Analysis Results",
         subtitle = "Odds Ratios for Treatment Success",
         x = "Treatment", y = "Odds Ratio (95% CI)")

  ggsave("drug_resistant_tb_nma/04_results/forest_plot.png", p, width = 10, height = 6)

  return(p)
}

# Assess heterogeneity and inconsistency
assess_heterogeneity <- function(nma_results) {
  "
  Evaluate heterogeneity and inconsistency in the network
  "

  # Overall heterogeneity
  heterogeneity <- mtc.anohe(nma_results)

  # Node-splitting for inconsistency
  nodesplit <- mtc.nodesplit(nma_results)

  # Compare direct and indirect evidence
  comparison <- data.frame(
    Comparison = names(nodesplit$direct),
    Direct_OR = exp(nodesplit$direct$logOR),
    Indirect_OR = exp(nodesplit$indirect$logOR),
    P_value = nodesplit$p.value
  )

  return(list(heterogeneity = heterogeneity,
              nodesplit = nodesplit,
              comparison = comparison))
}

# Subgroup analysis by resistance pattern
subgroup_analysis <- function(nma_data) {
  "
  Subgroup analysis by fluoroquinolone resistance status
  "

  # Split data by FQ resistance
  fq_resistant <- subset(nma_data, fq_resistance == "Yes")
  fq_susceptible <- subset(nma_data, fq_resistance == "No")

  # Fit separate models
  if (nrow(fq_resistant) > 0) {
    fq_res_model <- fit_bayesian_nma(fq_resistant)
  }

  if (nrow(fq_susceptible) > 0) {
    fq_sus_model <- fit_bayesian_nma(fq_susceptible)
  }

  return(list(fq_resistant_model = fq_res_model,
              fq_susceptible_model = fq_sus_model))
}

# Sensitivity analysis
sensitivity_analysis <- function(nma_data) {
  "
  Sensitivity analysis excluding high risk of bias studies
  "

  # Exclude high risk of bias studies
  low_rob_data <- subset(nma_data, risk_of_bias != "High")

  # Refit model
  sensitivity_model <- fit_bayesian_nma(low_rob_data)

  return(sensitivity_model)
}

# Generate comprehensive results summary
generate_results_summary <- function(nma_results, league_table, sucra_values) {
  "
  Generate comprehensive summary of NMA results
  "

  summary <- list(
    model_convergence = gelman.diag(nma_results),
    league_table = league_table,
    sucra_rankings = sucra_values,
    treatment_effects = summary(nma_results),
    model_fit = deviance(nma_results)
  )

  # Save summary statistics
  capture.output(summary, file = "drug_resistant_tb_nma/04_results/nma_summary.txt")

  return(summary)
}

# Main execution function
run_complete_nma <- function() {
  "
  Execute complete NMA pipeline
  "

  # Load and prepare data
  raw_data <- load_data()
  nma_data <- prepare_nma_data(raw_data)

  # Fit main NMA model
  nma_results <- fit_bayesian_nma(nma_data)

  # Generate outputs
  league_table <- create_league_table(nma_results)
  sucra_values <- calculate_sucra(nma_results)
  forest_plot <- create_forest_plot(nma_results)

  # Model assessment
  heterogeneity_results <- assess_heterogeneity(nma_results)

  # Subgroup and sensitivity analyses
  subgroup_results <- subgroup_analysis(nma_data)
  sensitivity_results <- sensitivity_analysis(nma_data)

  # Component NMA
  component_results <- fit_component_nma(nma_data)

  # Generate comprehensive summary
  results_summary <- generate_results_summary(nma_results, league_table, sucra_values)

  # Save all results
  saveRDS(list(
    nma_results = nma_results,
    league_table = league_table,
    sucra_values = sucra_values,
    heterogeneity = heterogeneity_results,
    subgroup = subgroup_results,
    sensitivity = sensitivity_results,
    component = component_results,
    summary = results_summary
  ), "drug_resistant_tb_nma/04_results/nma_complete_results.rds")

  # Export league table
  write.csv(league_table, "drug_resistant_tb_nma/04_results/league_table.csv", row.names = FALSE)
  write.csv(sucra_values, "drug_resistant_tb_nma/04_results/sucra_rankings.csv", row.names = FALSE)

  cat("NMA analysis completed successfully!\n")
  cat("Results saved to drug_resistant_tb_nma/04_results/\n")

  return(results_summary)
}

# Execute if run directly
if (sys.nframe() == 0) {
  results <- run_complete_nma()
  print("Analysis complete. Check output files for detailed results.")
}
