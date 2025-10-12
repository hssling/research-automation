.PHONY: all run test clean help

# Microbiome Analysis Pipeline using nf-core/ampliseq
# 16S rRNA amplicon sequencing analysis with DADA2 and QIIME2

# Default target
all: run

# Run the nf-core/ampliseq pipeline
run:
	@echo "🧬 Starting nf-core/ampliseq microbiome pipeline..."
	@echo "📋 Samplesheet: metadata.tsv"
	@echo "📁 Output directory: ../results/microbiome"
	@echo ""
	@echo "⚙️  16S rRNA parameters:"
	@echo "   - Forward primer: GTGCCAGCMGCCGCGGTAA"
	@echo "   - Reverse primer: GGACTACHVGGGTWTCTAAT"
	@echo "   - ASV length: 100-300 bp"
	@echo ""

	# Run the pipeline with Docker
	nextflow run nf-core/ampliseq \
		-profile docker \
		--input metadata.tsv \
		--outdir ../results/microbiome \
		--unite_its \
		-c nextflow.config \
		-resume

	@echo ""
	@echo "✅ Microbiome analysis completed!"
	@echo "📊 Key outputs:"
	@echo "   - ASV table: ../results/microbiome/dada2/ASV_table.tsv"
	@echo "   - Taxonomy: ../results/microbiome/dada2/taxonomy_tsv"
	@echo "   - Diversity: ../results/microbiome/qiime2/diversity"
	@echo "   - MultiQC: ../results/microbiome/multiqc/star_salmon"
	@echo ""

# Quick run with test data
test:
	@echo "🧪 Running microbiome pipeline with test data..."
	nextflow run nf-core/ampliseq \
		-profile docker,test \
		--outdir ../results/microbiome_test \
		-c nextflow.config

# Docker execution (default, local workstation)
docker: PROFILE=docker
docker: run

# Local execution (no containers, requires installed tools)
local: PROFILE=local
local: run

# Singularity execution (local HPC with Singularity)
singularity: PROFILE=singularity
singularity: run

# SLURM HPC cluster execution
slurm: PROFILE=slurm
slurm: run

# LSF HPC cluster execution
lsf: PROFILE=lsf
lsf: run

# SGE/GridEngine HPC cluster execution
sge: PROFILE=sge
sge: run

# Clean results (optional - be careful!)
clean:
	@echo "🧹 Cleaning microbiome results..."
	@echo "⚠️  WARNING: This will delete all output files!"
	@read -p "Are you sure you want to continue? (yes/no): " confirm; \
		if [ "$$confirm" = "yes" ]; then \
			rm -rf ../results/microbiome/*; \
			echo "✅ Results cleaned."; \
		else \
			echo "❌ Operation cancelled."; \
		fi

# Show help
help:
	@echo "Microbiome Analysis Pipeline (nf-core/ampliseq)"
	@echo ""
	@echo "Targets:"
	@echo "  all       - Run the complete microbiome pipeline"
	@echo "  run       - Execute nf-core/ampliseq pipeline"
	@echo "  test      - Run with nf-core test data"
	@echo "  clean     - Remove all results (CAUTION!)"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - Nextflow installed"
	@echo "  - Docker installed and running"
	@echo ""
	@echo "Usage:"
	@echo "  cd 03_omics_single/microbiome"
	@echo "  make all"
	@echo ""
	@echo "Update samples.tsv for your sample metadata"
	@echo "Update nextflow.config for primer sequences"
