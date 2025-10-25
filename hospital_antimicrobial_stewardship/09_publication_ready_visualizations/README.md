# Publication-Ready Visualizations

This directory contains high-resolution, publication-quality visualizations for the Antimicrobial Stewardship Mortality Systematic Review.

## Available Visualizations

### 1. Forest Plot (mortality_forest_plot.png)
- **Dimensions**: 1200x800px (4:3 aspect ratio)
- **Resolution**: 150 DPI
- **Format**: PNG with transparent background
- **Purpose**: Primary results visualization showing pooled risk ratios

### 2. Enhanced Forest Plot (enhanced_mortality_forest.png)
- **Dimensions**: 1400x900px
- **Resolution**: 150 DPI
- **Format**: PNG
- **Purpose**: Detailed forest plot with study labels and confidence intervals

### 3. GRADE Evidence Profile (grade_evidence_profile.png)
- **Dimensions**: 1000x600px
- **Resolution**: 150 DPI
- **Format**: PNG
- **Purpose**: Visual representation of evidence quality assessment

### 4. Geographic Evidence Map (world_evidence_map.png)
- **Dimensions**: 1200x800px
- **Resolution**: 150 DPI
- **Format**: PNG
- **Purpose**: Global distribution of ASP mortality studies

### 5. Intervention Effectiveness (intervention_comparison.png)
- **Dimensions**: 1000x700px
- **Resolution**: 150 DPI
- **Format**: PNG
- **Purpose**: Comparative effectiveness of different ASP interventions

## Technical Specifications

### Color Scheme
- **Primary Blue**: #1f77b4 (Asp stewardship theme)
- **Secondary Blue**: #aec7e8
- **Accent Colors**: #ff7f0e (intervention), #2ca02c (positive), #d62728 (negative)
- **Neutral Gray**: #7f7f7f
- **Background**: White (#ffffff)

### Typography
- **Primary Font**: Arial (or Arial-compatible)
- **Size**: 12pt base, 14pt titles, 10pt captions
- **Weight**: Regular for body text, Bold for headings
- **Alignment**: Left-aligned for English text

### Export Settings
- **Format**: PNG for web/SVG hybrid compatibility
- **Resolution**: Minimum 150 DPI for print quality
- **File Size**: Optimized for journal submission (under 5MB per figure)
- **Transparency**: Enabled where applicable

## Journal Formatting Templates

### The Lancet Format
- **Maximum width**: 180mm (single column), 360mm (double column)
- **Resolution**: 300+ DPI
- **Colors**: CMYK color space
- **File format**: TIFF or EPS

### JAMA Format
- **Width**: 210 mm maximum
- **Height**: 297 mm maximum
- **Resolution**: 600 DPI for line art, 300 DPI for color
- **Colors**: CMYK

### Generic Biomedical Journal
- **Width**: 8.5 inches maximum
- **Resolution**: 300 DPI minimum
- **Colors**: RGB or CMYK depending on publication
- **Format**: High-quality PNG or PDF

## Usage Instructions

### Including in Manuscripts
1. **Label appropriately**: "Figure 1. Forest plot showing..."
2. **Cite in text**: Reference figure numbers in results section
3. **Caption thoroughly**: Include statistical details and data sources
4. **Place strategically**: Position near relevant text discussion

### PowerPoint Presentations
- Use high-resolution versions (150+ DPI)
- Maintain aspect ratios to prevent distortion
- Consider color blindness accessibility (use colorblind-friendly palettes)

### Web Publication
- PNG format with transparency for flexible backgrounds
- Web-optimized resolution (72-96 DPI for screen display)
- Compressed file sizes for faster loading

## Data Sources

All visualizations are generated from:
- `meta_analysis_results.csv`: Statistical results
- `mortality_studies_data.csv`: Study-level data
- `antimicrobial_stewardship_meta_analysis.R`: Generation script

## Reproduction

To regenerate visualizations:

```r
# In R environment
source("03_statistical_analysis/antimicrobial_stewardship_meta_analysis.R")
```

Or manually recreate following the specifications above.

## Copyright and Usage

- **License**: Creative Commons Attribution 4.0 International
- **Citation**: Cite the systematic review when using visualizations
- **Attribution**: Include source information in figure legends
- **Commercial Use**: Contact research team for permission

---
*Updated 2025-10-13 21:07:22 via automated living review*

---
*Updated 2025-10-13 21:12:19 via automated living review*

---
*Updated 2025-10-13 21:14:05 via automated living review*
