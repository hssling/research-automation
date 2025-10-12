.PHONY: all docker run test clean help

# RNA-seq Analysis Pipeline using nf-core/rnaseq
# Automated RNA-seq quantification with differential expression analysis

# Default target
all: docker

# Run the nf-core/rnaseq pipeline with different execution profiles
run:
	@echo "🚀 Starting nf-core/rnaseq pipeline..."
	@echo "📋 Samplesheet: samplesheet.csv"
	@echo "📁 Output directory: ../results/rnaseq"
	@echo ""

	# Run the pipeline with specified profile (default: docker)
	nextflow run nf-core/rnaseq \
		-profile ${PROFILE} \
		--input samplesheet.csv \
		--outdir ../results/rnaseq \
		-c nextflow.config \
		-resume

	@echo ""
	@echo "✅ RNA-seq analysis completed!"
	@echo "📊 Key outputs:"
	@echo "   - DESeq2 results: ../results/rnaseq/star_salmon/deseq2"
	@echo "   - MultiQC report: ../results/rnaseq/multiqc/star_salmon"
	@echo "   - Salmon quantification: ../results/rnaseq/salmon"
	@echo ""

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
	@echo "🧹 Cleaning RNA-seq results..."
	@echo "⚠️  WARNING: This will delete all output files!"
	@read -p "Are you sure you want to continue? (yes/no): " confirm; \
		if [ "$$confirm" = "yes" ]; then \
			rm -rf ../results/rnaseq/*; \
			echo "✅ Results cleaned."; \
		else \
			echo "❌ Operation cancelled."; \
		fi

# Show help
help:
	@echo "RNA-seq Analysis Pipeline (nf-core/rnaseq)"
	@echo ""
	@echo "Targets:"
	@echo "  all       - Run pipeline with Docker (default)"
	@echo "  docker    - Run with Docker containers"
	@echo "  local     - Run without containers (requires installed tools)"
	@echo "  singularity - Run with Singularity containers"
	@echo "  slurm     - Run on SLURM HPC cluster"
	@echo "  lsf       - Run on LSF HPC cluster"
	@echo "  sge       - Run on SGE HPC cluster"
	@echo "  run       - Execute with custom PROFILE variable"
	@echo "  clean     - Remove all results (CAUTION!)"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - Nextflow installed"
	@echo "  - Container system (Docker/Singularity) or local tools"
	@echo "  - Reference genome FASTA file (update nextflow.config)"
	@echo "  - Reference annotation GTF file (update nextflow.config)"
	@echo ""
	@echo "Usage:"
	@echo "  cd 03_omics_single/rnaseq"
	@echo "  make all                    # Default: run with Docker"
	@echo "  make slurm                  # Run on SLURM cluster"
	@echo "  PROFILE=singularity make run # Run with Singularity"
	@echo ""
	@echo "Update samplesheet.csv for your samples"
	@echo "Update nextflow.config for reference files and HPC settings"

# Run with nf-core test data (fast validation)
test:
	@echo "🧪 Running nf-core/rnaseq with test dataset..."
	@echo "📋 Using nf-core test data"
	@echo "📁 Output directory: ../results/rnaseq_test"
	@echo ""

	# Run the pipeline with test profile
	nextflow run nf-core/rnaseq \
		-profile docker,test \
		--outdir ../results/rnaseq_test \
		-c nextflow.config \
		-resume

	@echo ""
	@echo "✅ RNA-seq test analysis completed!"
	@echo "📊 Test results: ../results/rnaseq_test"
	@echo ""
	@echo "✅ How to Use Nextflow Profiles"
	@echo "❯ Local run (Conda):      cd 03_omics_single/rnaseq && make all"
	@echo "❯ Docker run:             PROFILE=docker make run"
	@echo "❯ SLURM HPC:              PROFILE=slurm make run"
	@echo "❯ Test with public data:  make test"
	@echo ""
