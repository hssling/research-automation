# Climate Change and Vector-Borne Diseases: Climate Attribution Analysis
# Quantifying Climate Change Contribution to Disease Burden
# Population Attributable Fraction (PAF) Calculation and Counterfactual Modeling

# Load required libraries
library(dplyr)
library(ggplot2)
library(MASS)
library(boot)
library(lme4)
library(nlme)
library(quantreg)
library(scales)
library(gridExtra)
library(car)

# =============================================================================
# BASELINE TEMPERATURE ESTIMATION
# =============================================================================

#' Calculate baseline temperature for attribution analysis
calculate_baseline_temperature <- function(data, baseline_years = 2005:2010) {

  cat("🌡️ Calculating Baseline Temperature for Attribution Analysis...\n")

  # Extract baseline period data
  baseline_data <- data %>%
    filter(year %in% baseline_years)

  # Calculate mean baseline temperature by country
  baseline_temps <- baseline_data %>%
    group_by(country_name) %>%
    summarise(
      baseline_temp_mean = mean(temp_avg_mean, na.rm = TRUE),
      baseline_temp_sd = sd(temp_avg_mean, na.rm = TRUE),
      baseline_temp_min = min(temp_avg_mean, na.rm = TRUE),
      baseline_temp_max = max(temp_avg_mean, na.rm = TRUE),
      n_years_baseline = n()
    )

  # Overall baseline across all countries
  overall_baseline <- baseline_data %>%
    summarise(
      overall_baseline_temp = mean(temp_avg_mean, na.rm = TRUE),
      overall_baseline_sd = sd(temp_avg_mean, na.rm = TRUE),
      countries_included = n_distinct(country_name)
    )

  cat(sprintf("   Baseline period: %d-%d (%d years)\n",
              min(baseline_years), max(baseline_years),
              length(baseline_years)))
  cat(sprintf("   Overall baseline temperature: %.2f°C (±%.2f°C)\n",
              overall_baseline$overall_baseline_temp,
              overall_baseline$overall_baseline_sd))
  cat(sprintf("   Countries included: %d\n", overall_baseline$countries_included))

  return(list(
    country_baselines = baseline_temps,
    overall_baseline = overall_baseline,
    baseline_years = baseline_years
  ))
}

#' Calculate temperature change (exposure) for attribution
calculate_temperature_change <- function(data, baseline_temp) {

  cat("📊 Calculating Temperature Change Magnitude...\n")

  # Calculate year-by-year change from baseline
  data$temp_change_from_baseline <- data$temp_avg_mean - baseline_temp$overall_baseline_temp
  data$temp_change_percent <- (data$temp_change_from_baseline / baseline_temp$overall_baseline_temp) * 100

  # Calculate country-specific changes
  country_changes <- data %>%
    group_by(country_name, year) %>%
    summarise(
      temp_current = mean(temp_avg_mean, na.rm = TRUE),
      temp_change_country = temp_current - baseline_temp$overall_baseline_temp,
      temp_change_percent_country = (temp_change_country / baseline_temp$overall_baseline_temp) * 100
    )

  # Calculate annual trends
  annual_trends <- data %>%
    group_by(year) %>%
    summarise(
      avg_temp_regional = mean(temp_avg_mean, na.rm = TRUE),
      avg_temp_change = avg_temp_regional - baseline_temp$overall_baseline_temp,
      avg_temp_change_percent = (avg_temp_change / baseline_temp$overall_baseline_temp) * 100
    )

  cat(sprintf("   Current period temperature change:%.2f°C\n",
              tail(annual_trends$avg_temp_change, 1)))
  cat(sprintf("   Percent increase:%.1f%%\n",
              tail(annual_trends$avg_temp_change_percent, 1)))

  return(list(
    data_with_changes = data,
    country_changes = country_changes,
    annual_trends = annual_trends
  ))
}

# =============================================================================
# POPULATION ATTRIBUTABLE FRACTION (PAF) CALCULATION
# =============================================================================

#' Calculate Population Attributable Fraction using GEE model results
calculate_population_attributable_fraction <- function(model_results, temp_change, data) {

  cat("\n💰 Calculating Population Attributable Fraction (PAF)...\n")

  # Extract temperature coefficient from model
  temp_beta <- model_results$coef_table["temp_avg_mean", "Estimate"]
  temp_beta_se <- model_results$coef_table["temp_avg_mean", "SE"]

  # Calculate Relative Risk (RR) for observed temperature increase
  rr_observed <- exp(temp_beta * temp_change)

  # Population Attributable Fraction formula
  # PAF = (RR - 1) / RR * (cases attributable to exposure) / total cases
  paf_formula <- (rr_observed - 1) / rr_observed

  # Bootstrap confidence intervals for PAF
  set.seed(2025)
  paf_boot <- boot::boot(data.frame(temp_change = temp_change),
                        function(data, i) {
                          rr_boot <- exp(temp_beta * data[i, 1])
                          (rr_boot - 1) / rr_boot
                        }, R = 1000)

  paf_ci <- boot.ci(paf_boot, type = "perc")

  # Calculate attributable cases
  total_malaria_cases <- sum(data$total_malaria_cases, na.rm = TRUE)
  attributable_cases <- total_malaria_cases * paf_formula

  paf_results <- data.frame(
    Metric = c("Population Attributable Fraction (%)",
               "95% CI Lower Bound (%)",
               "95% CI Upper Bound (%)",
               "Relative Risk (observed temp change)",
               "Total Malaria Cases (2025)",
               "Climate Attributable Cases (2025)"),
    Value = c(
      sprintf("%.1f", paf_formula * 100),
      sprintf("%.1f", paf_ci$percent[4] * 100),
      sprintf("%.1f", paf_ci$percent[5] * 100),
      sprintf("%.3f", rr_observed),
      scales::comma(total_malaria_cases),
      scales::comma(attributable_cases)
    )
  )

  cat(sprintf("   PAF: %.1f%% (95%% CI: %.1f%% - %.1f%%)\n",
              paf_formula * 100, paf_ci$percent[4] * 100, paf_ci$percent[5] * 100))
  cat(sprintf("   Relative Risk: %.3f for observed temperature change\n", rr_observed))
  cat(sprintf("   Attributable cases: %s out of %s total cases\n",
              scales::comma(attributable_cases), scales::comma(total_malaria_cases)))

  return(list(
    paf_results = paf_results,
    paf_value = paf_formula,
    relative_risk = rr_observed,
    attributable_cases = attributable_cases,
    bootstrap_ci = paf_ci$percent
  ))
}

# =============================================================================
# COUNTERFACTUAL ANALYSIS - WHAT IF NO CLIMATE CHANGE?
# =============================================================================

#' Conduct counterfactual analysis (what if no climate change occurred?)
conduct_counterfactual_analysis <- function(data, baseline_temp, model_results) {

  cat("\n🔮 Conducting Counterfactual Analysis...\n")

  # Create counterfactual scenario: constant baseline temperature
  data_counterfactual <- data
  data_counterfactual$temp_counterfactual <- baseline_temp$overall_baseline_temp

  # Predict disease burden under counterfactual scenario
  temp_beta <- model_results$coef_table["temp_avg_mean", "Estimate"]

  # Actual disease burden
  data_counterfactual <- data_counterfactual %>%
    group_by(country_name, year) %>%
    mutate(
      predicted_actual = total_malaria_cases * exp(temp_beta * temp_change_from_baseline),
      predicted_counterfactual = total_malaria_cases * exp(0)  # No temperature change
    )

  # Aggregate results by year
  counterfactual_results <- data_counterfactual %>%
    group_by(year) %>%
    summarise(
      cases_actual = sum(predicted_actual, na.rm = TRUE),
      cases_counterfactual = sum(predicted_counterfactual, na.rm = TRUE),
      cases_attributable = sum(predicted_actual - predicted_counterfactual, na.rm = TRUE)
    )

  # Total attribution for 2025
  total_2025 <- counterfactual_results %>% filter(year == 2025)
  total_cases_prevented <- total_2025$cases_counterfactual - total_2025$cases_actual
  percent_reduction <- (total_cases_prevented / total_2025$cases_actual) * 100

  cat(sprintf("   If no climate change: %s malaria cases in 2025\n",
              scales::comma(total_2025$cases_counterfactual)))
  cat(sprintf("   Actual cases: %s\n", scales::comma(total_2025$cases_actual)))
  cat(sprintf("   Cases prevented by climate change prevention: %s (%.1f%%)\n",
              scales::comma(total_cases_prevented), percent_reduction))

  return(list(
    counterfactual_data = data_counterfactual,
    aggregate_results = counterfactual_results,
    total_cases_prevented = total_cases_prevented,
    percent_reduction = percent_reduction
  ))
}

# =============================================================================
# FUTURE PROJECTIONS UNDER DIFFERENT SCENARIOS
# =============================================================================

#' Project future disease burden under different temperature scenarios
project_future_burden <- function(data, model_results, future_years = 2026:2050) {

  cat("\n🔮 Projecting Future Disease Burden (2026-2050)...\n")

  # Climate change scenarios
  scenarios <- data.frame(
    year = rep(future_years, 3),
    scenario = rep(c("Low Warming (1.5°C)", "Medium Warming (2.5°C)", "High Warming (4.0°C)"),
                  each = length(future_years)),
    avg_temp_projection = c(
      seq(31.2, 33.1, length.out = length(future_years)),  # +1.8°C from 2025
      seq(31.2, 35.1, length.out = length(future_years)),  # +3.7°C from 2025
      seq(31.2, 37.0, length.out = length(future_years))   # +5.6°C from 2025
    )
  )

  # Extract model parameters
  temp_beta <- model_results$coef_table["temp_avg_mean", "Estimate"]
  baseline_temp <- mean(data[data$year == 2025,]$temp_avg_mean, na.rm = TRUE)

  # Calculate projections
  projections <- scenarios %>%
    mutate(
      temp_increase = avg_temp_projection - baseline_temp,
      relative_risk = exp(temp_beta * temp_increase),
      cases_projection = mean(data[data$year == 2025,]$total_malaria_cases) * relative_risk,
      attributable_cases = cases_projection - mean(data[data$year == 2025,]$total_malaria_cases)
    )

  # Summary by 2050
  projections_2050 <- projections %>% filter(year == 2050)

  cat("2050 Projections:\n")
  for (i in 1:nrow(projections_2050)) {
    cat(sprintf("   %s: %s additional malaria cases\n",
                projections_2050$scenario[i],
                scales::comma(abs(projections_2050$attributable_cases[i]))))
  }

  return(list(
    projections = projections,
    projections_2050 = projections_2050,
    model_coeffs = c(beta = temp_beta, baseline_temp = baseline_temp)
  ))
}

# =============================================================================
# ECONOMIC VALUATION FRAMEWORK
# =============================================================================

#' Calculate economic costs of climate-attributable disease burden
calculate_economic_attribution <- function(attributable_cases, economic_params = NULL) {

  cat("\n💰 Calculating Economic Burden of Climate-Attributed Disease...\n")

  # Default economic parameters per case
  if (is.null(economic_params)) {
    economic_params <- list(
      cost_per_outpatient_visit = 250,     # INR
      cost_per_inpatient_admission = 15000, # INR
      cost_per_death = 500000,            # INR (disability-adjusted life years)
      proportion_outpatient_only = 0.6,
      proportion_inpatient = 0.3,
      proportion_with_death = 0.1,
      productivity_loss_factor = 0.15     # % of GDP
    )
  }

  # Calculate costs per case type
  total_cost outpatient <- attributable_cases * economic_params$cost_per_outpatient_visit * economic_params$proportion_outpatient_only
  cost_inpatient <- attributable_cases * economic_params$cost_per_inpatient_admission * economic_params$proportion_inpatient
  cost_death <- attributable_cases * economic_params$cost_per_death * economic_params$proportion_with_death

  total_medical_cost <- cost_outpatient + cost_inpatient + cost_death
  productivity_cost <- total_medical_cost * economic_params$productivity_loss_factor

  total_economic_burden <- total_medical_cost + productivity_cost

  # Convert to USD (approximate)
  usd_conversion_rate <- 0.012  # INR to USD
  total_burden_usd <- total_economic_burden * usd_conversion_rate

  economic_summary <- data.frame(
    Cost_Component = c("Outpatient Care", "Inpatient Care", "Death-Related Costs",
                      "Medical Costs Total", "Productivity Losses", "Total Economic Burden"),
    Amount_INR_Crore = c(
      cost_outpatient / 1e7,
      cost_inpatient / 1e7,
      cost_death / 1e7,
      total_medical_cost / 1e7,
      productivity_cost / 1e7,
      total_economic_burden / 1e7
    ),
    Amount_USD_Million = c(
      (cost_outpatient * usd_conversion_rate) / 1e6,
      (cost_inpatient * usd_conversion_rate) / 1e6,
      (cost_death * usd_conversion_rate) / 1e6,
      (total_medical_cost * usd_conversion_rate) / 1e6,
      (productivity_cost * usd_conversion_rate) / 1e6,
      (total_burden_usd) / 1e6
    )
  )

  cat(sprintf("   Annual Economic Burden (attributable to climate change):\n"))
  cat(sprintf("   Medical Costs: ₹%.1f crore ($%.1f million)\n",
              total_medical_cost / 1e7, (total_medical_cost * usd_conversion_rate) / 1e6))
  cat(sprintf("   Productivity Losses: ₹%.1f crore ($%.1f million)\n",
              productivity_cost / 1e7, (productivity_cost * usd_conversion_rate) / 1e6))
  cat(sprintf("   Total Economic Burden: ₹%.1f crore ($%.1f million)\n",
              total_economic_burden / 1e7, total_burden_usd / 1e6))

  return(list(
    economic_summary = economic_summary,
    total_burden_inr = total_economic_burden,
    total_burden_usd = total_burden_usd,
    cost_breakdown = list(
      outpatient = cost_outpatient,
      inpatient = cost_inpatient,
      death = cost_death,
      productivity = productivity_cost
    )
  ))
}

# =============================================================================
# COMPREHENSIVE ATTRIBUTION DASHBOARD
# =============================================================================

#' Create comprehensive attribution dashboard
create_attribution_dashboard <- function(paf_results, counterfactual_results, future_projections, economic_results) {

  cat("\n📊 Creating Comprehensive Attribution Dashboard...\n")

  # Main attribution visualization
  attribution_plot <- ggplot(data.frame(
    category = c("Climate Attributable", "Other Factors"),
    proportion = c(paf_results$paf_value, 1 - paf_results$paf_value),
    cases = c(paf_results$attributable_cases, sum(study_data$total_malaria_cases) - paf_results$attributable_cases)
  )) +
    geom_bar(aes(x = "", y = proportion, fill = category), stat = "identity", width = 1) +
    coord_polar("y", start = 0) +
    scale_fill_manual(values = c("#E74C3C", "#95A5A6")) +
    labs(title = "Climate Attribution of Malaria Cases",
         subtitle = sprintf("%.1f%% of malaria cases attributable to climate change",
                           paf_results$paf_value * 100)) +
    theme_void() +
    theme(legend.title = element_blank())

  # Counterfactual scenarios over time
  counterfactual_plot <- ggplot(counterfactual_results$aggregate_results) +
    geom_line(aes(x = year, y = cases_actual / 1000, color = "Observed"), size = 1.5) +
    geom_line(aes(x = year, y = cases_counterfactual / 1000, color = "No Climate Change"),
              size = 1.5, linetype = "dashed") +
    labs(title = "Counterfactual Scenario Analysis",
         x = "Year", y = "Malaria Cases (Thousands)",
         caption = "Dashed line shows cases if no climate change occurred") +
    scale_color_manual(values = c("#E74C3C", "#2ECC71"))

  # Future projections by scenario
  future_plot <- ggplot(future_projections$projections) +
    geom_line(aes(x = year, y = attributable_cases / 1000, color = scenario), size = 1) +
    geom_point(aes(x = year, y = attributable_cases / 1000, color = scenario), size = 2) +
    facet_wrap(~scenario, scales = "free_y") +
    labs(title = "Climate Change Scenarios: Additional Malaria Burden",
         x = "Year", y = "Additional Cases (Thousands)",
         subtitle = "Projected under different warming scenarios") +
    theme(legend.position = "none")

  # Economic burden visualization
  economic_plot <- ggplot(economic_results$economic_summary %>%
                           filter(Cost_Component %in% c("Medical Costs Total",
                                                      "Productivity Losses",
                                                      "Total Economic Burden"))) +
    geom_bar(aes(x = Cost_Component, y = Amount_USD_Million),
             stat = "identity", fill = "#E74C3C") +
    geom_text(aes(x = Cost_Component, y = Amount_USD_Million + 50,
                  label = sprintf("$%.0fM", Amount_USD_Million)), fontface = "bold") +
    labs(title = "Economic Burden of Climate-Attributed Malaria",
         x = "", y = "Cost (USD Millions)") +
    coord_flip()

  # Combine all plots into dashboard
  dashboard <- grid.arrange(
    grobs = list(attribution_plot, counterfactual_plot, future_plot, economic_plot),
    layout_matrix = rbind(
      c(1, 1, 2, 2),
      c(3, 3, 4, 4)
    ),
    top = textGrob("CLIMATE CHANGE ATTRIBUTION DASHBOARD\nMalaria in South Asia (2005-2050)",
                   gp = gpar(fontsize = 20, fontface = "bold"))
  )

  # Save dashboard
  ggsave("../outputs/figures/climate_attribution_dashboard.png", dashboard,
         width = 18, height = 14, dpi = 600, bg = "white")
  ggsave("../outputs/figures/climate_attribution_dashboard.pdf", dashboard,
         width = 18, height = 14, dpi = 600, bg = "white")

  cat("✅ Comprehensive attribution dashboard created\n")
  cat("   Saved as: ../outputs/figures/climate_attribution_dashboard.png/.pdf\n")

  return(dashboard)
}

# =============================================================================
# MAIN ATTRIBUTION ANALYSIS PIPELINE
# =============================================================================

#' Execute complete climate attribution analysis
run_climate_attribution_analysis <- function(data, malaria_model_results) {

  cat("="*80)
  cat("\nCLIMATE CHANGE ATTRIBUTION ANALYSIS PIPELINE")
  cat("\n" + "="*80)

  # Create output directories
  dir.create("../outputs/tables", showWarnings = FALSE, recursive = TRUE)
  dir.create("../outputs/figures", showWarnings = FALSE, recursive = TRUE)
  dir.create("../outputs/models", showWarnings = FALSE, recursive = TRUE)

  # Step 1: Calculate baseline conditions
  cat("\n\nSTEP 1: BASELINE TEMPERATURE CALCULATION")
  baseline_info <- calculate_baseline_temperature(data)

  # Step 2: Calculate temperature changes
  cat("\n\nSTEP 2: TEMPERATURE CHANGE CALCULATION")
  temp_changes <- calculate_temperature_change(data, baseline_info)

  # Get latest temperature change
  latest_change <- tail(temp_changes$annual_trends$avg_temp_change, 1)

  # Step 3: Population Attributable Fraction
  cat("\n\nSTEP 3: POPULATION ATTRIBUTABLE FRACTION ANALYSIS")
  paf_analysis <- calculate_population_attributable_fraction(
    malaria_model_results, latest_change, data
  )

  # Step 4: Counterfactual Analysis
  cat("\n\nSTEP 4: COUNTERFACTUAL ANALYSIS")
  counterfactual_analysis <- conduct_counterfactual_analysis(
    temp_changes$data_with_changes, baseline_info, malaria_model_results
  )

  # Step 5: Future Projections
  cat("\n\nSTEP 5: FUTURE PROJECTIONS")
  future_projections <- project_future_burden(data, malaria_model_results)

  # Step 6: Economic Valuation
  cat("\n\nSTEP 6: ECONOMIC VALUATION")
  economic_analysis <- calculate_economic_attribution(
    paf_analysis$attributable_cases
  )

  # Step 7: Create Dashboard
  cat("\n\nSTEP 7: COMPREHENSIVE DASHBOARD")
  attribution_dashboard <- create_attribution_dashboard(
    paf_analysis, counterfactual_analysis, future_projections, economic_analysis
  )

  # Save complete attribution summary
  attribution_summary <- list(
    baseline_info = baseline_info,
    temperature_changes = temp_changes,
    paf_analysis = paf_analysis,
    counterfactual_analysis = counterfactual_analysis,
    future_projections = future_projections,
    economic_analysis = economic_analysis,
    analysis_timestamp = Sys.time(),
    attribution_summary_text = sprintf(
      "CLIMATE CHANGE ATTRIBUTION SUMMARY:\n%s"
      .1f",
      .3f"
      .0f",
      .0f"
    )
  )

  saveRDS(attribution_summary, "../outputs/climate_attribution_analysis.rds")

  # Print final summary
  cat("\n" + "="*80)
  cat("\nCLIMATE ATTRIBUTION ANALYSIS COMPLETE!")
  cat("\n" + "="*80)
  cat("\nKEY RESULTS:")
  cat(sprintf("\n• %.1f%% of malaria cases attributable to climate change",
             paf_analysis$paf_value * 100))
  cat(sprintf("\n• %s additional cases due to %.1f°C temperature increase",
             scales::comma(paf_analysis$attributable_cases), latest_change))
  cat(sprintf("\n• Counterfactual scenario: %.1f%% fewer cases without climate change",
             counterfactual_analysis$percent_reduction))
  cat(sprintf("\n• Economic burden: $%.0f million annually",
             economic_analysis$total_burden_usd / 1e6))
  cat(sprintf("\n• 2050 High Scenario: %s additional cases",
             scales::comma(abs(future_projections$projections_2050$attributable_cases[3]))))

  return(attribution_summary)
}

# =============================================================================
# EXECUTION BLOCK
# =============================================================================

if (interactive() || length(commandArgs()) > 0) {
  cat("Loading synthetic study data for attribution analysis...\n")
  # In practice, this would load real data from previous analysis
  # For demonstration, we'll assume study_data and model_results exist

  # Placeholder for execution - in practice you'd call:
  # attribution_results <- run_climate_attribution_analysis(study_data, malaria_model_results)

  cat("Climate Attribution Analysis Framework Loaded.\n")
  cat("Ready to process climate change-disease attribution calculations.\n")
}

# =============================================================================
# EXPORTED FUNCTIONS
# =============================================================================

# Export key functions for use by main analysis script
# calculate_population_attributable_fraction
# conduct_counterfactual_analysis
# project_future_burden
# calculate_economic_attribution
# create_attribution_dashboard
