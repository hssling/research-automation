#!/usr/bin/env Rscript
# Meta-analysis using metafor

suppressPackageStartupMessages({
  library(metafor)
  library(optparse)
})

option_list <- list(
  make_option("--in", type="character", help="Input CSV with extracted data"),
  make_option("--out", type="character", help="Output folder")
)

opt <- parse_args(OptionParser(option_list=option_list))

data <- read.csv(opt$`in`)

# Example: assuming EffectSize and SE columns exist
res <- rma(yi = data$EffectSize, sei = data$SE, method="REML")

# Forest plot
png(file.path(opt$`out`, "forest.png"), width=800, height=600)
forest(res, slab = paste(data$Author, data$Year))
dev.off()

# Funnel plot
png(file.path(opt$`out`, "funnel.png"), width=800, height=600)
funnel(res)
dev.off()

write.csv(summary(res)$coefficients, file.path(opt$`out`, "meta_results.csv"))
cat("✅ Meta-analysis complete. Results saved to", opt$`out`, "\n")
