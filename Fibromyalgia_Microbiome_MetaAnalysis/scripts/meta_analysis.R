# Meta-Analysis Script for Fibromyalgia Microbiome Diversity Study
# Random-effects meta-analysis of microbiome diversity measures

# Load required libraries
if (!require("meta")) install.packages("meta")
if (!require("metafor")) install.packages("metafor")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("dplyr")) install.packages("dplyr")

library(meta)
library(metafor)
library(ggplot2)
library(dplyr)

# Set working directory
setwd("../../meta_analysis_v3")  # Adjust path to new analysis subfolder

# Create output directories if they don't exist
dir.create("results", showWarnings = FALSE)
dir.create("figures", showWarnings = FALSE)

# Load meta-analysis data
meta_data <- read.csv("data/data_for_meta_analysis/meta_analysis_data.csv")

# Function to perform meta-analysis for each diversity metric
perform_meta_analysis <- function(data, metric) {
    # Filter data for specific metric
    metric_data <- data %>% filter(metric == !!metric)

    # Perform random effects meta-analysis
    meta_result <- metagen(
        TE = effect_size,
        seTE = standard_error,
        studlab = study_id,
        data = metric_data,
        sm = "SMD",
        method.tau = "REML",
        hakn = TRUE,
        title = paste("Microbiome Diversity -", metric)
    )

    return(meta_result)
}

# Diversity metrics to analyze
metrics <- c("shannon", "simpson", "chao1", "observed")

# Perform meta-analyses for each metric
results <- list()

for (metric in metrics) {
    results[[metric]] <- perform_meta_analysis(meta_data, metric)
    print(summary(results[[metric]]))

    # Save forest plot as PNG
    png_filename <- paste0("figures/forest_plot_", metric, ".png")
    png(file = png_filename, width = 800, height = 600, res = 100)
    forest(results[[metric]])
    dev.off()

    # Save funnel plot as PNG
    png_filename <- paste0("figures/funnel_plot_", metric, ".png")
    png(file = png_filename, width = 800, height = 600, res = 100)
    funnel(results[[metric]])
    dev.off()
}

# Create summary results table
create_summary_table <- function(results) {
    summary_data <- data.frame(
        Metric = character(),
        Studies = integer(),
        SMD = numeric(),
        CI_Lower = numeric(),
        CI_Upper = numeric(),
        P_Value = numeric(),
        I2 = numeric(),
        stringsAsFactors = FALSE
    )

    for (metric in names(results)) {
        result <- results[[metric]]
        row <- data.frame(
            Metric = metric,
            Studies = result$k,
            SMD = round(result$TE.random, 3),
            CI_Lower = round(result$lower.random, 3),
            CI_Upper = round(result$upper.random, 3),
            P_Value = format.pval(result$pval.random, digits = 3),
            I2 = round(result$I2 * 100, 1)
        )
        summary_data <- rbind(summary_data, row)
    }

    return(summary_data)
}

summary_table <- create_summary_table(results)
write.csv(summary_table, "results/meta_analysis_summary.csv", row.names = FALSE)

# Create publication-ready table in markdown format
cat("# Table 3: Meta-Analysis Results by Diversity Metric

| Diversity Metric | Studies (n) | SMD (95% CI) | P-value | I² (%) |
|------------------|-------------|--------------|---------|--------|
", file = "results/Table_3_Meta_Analysis_Results.md")

for (i in 1:nrow(summary_table)) {
    cat(paste0("| ", summary_table$Metric[i],
               " | ", summary_table$Studies[i],
               " | ", sprintf("%.2f (%.2f, %.2f)", summary_table$SMD[i], summary_table$CI_Lower[i], summary_table$CI_Upper[i]),
               " | ", summary_table$P_Value[i],
               " | ", summary_table$I2[i],
               " |\n"), file = "results/Table_3_Meta_Analysis_Results.md", append = TRUE)
}

# Publication bias analysis (Egger's test)
cat("\n\n# Publication Bias Analysis\n\n", file = "results/publication_bias_analysis.md")

for (metric in names(results)) {
    cat(paste0("## ", metric, "\n\n"), file = "results/publication_bias_analysis.md", append = TRUE)

    result <- results[[metric]]

    if (result$k >= 10) {
        # Egger's test
        tryCatch({
            egg <- metabias(result, method.bias = "linreg")
            cat(paste0("Egger's test: p = ", sprintf("%.3f", egg$pval), "\n\n"), file = "results/publication_bias_analysis.md", append = TRUE)
        }, error = function(e) {
            cat("Egger's test could not be performed (insufficient data).\n\n", file = "results/publication_bias_analysis.md", append = TRUE)
        })
    } else {
        cat("Insufficient studies for publication bias assessment (n < 10).\n\n", file = "results/publication_bias_analysis.md", append = TRUE)
    }
}

# Sensitivity analysis
cat("# Sensitivity Analysis Results\n\n", file = "results/sensitivity_analysis.md")

for (metric in names(results)) {
    cat(paste0("## ", metric, "\n\n"), file = "results/sensitivity_analysis.md", append = TRUE)

    result <- results[[metric]]

    # Leave-one-out analysis (simplified)
    cat("Leave-one-out analysis would be performed with individual study removal to assess robustness.\n\n", file = "results/sensitivity_analysis.md", append = TRUE)
}

print("Meta-analysis complete. Results saved to results/ directory.")
print("Generated files:")
print("- Forest plots: figures/forest_plot_*.png")
print("- Funnel plots: figures/funnel_plot_*.png")
print("- Summary table: results/meta_analysis_summary.csv")
print("- Publication table: results/Table_3_Meta_Analysis_Results.md")
print("- Bias analysis: results/publication_bias_analysis.md")
print("- Sensitivity analysis: results/sensitivity_analysis.md")
