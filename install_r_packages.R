# ===========================
# R PACKAGE INSTALLER SCRIPT
# For VS Code + Research + NMA + Automation
# ===========================

# 1️⃣  Core utilities
install.packages(c(
  "tidyverse",      # data wrangling, visualization
  "data.table",     # fast data handling
  "readxl", "openxlsx",  # Excel IO
  "here", "fs",     # project paths
  "janitor",        # clean variable names
  "lubridate",      # date/time
  "stringr", "glue" # string utilities
))

# 2️⃣  Systematic reviews & Meta-analysis
install.packages(c(
  "meta",           # classical meta-analysis
  "metafor",        # advanced meta-analysis models
  "netmeta",        # network meta-analysis
  "gemtc",          # Bayesian NMA (MCMC)
  "BUGSnet",        # user-friendly Bayesian NMA
  "robumeta",       # robust variance estimation
  "dmetar",         # companion for meta-analysis diagnostics
  "mada",           # diagnostic test meta-analysis
  "metagear"        # screening tool for systematic reviews
))

# 3️⃣  Evidence synthesis visualization
install.packages(c(
  "forestplot", "funnelR", "ggpubr", "plotly",
  "igraph", "ggraph", "visNetwork",
  "ComplexHeatmap", "corrplot", "RColorBrewer"
))

# 4️⃣  Bayesian modeling and MCMC
install.packages(c(
  "rjags", "R2jags", "coda", "bayesplot", "brms"
))

# 5️⃣  Automation and reproducibility
install.packages(c(
  "rmarkdown", "knitr", "bookdown", "quarto",
  "renv", "devtools", "usethis", "pak"
))

# 6️⃣  APIs, scraping, and integration
install.packages(c(
  "httr", "jsonlite", "xml2", "rvest", "RSelenium", "curl"
))

# 7️⃣  Text mining & AI augmentation
install.packages(c(
  "tm", "quanteda", "tidytext", "text2vec", "wordcloud", "topicmodels"
))

# 8️⃣  Machine learning (optional for modeling)
install.packages(c(
  "caret", "tidymodels", "randomForest", "xgboost", "glmnet", "ranger"
))

# 9️⃣  Geospatial & Epidemiology (Community Medicine relevance)
install.packages(c(
  "sf", "tmap", "sp", "raster", "leaflet",
  "epitools", "Epi", "incidence", "surveillance", "outbreaks"
))

# 🔟  Quality-of-life & automation utilities
install.packages(c(
  "beepr", "progress", "future", "parallel", "furrr"
))

# 11️⃣  Optional advanced meta-analysis from GitHub
if(!require(remotes)) install.packages("remotes")
remotes::install_github("guido-s/meta", upgrade="never")
remotes::install_github("MathiasHarrer/dmetar", upgrade="never")
remotes::install_github("dmetar/BUGSnet", upgrade="never")

# ===========================
# DONE
message("✅ All research-related R packages installed successfully.")
