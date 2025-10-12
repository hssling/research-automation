.PHONY: all fetch clean analyze help

# Pharmacovigilance Analysis Pipeline
# Automated FAERS database processing and signal detection

# Default target - run full pipeline
all: fetch clean analyze

# Step 1: Fetch FAERS data from FDA website
fetch:
	@echo "📥 Fetching FAERS database..."
	python fetch_faers.py
	@echo "✅ FAERS data downloaded successfully"

# Step 2: Clean and process the raw data
clean:
	@echo "🧹 Cleaning FAERS data..."
	Rscript clean_faers.R
	@echo "✅ FAERS data cleaned and processed"

# Step 3: Analyze data for signal detection
analyze:
	@echo "🎯 Analyzing FAERS data for adverse event signals..."
	Rscript analyze_faers.R
	@echo "✅ FAERS signal detection analysis completed"

# Help target
help:
	@echo "Pharmacovigilance FAERS Analysis Pipeline"
	@echo ""
	@echo "Targets:"
	@echo "  all      - Run complete pipeline (fetch → clean → analyze)"
	@echo "  fetch    - Download latest FAERS data from FDA"
	@echo "  clean    - Process and clean raw FAERS files"
	@echo "  analyze  - Perform signal detection analysis"
	@echo "  help     - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - Python 3.8+ with requests, pandas libraries"
	@echo "  - R 4.0+ with dplyr, readr, epitools packages"
	@echo "  - 5-10GB free disk space for FAERS data"
	@echo ""
	@echo "Output directories:"
	@echo "  raw_faers/  - Raw downloaded FAERS files"
	@echo "  clean/      - Processed and cleaned data"
	@echo "  results/pharmacovigilance/ - Analysis results"
	@echo ""
	@echo "Usage example:"
	@echo "  make all                    # Complete analysis"
	@echo "  make fetch && make clean    # Only data processing"
