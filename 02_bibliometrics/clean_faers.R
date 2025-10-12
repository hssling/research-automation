#!/usr/bin/env Rscript
"
FAERS Data Cleaner
Process and clean raw FAERS data files
"

# Setup
library(readr)
library(dplyr)
library(purrr)
library(stringr)

# Set working directory to script location
script_dir <- dirname(normalizePath(commandArgs(trailingOnly = FALSE)[grep("--file=", commandArgs(trailingOnly = FALSE))]))
if (length(script_dir) == 0) {
  script_dir <- getwd()
}
setwd(script_dir)

# Create output directory
dir.create("../results/pharmacovigilance", showWarnings = FALSE)
dir.create("clean", showWarnings = FALSE)

message("🧹 Starting FAERS data cleaning...")

# Function to safely read TSV files with proper column types
safe_read_tsv <- function(file_path) {
  tryCatch({
    # First, try to read with automatic column detection
    data <- read_tsv(file_path, col_types = cols(.default = "c"), progress = FALSE)

    # If successful, return data
    message(sprintf("✅ Successfully read: %s (%d rows)", basename(file_path), nrow(data)))
    return(data)

  }, error = function(e) {
    message(sprintf("❌ Error reading %s: %s", basename(file_path), e$message))
    return(NULL)
  })
}

# Clean DRUG files (most critical for pharmacovigilance)
message("\n📊 Processing DRUG files...")

# Find all DRUG files
drug_files <- list.files("raw_faers", pattern = ".*DRUG.*\\.txt$",
                         full.names = TRUE, ignore.case = TRUE)

message(sprintf("📋 Found %d DRUG files to process", length(drug_files)))

if (length(drug_files) == 0) {
  stop("❌ No DRUG files found in raw_faers directory. Please run fetch_faers.py first.")
}

# Process DRUG files
drug_data <- drug_files %>%
  map(safe_read_tsv) %>%
  keep(~ !is.null(.x)) %>%  # Remove failed files
  bind_rows()

if (nrow(drug_data) == 0) {
  stop("❌ No valid DRUG data found after processing files.")
}

# Clean DRUG data
message("🧼 Cleaning DRUG data...")

drug_clean <- drug_data %>%
  # Convert character columns to appropriate types where possible
  mutate(
    primaryid = str_trim(primaryid),
    caseid = str_trim(caseid),
    drug_seq = as.integer(drug_seq),
    role_cod = str_trim(role_cod),
    drugname = str_to_upper(str_trim(drugname)),  # Standardize drug names
    val_vbm = str_trim(val_vbm),
    route = str_trim(route),
    dose_amt = str_trim(dose_amt),
    dose_unit = str_trim(dose_unit),
    dose_form = str_trim(dose_form),
    dose_freq = str_trim(dose_freq),
    lot_num = str_trim(lot_num),
    exp_dt = str_trim(exp_dt),
    # Clean drug names - remove common prefixes/suffixes that interfere with matching
    drugname_clean = str_replace_all(drugname, "(TABS?|CAPS?|ORAL|INJ|IV|IM)\\s*", ""),
    drugname_clean = str_trim(drugname_clean)
  ) %>%
  # Remove rows with missing essential fields
  filter(!is.na(primaryid), !is.na(drugname_clean), drugname_clean != "")

# Save cleaned DRUG data
write_csv(drug_clean, "clean/faers_drug.csv")
message(sprintf("💾 Saved cleaned DRUG data: %d rows, %d columns", nrow(drug_clean), ncol(drug_clean)))

# Optional: Process other FAERS files (REACtions, OUTC comes, etc.)
message("\n📊 Processing REAC files...")

reac_files <- list.files("raw_faers", pattern = ".*REAC.*\\.txt$",
                         full.names = TRUE, ignore.case = TRUE)

if (length(reac_files) > 0) {
  reac_data <- reac_files %>%
    map(safe_read_tsv) %>%
    keep(~ !is.null(.x)) %>%
    bind_rows()

  # Clean REAC data
  reac_clean <- reac_data %>%
    mutate(
      primaryid = str_trim(primaryid),
      pt = str_to_upper(str_trim(pt)),  # Adverse event preferred term
      soc = str_to_upper(str_trim(soc)) # System organ class
    )

  write_csv(reac_clean, "clean/faers_reac.csv")
  message(sprintf("💾 Saved cleaned REAC data: %d rows, %d columns", nrow(reac_clean), ncol(reac_clean)))
}

# Summary
message("\n📈 FAERS Data Cleaning Complete!")
message("📋 Files created in 'clean/' directory:")
message("   - faers_drug.csv: Drug exposure data")
if (length(reac_files) > 0) {
  message("   - faers_reac.csv: Adverse reaction data")
}
message("
🧹 Cleaning completed successfully!")
