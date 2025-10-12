# Install R packages required for Type 2 Diabetes Drug Sequencing NMA

# List of required packages
required_packages <- c(
  "gemtc",        # GeMTC for network meta-analysis
  "rjags",        # JAGS interface for Bayesian analysis
  "coda",         # MCMC output analysis
  "ggplot2",      # Visualization
  "dplyr",        # Data manipulation
  "readr",        # CSV reading
  "tidyr",        # Data tidying
  "metafor",      # Additional meta-analysis tools
  "netmeta",      # Alternative NMA package
  "pcnetmeta",    # Another NMA package option
  "devtools"      # For installing packages from GitHub if needed
)

# Function to install packages if not already installed
install_if_missing <- function(package) {
  if (!require(package, character.only = TRUE)) {
    install.packages(package, dependencies = TRUE)
    library(package, character.only = TRUE)
  }
}

# Install CRAN packages
cat("Installing CRAN packages...\n")
for (package in required_packages) {
  tryCatch({
    install_if_missing(package)
    cat("✓", package, "installed/loaded successfully\n")
  }, error = function(e) {
    cat("✗ Failed to install", package, ":", e$message, "\n")
  })
}

# Install JAGS if not available (required for rjags)
cat("\nChecking for JAGS installation...\n")
jags_available <- tryCatch({
  require(rjags)
  cat("✓ JAGS is available\n")
  TRUE
}, error = function(e) {
  cat("! JAGS not found. Please install JAGS from https://mcmc-jags.sourceforge.io/\n")
  FALSE
})

# Verify key packages for NMA
cat("\nVerifying key NMA packages...\n")

if (require(gemtc)) {
  cat("✓ GeMTC loaded successfully\n")
} else {
  cat("✗ GeMTC failed to load\n")
}

if (require(netmeta)) {
  cat("✓ netmeta loaded successfully\n")
} else {
  cat("✗ netmeta failed to load\n")
}

# Create package status report
package_status <- data.frame(
  package = required_packages,
  status = sapply(required_packages, function(p) {
    tryCatch({
      require(p, character.only = TRUE)
      "Available"
    }, error = function(e) {
      "Failed"
    })
  })
)

write_csv(package_status, "03_statistical_analysis/package_status.csv")

cat("\n=== PACKAGE INSTALLATION SUMMARY ===\n")
print(package_status)

if (jags_available) {
  cat("\n✓ Ready for Bayesian network meta-analysis!\n")
} else {
  cat("\n! Please install JAGS to run Bayesian NMA\n")
  cat("  Download from: https://mcmc-jags.sourceforge.io/\n")
}

cat("\nPackage installation check complete.\n")
