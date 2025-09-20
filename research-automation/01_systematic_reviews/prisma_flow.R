#!/usr/bin/env Rscript
# PRISMA 2020 flow diagram

suppressPackageStartupMessages({
  library(PRISMA2020)
  library(jsonlite)
  library(optparse)
})

option_list <- list(
  make_option("--counts", type="character", help="JSON with PRISMA counts"),
  make_option("--out", type="character", help="Output HTML file")
)

opt <- parse_args(OptionParser(option_list=option_list))

# Example JSON structure: { "identified": 1000, "duplicates": 200, "screened": 800, "excluded": 600, "included": 200 }
counts <- fromJSON(opt$counts)

diagram <- PRISMA_flowdiagram(
  data = data.frame(
    database_results = counts$identified,
    duplicates_removed = counts$duplicates,
    records_screened = counts$screened,
    records_excluded = counts$excluded,
    studies_included = counts$included
  ),
  interactive = TRUE
)

htmlwidgets::saveWidget(diagram, opt$`out`, selfcontained=TRUE)
cat("✅ PRISMA diagram saved to", opt$`out`, "\n")
