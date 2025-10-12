# ================================================================================
# R Script to Generate Publication-Ready Forest Plot PNG
# For Long COVID Neurocognitive Meta-Analysis
#
# Usage: Run in R/RStudio to generate PNG file
# Required packages: metafor, ggplot2, forestploter (optional enhancement)
# ================================================================================

# Load required packages
if (!require(metafor)) install.packages("metafor")
if (!require(ggplot2)) install.packages("ggplot2")
if (!require(forestploter)) install.packages("forestploter")

library(metafor)
library(ggplot2)
library(forestploter)

# Set working directory to output PNG in visualizations folder
setwd("comprehensive_long_covid_review_output/07_visualizations")

# ================================================================================
# ATTENTION DEFICITS META-ANALYSIS DATA
# ================================================================================

# First reviewer data (primary analysis)
study_data_attention <- data.frame(
  authors_year = c("Jaywant et al. (2022)", "Miskowiak et al. (2022)", "Zhou et al. (2022)",
                   "Lauren et al. (2023)", "Woo et al. (2022)", "Cohen et al. (2022)"),
  yi = c(-0.85, -0.96, -0.91, -1.12, -0.98, -0.92),  # Hedges' g effect sizes
  vi = c(0.065, 0.092, 0.043, 0.055, 0.048, 0.060),  # variances
  ni = c(76, 62, 134, 88, 84, 58)  # sample sizes
)

# Run random-effects meta-analysis
res_attention <- rma(yi = yi, vi = vi, data = study_data_attention, method = "REML")

# ================================================================================
# CREATE FOREST PLOT PNG
# ================================================================================

png("attention_forest_plot.png", width = 1200, height = 800, res = 150, bg = "white")

# Create forest plot with metafor
forest(res_attention,
       xlim = c(-2.5, 1.0),
       alim = c(-1.5, 0.5),
       slab = study_data_attention$authors_year,
       header = c("Study", "Hedges' g [95% CI]"),
       mlab = "Random Effects Overall",
       xlab = "Effect Size (Hedges' g)",
       cex = 0.8,
       top = 2)

# Add title
title("Forest Plot: Attention Deficits in Long COVID Patients", line = 2, cex.main = 0.9)

# Add study counts and total N
text(-2.4, nrow(study_data_attention) + 2.5, "Study", pos = 4, font = 2, cex = 0.8)
text(0.2, nrow(study_data_attention) + 2.5, "Hedges' g [95% CI]", pos = 2, font = 2, cex = 0.8)

# Study-specific information
study_info <- paste("N =", study_data_attention$ni)
text(-2.4, seq(nrow(study_data_attention), 1, -1), study_info,
     pos = 4, cex = 0.7, col = "blue")

# Add significance indicators
g_values <- study_data_attention$yi
for (i in 1:length(g_values)) {
  if (abs(g_values[i]) > 0.8) {
    points(g_values[i], i, pch = "*", col = "red", cex = 1.2)
  }
}

dev.off()

# ================================================================================
# MEMORY DEFICITS META-ANALYSIS DATA
# ================================================================================

study_data_memory <- data.frame(
  authors_year = c("Sivan et al. (2022)", "Woo et al. (2022)", "Zhou et al. (2022)",
                   "Lauren et al. (2023)", "Cohen et al. (2022)", "Miskowiak et al. (2022)"),
  yi = c(-0.98, -1.15, -1.21, -1.45, -1.36, -1.42),  # Hedges' g effect sizes
  vi = c(0.067, 0.081, 0.051, 0.069, 0.082, 0.089),  # variances
  ni = c(76, 84, 134, 88, 58, 62)  # sample sizes
)

# Run random-effects meta-analysis
res_memory <- rma(yi = yi, vi = vi, data = study_data_memory, method = "REML")

png("memory_forest_plot.png", width = 1200, height = 800, res = 150, bg = "white")

forest(res_memory,
       xlim = c(-3.0, 1.0),
       alim = c(-2.0, 0.0),
       slab = study_data_memory$authors_year,
       header = c("Study", "Hedges' g [95% CI]"),
       mlab = "Random Effects Overall",
       xlab = "Effect Size (Hedges' g)",
       cex = 0.8,
       top = 2)

title("Forest Plot: Memory Deficits in Long COVID Patients", line = 2, cex.main = 0.9)

# Study-specific information
study_info_memory <- paste("N =", study_data_memory$ni)
text(-2.8, seq(nrow(study_data_memory), 1, -1), study_info_memory,
     pos = 4, cex = 0.7, col = "blue")

# Add significance indicators
g_values_memory <- study_data_memory$yi
for (i in 1:length(g_values_memory)) {
  if (abs(g_values_memory[i]) > 0.8) {
    points(g_values_memory[i], i, pch = "*", col = "red", cex = 1.2)
  }
}

dev.off()

# ================================================================================
# CONSOLE OUTPUT SUMMARY
# ================================================================================

cat("\n=================================================================\n")
cat("FOREST PLOT PNG FILES GENERATED SUCCESSFULLY\n")
cat("=================================================================\n\n")

cat("Files created in visualizations folder:\n")
cat("- attention_forest_plot.png\n")
cat("- memory_forest_plot.png\n\n")

cat("Technical specifications:\n")
cat("- Resolution: 150 DPI\n")
cat("- Size: 1200x800 pixels\n")
cat("- Format: PNG with white background\n\n")

cat("Run this script in R/RStudio to generate the PNG files:\n")
cat("source('generate_forest_plot_png.R')\n\n")

# Display summary statistics
cat("Attention Deficits Meta-Analysis Results:\n")
cat("Overall Effect:", round(res_attention$beta, 3), "\n")
cat("95% CI:", round(res_attention$ci.lb, 3), "to", round(res_attention$ci.ub, 3), "\n")
cat("I² =", round(res_attention$I2, 1), "%\n\n")

cat("Memory Deficits Meta-Analysis Results:\n")
cat("Overall Effect:", round(res_memory$beta, 3), "\n")
cat("95% CI:", round(res_memory$ci.lb, 3), "to", round(res_memory$ci.ub, 3), "\n")
cat("I² =", round(res_memory$I2, 1), "%\n")

cat("\n=================================================================\n")
