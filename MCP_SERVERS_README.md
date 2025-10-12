# MCP Servers for Systematic Literature Review

This configuration file provides direct access to major biomedical and health research databases through MCP (Model Context Protocol) servers. These servers enable seamless integration of systematic literature searches into AI-assisted research workflows.

## Configuration File: `mcp-config.json`

**ENHANCED 2025: 12-Source Comprehensive Literature Search**

```json
{
  "mcpServers": {
    "literature": {
      "command": "npx",
      "args": ["-y", "mcp-server-aggregator"],
      "env": {
        "SOURCES": "pubmed,clinicaltrials,who_ictrp,crossref,cochrane,arxiv,pmc,ssoar",
        "PUBMED_API": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/",
        "CLINICALTRIALS_API": "https://clinicaltrials.gov/api/v2/studies",
        "WHO_ICTRP_CSV": "https://trialsearch.who.int/export/trialsearch.csv",
        "CROSSREF_API": "https://api.crossref.org/works",
        "COCHRANE_SEARCH": "https://www.cochranelibrary.com/cdsr/reviews/topics"
      }
    },
    "pubmed": {
      "command": "npx",
      "args": ["-y", "mcp-server-pubmed"],
      "env": {
        "PUBMED_API": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
      }
    },
    "clinicaltrials": {
      "command": "npx",
      "args": ["-y", "mcp-server-rest-api"],
      "env": {
        "API_BASE_URL": "https://clinicaltrials.gov/api/v2/studies"
      }
    },
    "who_ictrp": {
      "command": "npx",
      "args": ["-y", "mcp-server-csv"],
      "env": {
        "CSV_URL": "https://trialsearch.who.int/export/trialsearch.csv"
      }
    },
    "crossref": {
      "command": "npx",
      "args": ["-y", "mcp-server-rest-api"],
      "env": {
        "API_BASE_URL": "https://api.crossref.org/works"
      }
    },
    "cochrane": {
      "command": "npx",
      "args": ["-y", "mcp-server-scraper"],
      "env": {
        "SEARCH_URL": "https://www.cochranelibrary.com/cdsr/reviews/topics"
      }
    },
    "arxiv": {
      "command": "npx",
      "args": ["-y", "mcp-server-oai"],
      "env": {
        "OAI_BASE_URL": "http://export.arxiv.org/oai2"
      }
    },
    "pmc": {
      "command": "npx",
      "args": ["-y", "mcp-server-oai"],
      "env": {
        "OAI_BASE_URL": "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"
      }
    },
    "ssoar": {
      "command": "npx",
      "args": ["-y", "mcp-server-oai"],
      "env": {
        "OAI_BASE_URL": "https://www.ssoar.info/oai/request"
      }
    },
    "europepmc": {
      "command": "npx",
      "args": ["-y", "mcp-server-rest-api"],
      "env": {
        "API_BASE_URL": "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
      }
    },
    "openalex": {
      "command": "npx",
      "args": ["-y", "mcp-server-rest-api"],
      "env": {
        "API_BASE_URL": "https://api.openalex.org/works"
      }
    },
    "doaj": {
      "command": "npx",
      "args": ["-y", "mcp-server-rest-api"],
      "env": {
        "API_BASE_URL": "https://doaj.org/api/v2/search/articles/"
      }
    }
  }
}
```

## Server Usage Strategies

### 🎯 **Recommended Approach: Use the "literature" Aggregator Server**
For easiest adoption, use the **"literature"** server which automatically searches across all databases:

```python
# Single query searches all 5 databases
mcp.literature.search("multidrug-resistant tuberculosis synbiotics postbiotics")
# Returns aggregated results from PubMed, ClinicalTrials.gov, CrossRef, Cochrane, WHO ICTRP
```

This provides a **one-stop solution** for comprehensive literature searches without needing to query each database separately.

### 🔧 **Advanced Approach: Individual Database Servers**
For specialized needs, access individual databases:

```python
# MeSH-optimized biomedical search
mcp.pubmed.search("multidrug-resistant tuberculosis[MH] AND (synbiotics OR postbiotics)")

# Trial registry search
mcp.clinicaltrials.search("MDR-TB microbiome intervention")

# Academic literature via DOI
mcp.crossref.search("tuberculosis synbiotic review")
```

## MCP Servers Available

### 0. Literature Aggregator Server (`literature`) ⭐ **RECOMMENDED**
- **Database**: All 5 databases combined
- **Server**: `mcp-server-aggregator`
- **Coverage**: Comprehensive biomedical literature
- **Capabilities**:
  - Unified search across all sources
  - Automatic deduplication
  - Relevance ranking
  - One-click comprehensive search

### 1. PubMed Server (`pubmed`)
- **Database**: PubMed/MEDLINE
- **Server**: `mcp-server-pubmed`
- **Coverage**: Biomedical and health sciences literature
- **Capabilities**:
  - Advanced search with filters
  - Retrieval of abstract/fulltext
  - Citation metadata
  - Related articles

### 2. ClinicalTrials.gov Server (`clinicaltrials`)
- **Database**: ClinicalTrials.gov
- **Server**: `mcp-server-rest-api`
- **Coverage**: Clinical trial registrations
- **Capabilities**:
  - Search trial registrations
  - Study design information
  - Enrollment data
  - Result availability

### 3. WHO ICTRP Server (`who_ictrp`)
- **Database**: WHO International Clinical Trials Registry Platform
- **Server**: `mcp-server-csv`
- **Coverage**: Global clinical trial registrations
- **Capabilities**:
  - Bulk trial data download
  - International collaboration studies
  - Trial registration status

### 4. CrossRef Server (`crossref`)
- **Database**: CrossRef DOI metadata
- **Server**: `mcp-server-rest-api`
- **Coverage**: Academic publications across disciplines
- **Capabilities**:
  - DOI resolution and metadata
  - Preprint and article information
  - Citation links

### 5. Cochrane Server (`cochrane`)
- **Database**: Cochrane Library CDSR reviews
- **Server**: `mcp-server-scraper`
- **Coverage**: Systematic reviews and meta-analyses
- **Capabilities**:
  - Cochrane review database searches
  - Systematic review identification
  - Quality assessment data

### 6. arXiv Server (`arxiv`)
- **Database**: arXiv preprint repository
- **Server**: `mcp-server-oai`
- **Coverage**: Open access preprints in physics, mathematics, computer science, and quantitative biology
- **Capabilities**:
  - Preprint search and retrieval
  - Version histories
  - Category-specific searches
  - Recent research access

### 7. PMC Server (`pmc`)
- **Database**: PubMed Central
- **Server**: `mcp-server-oai`
- **Coverage**: Open access full-text biomedical and life sciences articles
- **Capabilities**:
  - Full-text article search
  - Open access paper retrieval
  - Supplementary materials access
  - License information

### 8. SSOAR Server (`ssoar`)
- **Database**: Social Science Open Access Repository
- **Server**: `mcp-server-oai`
- **Coverage**: Open access social sciences and humanities papers
- **Capabilities**:
  - Social sciences research papers
  - Humanities articles
  - Interdisciplinary studies
  - Academic working papers

### 9. Europe PMC Server (`europepmc`)
- **Database**: Europe PubMed Central
- **Server**: `mcp-server-rest-api`
- **Coverage**: European biomedical and life sciences literature
- **Capabilities**:
  - European complement to PubMed
  - Enhanced full-text access
  - European clinical trials
  - Cross-European research data

### 10. OpenAlex Server (`openalex`)
- **Database**: OpenAlex academic discovery platform
- **Server**: `mcp-server-rest-api`
- **Coverage**: Global academic research across all disciplines
- **Capabilities**:
  - Large-scale academic metadata
  - Open research data
  - Global collaboration networks
  - Enhanced discovery algorithms

### 11. DOAJ Server (`doaj`)
- **Database**: Directory of Open Access Journals
- **Server**: `mcp-server-rest-api`
- **Coverage**: Quality peer-reviewed open access journals
- **Capabilities**:
  - Quality-controlled OA journals
  - Rigorous peer review standards
  - Subject categorization
  - Publication verification

## Usage

### MCP Server Installation

```bash
# Install MCP client if not already available
npm install -g @modelcontextprotocol/sdk

# The servers will auto-install via npx when called
```

### Integration with IDE/AI Assistants

1. **VSCode/Cursor**: Configure MCP in settings.json
2. **Other IDEs**: Reference mcp-config.json in MCP client configuration
3. **AI Assistants**: Configure MCP server access for literature search capabilities

### Example Usage in Research Code

```python
import requests

# Direct API usage (alternative to MCP)
def search_pubmed(query):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": 100}
    response = requests.get(url, params=params)
    return response.json()

# Example query
results = search_pubmed("(multidrug-resistant tuberculosis[Title/Abstract]) AND (synbiotic OR postbiotic)")
```

## Benefits for Systematic Reviews

### ⚡ **Efficiency**
- Direct API access eliminates manual database searches
- Automated result deduplication and formatting
- Batch processing capabilities

### 🔍 **Comprehensive Coverage**
- Access to 8 major research databases
- Biomedical, clinical, and academic literature
- Open access repositories (arXiv, PMC, SSOAR)
- Global clinical trial and review data

### 🤖 **AI Integration**
- Natural language processing of queries
- Automated relevance scoring
- Citation network analysis
- Systematic review assistance

### 📊 **Data Quality**
- Structured metadata extraction
- Standardized citation formats
- Quality assessment integration

## Search Strategy Examples

### MDR-TB Systematic Review
```python
# PubMed query
query = "(multidrug-resistant tuberculosis OR MDR tuberculosis) AND (synbiotic OR postbiotic OR probiotic OR prebiotic OR microbiome)"

# Clinical trials query
query = "multidrug-resistant tuberculosis AND synbiotic OR postbiotic OR probiotic OR microbiome"

# Cochrane search
query = "MDR tuberculosis synbiotic OR postbiotic OR probiotic OR microbiome"
```

## Maintenance

### Version Updates
- Monitor for updated MCP server packages
- Test API endpoints regularly
- Update database URLs if changed

### Error Handling
- Implement retry logic for API failures
- Handle rate limiting appropriately
- Log failed searches for troubleshooting

### Data Validation
- Verify citation accuracy
- Check for duplicate references
- Validate DOI resolution

## Alternative Access Methods

If MCP servers are not available, the databases can be accessed directly:

1. **PubMed**: https://pubmed.ncbi.nlm.nih.gov
2. **ClinicalTrials.gov**: https://clinicaltrials.gov
3. **WHO ICTRP**: https://trialsearch.who.int
4. **CrossRef**: https://www.crossref.org
5. **Cochrane**: https://www.cochranelibrary.com
6. **arXiv**: https://arxiv.org
7. **PMC**: https://www.ncbi.nlm.nih.gov/pmc
8. **SSOAR**: https://www.ssoar.info

## Support and Documentation

- MCP SDK Documentation: https://modelcontextprotocol.io
- PubMed API: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- ClinicalTrials.gov API: https://clinicaltrials.gov/api/gui
- CrossRef API: https://api.crossref.org

## Future Enhancements

- Add Open Access PDF enrichment via oa_pdf_enricher.py
- Add more specialized databases (EMBASE, Web of Science, CINAHL)
- Implement full-text download capabilities
- Add citation network analysis
