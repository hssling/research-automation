# =======================================================================================
# Package Installation Script for Antibiotic Consumption Meta-Analysis
# =======================================================================================
# This script installs all required R packages for the antibiotic consumption project
# Run this once at the beginning of your R session

# Check if pacman is available for easier package management
if (!requireNamespace("pacman", quietly = TRUE)) {
  install.packages("pacman")
}

# Load pacman for package management
library(pacman)

# Install/update core meta-analysis packages
pacman::p_install_version("meta", "7.0-0")        # Core meta-analysis functions
pacman::p_install_version("metafor", "4.6-0")     # Advanced meta-analysis & meta-regression
pacman::p_install_version("netmeta", "2.9-0")     # Network meta-analysis
pacman::p_install_version("dmetar", "1.0.0")      # Meta-analysis helper functions

# Install data manipulation and I/O packages
pacman::p_install_version("openxlsx", "4.2.5")    # Excel file reading/writing
pacman::p_install_version("readxl", "1.4.3")      # Alternative Excel reading
pacman::p_install_version("haven", "2.5.4")       # SPSS/Stata file support

# Install visualization packages
pacman::p_install_version("ggplot2", "3.5.1")     # Advanced plotting
pacman::p_install_version("ggpubr", "0.6.0")      # Publication-ready plots
pacman::p_install_version("gridExtra", "2.3")     # Multiple plot layout
pacman::p_install_version("forestplot", "3.1.3")  # Enhanced forest plots
pacman::p_install_version("ggforestplot", "0.1.2") # ggplot2-based forest plots

# Install statistical packages
pacman::p_install_version("lme4", "1.1-35.1")     # Linear mixed effects (if needed)
pacman::p_install_version("nlme", "3.1-164")      # Non-linear mixed effects
pacman::p_install_version("clubSandwich", "0.5.10") # Robust variance estimation

# Install reporting and document generation
pacman::p_install_version("knitr", "1.46")        # Dynamic report generation
pacman::p_install_version("rmarkdown", "2.26")    # R Markdown documents
pacman::p_install_version("officer", "0.6.5")     # Word document creation
pacman::p_install_version("flextable", "0.9.5")   # Publication tables

# Install utility packages
pacman::p_install_version("tidyverse", "2.0.0")   # Data manipulation suite
pacman::p_install_version("janitor", "2.2.0")     # Data cleaning
pacman::p_install_version("here", "1.0.1")        # Project-relative paths

# Check for conflicts and load required libraries
conflicts_detail <- pacman::p_conflicts()

if (length(conflicts_detail) > 0) {
  message("Package conflicts detected. Consider loading packages in order of priority.")
}

# Load core packages for immediate use
packages_to_load <- c("meta", "metafor", "netmeta", "dmetar",
                      "openxlsx", "ggplot2", "ggpubr", "tidyverse")

lapply(packages_to_load, function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    warning(paste("Failed to install/load package:", pkg))
  } else {
    library(pkg, character.only = TRUE, quietly = TRUE)
    message(paste("Loaded package:", pkg))
  }
})

# Verify installation
message("
=== PACKAGE INSTALLATION SUMMARY ===")
message("Core meta-analysis packages:")
message("- meta: ", packageVersion("meta"))
message("- metafor: ", packageVersion("metafor"))
message("- netmeta: ", packageVersion("netmeta"))
message("- dmetar: ", packageVersion("dmetar"))

message("
Data and visualization packages:")
message("- openxlsx: ", packageVersion("openxlsx"))
message("- ggplot2: ", packageVersion("ggplot2"))
message("- ggpubr: ", packageVersion("ggpubr"))
message("- tidyverse: ", packageVersion("tidyverse"))

message("
R version: ", R.version$version.string)
message("Installation completed at: ", Sys.time())

# Clean up
rm(packages_to_load, conflicts_detail)

# Optional: Update all installed packages (uncomment if needed)
# update.packages(ask = FALSE, checkBuilt = TRUE)
