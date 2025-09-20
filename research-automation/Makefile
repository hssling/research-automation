.PHONY: help sr bibliometrics omics_single omics_advanced integration cutting_edge all clean

# Research Automation Repository
# Main Makefile for orchestrating all research phases

# Default target
help:
	@echo "Research Automation Repository - Available targets:"
	@echo ""
	@echo "Systematic Reviews:"
	@echo "  sr              - Run systematic review pipeline"
	@echo ""
	@echo "Bibliometrics:"
	@echo "  bibliometrics   - Run bibliometric and citation network analysis"
	@echo ""
	@echo "Single Omics:"
	@echo "  omics_single    - Run RNA-seq, microbiome, pharmacovigilance workflows"
	@echo ""
	@echo "Advanced Omics:"
	@echo "  omics_advanced  - Run GWAS, single-cell, proteomics/metabolomics pipelines"
	@echo ""
	@echo "Integration:"
	@echo "  integration     - Run multi-omics integration and advanced analysis"
	@echo ""
	@echo "Cutting Edge:"
	@echo "  cutting_edge    - Run living reviews, knowledge graphs, precision medicine"
	@echo ""
	@echo "Utilities:"
	@echo "  all             - Run all phases in sequence"
	@echo "  clean           - Remove temporary files"
	@echo "  help            - Show this help message"

# Systematic Review Pipeline
sr:
	@echo "Running systematic review pipeline..."
	@$(MAKE) -C 01_systematic_reviews all

# Bibliometrics Pipeline
bibliometrics:
	@echo "Running bibliometrics pipeline..."
	@$(MAKE) -C 02_bibliometrics all

# Single Omics Pipeline
omics_single:
	@echo "Running single omics pipeline..."
	@$(MAKE) -C 03_omics_single all

# Advanced Omics Pipeline
omics_advanced:
	@echo "Running advanced omics pipeline..."
	@$(MAKE) -C 04_omics_advanced all

# Integration Pipeline
integration:
	@echo "Running integration pipeline..."
	@$(MAKE) -C 05_integration all

# Cutting Edge Pipeline
cutting_edge:
	@echo "Running cutting edge pipeline..."
	@$(MAKE) -C 06_cutting_edge all

# Run all phases in sequence
all: sr bibliometrics omics_single omics_advanced integration cutting_edge
	@echo "All research phases completed!"

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -name "*.tmp" -delete
	@find . -name "*.log" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name ".Rhistory" -delete
	@echo "Cleanup completed!"
