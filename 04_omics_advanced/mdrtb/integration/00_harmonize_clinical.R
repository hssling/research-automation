#!/usr/bin/env Rscript
# Joins clinical metadata across cohorts & timepoints, writes a single table.

suppressPackageStartupMessages({
  library(dplyr); library(readr); library(tidyr); library(stringr); library(here)
  library(jsonlite)
})

dir.create(here("04_omics_advanced/mdrtb/data_final"), recursive = TRUE, showWarnings = FALSE)

# ---- EDIT THESE INPUTS (or read from a config.json) ----
clin_paths <- c(
  here("04_omics_advanced/mdrtb/rnaseq/clinical.csv"),
  here("04_omics_advanced/mdrtb/microbiome/clinical.csv"),
  here("04_omics_advanced/mdrtb/mtb_wgs/clinical.csv")
)

# Read and standardize minimal columns
read_std <- function(p){
  readr::read_csv(p, show_col_types = FALSE) %>%
    rename_with(tolower) %>%
    rename(patient_id = any_of(c("patient_id","id","subject_id")),
           sample_id  = any_of(c("sample_id","sample")),
           timepoint  = any_of(c("timepoint","tp"))) %>%
    mutate(across(c(patient_id, sample_id, timepoint), as.character))
}

clin_list <- lapply(clin_paths[file.exists(clin_paths)], read_std)
stopifnot(length(clin_list) > 0)
clin <- bind_rows(clin_list) %>%
  group_by(patient_id) %>%
  arrange(patient_id, timepoint) %>%
  fill(.direction = "downup") %>%
  ungroup()

# Key outcomes & covariates (create placeholders if missing)
needed <- c("patient_id","sample_id","timepoint","age","sex","hiv","diabetes",
            "cavity","lineage","regimen","response_6m","relapse_12m")
for(n in needed) if(!n %in% names(clin)) clin[[n]] <- NA

write_csv(clin, here("04_omics_advanced/mdrtb/data_final/clinical_harmonized.csv"))
cat("✅ clinical_harmonized.csv written\n")
