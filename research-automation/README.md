# Research Automation Repository

A comprehensive, modular research automation platform supporting multiple research phases from systematic reviews to cutting-edge multi-omics integration and knowledge graphs.

## 🚀 Overview

This repository provides end-to-end automation for research workflows across multiple domains:

- **Systematic Reviews** - PubMed searching, deduplication, screening, meta-analysis, PRISMA diagrams
- **Bibliometrics** - Citation network analysis, scientometric mapping, research impact assessment
- **Single Omics** - RNA-seq, microbiome, pharmacovigilance workflows
- **Advanced Omics** - GWAS, single-cell, proteomics/metabolomics pipelines
- **Multi-Omics Integration** - Cross-platform data integration, environmental health, Bayesian meta-analysis
- **Cutting-Edge** - Living reviews with GitHub Actions, knowledge graphs, precision medicine demos

## 📁 Project Structure

```
research-automation/
├── 00_docs/                    # Documentation and protocols
├── 01_systematic_reviews/      # PubMed search, deduplication, meta-analysis
├── 02_bibliometrics/          # Citation analysis and network mapping
├── 03_omics_single/           # RNA-seq, microbiome, pharmacovigilance
├── 04_omics_advanced/         # GWAS, single-cell, proteomics
├── 05_integration/            # Multi-omics and advanced integration
├── 06_cutting_edge/           # Living reviews, knowledge graphs
├── env/                       # Environment setup (Docker, Conda, pip)
├── notebooks/                 # Jupyter and RMarkdown examples
├── results/                   # Output directory for all analyses
└── [config files]            # Makefiles, requirements, etc.
```

## ⚙️ Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourname/research-automation.git
cd research-automation
```

### 2. Choose Your Setup Method

## 🛠️ Quick Start

### Option 1: Docker (Recommended)

```bash
# Navigate to the env directory (where Dockerfile is located)
cd env

# Build the container
docker build -t research-automation .

# Run in development mode (interactive)
docker run -it -v $(pwd)/..:/workspace research-automation

# Run in development mode (with ports exposed)
docker run -p 8888:8888 -p 8501:8501 -v $(pwd)/..:/workspace research-automation

# Run in production mode
docker run -p 8501:8501 research-automation:latest
```

### Option 2: Conda/Mamba Environment (Recommended for speed)

```bash
# Navigate to the env directory
cd env

# Create environment (using mamba for faster installation)
mamba env create -f environment.yml

# Alternative using conda (slower but more widely available)
# conda env create -f environment.yml

# Activate environment
conda activate research-automation

# Install additional packages
pip install -r requirements.txt
```

### Option 3: Native Installation

```bash
# Install Python dependencies
pip install -r env/requirements.txt

# Install R packages (in R console)
install.packages(c("metafor", "revtools", "PRISMA2020", "tidyverse"))

# Install Nextflow
curl -s https://get.nextflow.io | bash
```

## 📋 Available Commands

### Main Pipeline Targets

```bash
make help              # Show all available targets
make sr               # Run systematic review pipeline
make bibliometrics    # Run bibliometric analysis
make omics_single     # Run single omics workflows
make omics_advanced   # Run advanced omics pipelines
make integration      # Run multi-omics integration
make cutting_edge     # Run cutting-edge features
make all              # Run all phases sequentially
make clean            # Clean temporary files
```

### Systematic Review Pipeline

```bash
cd 01_systematic_reviews/
make search           # Search PubMed for papers
make dedupe          # Deduplicate and screen results
make screen          # Launch AI-assisted screening
make extract         # Generate data extraction template
make meta            # Run meta-analysis
make prisma          # Generate PRISMA flow diagram
make all             # Run complete systematic review pipeline
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# API Keys
PUBMED_EMAIL=your.email@example.com
NCBI_API_KEY=your_ncbi_api_key

# Database
DATABASE_URL=postgresql://user:pass@localhost/research_db

# Compute Resources
CUDA_VISIBLE_DEVICES=0
OMP_NUM_THREADS=4

# Output Settings
RESULTS_DIR=./results
LOG_LEVEL=INFO
```

### Custom Configuration

Edit the configuration files in each phase directory:

- `01_systematic_reviews/config.yml` - Search terms, inclusion criteria
- `02_bibliometrics/network_config.yml` - Network analysis parameters
- `03_omics_single/pipeline_config.yml` - Omics processing settings

## 📊 Usage Examples

### Example 1: Systematic Review

```bash
# 1. Search PubMed for your research question
python 01_systematic_reviews/search_pubmed.py \
    "your search term" \
    --max-results 1000 \
    --start-date YYYY/MM/DD \
    --end-date YYYY/MM/DD

# 2. Deduplicate and screen results
Rscript 01_systematic_reviews/dedupe_screen.R

# 3. Run meta-analysis
Rscript 01_systematic_reviews/meta_analysis.R

# 4. Generate PRISMA diagram
Rscript 01_systematic_reviews/prisma_flow.R
```

### Example 2: Quick Meta-Analysis on Any Topic

```bash
# Navigate to systematic review directory
cd 01_systematic_reviews

# Step 1: Search PubMed database
make search  # PubMed search using the query in Makefile

# Step 2: Remove duplicates and screen
make dedupe  # Deduplication and cleaning

# Step 3: Run meta-analysis
make meta    # Statistical synthesis

# Step 4: Generate PRISMA flow diagram
make prisma  # Flow diagram for publication

# Run complete pipeline automatically
make all
```

### Example Custom Search Queries

```bash
# Alzheimer's disease treatments
python search_pubmed.py --query '("Alzheimer disease" OR dementia) AND (treatment OR therapy) AND clinical[trial]' --retmax 1500

# Diabetes interventions
python search_pubmed.py --query 'diabetes[MeSH] AND (intervention OR prevention) AND systematic[sb]' --retmax 2000

# Mental health outcomes
python search_pubmed.py --query 'mental health[MeSH] AND (outcome* OR effect*)' --retmax 1000

# Cancer therapies
python search_pubmed.py --query 'neoplasms[MeSH] AND (chemotherapy OR immunotherapy)' --retmax 2000
```

### Example 2: Bibliometric Analysis

```bash
# Run citation network analysis
make bibliometrics

# Generate co-authorship networks
python 02_bibliometrics/coauthorship_network.py

# Create scientometric maps
Rscript 02_bibliometrics/scientometric_mapping.R
```

### Example 3: Multi-Omics Integration

```bash
# Run multi-omics integration pipeline
make integration

# Perform Bayesian meta-analysis
python 05_integration/bayesian_meta_analysis.py

# Generate knowledge graphs
python 06_cutting_edge/knowledge_graph_builder.py
```

## 🔬 Research Phases

### Phase 1: Systematic Reviews (`01_systematic_reviews/`)

- **PubMed Search**: Automated literature retrieval with API integration
- **Deduplication**: Multiple algorithms for removing duplicate records
- **Screening**: Manual and AI-assisted screening workflows
- **Data Extraction**: Structured data extraction templates
- **Meta-Analysis**: Comprehensive statistical synthesis
- **PRISMA Reporting**: Automated flow diagram generation

### Phase 2: Bibliometrics (`02_bibliometrics/`)

- **Citation Analysis**: Impact factor and citation network analysis
- **Co-authorship Networks**: Research collaboration mapping
- **Scientometric Mapping**: Research landscape visualization
- **Altmetrics Integration**: Social media and web impact assessment

### Phase 3: Single Omics (`03_omics_single/`)

- **RNA-Seq Analysis**: Differential expression and pathway analysis
- **Microbiome Studies**: 16S rRNA and metagenomic workflows
- **Pharmacovigilance**: Adverse event detection and analysis

### Phase 4: Advanced Omics (`04_omics_advanced/`)

- **GWAS Analysis**: Genome-wide association studies
- **Single-Cell Analysis**: scRNA-seq and spatial transcriptomics
- **Proteomics/Metabolomics**: Mass spectrometry data analysis

### Phase 5: Integration (`05_integration/`)

- **Multi-Omics Integration**: Cross-platform data fusion
- **Environmental Health**: Environmental exposure analysis
- **Bayesian Meta-Analysis**: Advanced statistical modeling

### Phase 6: Cutting-Edge (`06_cutting_edge/`)

- **Living Reviews**: Automated monthly updates via GitHub Actions with **GitHub Pages deployment**
- **Knowledge Graphs**: Semantic data integration
- **Precision Medicine**: Personalized treatment optimization
- **Automated Reports**: Professional HTML/PDF reports published as public website

## 📈 Output and Results

All results are organized in the `results/` directory:

```
results/
├── reports/                    # Auto-generated HTML/PDF reports
│   ├── summary_report.html
│   └── publication_ready_figures/
├── figures/                    # Forest plots, volcano plots, Manhattan plots, etc.
│   ├── forest_plots/
│   ├── funnel_plots/
│   ├── volcano_plots/
│   ├── manhattan_plots/
│   └── network_graphs/
├── systematic_reviews/
│   ├── pubmed_results.csv
│   ├── deduplicated_papers.csv
│   ├── meta_analysis/
│   └── prisma/
├── bibliometrics/
│   ├── citation_networks/
│   └── scientometric_maps/
├── omics/
│   ├── rna_seq/
│   ├── gwas/
│   └── integration/
└── [additional phase outputs...]
```

## 🔧 Development

### Adding New Pipelines

1. Create a new directory under the appropriate phase
2. Add a Makefile with standard targets
3. Include configuration files
4. Update the main Makefile
5. Add documentation

### Contributing

```bash
# Fork the repository
git clone https://github.com/your-username/research-automation.git

# Create a feature branch
git checkout -b feature/new-analysis

# Make your changes
# Add tests
# Update documentation

# Submit a pull request
```

## 📚 Documentation

- [Systematic Review Guide](00_docs/protocols/systematic_review_protocol.md)
- [PRISMA Checklist](00_docs/protocols/prisma_checklist.md)
- [API Documentation](00_docs/api_documentation.md)
- [Troubleshooting Guide](00_docs/troubleshooting.md)

## 🔗 Integration with External Tools

### Supported Platforms

- **PubMed/NCBI**: Automated literature search and retrieval
- **ASReview**: AI-assisted screening integration
- **RevTools**: R-based systematic review tools
- **Metafor**: Comprehensive meta-analysis package
- **Nextflow**: Scalable workflow management
- **nf-core**: Community-curated bioinformatics pipelines

### Cloud Integration

- **AWS S3**: Data storage and retrieval
- **Google Cloud**: Big data processing
- **Docker Hub**: Container registry
- **GitHub Actions**: Automated workflows

## 🐛 Troubleshooting

### Common Issues

1. **PubMed API Limits**: Implement rate limiting and retry logic
2. **Memory Issues**: Use streaming for large datasets
3. **Package Conflicts**: Use virtual environments
4. **Path Issues**: Use absolute paths in configuration files

### Getting Help

- Check the [troubleshooting guide](00_docs/troubleshooting.md)
- Review the [FAQ](00_docs/faq.md)
- Open an issue on GitHub
- Join our community discussions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Funding**: [Add funding sources]
- **Contributors**: [Add contributor list]
- **Institutions**: [Add institutional support]

## 📞 Contact

- **Maintainer**: [Your Name]
- **Email**: [your.email@example.com]
- **Institution**: [Your Institution]
- **Website**: [https://your-website.com]

---

**Happy Researching!** 🔬📊✨

*This repository is continuously updated with the latest research automation tools and best practices.*
