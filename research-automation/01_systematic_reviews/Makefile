.PHONY: help all search dedupe screen extract meta prisma clean

# ===============================
# Phase 1: Systematic Review Pipeline
# ===============================

# Default target - runs complete pipeline
all: search dedupe screen extract meta prisma
	@echo ">>> Systematic review pipeline completed!"
	@echo ""
	@echo "📊 Results available in:"
	@echo "   - data/pubmed.xml (raw search results)"
	@echo "   - data/cleaned.rds (deduplicated data)"
	@echo "   - extracted/studies.csv (extraction sheet)"
	@echo "   - results/ (meta-analysis and PRISMA)"
	@echo ""
	@echo "🔍 Next steps:"
	@echo "   1. Review extracted/studies.csv for data quality"
	@echo "   2. Check results/meta_analysis/ for statistical outputs"
	@echo "   3. Review results/prisma.html for flow diagram"
	@echo "   4. Run 'make screen' if you have many papers for AI screening"

# -------------------------------
# Step 1: PubMed Search
# -------------------------------
search:
	@echo ">>> Fetching articles from PubMed..."
python search_pubmed.py --query '"allergy"[MeSH] OR "asthma"[MeSH] OR "atopic dermatitis"[MeSH] AND "microbiome"[MeSH] OR "microbiota"[MeSH] OR "gut microbiome" AND "association"[sb] AND systematic[sb]' --retmax 1500 --out results/microbiome_allergy_results.csv
	@echo "✅ Search completed. Results saved to results/pubmed_results.csv"

# -------------------------------
# Step 2: Deduplication
# -------------------------------
dedupe:
	@echo ">>> Deduplicating search results..."
	Rscript dedupe_screen.R --in results/pubmed_results.csv --out results/deduplicated_papers.csv
	@echo "✅ Deduplication completed. Clean data saved to results/deduplicated_papers.csv"

# -------------------------------
# Step 3: Screening
# -------------------------------
screen:
	@echo ">>> Running AI-assisted screening..."
	@echo "Choose your preferred screening tool:"
	@echo "1. ASReview (recommended for large datasets >1000 papers)"
	@echo "2. revtools (integrated with R, good for smaller datasets)"
	@echo ""
	@read -p "Enter choice (1 or 2): " choice; \
	if [ "$$choice" = "1" ]; then \
		echo "Starting ASReview..."; \
		asreview start --dataset results/deduplicated_papers.csv; \
	elif [ "$$choice" = "2" ]; then \
		echo "Starting revtools screening..."; \
		Rscript -e "library(revtools); data <- read.csv('results/deduplicated_papers.csv'); screen_duplicates(data)"; \
	else \
		echo "Invalid choice. Please run 'make screen' again and select 1 or 2."; \
		exit 1; \
	fi

# -------------------------------
# Step 4: Data Extraction Sheet
# -------------------------------
extract:
	@echo ">>> Creating data extraction template..."
	Rscript -e "library(writexl); data <- read.csv('results/deduplicated_papers.csv'); extract <- data.frame(Study=1:nrow(data), Title=data\$title, Include=NA, Reason=NA, Notes=NA); write_xlsx(extract, 'results/extraction_sheet.xlsx')"
	@echo "✅ Extraction sheet created: results/extraction_sheet.xlsx"
	@echo "📝 Please fill in the 'Include' column (TRUE/FALSE) and 'Reason' for exclusions"

# -------------------------------
# Step 5: Meta-analysis
# -------------------------------
meta:
	@echo ">>> Running meta-analysis with metafor..."
	Rscript meta_analysis.R --in results/deduplicated_papers.csv --out results/meta_analysis/
	@echo "✅ Meta-analysis completed. Results in results/meta_analysis/"

# -------------------------------
# Step 6: PRISMA Diagram
# -------------------------------
prisma:
	@echo ">>> Generating PRISMA 2020 flow diagram..."
	Rscript prisma_flow.R --in results/deduplicated_papers.csv --out results/prisma/prisma_flow.html
	@echo "✅ PRISMA diagram generated: results/prisma/prisma_flow.html"

# -------------------------------
# Help and Information
# -------------------------------
help:
	@echo "==============================="
	@echo "Phase 1: Systematic Review Pipeline"
	@echo "==============================="
	@echo ""
	@echo "📚 DESCRIPTION:"
	@echo "   Complete systematic review workflow from PubMed search to PRISMA reporting"
	@echo ""
	@echo "🎯 AVAILABLE TARGETS:"
	@echo "   all              - Run complete pipeline (default)"
	@echo "   search           - PubMed search with API"
	@echo "   dedupe           - Remove duplicate articles"
	@echo "   screen           - AI-assisted screening (ASReview/revtools)"
	@echo "   extract          - Generate data extraction template"
	@echo "   meta             - Statistical meta-analysis"
	@echo "   prisma           - PRISMA 2020 flow diagram"
	@echo "   clean            - Remove all generated files"
	@echo "   help             - Show this help message"
	@echo ""
	@echo "📋 USAGE EXAMPLES:"
	@echo "   make search      # Search PubMed for papers"
	@echo "   make all         # Run complete pipeline"
	@echo "   make screen      # Interactive screening choice"
	@echo ""
	@echo "📁 OUTPUT STRUCTURE:"
	@echo "   results/"
	@echo "   ├── pubmed_results.csv      # Raw search results"
	@echo "   ├── deduplicated_papers.csv # Clean data"
	@echo "   ├── extraction_sheet.xlsx   # Manual review template"
	@echo "   ├── meta_analysis/          # Statistical outputs"
	@echo "   └── prisma/                 # Flow diagram"
	@echo ""
	@echo "🔧 CUSTOMIZATION:"
	@echo "   Edit search terms in 'search' target above"
	@echo "   Modify parameters in individual scripts"
	@echo "   Update inclusion criteria in extraction sheet"

# -------------------------------
# Utilities
# -------------------------------
clean:
	@echo ">>> Cleaning systematic review outputs..."
	@rm -rf results/*.csv results/*.xlsx results/meta_analysis/* results/prisma/*
	@find . -name "*.tmp" -delete 2>/dev/null || true
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name ".Rhistory" -delete 2>/dev/null || true
	@echo "✅ Cleanup completed!"
