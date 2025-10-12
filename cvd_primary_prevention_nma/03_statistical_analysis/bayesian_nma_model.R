# Bayesian Network Meta-Analysis Model for CVD Primary Prevention
# R Script for GeMTC Implementation

# Load required packages
library(gemtc)
library(rjags)
library(coda)
library(netmeta)
library(ggplot2)
library(ggnetwork)
library(igraph)
library(dplyr)
library(readr)
library(tidyr)

# Set working directory
setwd("cvd_primary_prevention_nma/03_statistical_analysis")

# Load extracted data
data_file <- "../02_data_extraction/extracted_data.csv"
if (file.exists(data_file)) {
  extracted_data <- read_csv(data_file)
  print(paste("Loaded data from", data_file))
} else {
  # Create sample data structure for demonstration
  extracted_data <- data.frame(
    study_id = c("JUPITER", "HOPE-3", "FOURIER", "ODYSSEY"),
    treatment = c("Rosuvastatin", "Polypill", "Evolocumab", "Alirocumab"),
    control = c("Placebo", "Placebo", "Statin", "Statin"),
    responders = c(142, 89, 156, 134),
    sample_size = c(8901, 12605, 27564, 18924),
    follow_up_years = c(1.9, 5.6, 2.2, 2.8)
  )
  print("Using sample data for demonstration")
}

# Data Preparation for NMA
prepare_nma_data <- function(data) {
  # Create arm-level data structure for GeMTC
  studies <- unique(data$study_id)
  treatments <- unique(c(data$treatment, data$control))

  # Create treatment coding
  treatment_codes <- data.frame(
    treatment = treatments,
    code = 1:length(treatments)
  )

  # Create study data in GeMTC format
  nma_data <- list()

  for (i in 1:length(studies)) {
    study_data <- data[data$study_id == studies[i], ]

    # Treatment arm
    treat_arm <- data.frame(
      study = studies[i],
      treatment = as.numeric(treatment_codes$code[treatment_codes$treatment == study_data$treatment[1]]),
      responders = study_data$responders[1],
      sampleSize = study_data$sample_size[1]
    )

    # Control arm
    control_arm <- data.frame(
      study = studies[i],
      treatment = as.numeric(treatment_codes$code[treatment_codes$treatment == study_data$control[1]]),
      responders = sample_size - responders,  # Approximation
      sampleSize = study_data$sample_size[1]
    )

    nma_data[[i]] <- rbind(treat_arm, control_arm)
  }

  # Combine all study data
  combined_data <- do.call(rbind, nma_data)

  # Treatment names mapping
  treatment_names <- treatment_codes$treatment
  names(treatment_names) <- treatment_codes$code

  return(list(
    data = combined_data,
    treatments = treatment_names
  ))
}

# Prepare data
nma_input <- prepare_nma_data(extracted_data)

# Create GeMTC network
network <- mtc.network(data.re = nma_input$data)

# Run Bayesian NMA model
run_bayesian_nma <- function(network) {
  # Define model
  model <- mtc.model(network,
    type = "consistency",
    likelihood = "binom",
    link = "logit",
    linearModel = "random"
  )

  # Run MCMC simulation
  results <- mtc.run(model,
    n.adapt = 5000,
    n.iter = 20000,
    thin = 10
  )

  return(list(model = model, results = results))
}

# Execute NMA
nma_results <- run_bayesian_nma(network)

# Extract results
summary_results <- summary(nma_results$results)
forest_data <- forest(nma_results$results)

# Treatment rankings (SUCRA)
rank_results <- rank.probability(nma_results$results)

# Relative effects
relative_effects <- relative.effect(nma_results$results)

# Save results
save_nma_results <- function(results, filename) {
  # Summary statistics
  write.csv(as.data.frame(summary_results$samples), paste0(filename, "_summary.csv"))

  # Rankings
  write.csv(rank_results, paste0(filename, "_rankings.csv"))

  # Relative effects
  write.csv(relative_effects, paste0(filename, "_effects.csv"))

  # Forest plot data
  write.csv(forest_data, paste0(filename, "_forest.csv"))

  print(paste("Results saved to", filename, "_*.csv"))
}

# Save results
save_nma_results(summary_results, "cvd_prevention_nma_results")

# Generate network geometry plot
create_network_plot <- function(network) {
  # Create network graph
  treatments <- unique(c(network$data.re$treatment))
  n_treatments <- length(treatments)

  # Create adjacency matrix
  adj_matrix <- matrix(0, n_treatments, n_treatments)
  rownames(adj_matrix) <- colnames(adj_matrix) <- treatments

  # Fill adjacency matrix based on comparisons
  for (i in 1:nrow(network$data.re)) {
    treat1 <- network$data.re$treatment[i]
    study_id <- network$data.re$study[i]

    # Find other treatments in same study
    study_treatments <- network$data.re$treatment[network$data.re$study == study_id]

    for (j in study_treatments) {
      if (treat1 != j) {
        adj_matrix[as.character(treat1), as.character(j)] <- 1
        adj_matrix[as.character(j), as.character(treat1)] <- 1
      }
    }
  }

  # Create graph object
  graph_obj <- graph_from_adjacency_matrix(adj_matrix, mode = "undirected")

  # Plot network
  plot(graph_obj,
    vertex.size = 30,
    vertex.label.cex = 0.8,
    vertex.color = "lightblue",
    edge.width = 2,
    main = "Evidence Network: CVD Primary Prevention"
  )

  return(graph_obj)
}

# Create and save network plot
network_plot <- create_network_plot(network)
ggsave("network_geometry.png", width = 10, height = 8, dpi = 300)

# Generate SUCRA plot
create_sucra_plot <- function(rank_results) {
  # Convert rank probabilities to data frame
  rank_df <- as.data.frame(rank_results)
  rank_df$treatment <- rownames(rank_results)

  # Calculate SUCRA values
  sucra_values <- numeric(nrow(rank_df))
  for (i in 1:nrow(rank_df)) {
    sucra_values[i] <- sum(rank_df[i, 1:(ncol(rank_df)-1)] * seq(0, 1, length.out = ncol(rank_df)-1))
  }
  rank_df$sucra <- sucra_values

  # Sort by SUCRA
  rank_df <- rank_df[order(rank_df$sucra, decreasing = TRUE), ]

  # Create plot
  ggplot(rank_df, aes(x = reorder(treatment, sucra), y = sucra)) +
    geom_bar(stat = "identity", fill = "steelblue", alpha = 0.8) +
    geom_text(aes(label = sprintf("%.1f%%", sucra * 100)), hjust = -0.1) +
    coord_flip() +
    labs(
      title = "Surface Under the Cumulative Ranking Curve (SUCRA)",
      x = "Treatment",
      y = "SUCRA Value"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14),
      axis.title = element_text(size = 12),
      axis.text = element_text(size = 10)
    )

  ggsave("sucra_rankings.png", width = 10, height = 6, dpi = 300)
}

# Create SUCRA plot
create_sucra_plot(rank_results)

# Generate league table
create_league_table <- function(relative_effects) {
  # Extract treatment names
  treatments <- unique(rownames(relative_effects))

  # Create matrix for league table
  n_treatments <- length(treatments)
  league_matrix <- matrix(NA, n_treatments, n_treatments)
  rownames(league_matrix) <- colnames(league_matrix) <- treatments

  # Fill league table
  for (i in 1:n_treatments) {
    for (j in 1:n_treatments) {
      if (i != j) {
        comp_name <- paste0(treatments[i], " vs ", treatments[j])
        if (comp_name %in% rownames(relative_effects)) {
          league_matrix[i, j] <- sprintf("%.2f (%.2f, %.2f)",
            relative_effects[comp_name, "50%"],
            relative_effects[comp_name, "2.5%"],
            relative_effects[comp_name, "97.5%"]
          )
        }
      }
    }
  }

  # Save league table
  write.csv(league_matrix, "league_table.csv")
  return(league_matrix)
}

# Create league table
league_table <- create_league_table(relative_effects)

# Generate heterogeneity assessment
assess_heterogeneity <- function(results) {
  # Extract heterogeneity parameter
  heterogeneity <- results$samples[, "tau"]

  # Create summary
  hetero_summary <- data.frame(
    parameter = "tau",
    mean = mean(heterogeneity),
    sd = sd(heterogeneity),
    median = median(heterogeneity),
    lower_ci = quantile(heterogeneity, 0.025),
    upper_ci = quantile(heterogeneity, 0.975)
  )

  # Interpret heterogeneity
  interpretation <- case_when(
    hetero_summary$median < 0.1 ~ "Low heterogeneity",
    hetero_summary$median < 0.5 ~ "Moderate heterogeneity",
    hetero_summary$median < 1.0 ~ "Substantial heterogeneity",
    TRUE ~ "Considerable heterogeneity"
  )

  hetero_summary$interpretation <- interpretation

  # Save results
  write.csv(hetero_summary, "heterogeneity_assessment.csv")

  return(hetero_summary)
}

# Assess heterogeneity
hetero_assessment <- assess_heterogeneity(nma_results$results)

# Create convergence diagnostics
assess_convergence <- function(results) {
  # Gelman-Rubin diagnostic
  gelman_diag <- gelman.diag(results$samples)

  # Effective sample size
  effective_size <- effectiveSize(results$samples)

  # Create convergence summary
  convergence_summary <- data.frame(
    parameter = rownames(gelman_diag$psrf),
    psrf_point = gelman_diag$psrf[, 1],
    psrf_upper = gelman_diag$psrf[, 2],
    effective_sample_size = effective_size,
    converged = gelman_diag$psrf[, 1] < 1.1
  )

  # Save convergence assessment
  write.csv(convergence_summary, "convergence_diagnostics.csv")

  return(convergence_summary)
}

# Assess convergence
convergence_diag <- assess_convergence(nma_results$results)

# Generate comprehensive results summary
create_results_summary <- function() {
  summary <- list(
    network_characteristics = list(
      n_studies = length(unique(network$data.re$study)),
      n_treatments = length(unique(network$data.re$treatment)),
      n_participants = sum(network$data.re$sampleSize),
      n_comparisons = nrow(network$data.re) / 2
    ),

    model_fit = list(
      dic = dic(nma_results$results),
      deviance = nma_results$results$deviance,
      pD = nma_results$results$pD
    ),

    heterogeneity = hetero_assessment,
    convergence = convergence_diag,
    treatment_rankings = rank_results,
    relative_effects = relative_effects
  )

  # Save comprehensive summary
  saveRDS(summary, "comprehensive_nma_results.rds")

  return(summary)
}

# Create comprehensive results
final_summary <- create_results_summary()

# Print summary to console
print("=== CVD Primary Prevention NMA Results Summary ===")
print(paste("Number of studies:", final_summary$network_characteristics$n_studies))
print(paste("Number of treatments:", final_summary$network_characteristics$n_treatments))
print(paste("Total participants:", final_summary$network_characteristics$n_participants))
print(paste("Heterogeneity (tau):", round(final_summary$heterogeneity$median, 3)))
print("Treatment rankings (SUCRA):")
rank_df <- as.data.frame(final_summary$treatment_rankings)
rank_df$sucra <- apply(rank_df[, 1:(ncol(rank_df)-1)], 1, function(x) sum(x * seq(0, 1, length.out = ncol(rank_df)-1)))
print(rank_df[order(rank_df$sucra, decreasing = TRUE), c("sucra")])

# Save session info for reproducibility
writeLines(capture.output(sessionInfo()), "session_info.txt")

print("Bayesian NMA completed successfully!")
print("Results saved to:")
print("- comprehensive_nma_results.rds")
print("- league_table.csv")
print("- sucra_rankings.png")
print("- network_geometry.png")
print("- convergence_diagnostics.csv")
print("- heterogeneity_assessment.csv")
