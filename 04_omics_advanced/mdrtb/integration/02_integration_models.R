#!/usr/bin/env Rscript
# ==============================================================================
# 02_integration_models.R - DIABLO multi-omics integration + ML modeling
# MDR-TB Multi-omics Integration Pipeline
# ==============================================================================

suppressPackageStartupMessages({
  library(tidyverse)
  library(mixOmics)
  library(caret)
  library(xgboost)
  library(ggplot2)
  library(ggpubr)
  library(pROC)
  library(logger)
  library(data.table)
  library(here)
  library(PRROC)
  library(glue)
})

# Set up logging
log_threshold(DEBUG)
log_appender(appender_file("04_omics_advanced/mdrtb/results/02_integration_models.log"))

log_info("Starting DIABLO multi-omics integration modeling for MDR-TB")
log_info("Runtime: {format(Sys.time(), '%Y-%m-%d %H:%M:%S')}")

# ==============================================================================
# CONFIGURATION
# ==============================================================================

RESULTS_DIR <- "04_omics_advanced/mdrtb/results/models"
MATRICES_DIR <- "04_omics_advanced/mdrtb/data_final/matrices"

# Model parameters
CV_FOLDS <- 5
N_COMP <- 2  # Number of DIABLO components
OUTCOME_COL <- "culture_conversion_6mo"  # Focus on 6-month culture conversion
RANDOM_SEED <- 42

# DIABLO hyperparameters to tune
DIABLO_PARAMS <- list(
  design = c(0.1, 0.5, 0.9),  # Correlation between blocks
  ncomp = list(keepX = list(20, 50, 100))  # Number of features per component
)

# ==============================================================================
# DATA LOADING
# ==============================================================================

load_training_data <- function() {
  #' Load processed multi-omics training matrices

  training_file <- file.path(MATRICES_DIR, "training_data.rds")

  if (!file.exists(training_file)) {
    log_error("Training data file not found: {training_file}")
    log_error("Run 01_make_matrices.R first")
    stop("Training data unavailable")
  }

  training_data <- readRDS(training_file)

  log_info("Loaded training data: {nrow(training_data$y)} samples")

  # Available omics matrices
  available_omics <- grep("^(rnaseq|microbiome|mtb)$", names(training_data), value = TRUE)
  log_info("Available omics: {paste(available_omics, collapse = ', ')}")

  if (length(available_omics) == 0) {
    log_error("No omics data available for integration modeling")
    return(NULL)
  }

  # Filter samples with complete outcomes
  complete_outcomes <- training_data$y %>%
    filter(outcome_available == TRUE, !is.na(.data[[OUTCOME_COL]]))

  if (nrow(complete_outcomes) < 20) {
    log_error("Too few samples with complete outcomes: {nrow(complete_outcomes)}")
    return(NULL)
  }

  training_data$y <- complete_outcomes

  # Subset omics matrices to complete samples
  sample_ids <- complete_outcomes$patient_timepoint_id

  for (omics_type in available_omics) {
    if (omics_type %in% names(training_data)) {
      # Ensure samples are in matrix
      available_samples <- intersect(sample_ids, rownames(training_data[[omics_type]]))

      if (length(available_samples) == 0) {
        log_warn("No overlapping samples for {omics_type}")
        next
      }

      training_data[[omics_type]] <- training_data[[omics_type]][available_samples, , drop = FALSE]
      log_info("{omics_type}: {nrow(training_data[[omics_type]])} samples × {ncol(training_data[[omics_type]])} features")
    }
  }

  log_info("Final training dataset: {nrow(complete_outcomes)} samples with outcome data")

  return(training_data)
}

prepare_diablo_input <- function(training_data) {
  #' Prepare omics matrices and outcome vector for DIABLO

  available_omics <- grep("^(rnaseq|microbiome|mtb)$", names(training_data), value = TRUE)

  if (length(available_omics) < 2) {
    log_error("Need at least 2 omics layers for multi-omics integration")
    return(NULL)
  }

  # Extract outcome vector (binary: success = 1, failure = 0)
  Y <- training_data$y[[OUTCOME_COL]] %>% factor(labels = c("Failure", "Success"))

  # Prepare X data frames list for DIABLO
  X <- list()
  for (omics_type in available_omics) {
    if (omics_type %in% names(training_data)) {
      X[[omics_type]] <- as.data.frame(training_data[[omics_type]])
      log_info("Prepared {omics_type} matrix: {nrow(X[[omics_type]])} × {ncol(X[[omics_type]])}")
    }
  }

  # Ensure all matrices have same samples (should already be aligned)
  all_rownames <- lapply(X, rownames)
  common_samples <- Reduce(intersect, all_rownames)

  if (length(common_samples) == 0) {
    log_error("No common samples across all omics matrices")
    return(NULL)
  }

  # Subset to common samples
  Y <- Y[common_samples]
  for (i in seq_along(X)) {
    X[[i]] <- X[[i]][common_samples, , drop = FALSE]
  }

  log_info("DIABLO input prepared: {length(common_samples)} samples, {length(X)} omics layers")

  return(list(X = X, Y = Y))
}

# ==============================================================================
# DIABLO INTEGRATION MODELING
# ==============================================================================

run_diablo_integration <- function(diablo_data, n_comp = N_COMP) {
  #' Run DIABLO multi-omics integration with cross-validation

  log_info("Running DIABLO multi-omics integration (n_comp = {n_comp})")

  tryCatch({
    set.seed(RANDOM_SEED)

    # Basic DIABLO model for exploration
    diablo_basic <- block.splsda(
      X = diablo_data$X,
      Y = diablo_data$Y,
      ncomp = n_comp,
      design = "full"  # Start with full design matrix
    )

    log_info("DIABLO basic model fitted successfully")

    # Get performance metrics
    diablo_perf <- perf.diablo(
      diablo_basic,
      folds = CV_FOLDS,
      nrepeat = 3
    )

    log_info("DIABLO cross-validation completed: CV error = {min(diablo_perf$WeightedPredict.Error)}")

    # Tune number of features per component
    diablo_tuned <- tune.block.splsda(
      X = diablo_data$X,
      Y = diablo_data$Y,
      ncomp = n_comp,
      test.keepX = DIABLO_PARAMS$ncomp$keepX,
      design = DIABLO_PARAMS$design,
      folds = CV_FOLDS,
      nrepeat = 3
    )

    # Train final model with tuned parameters
    diablo_final <- block.splsda(
      X = diablo_data$X,
      Y = diablo_data$Y,
      ncomp = n_comp,
      keepX = diablo_tuned$choice.keepX,
      design = diablo_tuned$choice.ncomp$design
    )

    log_info("DIABLO tuned model fitted: keepX = {paste(diablo_tuned$choice.keepX, collapse = ', ')}")

    return(list(
      basic = diablo_basic,
      performance = diablo_perf,
      tuned = diablo_tuned,
      final = diablo_final
    ))

  }, error = function(e) {
    log_error("DIABLO modeling failed: {e$message}")
    return(NULL)
  })
}

generate_diablo_visualizations <- function(diablo_results) {
  #' Generate comprehensive DIABLO visualization suite

  plots <- list()

  tryCatch({
    # 1. Correlation circle plot
    plots$correlation_circle <- plotDiablo(diablo_results$final, type = "correlation",
                                          title = "DIABLO Correlation Circle")

    # 2. Component weights
    for (comp in 1:min(3, diablo_results$final$ncomp)) {
      plots[[paste0("weights_comp", comp)]] <- plotLoadings(
        diablo_results$final,
        comp = comp,
        contrib = "max"
      ) +
        ggtitle(glue("DIABLO Component {comp} Loadings")) +
        theme_minimal()
    }

    # 3. Sample plot (first 2 components)
    plots$sample_plot <- plotIndiv(diablo_results$final,
                                  comp = 1:2,
                                  group = diablo_results$final$Y,
                                  ind.names = FALSE,
                                  title = "DIABLO Sample Plot")

    # 4. Variable plot
    plots$variable_plot <- plotVar(diablo_results$final,
                                  comp = 1:2,
                                  var.names = FALSE,
                                  title = "DIABLO Variable Plot")

    # 5. Performance plots
    perf_df <- data.frame(
      Components = 1:length(diablo_results$performance$error.rate.class$DIABLO$Overall.ER.mean),
      Error_Rate = diablo_results$performance$error.rate.class$DIABLO$Overall.ER.mean,
      SD = diablo_results$performance$error.rate.class$DIABLO$Overall.ER.sd
    )

    plots$performance_plot <- ggplot(perf_df, aes(x = Components, y = Error_Rate)) +
      geom_line(color = "blue", size = 1) +
      geom_point(size = 3) +
      geom_errorbar(aes(ymin = Error_Rate - SD, ymax = Error_Rate + SD), width = 0.2) +
      labs(title = "DIABLO Model Performance",
           subtitle = glue("Cross-validation error by components (CV={CV_FOLDS})"),
           y = "Classification Error Rate") +
      theme_minimal()

    log_info("Generated {length(plots)} DIABLO visualizations")

    return(plots)

  }, error = function(e) {
    log_error("Visualization generation failed: {e$message}")
    return(plots)  # Return what we have
  })
}

# ==============================================================================
# MACHINE LEARNING STACK MODELING
# ==============================================================================

prepare_ml_data <- function(diablo_data, diablo_model) {
  #' Prepare integrated features for downstream ML modeling

  # Get DIABLO component scores (latent space)
  diablo_scores <- predict.diablo(diablo_model, diablo_data$X)$variates
  diablo_components <- do.call(cbind, diablo_scores) %>% as.data.frame()

  # Add individual omics features (selected ones)
  selected_features <- list()

  for (omics_name in names(diablo_data$X)) {
    # Get top features from DIABLO loadings
    loadings <- selectVar(diablo_model, block = omics_name, comp = 1:N_COMP)
    top_features <- unique(unlist(loadings$names))

    if (length(top_features) > 0 && length(top_features) <= 50) {  # Limit to prevent overfitting
      selected_features[[omics_name]] <- diablo_data$X[[omics_name]][, top_features, drop = FALSE]
      log_info("{omics_name}: selected {length(top_features)} features")
    }
  }

  # Combine all features
  if (length(selected_features) > 0) {
    individual_features <- do.call(cbind, selected_features)
    ml_features <- cbind(diablo_components, individual_features)
  } else {
    ml_features <- diablo_components
  }

  # Prepare ML input
  ml_data <- data.frame(
    outcome = diablo_data$Y,
    ml_features
  )

  log_info("ML feature matrix: {nrow(ml_data)} samples × {ncol(ml_data)} features")
  log_info("Feature breakdown: DIABLO components + {ncol(ml_features) - ncol(diablo_components)} individual features")

  return(ml_data)
}

train_ml_stack <- function(ml_data, outcome_col = "outcome") {
  #' Train ensemble ML models on integrated multi-omics features

  set.seed(RANDOM_SEED)

  # Prepare training control
  train_control <- trainControl(
    method = "cv",
    number = CV_FOLDS,
    classProbs = TRUE,
    summaryFunction = twoClassSummary,
    savePredictions = "final"
  )

  # Models to try
  model_grid <- expand.grid(
    # Random Forest
    rf = list(ntree = c(500, 1000), nodesize = c(1, 5)),

    # XGBoost
    xgb = expand.grid(
      nrounds = c(100, 200),
      max_depth = c(3, 6),
      eta = c(0.1, 0.3)
    ),

    # SVM
    svm = expand.grid(C = c(0.1, 1, 10), sigma = c(0.01, 0.1)),

    # Elastic Net
    glmnet = expand.grid(alpha = c(0.1, 0.5, 0.9), lambda = c(0.01, 0.1))
  )

  models_trained <- list()

  # Train Random Forest
  tryCatch({
    rf_model <- train(
      outcome ~ .,
      data = ml_data,
      method = "rf",
      trControl = train_control,
      tuneGrid = model_grid$rf,
      metric = "ROC"
    )
    models_trained$rf <- rf_model
    log_info("Random Forest: AUC = {max(rf_model$results$ROC)}")
  }, error = function(e) log_warn("Random Forest failed: {e$message}"))

  # Train XGBoost
  tryCatch({
    xgb_model <- train(
      outcome ~ .,
      data = ml_data,
      method = "xgbTree",
      trControl = train_control,
      tuneGrid = model_grid$xgb,
      metric = "ROC"
    )
    models_trained$xgb <- xgb_model
    log_info("XGBoost: AUC = {max(xgb_model$results$ROC)}")
  }, error = function(e) log_warn("XGBoost failed: {e$message}"))

  # Train SVM
  tryCatch({
    svm_model <- train(
      outcome ~ .,
      data = ml_data,
      method = "svmRadial",
      trControl = train_control,
      tuneGrid = model_grid$svm,
      metric = "ROC"
    )
    models_trained$svm <- svm_model
    log_info("SVM: AUC = {max(svm_model$results$ROC)}")
  }, error = function(e) log_warn("SVM failed: {e$message}"))

  # Train Elastic Net
  tryCatch({
    glmnet_model <- train(
      outcome ~ .,
      data = ml_data,
      method = "glmnet",
      trControl = train_control,
      tuneGrid = model_grid$glmnet,
      metric = "ROC"
    )
    models_trained$glmnet <- glmnet_model
    log_info("Elastic Net: AUC = {max(glmnet_model$results$ROC)}")
  }, error = function(e) log_warn("Elastic Net failed: {e$message}"))

  # Select best model
  if (length(models_trained) > 0) {
    model_performance <- sapply(models_trained, function(m) max(m$results$ROC))
    best_model_name <- names(model_performance)[which.max(model_performance)]
    best_model <- models_trained[[best_model_name]]

    log_info("Best ML model: {best_model_name} (AUC = {max(model_performance)})")

    return(list(
      all_models = models_trained,
      best_model = best_model,
      best_name = best_model_name,
      performance = model_performance
    ))
  } else {
    log_error("No ML models could be trained successfully")
    return(NULL)
  }
}

# ==============================================================================
# MODEL EVALUATION AND FEATURE IMPORTANCE
# ==============================================================================

evaluate_models <- function(diablo_results, ml_results) {
  #' Comprehensive model evaluation with metrics and interpretations

  results <- list()

  tryCatch({
    # Train/test predictions from best ML model
    best_ml <- ml_results$best_model

    # Get predictions on training data
    train_pred <- predict(best_ml, type = "prob")
    train_actual <- best_ml$trainingData$.outcome

    # ROC analysis
    roc_obj <- roc(train_actual, train_pred$Success)
    results$roc_curve <- roc_obj
    results$auc <- auc(roc_obj)

    log_info("Best model AUC: {sprintf('%.3f', results$auc)}")

    # Feature importance (varies by model type)
    if (results$best_name == "rf") {
      var_importance <- varImp(best_ml, scale = FALSE)
      results$importance <- var_importance$importance %>%
        rownames_to_column("feature") %>%
        arrange(desc(Overall)) %>%
        head(20)
    } else if (results$best_name == "xgb") {
      importance_matrix <- xgb.importance(model = best_ml$finalModel)
      results$importance <- importance_matrix %>%
        select(Feature, Gain) %>%
        rename(feature = Feature, importance = Gain) %>%
        head(20)
    }

    if (exists("results$importance")) {
      log_info("Top features: {paste(results$importance$feature[1:5], collapse = ', ')}")
    }

    # Model calibration
    prob_bins <- cut(train_pred$Success, breaks = seq(0, 1, 0.1))
    observed_prob <- tapply(train_actual == "Success", prob_bins, mean)
    predicted_prob <- tapply(train_pred$Success, prob_bins, mean)

    results$calibration <- data.frame(
      bin = levels(prob_bins),
      observed = observed_prob,
      predicted = predicted_prob
    )

    log_info("Model evaluation completed")

    return(results)

  }, error = function(e) {
    log_error("Model evaluation failed: {e$message}")
    return(results)
  })
}

create_evaluation_plots <- function(evaluation_results) {
  #' Create comprehensive evaluation visualizations

  plots <- list()

  tryCatch({
    # ROC curve
    roc_data <- data.frame(
      fpr = rev(1 - evaluation_results$roc_curve$specificities),
      tpr = rev(evaluation_results$roc_curve$sensitivities)
    )

    plots$roc_plot <- ggplot(roc_data, aes(x = fpr, y = tpr)) +
      geom_line(color = "blue", size = 1.5) +
      geom_abline(intercept = 0, slope = 1, color = "gray", linetype = "dashed") +
      labs(title = glue("ROC Curve (AUC = {sprintf('%.3f', evaluation_results$auc)})"),
           x = "False Positive Rate", y = "True Positive Rate") +
      theme_minimal()

    # Feature importance plot
    if (!is.null(evaluation_results$importance)) {
      plots$importance_plot <- ggplot(evaluation_results$importance[1:10, ], aes(x = reorder(feature, importance), y = importance)) +
        geom_bar(stat = "identity", fill = "steelblue") +
        coord_flip() +
        labs(title = "Top 10 Feature Importance", x = "Feature", y = "Importance") +
        theme_minimal()
    }

    # Calibration plot
    if (!is.null(evaluation_results$calibration)) {
      plots$calibration_plot <- ggplot(evaluation_results$calibration %>% na.omit(),
                                     aes(x = predicted, y = observed)) +
        geom_point(size = 3) +
        geom_abline(intercept = 0, slope = 1, color = "red", linetype = "dashed") +
        geom_smooth(method = "lm", color = "blue", alpha = 0.5) +
        labs(title = "Model Calibration",
             x = "Predicted Probability", y = "Observed Probability") +
        theme_minimal()
    }

    log_info("Generated {length(plots)} evaluation plots")

    return(plots)

  }, error = function(e) {
    log_error("Plot generation failed: {e$message}")
    return(plots)
  })
}

# ==============================================================================
# SAVE RESULTS
# ==============================================================================

save_model_results <- function(diablo_results, ml_results, evaluation_results) {
  #' Save all model results, plots, and metrics

  dir.create(RESULTS_DIR, recursive = TRUE, showWarnings = FALSE)

  # Save model objects
  saveRDS(diablo_results, file.path(RESULTS_DIR, "diablo_model.rds"))
  saveRDS(ml_results, file.path(RESULTS_DIR, "ml_models.rds"))
  saveRDS(evaluation_results, file.path(RESULTS_DIR, "evaluation_results.rds"))

  # Generate and save plots
  diablo_plots <- generate_diablo_visualizations(diablo_results)
  evaluation_plots <- create_evaluation_plots(evaluation_results)

  # Save plots as PDF
  if (length(diablo_plots) > 0) {
    ggexport(diablo_plots, filename = file.path(RESULTS_DIR, "diablo_plots.pdf"), verbose = FALSE)
  }

  if (length(evaluation_plots) > 0) {
    ggexport(evaluation_plots, filename = file.path(RESULTS_DIR, "evaluation_plots.pdf"), verbose = FALSE)
  }

  # Save metrics summary
  model_summary <- list(
    diablo = list(
      n_components = diablo_results$final$ncomp,
      n_blocks = length(diablo_results$final$names$blocks),
      keepX = diablo_results$tuned$choice.keepX,
      cv_error = min(diablo_results$performance$WeightedPredict.Error)
    ),
    ml = list(
      best_model = ml_results$best_name,
      auc = evaluation_results$auc,
      n_features = length(evaluation_results$importance$feature)
    ),
    timestamp = format(Sys.time())
  )

  saveRDS(model_summary, file.path(RESULTS_DIR, "model_summary.rds"))

  # Create human-readable summary
  summary_text <- sprintf("
MDR-TB Multi-Omics Model Summary
================================

DIABLO Integration:
- Components: %d
- Omics blocks: %d
- CV error: %.3f
- Features selected: %s

ML Modeling:
- Best model: %s
- AUC: %.3f
- Top features: %s

Generated: %s
",
  model_summary$diablo$n_components,
  model_summary$diablo$n_blocks,
  model_summary$diablo$cv_error,
  paste(model_summary$diablo$keepX, collapse = ", "),
  model_summary$ml$best_model,
  model_summary$ml$auc,
  ifelse(exists("evaluation_results$importance"),
         paste(evaluation_results$importance$feature[1:5], collapse = ", "),
         "N/A"),
  model_summary$timestamp
  )

  writeLines(summary_text, file.path(RESULTS_DIR, "model_summary.txt"))

  log_info("All model results saved to: {RESULTS_DIR}")
  log_info("Summary: AUC = {sprintf('%.3f', evaluation_results$auc)}, Best Model = {ml_results$best_name}")
}

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

main <- function() {
  #' Main integration modeling workflow

  tryCatch({
    log_info("Starting MDR-TB multi-omics integration modeling")

    # Load training data
    training_data <- load_training_data()
    if (is.null(training_data)) return(invisible(FALSE))

    # Prepare DIABLO input
    diablo_data <- prepare_diablo_input(training_data)
    if (is.null(diablo_data)) return(invisible(FALSE))

    # Run DIABLO integration
    diablo_results <- run_diablo_integration(diablo_data)
    if (is.null(diablo_results)) return(invisible(FALSE))

    # Prepare ML data
    ml_data <- prepare_ml_data(diablo_data, diablo_results$final)

    # Train ML stack
    ml_results <- train_ml_stack(ml_data)
    if (is.null(ml_results)) return(invisible(FALSE))

    # Evaluate models
    evaluation_results <- evaluate_models(diablo_data, ml_results)

    # Save all results
    save_model_results(diablo_results, ml_results, evaluation_results)

    log_info("Integration modeling completed successfully ✅")
    log_info("Best predictive model: {ml_results$best_name} with AUC = {sprintf('%.3f', evaluation_results$auc)}")

  }, error = function(e) {
    log_error("Integration modeling failed: {e$message}")
    return(invisible(FALSE))
  })

  return(invisible(TRUE))
}

# Execute if run as script
if (!interactive()) {
  main()
}

log_info("02_integration_models.R loaded successfully - call main() to run DIABLO + ML modeling")
# ==============================================================================
