# ==============================================================================
# MDR-TB Multi-Omics Integration Pipeline Makefile
# Phase 4 Advanced Multi-Omics Analysis
# ==============================================================================

.PHONY: all rnaseq microbiome mtb_wgs harmonize integrate validate report clean help

# Configuration
NFCORE_PROFILE ?= docker
NEXTFLOW_OPTS ?= -resume
RSCRIPT_OPTS ?= --vanilla

# ==============================================================================
# MAIN TARGETS
# ==============================================================================

all: report
	@echo "✅ MDR-TB multi-omics pipeline completed successfully!"
	@echo "📊 Results saved to: 04_omics_advanced/mdrtb/results/"
	@echo "📄 Final report: 04_omics_advanced/mdrtb/results/integration_report.html"

# ==============================================================================
# NF-CORE PIPELINES (Data Processing)
# ==============================================================================

rnaseq: init
	@echo "🔬 Running nf-core/rnaseq for host transcriptomics..."
	nextflow run nf-core/rnaseq \
		-profile $(NFCORE_PROFILE) \
		--input rnaseq/samplesheet.csv \
		--outdir results/rnaseq \
		--genome GRCh38 \
		--gencode \
		--aligner star \
		--pseudo_aligner salmon \
		$(NEXTFLOW_OPTS)
	@echo "✅ RNA-seq pipeline completed"

microbiome: init
	@echo "🦠 Running nf-core/ampliseq for microbiome profiling..."
	nextflow run nf-core/ampliseq \
		-profile $(NFCORE_PROFILE) \
		--input microbiome/metadata.tsv \
		--outdir results/microbiome \
		--classifier "rdp=species,decipher=ssu" \
		--trunclen 230,200 \
		--trunc_q 25,25 \
		$(NEXTFLOW_OPTS)
	@echo "✅ Microbiome pipeline completed"

mtb_wgs: init
	@echo "🦠 Running nf-core/bacterialwgs for MTB genomics..."
	nextflow run nf-core/bacterialwgs \
		-profile $(NFCORE_PROFILE) \
		--input mtb_wgs/samplesheet.csv \
		--outdir results/mtb_wgs \
		--genome 'NC_000962.3' \
		--variant_calling \
		$(NEXTFLOW_OPTS)
	@echo "✅ MTB WGS pipeline completed"

# ==============================================================================
# R INTEGRATION PIPELINE
# ==============================================================================

harmonize: rnaseq microbiome mtb_wgs
	@echo "🔗 Running clinical data harmonization..."
	Rscript $(RSCRIPT_OPTS) integration/00_harmonize_clinical.R
	@echo "✅ Clinical harmonization completed"

integrate: harmonize
	@echo "🧬 Running multi-omics matrix construction..."
	Rscript $(RSCRIPT_OPTS) integration/01_make_matrices.R
	@echo "🧠 Running DIABLO integration and ML modeling..."
	Rscript $(RSCRIPT_OPTS) integration/02_integration_models.R
	@echo "📊 Running external validation..."
	Rscript $(RSCRIPT_OPTS) integration/03_external_validation.R
	@echo "✅ Integration and modeling completed"

validate: integrate
	@echo "📊 Validation pipelines already included in integrate step"

# ==============================================================================
# REPORTING
# ==============================================================================

report: integrate
	@echo "📊 Generating final integration report..."
	quarto render notebooks/integration.qmd --to html --output-dir results --output integration_report.html
	@echo "✅ Report generated: results/integration_report.html"

# ==============================================================================
# UTILITY TARGETS
# ==============================================================================

init:
	@echo "🏗️ Initializing MDR-TB pipeline directories..."
	mkdir -p results/{rnaseq,microbiome,mtb_wgs,models,validation}
	mkdir -p data_raw data_interim data_final/matrices
	@echo "✅ Pipeline initialized"

clean:
	@echo "🧹 Cleaning results directory..."
	rm -rf results/
	mkdir -p results/{rnaseq,microbiome,mtb_wgs,models,validation}
	@echo "✅ Cleaned results directory"

clean-data:
	@echo "🧹 Cleaning intermediate data..."
	rm -rf data_interim/ data_final/
	mkdir -p data_final/matrices
	@echo "✅ Cleaned intermediate data"

help:
	@echo "MDR-TB Multi-Omics Integration Pipeline"
	@echo ""
	@echo "Available targets:"
	@echo "  all          - Run complete pipeline (default)"
	@echo "  rnaseq       - Host transcriptomics (nf-core/rnaseq)"
	@echo "  microbiome   - Microbiome profiling (nf-core/ampliseq)"
	@echo "  mtb_wgs      - MTB genomics (nf-core/bacterialwgs)"
	@echo "  harmonize    - Clinical data harmonization"
	@echo "  integrate    - Multi-omics integration & modeling"
	@echo "  validate     - Cross-validation & external validation"
	@echo "  report       - Generate final Quarto report"
	@echo "  init         - Initialize pipeline directories"
	@echo "  clean        - Clean results while keeping data"
	@echo "  clean-data   - Clean all processed data"
	@echo ""
	@echo "Configuration:"
	@echo "  NFCORE_PROFILE  - nf-core profile (default: docker)"
	@echo "  NEXTFLOW_OPTS   - Nextflow options (default: -resume)"
	@echo "  RSCRIPT_OPTS    - R script options (default: --vanilla)"
	@echo ""
	@echo "Usage:"
	@echo "  make all                    # Complete pipeline"
	@echo "  make rnaseq microbiome      # Only omics processing"
	@echo "  make report                 # Generate report from existing results"

# ==============================================================================
# CONDITIONAL TARGETS (Check for Real Data)
# ==============================================================================

# Try to use real data first, fall back to demo if not available
check-data:
	@if [ -f "rnaseq/samplesheet.csv" ] && [ -f "microbiome/metadata.tsv" ]; then \
		echo "✅ Real data found - using real datasets"; \
	else \
		echo "⚠️  No real data found - will use demo data during integration"; \
	fi

# Enhanced make integrate to handle missing real data
demo-integrate: init check-data
	@echo "🔗 Running MDR-TB multi-omics integration (with fallback to demo data)..."
	@echo "⚠️  Note: If real omics data not available, demo data will be generated"
	Rscript $(RSCRIPT_OPTS) integration/00_harmonize_clinical.R 2>/dev/null || \
		Rscript $(RSCRIPT_OPTS) -e "source('integration/00_harmonize_clinical.R'); generate_demo_clinical(n_patients = 300)"
	Rscript $(RSCRIPT_OPTS) integration/01_make_matrices.R
	Rscript $(RSCRIPT_OPTS) integration/02_integration_models.R
	Rscript $(RSCRIPT_OPTS) integration/03_external_validation.R
	@echo "✅ Integration with demo data completed"

# ==============================================================================
# DEVELOPMENT TARGETS
# ==============================================================================

dry-run: check-data
	@echo "🔍 Performing dry-run validation..."
	@echo "Checking for required files and dependencies..."
	@command -v nextflow >/dev/null 2>&1 || { echo "❌ Nextflow not found"; exit 1; }
	@command -v R >/dev/null 2>&1 || { echo "❌ R not found"; exit 1; }
	@command -v quarto >/dev/null 2>&1 || { echo "❌ Quarto not found"; exit 1; }
	@echo "✅ All dependencies found"
	@echo "✅ Ready for pipeline execution"

# ==============================================================================
# DOCUMENTATION TARGET
# ==============================================================================

readme:
	@echo "# MDR-TB Multi-Omics Integration Pipeline

## Overview
This automated pipeline integrates host transcriptomics, microbiome profiling, and *Mycobacterium tuberculosis* genomics to predict MDR-TB treatment outcomes using DIABLO multi-omics integration and machine learning.

## Pipeline Steps
1. **Clinical Data Harmonization** - Standardize clinical metadata across cohorts
2. **Multi-Omics Matrix Construction** - Process nf-core outputs into integrated matrices
3. **DIABLO Integration & ML Modeling** - Sparse multi-block PLS-DA + ML stacking
4. **External Validation** - Nested cross-validation and external cohort validation
5. **Interactive Reporting** - Generate comprehensive Quarto report

## Quick Start
\`\`\`bash
# Complete pipeline
make all

# Individual components
make rnaseq microbiome mtb_wgs harmonize integrate validate report
\`\`\`

## Dependencies
- Nextflow (nf-core pipelines)
- R 4.1+ (mixOmics, caret, pROC, etc.)
- Quarto (reporting)
- Docker/Singularity (nf-core profiles)

## File Structure
\`\`\`
mdrtb/
├── integration/          # R integration scripts
├── notebooks/           # Quarto reports
├── rnaseq/             # Host transcriptomics
├── microbiome/         # Microbiome profiling
├── mtb_wgs/            # MTB genomics
├── data_*/             # Data processing stages
├── results/            # Output results
└── Makefile           # Pipeline orchestration
\`\`\`
" > README.md

.PHONY: readme

# ==============================================================================
# AUTO-GENERATION NOTE
# ==============================================================================
#
# This Makefile was generated by AI-assisted research automation pipeline.
# It orchestrates a complete multi-omics MDR-TB analysis workflow including:
# - nf-core data processing pipelines
# - R-based statistical integration
# - Machine learning model development
# - External validation and reporting
#
# Pipeline execution: make all
# Generated: $(shell date +"%Y-%m-%d %H:%M:%S")
# ==============================================================================
