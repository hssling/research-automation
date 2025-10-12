#!/usr/bin/env Rscript
# Deduplication and Screening using revtools

suppressPackageStartupMessages({
  library(revtools)
  library(optparse)
})

option_list <- list(
  make_option("--in", type="character", help="Input file (PubMed CSV)"),
  make_option("--out", type="character", help="Output RDS/CSV file"),
  make_option("--screen", action="store_true", default=FALSE, help="Launch screening interface"),
  make_option("--export-extraction", type="character", default=NULL, help="Path to export extraction sheet")
)

opt <- parse_args(OptionParser(option_list=option_list))

if (!is.null(opt$`in`)) {
  df <- read_bibliography(opt$`in`)
}

if (opt$screen) {
  cat("Launching screening tool...\n")
  result <- start_screening(df)
  saveRDS(result, opt$`out`)
} else if (!is.null(opt$`export-extraction`)) {
  template <- data.frame(
    StudyID = df$label,
    Author = df$author,
    Year = df$year,
    Outcome = NA,
    EffectSize = NA,
    Notes = NA
  )
  write.csv(template, opt$`export-extraction`, row.names = FALSE)
  cat("✅ Extraction template saved.\n")
} else {
  deduped <- find_duplicates(df)
  write_bibliography(deduped, file = opt$`out`)
  cat("✅ Deduplicated dataset saved.\n")
}
