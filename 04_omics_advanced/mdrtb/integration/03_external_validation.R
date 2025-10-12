#!/usr/bin/env Rscript
# ==============================================================================
# 03_external_validation.R - Cross-validation and external validation
# MDR-TB Multi-omics Integration Pipeline
# ==============================================================================

suppressPackageStartupMessages({
  library(tidyverse)
  library(mixOmics)
  library(caret)
  library(pROC)
  library(logger)
  library(data.table)
  library(ggplot2)
  library(ggpubr)
  library(patients)
  library(PRROC)
  library(glue)
})

# Set up logging
log_threshold(DEBUG)
log_appender(appender_file("04_omics_advanced/mdrtb/results/03_external_validation.log"))

log_info("Starting external validation for MDR-TB multi-omics models")
log_info("Runtime: {format(Sys.time(), '%Y-%m-%d %H:%M:%S')}")

# ==============================================================================
# CONFIGURATION
# ==============================================================================

MODEL_DIR <- "04_omics_advanced/mdrtb/results/models"
MATRICES_DIR <- "04_omics_advanced/mdrtb/data_final/matrices"
RESULTS_DIR <- "04_omics_advanced/mdrtb/results/validation"

# Validation parameters
CV_FOLDS_OUTER <- 5
CV_FOLDS_INNER <- 3
RANDOM_SEED <- 42
PERFORMANCE_METRICS <- c("auc", "auprc", "accuracy", "sensitivity", "specificity", "brier_score")

# ==============================================================================
# MODEL LOADING
# ==============================================================================

load_trained_models <- function() {
  #' Load trained DIABLO and ML models

  diablo_file <- file.path(MODEL_DIR, "diablo_model.rds")
  ml_file <- file.path(MODEL_DIR, "ml_models.rds")

  if (!file.exists(diablo_file) || !file.exists(ml_file)) {
    log_error("Trained models not found - run 02_integration_models.R first")
    return(NULL)
  }

  diablo_results <- readRDS(diablo_file)
  ml_results <- readRDS(ml_file)

  log_info("Loaded trained models: DIABLO + {length(ml_results$all_models)} ML models")

  return(list(diablo = diablo_results$final, ml = ml_results))
}

load_evaluation_data <- function() {
  #' Load training data for nested CV

  matrices_file <- file.path(MATRICES_DIR, "training_data.rds")

  if (!file.exists(matrices_file)) {
    log_error("Training matrices not found - run 01_make_matrices.R first")
    return(NULL)
  }

  training_data <- readRDS(matrices_file)

  # Prepare DIABLO format
  available_omics <- grep("^(rnaseq|microbiome|mtb)$", names(training_data), value = TRUE)

  if (length(available_omics) < 2) {
    log_error("Need at least 2 omics layers for validation")
    return(NULL)
  }

  # Prepare omics matrices
  X_list <- lapply(training_data[available_omics], as.data.frame)
  Y <- factor(training_data$y$culture_conversion_6mo, labels = c("Failure", "Success"))

  # Ensure sample alignment
  common_samples <- Reduce(intersect, lapply(X_list, rownames))
  X_list <- lapply(X_list, function(x) x[common_samples, ])
  Y <- Y[common_samples]

  log_info("Prepared evaluation data: {length(common_samples)} samples, {length(X_list)} omics layers")

  return(list(X = X_list, Y = Y, sample_info = training_data$y[common_samples, ]))
}

# ==============================================================================
# NESTED CROSS-VALIDATION
# ==============================================================================

perform_nested_cv <- function(diablo_model, X_list, Y) {
  #' Perform nested cross-validation to get unbiased performance estimates

  log_info("Running nested {CV_FOLDS_OUTER}×{CV_FOLDS_INNER} cross-validation")

  set.seed(RANDOM_SEED)

  # Results storage
  cv_results <- list()

  # Outer CV loop (for unbiased performance)
  outer_folds <- createFolds(Y, k = CV_FOLDS_OUTER)

  for (i in seq_along(outer_folds)) {
    log_info("Outer fold {i}/{CV_FOLDS_OUTER}")

    # Split data
    test_idx <- outer_folds[[i]]
    train_idx <- setdiff(seq_along(Y), test_idx)

    X_train <- lapply(X_list, function(x) x[train_idx, ])
    Y_train <- Y[train_idx]
    X_test <- lapply(X_list, function(x) x[test_idx, ])
    Y_test <- Y[test_idx]

    # Inner CV loop (for parameter tuning)
    inner_folds <- createFolds(Y_train, k = CV_FOLDS_INNER)

    tryCatch({
      # Tune DIABLO on training data
      tuned_diablo <- tune.block.splsda(
        X = X_train,
        Y = Y_train,
        ncomp = 2,
        test.keepX = list(20, 50, 100),
        design = c(0.1, 0.5, 0.9),
        folds = inner_folds,
        nrepeat = 1  # Speed up
      )

      # Train optimal model
      optimized_model <- block.splsda(
        X = X_train,
        Y = Y_train,
        ncomp = 2,
        keepX = tuned_diablo$choice.keepX,
        design = tuned_diablo$choice.ncomp$design
      )

      # Get test predictions
      test_pred <- predict.diablo(optimized_model, X_test)

      # Calculate metrics
      fold_results <- evaluate_predictions(test_pred$WeightedPredict[, "comp1"], Y_test)

      cv_results[[paste0("fold_", i)]] <- fold_results

      log_info("Fold {i}: AUC = {sprintf('%.3f', fold_results$auc)}")

    }, error = function(e) {
      log_error("Error in fold {i}: {e$message}")
      cv_results[[paste0("fold_", i)]] <- NULL
    })
  }

  # Aggregate results
  valid_folds <- cv_results[!sapply(cv_results, is.null)]

  if (length(valid_folds) == 0) {
    log_error("No valid CV folds completed")
    return(NULL)
  }

  metric_names <- names(valid_folds[[1]])
  aggregated_results <- lapply(metric_names, function(metric) {
    metric_values <- sapply(valid_folds, function(x) x[[metric]])
    c(mean = mean(metric_values, na.rm = TRUE),
      sd = sd(metric_values, na.rm = TRUE),
      n = length(metric_values))
  })
  names(aggregated_results) <- metric_names

  log_info("Nested CV completed: {length(valid_folds)}/{CV_FOLDS_OUTER} folds successful")

  return(list(
    individual_folds = cv_results,
    aggregated = aggregated_results,
    summary = data.frame(
      metric = names(aggregated_results),
      mean = sapply(aggregated_results, `[[`, "mean"),
      sd = sapply(aggregated_results, `[[`, "sd"),
      n_folds = sapply(aggregated_results, `[[`, "n")
    )
  ))
}

# ==============================================================================
# EXTERNAL VALIDATION
# ==============================================================================

simulate_external_validation <- function(diablo_model, evaluation_data, n_external = 3) {
  #' Simulate external validation by splitting data into discovery/validation sets

  log_info("Simulating {n_external} external validation scenarios")

  set.seed(RANDOM_SEED)

  validation_results <- list()

  for (i in 1:n_external) {
    # Random discovery/validation split (60/40)
    discovery_prop <- 0.6
    discovery_idx <- sample(seq_along(evaluation_data$Y), size = round(discovery_prop * length(evaluation_data$Y)))

    X_discovery <- lapply(evaluation_data$X, function(x) x[discovery_idx, ])
    Y_discovery <- evaluation_data$Y[discovery_idx]

    X_validation <- lapply(evaluation_data$X, function(x) x[-discovery_idx, ])
    Y_validation <- evaluation_data$Y[-discovery_idx]

    tryCatch({
      # Re-train model on discovery set
      validation_diablo <- tune.block.splsda(
        X = X_discovery,
        Y = Y_discovery,
        ncomp = 2,
        test.keepX = list(20, 50, 100),
        design = c(0.1, 0.5, 0.9),
        folds = CV_FOLDS_INNER,
        nrepeat = 1
      )

      tuned_model <- block.splsda(
        X = X_discovery,
        Y = Y_discovery,
        ncomp = 2,
        keepX = validation_diablo$choice.keepX,
        design = validation_diablo$choice.ncomp$design
      )

      # Test on validation set
      val_pred <- predict.diablo(tuned_model, X_validation)
      val_metrics <- evaluate_predictions(val_pred$WeightedPredict[, "comp1"], Y_validation)

      validation_results[[paste0("external_", i)]] <- list(
        discovery_n = length(discovery_idx),
        validation_n = length(Y_validation),
        metrics = val_metrics
      )

      log_info("External validation {i}: Discovery={length(discovery_idx)}, Validation={length(Y_validation)}, AUC={sprintf('%.3f', val_metrics$auc)}")

    }, error = function(e) {
      log_error("External validation {i} failed: {e$message}")
    })
  }

  # Aggregate external validation results
  external_valid <- validation_results[!sapply(validation_results, is.null)]

  if (length(external_valid) > 0) {
    auc_values <- sapply(external_valid, function(x) x$metrics$auc)
    external_summary <- list(
      n_scenarios = length(external_valid),
      auc_mean = mean(auc_values),
      auc_sd = sd(auc_values),
      auc_range = range(auc_values)
    )
  } else {
    external_summary <- NULL
  }

  return(list(
    individual = validation_results,
    summary = external_summary
  ))
}

# ==============================================================================
# PERFORMANCE METRICS CALCULATION
# ==============================================================================

evaluate_predictions <- function(predictions, true_labels) {
  #' Calculate comprehensive performance metrics

  # Convert to probabilities if needed (assuming predictions are decision values)
  if (is.numeric(predictions) && length(unique(predictions)) > 2) {
    # Convert decision values to probabilities using logistic scaling
    pred_probs <- 1 / (1 + exp(-predictions))
  } else if (is.factor(predictions)) {
    pred_probs <- as.numeric(predictions == "Success")
  } else {
    pred_probs <- predictions
  }

  # Convert true labels to binary
  true_binary <- as.numeric(true_labels == "Success")

  # ROC analysis
  roc_obj <- tryCatch(
    roc(true_binary, pred_probs, levels = c(0, 1), direction = "<"),
    error = function(e) {
      log_warn("ROC calculation failed: {e$message}")
      return(NULL)
    }
  )

  # AUPRC calculation
  auprc <- tryCatch(
    pr.curve(scores.class0 = pred_probs, weights.class0 = 1 - true_binary)$auc.integral,
    error = function(e) {
    }
  )

  # Classification metrics at optimal threshold
  if (!is.null(roc_obj)) {
    optimal_coords <- coords(roc_obj, "best", ret = c("threshold", "sensitivity", "specificity"))

    pred_classes <- as.numeric(pred_probs >= optimal_coords["threshold"])
    conf_matrix <- table(pred_classes, true_binary)

    if (nrow(conf_matrix) > 1 && ncol(conf_matrix) > 1) {
      accuracy <- sum(diag(conf_matrix)) / sum(conf_matrix)
      sensitivity <- conf_matrix[2, 2] / sum(conf_matrix[, 2])
      specificity <- conf_matrix[1, 1] / sum(conf_matrix[, 1])
    } else {
      accuracy <- sensitivity <- specificity <- NA
    }
  } else {
    accuracy <- sensitivity <- specificity <- NA
  }

  # Brier score
  brier_score <- mean((pred_probs - true_binary)^2)

  return(list(
    auc = if (!is.null(roc_obj)) auc(roc_obj) else NA,
    auprc = auprc,
    accuracy = accuracy,
    sensitivity = sensitivity,
    specificity = specificity,
    brier_score = brier_score,
    roc_data = if (!is.null(roc_obj)) data.frame(
      fpr = 1 - roc_obj$specificities,
      tpr = roc_obj$sensitivities
    ) else NULL
  ))
}

generate_decision_curves <- function(predictions, true_labels, thresholds = seq(0.1, 0.9, 0.1)) {
  #' Generate decision curve analysis for clinical utility

  log_info("Generating decision curve analysis")

  pred_probs <- 1 / (1 + exp(-predictions))
  true_binary <- as.numeric(true_labels == "Success")

  decision_points <- data.frame()

  for (thresh in thresholds) {
    pred_classes <- as.numeric(pred_probs >= thresh)
    conf_matrix <- table(pred_classes, true_binary)

    if (nrow(conf_matrix) > 1 && ncol(conf_matrix) > 1) {
      tn <- conf_matrix[1, 1]
      tp <- conf_matrix[2, 2]
      fn <- conf_matrix[1, 2]
      fp <- conf_matrix[2, 1]

      net_benefit <- (tp / sum(true_binary)) - (fp / sum(1 - true_binary)) * (thresh / (1 - thresh))
      true_pos_rate <- tp / (tp + fn)

      decision_points <- rbind(decision_points, data.frame(
        threshold = thresh,
        net_benefit = net_benefit,
        treat_all = true_pos_rate - 1 + thresh,
        treat_none = 0
      ))
    }
  }

  return(decision_points)
}

# ==============================================================================
# MULTI-OMICS FEATURE IMPORTANCE
# ==============================================================================

analyze_feature_importance <- function(diablo_model, evaluation_data, n_top = 20) {
  #' Analyze feature importance across omics layers

  log_info("Analyzing multi-omics feature importance")

  feature_importance <- list()

  tryCatch({
    for (omics_name in names(evaluation_data$X)) {
      # Get selected variables for this omics layer
      selected_vars <- selectVar(diablo_model, block = omics_name, comp = 1)$names

      if (length(selected_vars) > 0) {
        # Calculate feature loadings (most important)
        loadings <- diablo_model$loadings[[omics_name]][selected_vars, ]

        # Sort by absolute loading
        feature_importance[[omics_name]] <- data.frame(
          feature = selected_vars,
          loading_comp1 = abs(loadings[, 1]),
          loading_comp2 = abs(loadings[, 2])
        ) %>%
          arrange(desc(loading_comp1 + loading_comp2)) %>%
          head(n_top)

        log_info("{omics_name}: top {nrow(feature_importance[[omics_name]])} features identified")
      }
    }

    # Overall omics contribution
    omics_contribution <- sapply(names(evaluation_data$X), function(omics_name) {
      length(diablo_model$names$blocks[[omics_name]]) / length(unlist(diablo_model$names$blocks))
    })
    names(omics_contribution) <- names(evaluation_data$X)

    return(list(
      feature_importance = feature_importance,
      omics_contribution = omics_contribution
    ))

  }, error = function(e) {
    log_error("Feature importance analysis failed: {e$message}")
    return(NULL)
  })
}

# ==============================================================================
# VISUALIZATION FUNCTIONS
# ==============================================================================

create_validation_plots <- function(cv_results, external_results, feature_analysis) {
  #' Create comprehensive validation visualization suite

  plots <- list()

  tryCatch({
    # 1. CV performance summary
    cv_summary <- cv_results$summary
    plots$cv_performance <- ggplot(cv_summary, aes(x = metric, y = mean)) +
      geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7) +
      geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), width = 0.2) +
      labs(title = "Cross-validation Performance (mean ± SD)",
           y = "Performance", x = "Metric") +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))

    # 2. External validation comparison
    if (!is.null(external_results$summary)) {
      ext_data <- data.frame(
        scenario = paste0("External ", 1:external_results$summary$n_scenarios),
        auc = sapply(external_results$individual, function(x) x$metrics$auc)
      )

      plots$external_validation <- ggplot(ext_data, aes(x = scenario, y = auc)) +
        geom_bar(stat = "identity", fill = "darkgreen", alpha = 0.7) +
        geom_hline(yintercept = cv_results$aggregated$auc["mean"], color = "red", linetype = "dashed") +
        labs(title = "External Validation AUC vs CV Performance",
             subtitle = glue("Red line = CV mean (AUC = {sprintf('%.3f', cv_results$aggregated$auc['mean'])})"),
             y = "AUC") +
        theme_minimal()
    }

    # 3. Omics contribution plot
    if (!is.null(feature_analysis)) {
      contrib_data <- data.frame(
        omics = names(feature_analysis$omics_contribution),
        contribution = feature_analysis$omics_contribution
      )

      plots$omics_contribution <- ggplot(contrib_data, aes(x = reorder(omics, contribution), y = contribution)) +
        geom_bar(stat = "identity", fill = "purple", alpha = 0.7) +
        coord_flip() +
        labs(title = "Omics Layer Contributions", x = "Omics Type", y = "Relative Contribution") +
        theme_minimal()
    }

    # 4. Feature importance plot (aggregate across omics)
    if (!is.null(feature_analysis$feature_importance)) {
      all_features <- do.call(rbind, lapply(names(feature_analysis$feature_importance), function(omics) {
        df <- feature_analysis$feature_importance[[omics]]
        if (!is.null(df)) {
          df$omics <- omics
          return(head(df, 5))  # Top 5 per omics
        }
        return(NULL)
      }))

      if (!is.null(all_features) && nrow(all_features) > 0) {
        plots$feature_importance <- ggplot(all_features, aes(x = reorder(feature, loading_comp1), y = loading_comp1, fill = omics)) +
          geom_bar(stat = "identity", alpha = 0.8) +
          coord_flip() +
          labs(title = "Top Multi-Omics Features", x = "Feature", y = "Absolute Loading") +
          theme_minimal() +
          theme(legend.position = "top")
      }
    }

    log_info("Generated {length(plots)} validation plots")

    return(plots)

  }, error = function(e) {
    log_error("Plot generation failed: {e$message}")
    return(plots)
  })
}

# ==============================================================================
# SAVE VALIDATION RESULTS
# ==============================================================================

save_validation_results <- function(cv_results, external_results, feature_analysis) {
  #' Save all validation results

  dir.create(RESULTS_DIR, recursive = TRUE, showWarnings = FALSE)

  # Save results objects
  saveRDS(cv_results, file.path(RESULTS_DIR, "cv_results.rds"))
  saveRDS(external_results, file.path(RESULTS_DIR, "external_validation.rds"))
  saveRDS(feature_analysis, file.path(RESULTS_DIR, "feature_analysis.rds"))

  # Generate and save plots
  validation_plots <- create_validation_plots(cv_results, external_results, feature_analysis)

  if (length(validation_plots) > 0) {
    ggexport(validation_plots, filename = file.path(RESULTS_DIR, "validation_plots.pdf"), verbose = FALSE)
  }

  # Create validation summary report
  validation_summary <- sprintf("
MDR-TB Multi-Omics Validation Report
===================================

Cross-validation (Nested %d×%d):
- AUC: %.3f ± %.3f (n=%d folds)
- AUPRC: %.3f ± %.3f
- Accuracy: %.3f ± %.3f

External Validation (%d scenarios):
- AUC range: %.3f - %.3f
- Mean AUC: %.3f ± %.3f

Omics Contributions:
%s

Generated: %s

Recommendations:
- Model appears %s (AUC > 0.8 recommended for clinical use)
- Top predictive features identified in each omics layer
- External validation shows %s generalizability
",
  CV_FOLDS_OUTER, CV_FOLDS_INNER,
  cv_results$aggregated$auc["mean"], cv_results$aggregated$auc["sd"], cv_results$aggregated$auc["n"],
  cv_results$aggregated$auprc["mean"], cv_results$aggregated$auprc["sd"],
  cv_results$aggregated$accuracy["mean"], cv_results$aggregated$accuracy["sd"],
  external_results$summary$n_scenarios,
  external_results$summary$auc_range[1], external_results$summary$auc_range[2],
  external_results$summary$auc_mean, external_results$summary$auc_sd,
  paste(names(feature_analysis$omics_contribution),
        sprintf("%.1f%%", feature_analysis$omics_contribution * 100), collapse = ", "),
  format(Sys.time()),
  ifelse(cv_results$aggregated$auc["mean"] > 0.8, "promising", "needs improvement"),
  ifelse(external_results$summary$auc_sd < 0.1, "strong", "moderate")
  )

  writeLines(validation_summary, file.path(RESULTS_DIR, "validation_report.txt"))

  log_info("Validation results saved to: {RESULTS_DIR}")
  log_info("Model validation: AUC = {sprintf('%.3f', cv_results$aggregated$auc['mean'])} (±{sprintf('%.3f', cv_results$aggregated$auc['sd'])})")
}

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

main <- function() {
  #' Main validation workflow

  tryCatch({
    log_info("Starting MDR-TB multi-omics validation pipeline")

    # Load trained models and data
    trained_models <- load_trained_models()
    evaluation_data <- load_evaluation_data()

    if (is.null(trained_models) || is.null(evaluation_data)) {
      return(invisible(FALSE))
    }

    # Perform nested cross-validation
    cv_results <- perform_nested_cv(trained_models$diablo$final, evaluation_data$X, evaluation_data$Y)
    if (is.null(cv_results)) return(invisible(FALSE))

    # Perform external validation
    external_results <- simulate_external_validation(trained_models$diablo$final, evaluation_data)
    if (is.null(external_results)) return(invisible(FALSE))

    # Analyze feature importance
    feature_analysis <- analyze_feature_importance(trained_models$diablo$final, evaluation_data)

    # Save all validation results
    save_validation_results(cv_results, external_results, feature_analysis)

    log_info("Validation pipeline completed successfully ✅")
    log_info("Final AUC: CV = {sprintf('%.3f', cv_results$aggregated$auc['mean'])}, External = {sprintf('%.3f', external_results$summary$auc_mean)}")

  }, error = function(e) {
    log_error("Validation failed: {e$message}")
    return(invisible(FALSE))
  })

  return(invisible(TRUE))
}

# Execute if run as script
if (!interactive()) {
  main()
}

log_info("03_external_validation.R loaded successfully - call main() to run comprehensive validation")
# ==============================================================================
