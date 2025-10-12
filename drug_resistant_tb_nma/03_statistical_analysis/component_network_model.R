# Component Network Meta-Analysis for Drug-Resistant Tuberculosis
# Evaluates individual drug contributions using component-based modeling

library(rjags)
library(coda)
library(ggplot2)
library(dplyr)
library(tidyr)

# Define treatment compositions for component NMA
define_treatment_compositions <- function() {
  "
  Define which drugs/components are included in each regimen
  "

  compositions <- list(

    # BPaL Components
    "BPaL" = list(
      "Bedaquiline" = TRUE,
      "Pretomanid" = TRUE,
      "Linezolid" = TRUE,
      "Moxifloxacin" = FALSE,
      "Short_Backbone" = FALSE,
      "Long_Backbone" = FALSE
    ),

    # BPaLM Components
    "BPaLM" = list(
      "Bedaquiline" = TRUE,
      "Pretomanid" = TRUE,
      "Linezolid" = TRUE,
      "Moxifloxacin" = TRUE,
      "Short_Backbone" = FALSE,
      "Long_Backbone" = FALSE
    ),

    # Short MDR Regimen Components
    "Short_MDR" = list(
      "Bedaquiline" = FALSE,
      "Pretomanid" = FALSE,
      "Linezolid" = FALSE,
      "Moxifloxacin" = TRUE,
      "Short_Backbone" = TRUE,
      "Long_Backbone" = FALSE
    ),

    # Long Individualized Regimen Components
    "Long_Individualized" = list(
      "Bedaquiline" = FALSE,  # May or may not include
      "Pretomanid" = FALSE,   # May or may not include
      "Linezolid" = FALSE,    # May or may not include
      "Moxifloxacin" = FALSE, # May or may not include
      "Short_Backbone" = FALSE,
      "Long_Backbone" = TRUE
    )
  )

  return(compositions)
}

# JAGS model for component NMA
component_nma_model <- function() {
  "
  JAGS model specification for component network meta-analysis
  "

  model_string <- "
  model {
    # Random effects component NMA model

    for(i in 1:ns) {
      # Treatment effect for each study
      delta[i,1] <- 0
      mu[i] ~ dnorm(0, 0.0001)

      for(k in 2:nt) {
        delta[i,k] ~ dnorm(md[i,k], precd[i,k])
        md[i,k] <- mu[i] + d[k] - d[1]
        precd[i,k] <- 1 / (se[i,k] * se[i,k])
      }

      # Likelihood
      r[i] ~ dbin(p[i], n[i])
      logit(p[i]) <- delta[i,t[i]]
    }

    # Component effects (main effects)
    d[1] <- 0  # Reference treatment

    for(k in 2:nt) {
      # Treatment effect as sum of component effects
      d[k] <- sum_components[k]
    }

    # Component effect parameters
    beta_BDQ ~ dnorm(0, 0.0001)      # Bedaquiline effect
    beta_Pa ~ dnorm(0, 0.0001)       # Pretomanid effect
    beta_LZD ~ dnorm(0, 0.0001)      # Linezolid effect
    beta_MFX ~ dnorm(0, 0.0001)      # Moxifloxacin effect
    beta_Short ~ dnorm(0, 0.0001)    # Short regimen backbone
    beta_Long ~ dnorm(0, 0.0001)     # Long regimen backbone

    # Interaction terms (for non-additive effects)
    beta_BDQ_Pa ~ dnorm(0, 0.0001)   # BDQ + Pa interaction
    beta_BDQ_LZD ~ dnorm(0, 0.0001)  # BDQ + LZD interaction
    beta_Pa_LZD ~ dnorm(0, 0.0001)   # Pa + LZD interaction

    # Calculate treatment effects based on component compositions
    sum_components[1] <- 0  # Reference

    sum_components[2] <- beta_BDQ + beta_Pa + beta_LZD +
                        beta_BDQ_Pa + beta_BDQ_LZD + beta_Pa_LZD  # BPaL

    sum_components[3] <- beta_BDQ + beta_Pa + beta_LZD + beta_MFX +
                        beta_BDQ_Pa + beta_BDQ_LZD + beta_Pa_LZD  # BPaLM

    sum_components[4] <- beta_MFX + beta_Short  # Short MDR

    sum_components[5] <- beta_Long  # Long Individualized

    # Prior for between-study heterogeneity
    tau ~ dgamma(0.01, 0.01)
    sd <- 1/sqrt(tau)
  }
  "

  return(model_string)
}

# Prepare data for component NMA
prepare_component_data <- function(study_data) {
  "
  Prepare data in format suitable for component NMA
  "

  # Create component matrix
  components <- define_treatment_compositions()

  # Convert to matrix format for JAGS
  component_matrix <- data.frame(
    Treatment = names(components),
    BDQ = c(1, 1, 0, 0),  # BPaL, BPaLM have BDQ; others don't
    Pa = c(1, 1, 0, 0),   # BPaL, BPaLM have Pa; others don't
    LZD = c(1, 1, 0, 0),  # BPaL, BPaLM have LZD; others don't
    MFX = c(0, 1, 1, 0),  # BPaLM and Short have MFX
    Short = c(0, 0, 1, 0), # Only Short regimen
    Long = c(0, 0, 0, 1)   # Only Long regimen
  )

  return(component_matrix)
}

# Fit component NMA model
fit_component_model <- function(study_data) {
  "
  Fit the component network meta-analysis model
  "

  # Prepare data for JAGS
  jags_data <- list(
    ns = length(unique(study_data$study)),
    nt = length(unique(study_data$treatment)),
    t = as.numeric(factor(study_data$treatment)),
    r = study_data$responders,
    n = study_data$sampleSize
  )

  # Initial values
  inits <- list(
    list(beta_BDQ = 0, beta_Pa = 0, beta_LZD = 0, beta_MFX = 0,
         beta_Short = 0, beta_Long = 0, tau = 1),
    list(beta_BDQ = 0.5, beta_Pa = 0.5, beta_LZD = 0.5, beta_MFX = 0.5,
         beta_Short = 0.5, beta_Long = 0.5, tau = 0.5),
    list(beta_BDQ = -0.5, beta_Pa = -0.5, beta_LZD = -0.5, beta_MFX = -0.5,
         beta_Short = -0.5, beta_Long = -0.5, tau = 2)
  )

  # Fit model
  model <- jags.model(textConnection(component_nma_model()),
                     data = jags_data,
                     inits = inits,
                     n.chains = 3)

  # Burn-in
  update(model, n.iter = 10000)

  # Sample
  samples <- coda.samples(model,
                         variable.names = c("beta_BDQ", "beta_Pa", "beta_LZD",
                                          "beta_MFX", "beta_Short", "beta_Long",
                                          "d", "sd"),
                         n.iter = 50000,
                         thin = 10)

  return(list(model = model, samples = samples, data = jags_data))
}

# Analyze component effects
analyze_component_effects <- function(component_results) {
  "
  Analyze the estimated effects of individual components
  "

  samples <- component_results$samples

  # Summarize component effects
  component_summary <- summary(samples)$quantiles[c("beta_BDQ", "beta_Pa", "beta_LZD",
                                                   "beta_MFX", "beta_Short", "beta_Long"), ]

  # Convert to odds ratios
  component_summary <- data.frame(
    Component = rownames(component_summary),
    OR = exp(component_summary[, "50%"]),
    lowerCI = exp(component_summary[, "2.5%"]),
    upperCI = exp(component_summary[, "97.5%"])
  )

  # Add interpretation
  component_summary$Interpretation <- ifelse(
    component_summary$lowerCI > 1, "Beneficial",
    ifelse(component_summary$upperCI < 1, "Harmful", "Uncertain")
  )

  return(component_summary)
}

# Treatment interaction analysis
analyze_interactions <- function(component_results) {
  "
  Analyze interaction effects between drugs
  "

  samples <- component_results$samples

  # Extract interaction parameters
  interactions <- summary(samples)$quantiles[
    c("beta_BDQ_Pa", "beta_BDQ_LZD", "beta_Pa_LZD"), ]

  # Convert to odds ratios
  interaction_summary <- data.frame(
    Interaction = rownames(interactions),
    OR = exp(interactions[, "50%"]),
    lowerCI = exp(interactions[, "2.5%"]),
    upperCI = exp(interactions[, "97.5%"])
  )

  return(interaction_summary)
}

# Linezolid dose-response analysis
linezolid_dose_response <- function(study_data) {
  "
  Analyze the effect of different linezolid doses
  "

  # Extract linezolid dose information
  lzd_data <- study_data %>%
    filter(treatment %in% c("BPaL", "BPaLM")) %>%
    mutate(lzd_dose_mg = case_when(
      treatment == "BPaL" ~ 600,  # Standard dose
      treatment == "BPaLM" ~ 600, # Standard dose
      TRUE ~ NA_real_
    ))

  # Dose-response model
  dose_model <- "
  model {
    for(i in 1:length(r)) {
      r[i] ~ dbin(p[i], n[i])
      logit(p[i]) <- alpha + beta * dose[i]
    }

    alpha ~ dnorm(0, 0.0001)
    beta ~ dnorm(0, 0.0001)
  }
  "

  # Fit dose-response model if sufficient data
  if (nrow(lzd_data) > 0) {
    dose_jags_data <- list(
      r = lzd_data$responders,
      n = lzd_data$sampleSize,
      dose = lzd_data$lzd_dose_mg
    )

    dose_model_fit <- jags.model(textConnection(dose_model),
                                data = dose_jags_data,
                                n.chains = 2)

    update(dose_model_fit, 5000)

    dose_samples <- coda.samples(dose_model_fit,
                                variable.names = c("alpha", "beta"),
                                n.iter = 20000, thin = 10)

    return(dose_samples)
  }

  return(NULL)
}

# Create component effect visualization
plot_component_effects <- function(component_summary) {
  "
  Create forest plot of component effects
  "

  p <- ggplot(component_summary, aes(x = Component, y = OR,
                                   ymin = lowerCI, ymax = upperCI)) +
    geom_pointrange() +
    geom_hline(yintercept = 1, linetype = "dashed") +
    coord_flip() +
    theme_minimal() +
    labs(title = "Component Effects on Treatment Success",
         subtitle = "Odds Ratios for Individual Drug Contributions",
         x = "Component", y = "Odds Ratio (95% CI)") +
    theme(axis.text.y = element_text(size = 10))

  ggsave("drug_resistant_tb_nma/04_results/component_effects_plot.png",
         p, width = 8, height = 6)

  return(p)
}

# Generate comprehensive component analysis report
generate_component_report <- function(study_data) {
  "
  Generate complete component NMA analysis report
  "

  # Fit component model
  component_results <- fit_component_model(study_data)

  # Analyze effects
  component_effects <- analyze_component_effects(component_results)
  interactions <- analyze_interactions(component_results)
  dose_response <- linezolid_dose_response(study_data)

  # Create visualizations
  effects_plot <- plot_component_effects(component_effects)

  # Save results
  results <- list(
    component_effects = component_effects,
    interactions = interactions,
    dose_response = dose_response,
    model_results = component_results,
    plot = effects_plot
  )

  # Save to files
  write.csv(component_effects, "drug_resistant_tb_nma/04_results/component_effects.csv")
  write.csv(interactions, "drug_resistant_tb_nma/04_results/drug_interactions.csv")

  if (!is.null(dose_response)) {
    saveRDS(dose_response, "drug_resistant_tb_nma/04_results/dose_response_results.rds")
  }

  saveRDS(results, "drug_resistant_tb_nma/04_results/component_nma_complete.rds")

  return(results)
}

# Main execution
if (sys.nframe() == 0) {
  # Load sample data (replace with actual data loading)
  study_data <- read.csv("drug_resistant_tb_nma/02_data_extraction/extracted_data.csv")

  # Run component analysis
  component_analysis <- generate_component_report(study_data)

  cat("Component NMA analysis completed!\n")
  cat("Results saved to drug_resistant_tb_nma/04_results/\n")
}
