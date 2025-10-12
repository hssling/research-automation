# Phase 2 Omics Single: Advanced Bioinformatics Pipelines

**COVID-19 Research Automation Framework**

This directory contains production-ready omics analysis pipelines designed to investigate the multi-modal molecular signatures of COVID-19 disease states. The pipelines are optimized for answering the core research question:

> *"How do gut microbiome alterations and host gene expression changes jointly predict the severity and treatment response in COVID-19 patients?"*

## 🚀 Pipeline Overview

### 🧬 RNA-seq Pipeline (nf-core/rnaseq)
**Host Transcriptomic Analysis** - Characterizes PBMC gene expression patterns in COVID-19
- **Pipeline**: nf-core/rnaseq (STAR/Salmon/DESeq2)
- **Data Source**: GSE157103 (GEO accession)
- **Sample Type**: PBMC (Peripheral Blood Mononuclear Cells)
- **Technology**: Paired-end RNA-seq

### 🦠 Microbiome Pipeline (nf-core/ampliseq)
**Gut Microbial Community Analysis** - Profiles microbiome dysbiosis in COVID-19
- **Pipeline**: nf-core/ampliseq (DADA2/QIIME2)
- **Data Source**: PRJNA646614 (SRA project)
- **Sample Type**: Stool microbiome
- **Technology**: 16S rRNA sequencing

### 💊 Pharmacovigilance Pipeline (Custom)
**Safety Signal Detection** - Monitors COVID-19 treatment adverse events
- **Framework**: Custom FAERS database processing
- **Data Source**: FDA FAERS quarterly datasets
- **Analysis**: ROR/PRR statistical signal detection
- **Technology**: Python/R pharmacovigilance tools

## 📊 Data Sources for Testing

### 🧬 RNA-seq Testing Data
**File**: `rnaseq/samplesheet.csv` (GEO Accession GSE157103)
- **10 Samples**: Mixed COVID-19 cases and healthy controls
- **Disease States**: Asymptomatic, Mild, Moderate, Severe COVID-19
- **Format**: GEO-compatible FASTQ samples with metadata

```csv
sample,fastq_1,fastq_2,strandedness,condition
GSM4758322,...,...,reverse,mild_covid
GSM4758323,...,...,reverse,moderate_covid
GSM4758325,...,...,reverse,healthy
```

### 🦠 Microbiome Testing Data
**File**: `microbiome/metadata.tsv` (SRA PRJNA646614)
- **9 Samples**: COVID-19 positive/negative stool microbiome
- **Clinical Covariates**: Disease severity, treatment interventions
- **Format**: Ampliseq-compatible FASTQ paths and metadata

```tsv
sample-id	forward-absolute-filepath	reverse-absolute-filepath	covid_status	severity	treatment
PRJNA646614_SRS8596288	https://...	SRR11373875	covid_positive	mild	none
PRJNA646614_SRS8596290	https://...	SRR11373876	covid_positive	moderate	antiviral
```

### 💊 Pharmacovigilance Testing
**Source**: FDA FAERS quarterly ASCII datasets
- **URL**: https://fis.fda.gov/extensions/FPD/FAERS/FAERS.html
- **Latest**: 2024Q1 quarterly dataset (~1GB compressed)
- **Pipeline**: Automated download + ROR/PRR signal detection

## 🚀 Quick Start

### Environment Setup
```bash
# Create complete bioinformatics environment
conda env create -f ../env/environment.yml
conda activate research-automation
```

### Pipeline Execution

**RNA-seq Analysis**:
```bash
cd rnaseq && make all
# Generates: STAR alignment, Salmon quantification, DESeq2 differential expression
```

**Microbiome Analysis**:
```bash
cd microbiome && make all
# Generates: DADA2 ASV calling, QIIME2 diversity analysis, taxonomy assignment
```

**Pharmacovigilance**:
```bash
cd pharmacovigilance && make all
# Generates: FAERS data download, signal detection analysis (ROR/PRR)
```

## 📋 Research Integration

### 🧬 Host Response Patterns
- Host gene expression signatures across COVID-19 severity
- PBMC RNA-seq profiles reveal immune dysregulation
- Differential expression analysis (healthy vs COVID-19)

### 🦠 Microbiome Dysbiosis
- Gut microbial community alterations
- 16S composition changes by disease state
- Taxonomic differences: controls vs mild/moderate/severe COVID-19

### 💊 Treatment Safety
- FAERS adverse event monitoring
- ROR/PRR statistical signal detection
- Treatment outcome correlations

### 🔗 Joint Analysis Integration
**Combined Molecular Insights**:
1. **Host-Microbiome Correlation**: How immune response links to gut dysbiosis
2. **Severity Prediction**: Multi-modal molecular signatures
3. **Treatment Response**: Host-microbiome-treatment relationship characterization

## 📁 Directory Structure

```
03_omics_single/
├── rnaseq/                 # Host transcriptomics (PBMC)
│   ├── samplesheet.csv    # GSE157103 metadata
│   ├── nextflow.config    # Pipeline configuration
│   └── Makefile          # Execution orchestration
├── microbiome/            # Gut microbiome analysis
│   ├── metadata.tsv       # PRJNA646614 sample metadata
│   ├── nextflow.config    # QIIME2 pipeline config
│   └── Makefile          # Docker/Singularity execution
├── pharmacovigilance/     # Drug safety monitoring
│   ├── fetch_faers.py     # FDA data download
│   ├── clean_faers.R      # Data processing (DRUG/REAC)
│   ├── analyze_faers.R    # ROR/PRR signal detection
│   └── Makefile          # Three-stage pipeline
└── README.md             # This documentation
```

## 🔧 Technical Configuration

### Multi-Environment Deployment
- **🔶 Local Desktop**: Direct tool execution
- **🔶 Docker**: Containerized reproducible workflows
- **🔶 SLURM/SGE/LSF**: High-performance cluster deployment
- **🔶 Singularity**: Scientific HPC environments

### Production Features
- **Nextflow DSL2**: Scalable workflow orchestration
- **nf-core Standards**: Production bioinformatics pipelines
- **Resource Management**: Automatic scaling and monitoring
- **Error Handling**: Resumable execution on failure

## 📈 Expected Outputs

### RNA-seq Pipeline
- `../results/rnaseq/deseq2/` - Differential expression results
- `../results/rnaseq/salmon/` - Transcript abundance quantification
- `../results/rnaseq/star/` - Genome alignments and quality metrics

### Microbiome Pipeline
- `../results/microbiome/qiime2/` - Diversity analysis and taxonomy
- `../results/microbiome/dada2/` - Amplicon sequence variants (ASVs)
- `../results/microbiome/multiqc/` - Comprehensive quality reports

### Pharmacovigilance Pipeline
- `../results/pharmacovigilance/ror_signals.csv` - Reporting Odds Ratio analysis
- `../results/pharmacovigilance/prr_signals.csv` - Proportional Reporting Ratio
- `../results/pharmacovigilance/top_signals.csv` - High-frequency safety signals

## 🎯 Research Applications

**Optimized for COVID-19 Biomarker Discovery**:
- 🧬 Host immune response characterization
- 🦠 Microbiome-COVID-19 interaction studies
- 💊 Treatment safety and efficacy monitoring
- 🔗 Multi-modal phenotype prediction models

**Scalable to Other Research Questions**:
- Template structure enables rapid adaptation to other diseases
- Bioinformatics core maintains standardization and reproducibility

---

**Ready for immediate COVID-19 research acceleration!** 🚀🔬🦠💊
