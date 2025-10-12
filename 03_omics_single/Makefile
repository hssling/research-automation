.PHONY: all rnaseq microbiome pharmacovigilance integration clean help

# Omics Single Analysis Pipelines
# Coordinate RNA-seq, Microbiome, and Pharmacovigilance workflows

# Default target - run all three pipelines + integration sequentially
all: rnaseq microbiome pharmacovigilance integration
	@echo "🎉 Complete multi-omics integration pipeline completed successfully!"
	@echo "📄 Integration report: integration_covid_microbiome_transcriptome.html"

# Full pipeline: run all omics + integration analysis
full: all integration
	@echo "🚀 Complete Multi-Omics Integration Framework Executed!"
	@echo "📊 Results available:"
	@echo "   - RNA-seq analysis: results/rnaseq/"
	@echo "   - Microbiome analysis: results/microbiome/"
	@echo "   - Pharmacovigilance: results/pharmacovigilance/"
	@echo "   - Integration report: integration_covid_microbiome_transcriptome.html"

# RNA-seq pipeline (nf-core/rnaseq)
rnaseq:
	@echo "🧬 Running RNA-seq pipeline (nf-core/rnaseq)..."
	@cd rnaseq && $(MAKE) all

# Microbiome pipeline (nf-core/ampliseq)
microbiome:
	@echo "🦠 Running Microbiome pipeline (nf-core/ampliseq)..."
	@cd microbiome && $(MAKE) all

# Pharmacovigilance pipeline
pharmacovigilance:
	@echo "💊 Running Pharmacovigilance pipeline (FAERS analysis)..."
	@cd pharmacovigilance && $(MAKE) all

# Integration analysis: RNA-seq + Microbiome
integration:
	@echo "🔗 Running Multi-Omics Integration Analysis..."
	@echo "📊 Combining RNA-seq and Microbiome data for COVID-19 severity prediction"
	@quarto render integration_covid_microbiome_transcriptome.qmd --to html
	@echo "✅ Integration analysis completed!"
	@echo "📄 View results: integration_covid_microbiome_transcriptome.html"

# Run with test datasets for development
test: test_rnaseq test_microbiome test_pharmacovigilance
	@echo "🧪 All test pipelines completed!"

# Test RNA-seq pipeline
test_rnaseq:
	@echo "🧪 Testing RNA-seq pipeline with nf-core test data..."
	@cd rnaseq && $(MAKE) test

# Test Microbiome pipeline
test_microbiome:
	@echo "🧪 Testing Microbiome pipeline with nf-core test data..."
	@cd microbiome && $(MAKE) test

# Test Pharmacovigilance pipeline
test_pharmacovigilance:
	@echo "🧪 Testing Pharmacovigilance pipeline..."
	@cd pharmacovigilance && $(MAKE) test

# Clean all pipeline results
clean:
	@echo "🧹 Cleaning all pipeline results..."
	@cd rnaseq && $(MAKE) clean 2>/dev/null || true
	@cd microbiome && $(MAKE) clean 2>/dev/null || true
	@cd pharmacovigilance && $(MAKE) clean 2>/dev/null || true
	@rm -rf results/
	@echo "✅ Cleanup completed!"

# Show help
help:
	@echo "Omics Single Analysis Pipelines"
	@echo "==============================="
	@echo ""
	@echo "Targets:"
	@echo "  full                   - Run complete pipeline: all omics + integration"
	@echo "  all                    - Run all three omics pipelines sequentially"
	@echo "  rnaseq                 - Run RNA-seq pipeline only"
	@echo "  microbiome             - Run Microbiome pipeline only"
	@echo "  pharmacovigilance      - Run Pharmacovigilance pipeline only"
	@echo "  integration            - Run multi-omics integration analysis"
	@echo "  test                   - Run all pipelines with test data"
	@echo "  test_rnaseq           - Test RNA-seq pipeline with nf-core test data"
	@echo "  test_microbiome       - Test Microbiome pipeline with nf-core test data"
	@echo "  test_pharmacovigilance - Test Pharmacovigilance pipeline"
	@echo "  clean                  - Clean all results and intermediate files"
	@echo "  help                   - Show this help message"
	@echo ""
	@echo "Pipelines:"
	@echo "  🧬 RNA-seq:    nf-core/rnaseq (host transcriptomics, GSE157103)"
	@echo "  🦠 Microbiome: nf-core/ampliseq (gut 16S, PRJNA646614)"
	@echo "  💊 FAERS:      Custom pharmacovigilance (ROR/PRR analysis)"
	@echo ""
	@echo "Usage:"
	@echo "  make all          # Run production analysis"
	@echo "  make test         # Run with test datasets"
	@echo "  make clean        # Clean results"
