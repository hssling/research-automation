# 🔬 Research Automation Repository

This repository is a **modular framework for automated research pipelines**.  
It covers **systematic reviews, bibliometrics, omics pipelines (RNA-seq, GWAS, microbiome, single-cell, proteomics/metabolomics), multi-omics integration, and cutting-edge approaches** like living systematic reviews and knowledge graph mining.  

Designed for **VS Code + AI coding agents (Codex, Cursor, Windsurf, etc.)**, the repo supports reproducibility with **Makefiles, Nextflow, Conda/Docker, and GitHub Actions**.

---

## 📂 Repository Structure

## 🌐 Full Research-Automation Platform + Dashboard

This section describes the full research automation platform with PDF extraction, summarization, RAG indexing, and a Streamlit dashboard.

### Setup

1. Activate the virtual environment: `.\.venv\Scripts\activate`

2. Install dependencies: `pip install -r requirements.txt`

3. Add your API keys to .env

4. Run the dashboard: `streamlit run dashboards/app.py`

5. Add PDFs to ./data/pdfs and run the pipeline.

### Features

- PDF text extraction

- AI summarization using Hugging Face

- RAG indexing with Chroma

- Interactive dashboard

- GitHub integration
