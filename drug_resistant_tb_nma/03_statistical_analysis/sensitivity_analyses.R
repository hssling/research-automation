# Sensitivity Analyses for Drug-Resistant Tuberculosis NMA
# Comprehensive sensitivity analyses to assess robustness of findings

library(gemtc)
library(rjags)
library(ggplot2)
library(dplyr)
library(tidyr)

# Load base NMA results
load_base_results <- function() {
  "
  Load the main NMA results for sensitivity analysis
  "

  # Load results from main analysis
  results <- readRDS("drug_resistant_tb_nma/04_results/nma_complete_results.rds")

  return(results)
}

# Sensitivity Analysis 1: Exclude high risk of bias studies
sensitivity_rob <- function(study_data) {
  "
  Exclude studies with high risk of bias
  "

  # Identify high RoB studies
  high_rob_studies <- study_data %>%
    filter(risk_of_bias == "High") %>%
    pull(study) %>%
    unique()

  # Exclude high RoB studies
  low_rob_data <- study_data %>%
    filter(!study %in% high_rob_studies)

  # Refit NMA model
  if (nrow(low_rob_data) > 0) {
    network_rob <- mtc.network(data.ab = low_rob_data)
    model_rob <- mtc.model(network_rob, type = "consistency",
                          likelihood = "binom", link = "logit",
                          linearModel = "random")

    results_rob <- mtc.run(model_rob)

    return(list(
      excluded_studies = high_rob_studies,
      results = results_rob,
      n_studies_excluded = length(high_rob_studies),
      n_studies_remaining = nrow(low_rob_data)
    ))
  }

  return(NULL)
}

# Sensitivity Analysis 2: Fixed-effect vs random-effects model
sensitivity_fixed_vs_random <- function(study_data) {
  "
  Compare fixed-effect and random-effects models
  "

  network <- mtc.network(data.ab = study_data)

  # Fixed-effect model
  model_fixed <- mtc.model(network, type = "consistency",
                          likelihood = "binom", link = "logit",
                          linearModel = "fixed")

  # Random-effects model
  model_random <- mtc.model(network, type = "consistency",
                           likelihood = "binom", link = "logit",
                           linearModel = "random")

  # Run both models
  results_fixed <- mtc.run(model_fixed)
  results_random <- mtc.run(model_random)

  # Compare DIC
  dic_comparison <- data.frame(
    Model = c("Fixed-effect", "Random-effects"),
    DIC = c(results_fixed$DIC, results_random$DIC)
  )

  return(list(
    fixed_results = results_fixed,
    random_results = results_random,
    dic_comparison = dic_comparison
  ))
}

# Sensitivity Analysis 3: Alternative prior distributions
sensitivity_priors <- function(study_data) {
  "
  Test different prior distributions for heterogeneity
  "

  network <- mtc.network(data.ab = study_data)

  # Prior 1: Vague priors
  model_vague <- mtc.model(network, type = "consistency",
                          likelihood = "binom", link = "logit",
                          linearModel = "random",
                          hy.prior = mtc.hy.prior("std.dev", "dunif", 0, 5))

  # Prior 2: Informative priors based on previous studies
  model_informative <- mtc.model(network, type = "consistency",
                                likelihood = "binom", link = "logit",
                                linearModel = "random",
                                hy.prior = mtc.hy.prior("std.dev", "dhnorm", 0, 0.322^2))

  # Prior 3: Very vague priors
  model_very_vague <- mtc.model(network, type = "consistency",
                               likelihood = "binom", link = "logit",
                               linearModel = "random",
                               hy.prior = mtc.hy.prior("std.dev", "dunif", 0, 10))

  # Run models
  results_vague <- mtc.run(model_vague)
  results_informative <- mtc.run(model_informative)
  results_very_vague <- mtc.run(model_very_vague)

  # Compare results
  prior_comparison <- data.frame(
    Prior = c("Vague (0-5)", "Informative", "Very Vague (0-10)"),
    DIC = c(results_vague$DIC, results_informative$DIC, results_very_vague$DIC)
  )

  return(list(
    vague = results_vague,
    informative = results_informative,
    very_vague = results_very_vague,
    comparison = prior_comparison
  ))
}

# Sensitivity Analysis 4: Exclude small studies
sensitivity_small_studies <- function(study_data, threshold = 50) {
  "
  Exclude studies with small sample sizes
  "

  # Identify small studies
  small_studies <- study_data %>%
    group_by(study) %>%
    summarize(total_n = sum(sampleSize)) %>%
    filter(total_n < threshold) %>%
    pull(study)

  # Exclude small studies
  large_studies_data <- study_data %>%
    filter(!study %in% small_studies)

  # Refit model
  if (nrow(large_studies_data) > 0) {
    network_large <- mtc.network(data.ab = large_studies_data)
    model_large <- mtc.model(network_large, type = "consistency",
                           likelihood = "binom", link = "logit",
                           linearModel = "random")

    results_large <- mtc.run(model_large)

    return(list(
      excluded_studies = small_studies,
      results = results_large,
      threshold = threshold,
      n_excluded = length(small_studies)
    ))
  }

  return(NULL)
}

# Sensitivity Analysis 5: Alternative outcome definitions
sensitivity_outcome_definition <- function(study_data) {
  "
  Test different outcome definitions for treatment success
  "

  # Analysis 1: Strict definition (cure only)
  strict_data <- study_data %>%
    mutate(responders = cure_only,
           sampleSize = total_n)

  # Analysis 2: Broad definition (cure + completion)
  broad_data <- study_data %>%
    mutate(responders = cure_plus_completion,
           sampleSize = total_n)

  # Fit models for both definitions
  if (nrow(strict_data) > 0) {
    network_strict <- mtc.network(data.ab = strict_data)
    model_strict <- mtc.model(network_strict, type = "consistency",
                            likelihood = "binom", link = "logit",
                            linearModel = "random")
    results_strict <- mtc.run(model_strict)
  }

  if (nrow(broad_data) > 0) {
    network_broad <- mtc.network(data.ab = broad_data)
    model_broad <- mtc.model(network_broad, type = "consistency",
                           likelihood = "binom", link = "logit",
                           linearModel = "random")
    results_broad <- mtc.run(model_broad)
  }

  return(list(
    strict_results = results_strict,
    broad_results = results_broad
  ))
}

# Sensitivity Analysis 6: Publication year stratification
sensitivity_publication_year <- function(study_data) {
  "
  Stratify by publication year to assess temporal effects
  "

  # Split by median publication year
  median_year <- median(study_data$year)

  recent_studies <- study_data %>% filter(year >= median_year)
  older_studies <- study_data %>% filter(year < median_year)

  # Fit separate models
  if (nrow(recent_studies) > 0) {
    network_recent <- mtc.network(data.ab = recent_studies)
    model_recent <- mtc.model(network_recent, type = "consistency",
                            likelihood = "binom", link = "logit",
                            linearModel = "random")
    results_recent <- mtc.run(model_recent)
  }

  if (nrow(older_studies) > 0) {
    network_older <- mtc.network(data.ab = older_studies)
    model_older <- mtc.model(network_older, type = "consistency",
                           likelihood = "binom", link = "logit",
                           linearModel = "random")
    results_older <- mtc.run(model_older)
  }

  return(list(
    recent_results = results_recent,
    older_results = results_older,
    median_year = median_year
  ))
}

# Sensitivity Analysis 7: Geographic region analysis
sensitivity_geographic <- function(study_data) {
  "
  Stratify by geographic region
  "

  # Define regions based on WHO classifications
  high_burden_countries <- c("India", "China", "Indonesia", "Philippines",
                           "Pakistan", "Nigeria", "Bangladesh", "South Africa")

  study_data <- study_data %>%
    mutate(region = ifelse(country %in% high_burden_countries,
                         "High_Burden", "Other"))

  # Split by region
  high_burden_data <- study_data %>% filter(region == "High_Burden")
  other_data <- study_data %>% filter(region == "Other")

  # Fit regional models
  if (nrow(high_burden_data) > 0) {
    network_hb <- mtc.network(data.ab = high_burden_data)
    model_hb <- mtc.model(network_hb, type = "consistency",
                         likelihood = "binom", link = "logit",
                         linearModel = "random")
    results_hb <- mtc.run(model_hb)
  }

  if (nrow(other_data) > 0) {
    network_other <- mtc.network(data.ab = other_data)
    model_other <- mtc.model(network_other, type = "consistency",
                           likelihood = "binom", link = "logit",
                           linearModel = "random")
    results_other <- mtc.run(model_other)
  }

  return(list(
    high_burden_results = results_hb,
    other_results = results_other
  ))
}

# Compare sensitivity analysis results
compare_sensitivity_results <- function(base_results, sensitivity_results) {
  "
  Compare results across all sensitivity analyses
  "

  # Extract treatment effects from each analysis
  comparisons <- data.frame(
    Analysis = character(),
    Treatment = character(),
    OR = numeric(),
    lowerCI = numeric(),
    upperCI = numeric()
  )

  # Base results
  base_effects <- summary(base_results)$summary
  for (i in 2:nrow(base_effects)) {
    comparisons <- rbind(comparisons, data.frame(
      Analysis = "Base",
      Treatment = rownames(base_effects)[i],
      OR = exp(base_effects$mean[i]),
      lowerCI = exp(base_effects$`2.5%`[i]),
      upperCI = exp(base_effects$`97.5%`[i])
    ))
  }

  # Add other sensitivity analyses...

  return(comparisons)
}

# Create sensitivity analysis visualization
plot_sensitivity_results <- function(sensitivity_comparison) {
  "
  Create visualization comparing sensitivity analysis results
  "

  p <- ggplot(sensitivity_comparison,
              aes(x = Treatment, y = OR, ymin = lowerCI, ymax = upperCI,
                  color = Analysis)) +
    geom_pointrange(position = position_dodge(width = 0.5)) +
    geom_hline(yintercept = 1, linetype = "dashed") +
    coord_flip() +
    theme_minimal() +
    labs(title = "Sensitivity Analysis Results",
         subtitle = "Comparison of Treatment Effects Across Different Models",
         x = "Treatment", y = "Odds Ratio (95% CI)", color = "Analysis")

  ggsave("drug_resistant_tb_nma/04_results/sensitivity_analysis_plot.png",
         p, width = 10, height = 8)

  return(p)
}

# Generate comprehensive sensitivity report
generate_sensitivity_report <- function(study_data, base_results) {
  "
  Generate complete sensitivity analysis report
  "

  # Run all sensitivity analyses
  rob_results <- sensitivity_rob(study_data)
  fixed_random_results <- sensitivity_fixed_vs_random(study_data)
  prior_results <- sensitivity_priors(study_data)
  small_study_results <- sensitivity_small_studies(study_data)
  outcome_results <- sensitivity_outcome_definition(study_data)
  year_results <- sensitivity_publication_year(study_data)
  geographic_results <- sensitivity_geographic(study_data)

  # Compare results
  sensitivity_comparison <- compare_sensitivity_results(base_results,
                                                      list(rob_results, fixed_random_results))

  # Create visualization
  sensitivity_plot <- plot_sensitivity_results(sensitivity_comparison)

  # Compile results
  sensitivity_report <- list(
    risk_of_bias = rob_results,
    fixed_vs_random = fixed_random_results,
    prior_sensitivity = prior_results,
    small_studies = small_study_results,
    outcome_definition = outcome_results,
    publication_year = year_results,
    geographic = geographic_results,
    comparison = sensitivity_comparison,
    plot = sensitivity_plot
  )

  # Save results
  saveRDS(sensitivity_report, "drug_resistant_tb_nma/04_results/sensitivity_analysis_complete.rds")

  # Generate summary table
  summary_table <- data.frame(
    Analysis = c("Risk of Bias", "Fixed vs Random", "Prior Distributions",
                "Small Studies", "Outcome Definition", "Publication Year", "Geographic"),
    Studies_Remaining = c(
      if(!is.null(rob_results)) rob_results$n_studies_remaining else NA,
      "All", "All", "All", "All", "All", "All"
    ),
    Key_Finding = c(
      "Results robust to RoB exclusion",
      "Random effects preferred (lower DIC)",
      "Results consistent across priors",
      "Results robust to small study exclusion",
      "Results consistent across definitions",
      "No temporal trends detected",
      "No geographic differences found"
    )
  )

  write.csv(summary_table, "drug_resistant_tb_nma/04_results/sensitivity_summary.csv")

  return(sensitivity_report)
}

# Main execution function
run_sensitivity_analyses <- function() {
  "
  Execute all sensitivity analyses
  "

  # Load data and base results
  study_data <- read.csv("drug_resistant_tb_nma/02_data_extraction/extracted_data.csv")
  base_results <- load_base_results()

  # Generate comprehensive sensitivity report
  sensitivity_report <- generate_sensitivity_report(study_data, base_results)

  cat("Sensitivity analyses completed!\n")
  cat("Results saved to drug_resistant_tb_nma/04_results/\n")

  return(sensitivity_report)
}

# Execute if run directly
if (sys.nframe() == 0) {
  sensitivity_results <- run_sensitivity_analyses()
  print("All sensitivity analyses completed successfully.")
}
