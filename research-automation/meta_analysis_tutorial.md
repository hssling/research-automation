# Meta-Analysis Tutorial: Any Topic in Minutes

This tutorial shows how to automatically run a complete meta-analysis on ANY research topic using the research automation system.

## 🎯 Quick Start - 5 Minutes to Results

### Step 1: Setup (1 minute)
```bash
# Clone and setup the repository
git clone https://github.com/yourname/research-automation.git
cd research-automation

# Option 1: Docker (recommended)
cd env && docker build -t research-automation . && docker run -it -v $(pwd)/..:/workspace research-automation

# Option 2: Conda/mamba
cd env && mamba env create -f environment.yml && conda activate research-automation
```

### Step 2: Customize Search Query (30 seconds)

Edit the search query in `01_systematic_reviews/Makefile`:

```makefile
search:
	@echo ">>> Fetching articles from PubMed..."
	python search_pubmed.py --query '("your topic"[TI] OR related terms) AND (trial OR study) AND systematic[sb]' --retmax 1000 --out results/pubmed_results.csv
```

**Examples of search queries for different topics:**

| Research Topic | Search Query |
|---------------|--------------|
| **Mental Health & Depression** | `("depression"[MeSH] OR "major depressive disorder") AND (treatment OR therapy) AND clinical[trial]` |
| **Diabetes & Exercise** | `(diabetes[MeSH] OR "diabetes mellitus") AND (exercise OR physical activity) AND intervention` |
| **Cancer & Nutrition** | `(neoplasms[MeSH] OR cancer) AND (diet OR nutrition) AND prevention` |
| **Cardiovascular & Diet** | `(cardiovascular diseases[MeSH]) AND (diet* OR nutrition) AND dietary intervention` |
| **Pediatric ADHD** | `(attention-deficit hyperactivity disorder[MeSH]) AND (child OR pediatric OR adolescent) AND clinical[trial]` |
| **Sleep & Cognitive Function** | `(sleep[MeSH] OR "sleep deprivation") AND (cognitive OR cognition) AND systematic[sb]` |

### Step 3: Run Complete Meta-Analysis (3 minutes)

```bash
# Navigate to systematic review directory
cd 01_systematic_reviews/

# Run the complete automated pipeline
make all

# Or run step-by-step for monitoring
make search   # 🔍 Search PubMed
make dedupe   # 🧹 Deduplicate results
make meta     # 📊 Run statistical meta-analysis
make prisma   # 📈 Generate PRISMA flow diagram
```

### Step 4: View Results

Access your results in `results/` directory:
- `pubmed_results.csv` - Raw search results
- `deduplicated_papers.csv` - Cleaned dataset
- `meta_analysis/` - Statistical synthesis (forest plots, funnel plots)
- `prisma/prisma_flow.html` - PRISMA flow diagram for publication

## 🚀 Advanced Tutorial - Customizing for Specific Topics

### Example 1: Coffee Consumption and Mortality

```bash
# 1. Edit search query in Makefile
sed -i 's/your search term/coffee AND mortality/' 01_systematic_reviews/Makefile

# 2. Run meta-analysis
cd 01_systematic_reviews && make all

# 3. Results appear in results/ directory within 2-3 minutes
```

### Example 2: Vegan Diet and Cholesterol

```bash
# 1. Direct command line search
python 01_systematic_reviews/search_pubmed.py \
    --query '("vegan diet" OR "plant-based diet") AND cholesterol AND systematic[sb]' \
    --retmax 800

# 2. Process and analyze
Rscript 01_systematic_reviews/dedupe_screen.R
Rscript 01_systematic_reviews/meta_analysis.R
Rscript 01_systematic_reviews/prisma_flow.R
```

### Example 3: Social Media and Anxiety

```bash
# 1. Themed search for behavioral studies
python search_pubmed.py --query '"social media"[TI] AND anxiety[MeSH] AND (systematic[sb] OR meta-analysis['

# 2. Run complete pipeline
make all
```

## 🧪 Testing Different Meta-Analysis Methods

The system supports multiple statistical approaches:

### Random Effects Model (Default)
```bash
# Uses REML estimation with Knapp-Hartung adjustment
# Best for heterogeneous studies
make meta
```

### Fixed Effect Model
```r
# Edit meta_analysis.R to change:
res <- rma(yi = data$EffectSize, sei = data$SE, method="FE")
```

### Bayesian Methods
```r
# For advanced Bayesian meta-analysis
library(brms)
# Edit the R script for Bayesian models
```

## 📊 Interpreting Your Results

### Forest Plot Reading
- **X-axis**: Effect size (e.g., standardized mean difference)
- **Squares**: Individual study effect sizes
- **Horizontal lines**: Confidence intervals
- **Diamond**: Overall pooled effect size

### Heterogeneity Assessment
- **I² statistic**: Percentage of variation due to heterogeneity
  - < 25%: Low heterogeneity
  - 25-75%: Moderate heterogeneity
  - > 75%: High heterogeneity

### Publication Bias
- **Funnel Plot**: Visual assessment of asymmetry
- **Egger's Test**: Statistical test for funnel plot asymmetry
- **Trim and Fill**: Adjustment for missing studies

## 🔄 Living Systematic Review

Enable automatic monthly updates:

1. Go to GitHub Repository Settings
2. Navigate to Pages → Source: "Deploy from a branch"
3. Select "gh-pages" branch
4. Your monthly meta-analysis reports will be published at:
   `https://yourusername.github.io/research-automation/reports/`

## 🛠️ Troubleshooting

### Common Issues:

1. **Empty Results**: Refine your search query with MeSH terms
2. **Low Study Count**: Broaden date range or inclusion criteria
3. **Heterogeneity**: Consider sub-group analyses or different effect measures
4. **Publication Bias**: Limited studies - interpret cautiously

### Advanced Debugging:

```bash
# Check search results
head results/pubmed_results.csv

# Verify statistical inputs
Rscript -e "data <- read.csv('results/deduplicated_papers.csv'); summary(data)"

# View meta-analysis diagnostics
ls results/meta_analysis/
```

## 🎯 Best Practices

1. **Start Broad**: Use comprehensive search strategies initially
2. **Iterate**: Run small searches first to validate queries
3. **Document**: Keep track of search strategies and decisions
4. **Quality Check**: Always review included studies
5. **Transparency**: Publish search syntax and inclusion criteria

## 🚀 Production Usage

For large-scale research, consider:

```bash
# Batch processing multiple topics
for topic in "coffee" "exercise" "meditation"; do
    # Customize query
    sed -i "s/your topic/$topic/" 01_systematic_reviews/Makefile
    # Run pipeline
    make clean && make all
    # Archive results
    mkdir ../archive/$topic && mv results/* ../archive/$topic/
done
```

---

**Time to Results: 2-5 minutes for any topic!**

This automation transforms hours of manual work into minutes of automated analysis, making meta-analysis accessible to all researchers while maintaining the highest standards of systematic review methodology.
