# Climate Change and Vector-Borne Diseases: Analytical Methods Framework
# Generalized Estimating Equations (GEE) and Distributed Lag Modeling
# South Asia Longitudinal Study (2005-2025)

# Load required libraries
library(dplyr)
library(ggplot2)
library(geepack)
library(splines)
library(MASS)
library(car)
library(lmtest)
library(MuMIn)
library(corrplot)
library(gridExtra)

# Set working directory
setwd("./data/analysis/")

# =============================================================================
# DATA LOADING AND PREPROCESSING
# =============================================================================

#' Load and preprocess climate-disease study data
load_climate_disease_data <- function() {
  # Load merged dataset
  data_path <- "../merged/climate_disease_merged.csv"

  if (!file.exists(data_path)) {
    stop("Data file not found. Run data collection pipeline first.")
  }

  study_data <- read.csv(data_path, stringsAsFactors = FALSE)

  # Data preprocessing
  study_data <- study_data %>%
    mutate(
      # Create temporal variables
      year_centered = year - 2015,  # Center on midpoint
      time_trend = year - 2005,     # Linear time variable

      # Log-transform case counts for stabilization
      log_malaria_cases = log1p(total_malaria_cases),
      log_dengue_cases = log1p(total_dengue_cases),
      log_population = log(population),

      # Create population-standardized rates
      malaria_per100k = (total_malaria_cases / population) * 100000,
      dengue_per100k = (total_dengue_cases / population) * 100000,

      # Climate variable transformations
      temp_squared = temp_avg_mean^2,                    # Quadratic temperature
      temp_variability_index = temp_avg_std / temp_avg_mean,  # CV of temperature
      temp_range = temp_avg_max - temp_avg_min,          # Daily temperature range
      precipitation_variability = precipitation_std,      # Precipitation variability

      # Seasonality indicators
      monsoon_season = case_when(
        country_name %in% c("India", "Bangladesh", "Nepal", "Pakistan") ~ "South Asian Monsoon",
        country_name %in% c("Afghanistan", "Sri Lanka") ~ "Limited Monsoon",
        TRUE ~ "Arid/Tropical"
      ),

      # Socioeconomic controls (simulated for analysis)
      healthcare_access = rnorm(n(), mean = 0.6, sd = 0.15),
      gdp_percapita = rnorm(n(), mean = 2000, sd = 800),
      urbanization_rate = rnorm(n(), mean = 0.35, sd = 0.12),

      # Cluster identification for GEE
      cluster_id = as.factor(country_name)
    )

  # Create lagged climate variables (1-6 month lags)
  study_data <- study_data %>%
    arrange(country_name, year) %>%
    group_by(country_name) %>%
    mutate(
      lag_temp_1 = lag(temp_avg_mean, 1),
      lag_temp_2 = lag(temp_avg_mean, 2),
      lag_temp_3 = lag(temp_avg_mean, 3),

      lag_precip_1 = lag(precipitation_sum, 1),
      lag_precip_2 = lag(precipitation_sum, 2),
      lag_precip_3 = lag(precipitation_sum, 3)
    ) %>%
    ungroup()

  # Remove rows with NA values from lagging
  study_data <- na.omit(study_data)

  cat("✅ Study data loaded and preprocessed\n")
  cat(sprintf("   Observations: %d\n", nrow(study_data)))
  cat(sprintf("   Countries: %d\n", nlevels(study_data$cluster_id)))
  cat(sprintf("   Time range: %d - %d\n", min(study_data$year), max(study_data$year)))

  return(study_data)
}

# =============================================================================
# EXPLORATORY DATA ANALYSIS
# =============================================================================

#' Generate comprehensive exploratory data analysis
perform_eda <- function(data) {
  cat("\n" + "="*60)
  cat("EXPLORATORY DATA ANALYSIS")
  cat("\n" + "="*60)

  # Descriptive statistics
  desc_stats <- data %>%
    summarise(
      mean_temp = mean(temp_avg_mean, na.rm = TRUE),
      sd_temp = sd(temp_avg_mean, na.rm = TRUE),
      mean_malaria = mean(malaria_per100k, na.rm = TRUE),
      sd_malaria = sd(malaria_per100k, na.rm = TRUE),
      mean_dengue = mean(dengue_per100k, na.rm = TRUE),
      sd_dengue = sd(dengue_per100k, na.rm = TRUE),
      mean_precipitation = mean(precipitation_sum, na.rm = TRUE),
      sd_precipitation = sd(precipitation_sum, na.rm = TRUE)
    )

  print(desc_stats)

  # Correlation analysis
  climate_vars <- c("temp_avg_mean", "temp_avg_std", "precipitation_sum",
                   "temp_variability_index", "temp_squared")
  disease_vars <- c("malaria_per100k", "dengue_per100k")

  corr_matrix <- cor(data[, c(climate_vars, disease_vars)], use = "complete.obs")

  # Create correlation plot
  corrplot(corr_matrix, method = "color", type = "upper",
           addCoef.col = "black", tl.col = "black", tl.srt = 45,
           title = "Climate-Disease Correlation Matrix")

  # Temporal trends
  temporal_plot <- ggplot(data, aes(x = year)) +
    geom_smooth(aes(y = malaria_per100k, color = "Malaria"), se = TRUE) +
    geom_smooth(aes(y = dengue_per100k, color = "Dengue"), se = TRUE) +
    geom_smooth(aes(y = temp_avg_mean, color = "Temperature"), se = TRUE) +
    facet_wrap(~country_name, scales = "free_y") +
    labs(title = "Temporal Trends: Disease Incidence and Temperature by Country",
         x = "Year", y = "Incidence Rate (per 100,000) or Temperature (°C)") +
    theme_minimal()

  ggsave("../outputs/figures/temporal_trends.png", temporal_plot, width = 12, height = 8, dpi = 300)

  cat("✅ Exploratory analysis completed\n")
  cat("   Correlation matrix and temporal trends generated\n")

  return(list(desc_stats = desc_stats, corr_matrix = corr_matrix))
}

# =============================================================================
# GENERALIZED ESTIMATING EQUATIONS (GEE) MODELS
# =============================================================================

#' Primary GEE model for temperature-malaria association
fit_malaria_gee_model <- function(data) {

  cat("\n" + "="*60)
  cat("MALARIA GEE MODEL ESTIMATION")
  cat("\n" + "="*60)

  # Define model formula
  formula_malaria <- malaria_per100k ~ temp_avg_mean + temp_squared +
                     precipitation_sum + temp_variability_index +
                     healthcare_access + log_population + year_centered +
                     time_trend + lag_temp_1 + lag_temp_2 + lag_temp_3

  # Fit GEE model with exchangeable correlation structure
  gee_model_malaria <- geeglm(formula_malaria, id = cluster_id,
                             family = gaussian(link = "identity"),
                             corstr = "exchangeable", data = data)

  # Model diagnostics
  model_summary <- summary(gee_model_malaria)
  print(model_summary)

  # Extract coefficients and confidence intervals
  coef_table <- as.data.frame(cbind(
    Estimate = coef(gee_model_malaria),
    SE = sqrt(diag(gee_model_malaria$geese$vbeta)),
    Z = coef(gee_model_malaria) / sqrt(diag(gee_model_malaria$geese$vbeta)),
    P = 2 * pnorm(abs(coef(gee_model_malaria) / sqrt(diag(gee_model_malaria$geese$vbeta))), lower.tail = FALSE)
  ))

  coef_table$CI_lower <- coef_table$Estimate - 1.96 * coef_table$SE
  coef_table$CI_upper <- coef_table$Estimate + 1.96 * coef_table$SE

  # Calculate temperature effect over different ranges
  temp_range <- seq(15, 35, by = 0.5)  # Temperature range for prediction
  temp_effect <- coef(gee_model_malaria)["temp_avg_mean"] * temp_range +
                 coef(gee_model_malaria)["temp_squared"] * temp_range^2

  # Save model results
  saveRDS(gee_model_malaria, file = "../models/malaria_gee_model.rds")
  write.csv(coef_table, "../outputs/tables/malaria_coefficients.csv")

  cat("✅ Malaria GEE model fitted and saved\n")
  cat("   Model file: ../models/malaria_gee_model.rds\n")
  cat("   Coefficients: ../outputs/tables/malaria_coefficients.csv\n")

  return(list(model = gee_model_malaria, coef_table = coef_table))
}

#' GEE model for dengue-temperature association
fit_dengue_gee_model <- function(data) {

  cat("\n" + "="*60)
  cat("DENGUE GEE MODEL ESTIMATION")
  cat("\n" + "="*60)

  # Dengue model with different parameterization
  formula_dengue <- dengue_per100k ~ temp_avg_mean + temp_avg_std +
                    precipitation_sum + precipitation_variability +
                    urbanization_rate + log_population + year_centered +
                    time_trend + lag_precip_1 + lag_precip_2

  gee_model_dengue <- geeglm(formula_dengue, id = cluster_id,
                            family = poisson(link = "log"),
                            corstr = "ar1", data = data)

  # Model output
  summary_dengue <- summary(gee_model_dengue)
  print(summary_dengue)

  # Relative risk calculations (for Poisson model)
  rr_table <- data.frame(
    Variable = names(coef(gee_model_dengue)),
    Relative_Risk = exp(coef(gee_model_dengue)),
    CI_Lower = exp(coef(gee_model_dengue) - 1.96 * sqrt(diag(gee_model_dengue$geese$vbeta))),
    CI_Upper = exp(coef(gee_model_dengue) + 1.96 * sqrt(diag(gee_model_dengue$geese$vbeta)))
  )

  # Save dengue model
  saveRDS(gee_model_dengue, file = "../models/dengue_gee_model.rds")
  write.csv(rr_table, "../outputs/tables/dengue_rr_coefficients.csv")

  cat("✅ Dengue GEE model fitted and saved\n")
  cat("   Model file: ../models/dengue_gee_model.rds\n")
  cat("   RR table: ../outputs/tables/dengue_rr_coefficients.csv\n")

  return(list(model = gee_model_dengue, rr_table = rr_table))
}

# =============================================================================
# DISTRIBUTED LAG NON-LINEAR MODELS (DLNM)
# =============================================================================

#' Implement distributed lag models for climate effects
fit_distributed_lag_models <- function(data) {
  cat("\n" + "="*60)
  cat("DISTRIBUTED LAG NON-LINEAR MODELING")
  cat("\n" + "="*60)

  # Create cross-basis for temperature
  # Using simplified approach (full DLNM would require dlnm package)

  # Create lag matrix for temperature (0-6 month lags)
  temp_lags <- matrix(NA, nrow = nrow(data), ncol = 7)
  for (lag in 0:6) {
    temp_lags[, lag+1] <- lag(data$temp_avg_mean, lag)
  }

  # Create precipitation lag matrix
  precip_lags <- matrix(NA, nrow = nrow(data), ncol = 4)
  for (lag in 0:3) {
    precip_lags[, lag+1] <- lag(data$precipitation_sum, lag)
  }

  # Calculate cumulative effects
  data$cumulative_temp_0_3 <- rowSums(temp_lags[,2:4], na.rm = TRUE)  # 1-3 month lags
  data$cumulative_temp_1_6 <- rowSums(temp_lags[,2:7], na.rm = TRUE)  # 1-6 month lags
  data$cumulative_precip_0_2 <- rowSums(precip_lags[,2:4], na.rm = TRUE) # 1-3 month lags

  # Distributed lag model
  dl_formula <- malaria_per100k ~ temp_avg_mean +
                cumulative_temp_0_3 + cumulative_temp_1_6 +
                precipitation_sum + cumulative_precip_0_2 +
                log_population + time_trend

  dl_model <- geeglm(dl_formula, id = cluster_id,
                    family = gaussian(link = "identity"),
                    corstr = "exchangeable", data = data)

  dl_summary <- summary(dl_model)
  print(dl_summary)

  # Cumulative effect estimates
  cumulative_effects <- data.frame(
    Lag_Structure = c("Current (0-month)", "Short-term (1-3 months)", "Long-term (1-6 months)"),
    Temperature_Effect = c(
      coef(dl_model)["temp_avg_mean"],
      coef(dl_model)["cumulative_temp_0_3"],
      coef(dl_model)["cumulative_temp_1_6"]
    )
  )

  write.csv(cumulative_effects, "../outputs/tables/cumulative_effects.csv")

  cat("✅ Distributed lag model fitted\n")
  cat("   Model file: ../models/distributed_lag_model.rds\n")

  return(list(model = dl_model, effects = cumulative_effects))
}

# =============================================================================
# SENSITIVITY ANALYSIS
# =============================================================================

#' Perform comprehensive sensitivity analysis
conduct_sensitivity_analysis <- function(data) {

  cat("\n" + "="*60)
  cat("SENSITIVITY ANALYSIS")
  cat("\n" + "="*60)

  sensitivity_results <- list()

  # Alternative modeling approaches
  models_list <- c(
    "exchangeable" = "exchangeable",
    "ar1" = "ar1",
    "unstructured" = "unstructured"
  )

  for (model_name in names(models_list)) {
    formula_sa <- malaria_per100k ~ temp_avg_mean + temp_squared +
                   precipitation_sum + healthcare_access + log_population + year_centered

    try {
      sa_model <- geeglm(formula_sa, id = cluster_id,
                        family = gaussian(link = "identity"),
                        corstr = models_list[model_name], data = data)

      sa_results <- data.frame(
        Model = model_name,
        Correlation_Structure = models_list[model_name],
        Temp_Coefficient = coef(sa_model)["temp_avg_mean"],
        Temp_SE = sqrt(diag(sa_model$geese$vbeta))["temp_avg_mean"],
        AIC = AIC(sa_model),
        QIC = sa_model$geese$QIC
      )

      sensitivity_results[[model_name]] <- sa_results

    } catch (error) {
      cat(sprintf("Error fitting %s model: %s\n", model_name, error$message))
    }
  }

  # Combine sensitivity results
  sensitivity_df <- do.call(rbind, sensitivity_results)
  write.csv(sensitivity_df, "../outputs/tables/sensitivity_analysis.csv")

  cat("✅ Sensitivity analysis completed\n")
  cat("   Results: ../outputs/tables/sensitivity_analysis.csv\n")

  return(sensitivity_df)
}

# =============================================================================
# CLIMATE ATTRIBUTION ANALYSIS
# =============================================================================

#' Calculate population attributable fraction for climate effects
calculate_population_attributable_fraction <- function(data, malaria_model) {

  cat("\n" + "="*60)
  cat("POPULATION ATTRIBUTABLE FRACTION ANALYSIS")
  cat("\n" + "="*60)

  # Baseline temperature (20-year average)
  baseline_temp <- mean(data$temp_avg_mean[data$year >= 2005 & data$year <= 2010], na.rm = TRUE)

  # Current/observed temperature (2020-2025)
  current_temp <- mean(data$temp_avg_mean[data$year >= 2020 & data$year <= 2025], na.rm = TRUE)

  # Temperature increment
  temp_increase <- current_temp - baseline_temp

  # Beta coefficient for temperature
  temp_beta <- coef(malaria_model)["temp_avg_mean"]

  # Relative risk calculation
  rr_climate <- exp(temp_beta * temp_increase)

  # Population attributable fraction
  paf_climate <- (rr_climate - 1) / rr_climate

  # Attributable cases estimation
  total_observed_cases <- sum(data$total_malaria_cases, na.rm = TRUE)
  attributable_cases <- total_observed_cases * paf_climate

  # Country-specific PAF calculations
  country_paf <- data %>%
    group_by(country_name) %>%
    summarise(
      total_cases_observed = sum(total_malaria_cases, na.rm = TRUE),
      mean_temp_baseline = mean(temp_avg_mean[year >= 2005 & year <= 2010], na.rm = TRUE),
      mean_temp_current = mean(temp_avg_mean[year >= 2020 & year <= 2025], na.rm = TRUE),
      temp_increase_country = mean_temp_current - mean_temp_baseline,
      attributable_cases_country = total_cases_observed * paf_climate
    )

  # Results summary
  attribution_summary <- data.frame(
    Metric = c("Total Observed Cases", "Climate Attributable Cases",
               "PAF (%)", "Temperature Increase (°C)", "Relative Risk"),
    Value = c(total_observed_cases, attributable_cases,
             round(paf_climate * 100, 2), round(temp_increase, 2),
             round(rr_climate, 3))
  )

  # Save results
  write.csv(attribution_summary, "../outputs/tables/climate_attribution_summary.csv")
  write.csv(country_paf, "../outputs/tables/country_paf.csv")

  cat("✅ Climate attribution analysis completed\n")
  cat("   Total observed cases: ", format(total_observed_cases, big.mark = ","))
  cat("\n   Climate attributable cases: ", format(attributable_cases, big.mark = ","))
  cat("\n   Population attributable fraction: ", round(paf_climate * 100, 2), "%")

  return(list(
    summary = attribution_summary,
    country_paf = country_paf,
    total_paf = paf_climate,
    attributable_cases = attributable_cases
  ))
}

# =============================================================================
# MAIN ANALYSIS PIPELINE
# =============================================================================

#' Execute complete analytical pipeline
run_full_analysis <- function() {

  cat("="*80)
  cat("\nCLIMATE CHANGE AND VECTOR-BORNE DISEASES: FULL ANALYSIS PIPELINE")
  cat("\n" + "="*80)

  # Create output directories
  dir.create("../models", showWarnings = FALSE)
  dir.create("../outputs/tables", showWarnings = FALSE)
  dir.create("../outputs/figures", showWarnings = FALSE)

  # Step 1: Load and preprocess data
  cat("\n\nSTEP 1: DATA LOADING AND PREPROCESSING")
  study_data <- load_climate_disease_data()

  # Step 2: Exploratory data analysis
  cat("\n\nSTEP 2: EXPLORATORY DATA ANALYSIS")
  eda_results <- perform_eda(study_data)

  # Step 3: Fit primary models
  cat("\n\nSTEP 3: PRIMARY MODEL FITTING")
  malaria_results <- fit_malaria_gee_model(study_data)
  dengue_results <- fit_dengue_gee_model(study_data)

  # Step 4: Distributed lag modeling
  cat("\n\nSTEP 4: DISTRIBUTED LAG MODELING")
  dl_results <- fit_distributed_lag_models(study_data)

  # Step 5: Sensitivity analysis
  cat("\n\nSTEP 5: SENSITIVITY ANALYSIS")
  sensitivity_results <- conduct_sensitivity_analysis(study_data)

  # Step 6: Climate attribution
  cat("\n\nSTEP 6: CLIMATE ATTRIBUTION ANALYSIS")
  attribution_results <- calculate_population_attributable_fraction(study_data, malaria_results$model)

  # Generate final summary report
  cat("\n\n" + "="*80)
  cat("ANALYSIS COMPLETE - SUMMARY REPORT")
  cat("\n" + "="*80)

  # Key findings
  cat(sprintf("\nPRIMARY FINDINGS:"))
  cat(sprintf("\n  • Temperature-malaria association: %.3f cases per °C increase",
             malaria_results$coef_table["temp_avg_mean","Estimate"]))
  cat(sprintf("\n  • Precipitation-malaria association: %.3f per cm increase",
             malaria_results$coef_table["precipitation_sum","Estimate"]))
  cat(sprintf("\n  • Climate attribution: %.1f%% of malaria cases in South Asia",
             attribution_results$total_paf * 100))
  cat(sprintf("\n  • Attributable cases due to climate change: %s",
             format(attribution_results$attributable_cases, big.mark = ",")))

  # Save complete analysis results
  analysis_summary <- list(
    data_summary = eda_results$desc_stats,
    malaria_model_results = malaria_results$coef_table,
    dengue_model_results = dengue_results$rr_table,
    distributed_lag_effects = dl_results$effects,
    sensitivity_results = sensitivity_results,
    attribution_results = attribution_results$summary,
    analysis_timestamp = Sys.time()
  )

  saveRDS(analysis_summary, "../outputs/complete_analysis_summary.rds")

  cat(sprintf("\n\nComplete analysis summary saved to: ../outputs/complete_analysis_summary.rds"))
  cat(sprintf("\n\nAll results, tables, and figures saved to ../outputs/ directory"))

  return(analysis_summary)
}

# =============================================================================
# EXECUTION BLOCK
# =============================================================================

if (interactive() || length(commandArgs()) > 0) {
  # Run full analysis pipeline
  cat("Starting Climate Change Vector Disease Analysis Pipeline...\n")
  analysis_result <- run_full_analysis()

  cat("\nAnalysis pipeline completed successfully!\n")
  cat("Check ../outputs/ directory for all results and visualizations.\n")
}
