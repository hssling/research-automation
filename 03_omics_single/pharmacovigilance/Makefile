PHONY: all fetch clean analyze test help

all: fetch clean analyze

fetch:
	python fetch_faers.py

clean:
	Rscript clean_faers.R

analyze:
	Rscript analyze_faers.R

test:
	@echo "🧪 Testing pharmacovigilance pipeline with mock data..."
	@mkdir -p raw_faers
	@echo "FAERS Mock Data" > raw_faers/FAERS_mock.txt
	@echo "🧹 Creating mock FAERS data for testing..."
	@make clean
	@echo "📊 Running analysis with mock data..."
	@echo "⚠️  This is a test run - real FAERS data download skipped"
	Rscript analyze_faers.R
	@echo "✅ Pharmacovigilance test completed!"

help:
	@echo "FAERS Pharmacovigilance Pipeline"
	@echo ""
	@echo "Targets:"
	@echo "  all        - Complete pipeline: fetch -> clean -> analyze"
	@echo "  fetch      - Download latest FAERS data from FDA"
	@echo "  clean      - Process and clean DRUG/REAC tables"
	@echo "  analyze    - ROR/PRR signal detection analysis"
	@echo "  test       - Run with mock data (no download)"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "Outputs:"
	@echo "  fetch      -> raw_faers/ (FAERS ASCII files)"
	@echo "  clean      -> clean/ (tidy CSVs)"
	@echo "  analyze    -> results/pharmacovigilance/"
