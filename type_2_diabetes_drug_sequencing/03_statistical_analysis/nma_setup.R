# Type 2 Diabetes Drug Sequencing - Network Meta-Analysis Setup
# R Script for Bayesian hierarchical NMA with multi-outcome analysis

# Load required packages
library(gemtc)      # GeMTC for network meta-analysis
library(rjags)      # JAGS interface for Bayesian analysis
library(coda)       # MCMC output analysis
library(ggplot2)    # Visualization
library(dplyr)      # Data manipulation
library(readr)      # CSV reading
library(tidyr)      # Data tidying
library(metafor)    # Additional meta-analysis tools

# Set seed for reproducibility
set.seed(12345)

# Create output directory for results
dir.create("03_statistical_analysis/output", showWarnings = FALSE)
dir.create("03_statistical_analysis/plots", showWarnings = FALSE)

# Load and prepare the extracted data
load_extracted_data <- function() {
  # Read all extracted study data files
  data_files <- list.files("02_data_extraction",
                          pattern = "*_extraction.csv",
                          full.names = TRUE)

  study_data <- list()

  for(file in data_files) {
    study_name <- gsub("_extraction.csv", "", basename(file))
    study_data[[study_name]] <- read_csv(file, show_col_types = FALSE)
  }

  return(study_data)
}

# Prepare data for GeMTC format
prepare_gemtc_data <- function(study_data) {
  # Extract treatment comparisons and outcomes
  treatments <- data.frame(
    id = 1:8,
    treatment = c("SGLT2i", "GLP-1RA", "DPP-4i", "TZD", "Basal insulin",
                  "SGLT2i+DPP-4i", "TZD+SGLT2i+Metformin", "Tirzepatide")
  )

  # Create study-treatment-outcome matrix
  nma_data <- data.frame(
    study = character(),
    treatment = character(),
    outcome_type = character(),
    mean_effect = numeric(),
    std_error = numeric(),
    stringsAsFactors = FALSE
  )

  # Process each study
  for(study_name in names(study_data)) {
    study <- study_data[[study_name]]

    # Extract HbA1c data
    if(!is.na(study$`OUTCOME_HBA1C_ARM1_MD`)) {
      nma_data <- rbind(nma_data, data.frame(
        study = study_name,
        treatment = study$INTERVENTION_ARM1_DRUG_CLASS,
        outcome_type = "HbA1c",
        mean_effect = as.numeric(gsub("%.*", "", study$`OUTCOME_HBA1C_ARM1_MD`)),
        std_error = 0.1  # Placeholder - should be calculated from CI
      ))
    }

    # Extract weight data
    if(!is.na(study$`OUTCOME_WEIGHT_ARM1_MD`)) {
      nma_data <- rbind(nma_data, data.frame(
        study = study_name,
        treatment = study$INTERVENTION_ARM1_DRUG_CLASS,
        outcome_type = "Weight",
        mean_effect = as.numeric(gsub("kg.*", "", study$`OUTCOME_WEIGHT_ARM1_MD`)),
        std_error = 0.2  # Placeholder - should be calculated from CI
      ))
    }

    # Extract CV outcome data (convert HR to log HR for NMA)
    if(!is.na(study$`OUTCOME_CV_COMPOSITE_ARM1_EFFECT`)) {
      hr_value <- as.numeric(gsub("HR ", "", gsub(" .*", "", study$`OUTCOME_CV_COMPOSITE_ARM1_EFFECT`)))
      if(!is.na(hr_value)) {
        nma_data <- rbind(nma_data, data.frame(
          study = study_name,
          treatment = study$INTERVENTION_ARM1_DRUG_CLASS,
          outcome_type = "CV",
          mean_effect = log(hr_value),
          std_error = 0.15  # Placeholder - should be calculated from CI
        ))
      }
    }
  }

  return(list(data = nma_data, treatments = treatments))
}

# Set up JAGS model for Bayesian NMA
setup_jags_model <- function() {
  jags_model <- "
  model {
    for(i in 1:ns) {
      # Random effects model for multi-arm trials
      for(k in 1:na[i]) {
        y[i,k] ~ dnorm(theta[i,t[i,k]], prec[i,k])
        theta[i,t[i,k]] <- mu[t[i,k]] + delta[i,t[i,k]]
      }

      # Study-specific random effects
      delta[i,1] <- 0
      for(k in 2:nt[i]) {
        delta[i,k] ~ dnorm(0, tau)
      }
    }

    # Treatment effects (hierarchical model)
    for(j in 1:nt) {
      mu[j] ~ dnorm(0, 0.001)
    }

    # Heterogeneity parameter
    tau ~ dgamma(0.1, 0.1)

    # Between-study variance
    sd <- sqrt(1/tau)
  }
  "

  return(jags_model)
}

# Run network meta-analysis
run_nma_analysis <- function(gemtc_data) {
  # Create GeMTC network object
  network <- mtc.network(data.ab = gemtc_data$data)

  # Set up model
  model <- mtc.model(network,
                    type = "consistency",
                    likelihood = "normal",
                    link = "identity",
                    linearModel = "random")

  # Run MCMC simulation
  mcmc_results <- mtc.run(model,
                         n.adapt = 1000,
                         n.iter = 5000,
                         thin = 1)

  # Summarize results
  summary_results <- summary(mcmc_results)

  return(list(network = network,
              model = model,
              results = mcmc_results,
              summary = summary_results))
}

# Generate ranking probabilities (SUCRA)
calculate_sucra <- function(mcmc_results) {
  # Extract treatment effect samples
  effect_samples <- as.matrix(mcmc_results)

  # Calculate ranking probabilities
  rank_probs <- data.frame()

  for(outcome in unique(gemtc_data$data$outcome_type)) {
    outcome_cols <- grep(outcome, colnames(effect_samples))
    if(length(outcome_cols) > 0) {
      outcome_effects <- effect_samples[, outcome_cols]

      # Calculate rank probabilities for each treatment
      ranks <- t(apply(-outcome_effects, 1, rank))  # Negative for benefit outcomes

      # Average rank probabilities
      avg_ranks <- colMeans(ranks)

      # Calculate SUCRA values
      sucra_values <- colMeans(ranks <= matrix(rep(1:ncol(ranks), nrow(ranks)),
                                              nrow = nrow(ranks), byrow = TRUE))

      rank_probs <- rbind(rank_probs, data.frame(
        Outcome = outcome,
        Treatment = colnames(outcome_effects),
        Mean_Rank = avg_ranks,
        SUCRA = sucra_values
      ))
    }
  }

  return(rank_probs)
}

# Create visualization functions
create_forest_plot <- function(nma_results, outcome_type) {
  # Extract results for specific outcome
  outcome_data <- nma_results$summary$samples[[outcome_type]]

  # Create forest plot
  p <- ggplot(outcome_data, aes(x = treatment, y = TE, ymin = lower, ymax = upper)) +
    geom_pointrange() +
    geom_hline(yintercept = 0, lty = 2) +
    coord_flip() +
    labs(title = paste(outcome_type, "Treatment Effects"),
         x = "Treatment", y = "Effect Size (95% CI)") +
    theme_minimal()

  return(p)
}

# Main execution function
main_nma_analysis <- function() {
  cat("Loading extracted study data...\n")
  study_data <- load_extracted_data()

  cat("Preparing data for GeMTC format...\n")
  gemtc_data <- prepare_gemtc_data(study_data)

  cat("Setting up JAGS model...\n")
  jags_model <- setup_jags_model()

  cat("Running network meta-analysis...\n")
  nma_results <- run_nma_analysis(gemtc_data)

  cat("Calculating SUCRA rankings...\n")
  sucra_results <- calculate_sucra(nma_results$results)

  cat("Generating visualizations...\n")

  # Create forest plots for each outcome
  outcomes <- unique(gemtc_data$data$outcome_type)
  plots <- list()

  for(outcome in outcomes) {
    plots[[outcome]] <- create_forest_plot(nma_results, outcome)
    ggsave(filename = paste0("03_statistical_analysis/plots/forest_", outcome, ".png"),
           plot = plots[[outcome]], width = 10, height = 6)
  }

  # Save results
  write_csv(sucra_results, "03_statistical_analysis/output/sucra_rankings.csv")
  saveRDS(nma_results, "03_statistical_analysis/output/nma_results.rds")

  cat("Analysis complete! Results saved to 03_statistical_analysis/output/\n")

  return(list(
    nma_results = nma_results,
    sucra_results = sucra_results,
    plots = plots
  ))
}

# Execute the analysis
if(interactive()) {
  results <- main_nma_analysis()

  # Print summary of findings
  cat("\n=== NETWORK META-ANALYSIS RESULTS ===\n")
  cat("SUCRA Rankings:\n")
  print(results$sucra_results)

  cat("\nAnalysis completed successfully!\n")
  cat("Check 03_statistical_analysis/output/ for detailed results\n")
  cat("Check 03_statistical_analysis/plots/ for visualizations\n")
}
