"""
Automated Visualization Generation System
Publication-quality charts, graphs, and dashboards for systematic reviews
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetaAnalysisVisualizer:
    """Enhanced meta-analysis visualization generator"""

    def __init__(self, style: str = 'default'):
        self.style = style
        if style == 'publication':
            plt.style.use('seaborn-v0_8-whitegrid')
            sns.set_palette("husl")
        elif style == 'presentation':
            plt.style.use('seaborn-v0_8-darkgrid')
            sns.set_palette("bright")

        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'positive': '#2ca02c',
            'negative': '#d62728',
            'neutral': '#7f7f7f'
        }

    def forest_plot(self, study_data: pd.DataFrame,
                   title: str = "Forest Plot",
                   save_path: str = None,
                   figsize: Tuple[int, int] = (12, 8),
                   interactive: bool = False) -> Union[plt.Figure, go.Figure]:
        """Generate publication-quality forest plot"""

        if interactive:
            return self._forest_plot_plotly(study_data, title, save_path)
        else:
            return self._forest_plot_matplotlib(study_data, title, save_path, figsize)

    def _forest_plot_plotly(self, study_data: pd.DataFrame, title: str, save_path: str) -> go.Figure:
        """Interactive forest plot using Plotly"""

        fig = go.Figure()

        # Individual studies
        for i, (_, study) in enumerate(study_data.iterrows()):
            effect = study['effect_size']
            ci_lower = study['ci_lower']
            ci_upper = study['ci_upper']
            weight = study.get('weight', 1)

            # Study effect point
            fig.add_trace(go.Scatter(
                x=[effect], y=[i],
                mode='markers',
                marker=dict(size=weight*5 + 5, color='blue'),
                name=study.get('study_label', f'Study {i+1}'),
                hovertemplate=f"Effect: {effect:.3f}<br>95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]<br>Weight: {weight:.1f}%"
            ))

            # Confidence interval line
            fig.add_trace(go.Scatter(
                x=[ci_lower, ci_upper], y=[i, i],
                mode='lines',
                line=dict(color='blue', width=2),
                showlegend=False,
                hoverinfo='skip'
            ))

        # Overall effect (if available)
        if 'overall_effect' in study_data.columns:
            overall = study_data.iloc[-1] if study_data.iloc[-1].get('overall', False) else None
            if overall is not None:
                fig.add_trace(go.Scatter(
                    x=[overall['effect_size']], y=[len(study_data)-1],
                    mode='markers',
                    marker=dict(size=15, color='red', symbol='diamond'),
                    name='Overall Effect'
                ))

        # Vertical line at no effect
        fig.add_vline(x=0, line_dash="dash", line_color="red")

        fig.update_layout(
            title=title,
            xaxis_title="Effect Size (95% CI)",
            yaxis=dict(
                tickvals=list(range(len(study_data))),
                ticktext=study_data.get('study_label', [f'Study {i+1}' for i in range(len(study_data))])
            ),
            height=600,
            showlegend=False
        )

        if save_path:
            fig.write_html(save_path.replace('.png', '.html'))

        return fig

    def _forest_plot_matplotlib(self, study_data: pd.DataFrame, title: str,
                              save_path: str, figsize: Tuple[int, int]) -> plt.Figure:
        """Static forest plot using matplotlib"""

        fig, ax = plt.subplots(figsize=figsize)

        # Plot individual studies
        y_positions = np.arange(len(study_data))

        for i, (_, study) in enumerate(study_data.iterrows()):
            effect = study['effect_size']
            ci_lower = study['ci_lower']
            ci_upper = study['ci_upper']
            weight = study.get('weight', 1)

            # Study effect point
            ax.plot(effect, i, 's', color='blue', markersize=weight*3 + 3)

            # Confidence interval line
            ax.plot([ci_lower, ci_upper], [i, i], color='blue', linewidth=2)

        # Overall effect if exists
        overall_row = study_data[study_data.get('overall', pd.Series([False]*len(study_data))) == True]
        if not overall_row.empty:
            overall = overall_row.iloc[0]
            ax.plot(overall['effect_size'], len(study_data), 'D', color='red', markersize=8)
            ax.plot([overall['ci_lower'], overall['ci_upper']], [len(study_data), len(study_data)],
                   color='red', linewidth=3)

        # Vertical line at no effect
        ax.axvline(x=0, color='red', linestyle='--', alpha=0.7)

        # Labels and formatting
        ax.set_xlabel('Effect Size (95% CI)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_yticks(y_positions)
        ax.set_yticklabels(study_data.get('study_label', [f'Study {i+1}' for i in range(len(study_data))]))
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig

    def funnel_plot(self, study_data: pd.DataFrame,
                   title: str = "Funnel Plot",
                   save_path: str = None,
                   figsize: Tuple[int, int] = (10, 8),
                   interactive: bool = False) -> Union[plt.Figure, go.Figure]:
        """Generate funnel plot for publication bias assessment"""

        if interactive:
            return self._funnel_plot_plotly(study_data, title, save_path)
        else:
            return self._funnel_plot_matplotlib(study_data, title, save_path, figsize)

    def _funnel_plot_plotly(self, study_data: pd.DataFrame, title: str, save_path: str) -> go.Figure:
        """Interactive funnel plot using Plotly"""

        fig = go.Figure()

        # Individual studies
        fig.add_trace(go.Scatter(
            x=study_data['effect_size'],
            y=study_data['se'],
            mode='markers',
            marker=dict(size=8, color='blue', opacity=0.7),
            name='Studies',
            hovertemplate='Effect: %{x:.3f}<br>SE: %{y:.3f}'
        ))

        # Pseudo-confidence intervals
        se_range = np.linspace(study_data['se'].min(), study_data['se'].max(), 100)
        ci_width = 1.96 * se_range

        fig.add_trace(go.Scatter(
            x=se_range, y=ci_width,
            mode='lines', line=dict(color='red', dash='dash'),
            name='95% CI Upper'
        ))

        fig.add_trace(go.Scatter(
            x=se_range, y=-ci_width,
            mode='lines', line=dict(color='red', dash='dash'),
            name='95% CI Lower'
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Effect Size",
            yaxis_title="Standard Error",
            height=600
        )

        # Invert y-axis (convention)
        fig.update_yaxes(autorange="reversed")

        if save_path:
            fig.write_html(save_path.replace('.png', '.html'))

        return fig

    def _funnel_plot_matplotlib(self, study_data: pd.DataFrame, title: str,
                              save_path: str, figsize: Tuple[int, int]) -> plt.Figure:
        """Static funnel plot using matplotlib"""

        fig, ax = plt.subplots(figsize=figsize)

        # Individual studies
        ax.scatter(study_data['effect_size'], study_data['se'],
                  alpha=0.7, s=50, color='blue', edgecolors='black')

        # Pseudo-confidence intervals
        se_range = np.linspace(study_data['se'].min(), study_data['se'].max(), 100)
        ci_width = 1.96 * se_range

        ax.plot(se_range, ci_width, '--', color='red', alpha=0.7, label='95% CI')
        ax.plot(se_range, -ci_width, '--', color='red', alpha=0.7)

        ax.set_xlabel('Effect Size', fontsize=12, fontweight='bold')
        ax.set_ylabel('Standard Error', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Invert y-axis (convention)
        ax.invert_yaxis()

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig


class ResearchDashboardGenerator:
    """Generate comprehensive research dashboards"""

    def __init__(self, output_dir: str = "research_dashboards"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_systematic_review_dashboard(self,
                                        literature_data: pd.DataFrame,
                                        meta_results: Dict[str, Any] = None,
                                        quality_data: pd.DataFrame = None) -> str:
        """Create comprehensive systematic review dashboard"""

        dashboard_data = {
            'literature_overview': self._create_literature_overview(literature_data),
            'study_characteristics': self._create_study_characteristics_plot(literature_data),
            'temporal_trends': self._create_temporal_trends(literature_data),
        }

        if meta_results:
            dashboard_data.update({
                'meta_analysis_summary': self._create_meta_summary(meta_results),
                'heterogeneity_visualization': self._create_heterogeneity_plot(meta_results),
                'forest_plot': self._create_forest_plot(meta_results),
                'funnel_plot': self._create_funnel_plot(meta_results)
            })

        if quality_data is not None:
            dashboard_data['quality_assessment'] = self._create_quality_dashboard(quality_data)

        # Generate HTML dashboard
        dashboard_html = self._generate_html_dashboard(dashboard_data, "Systematic Review Dashboard")
        dashboard_path = self.output_dir / "systematic_review_dashboard.html"

        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)

        logger.info(f"Systematic review dashboard created: {dashboard_path}")
        return str(dashboard_path)

    def _create_literature_overview(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Create literature overview statistics"""

        overview = {
            'total_studies': len(data),
            'publication_years': data['publication_year'].value_counts().sort_index(),
            'study_designs': data['study_design'].value_counts() if 'study_design' in data.columns else None,
            'countries': data['country'].value_counts().head(10) if 'country' in data.columns else None,
            'journals': data['journal'].value_counts().head(10) if 'journal' in data.columns else None
        }

        return overview

    def _create_study_characteristics_plot(self, data: pd.DataFrame) -> plt.Figure:
        """Create study characteristics visualization"""

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Study design distribution
        if 'study_design' in data.columns:
            design_counts = data['study_design'].value_counts()
            ax1.pie(design_counts.values, labels=design_counts.index, autopct='%1.1f%%')
            ax1.set_title('Study Design Distribution')

        # Publication year trend
        if 'publication_year' in data.columns:
            yearly_counts = data['publication_year'].value_counts().sort_index()
            ax2.bar(yearly_counts.index, yearly_counts.values)
            ax2.set_title('Publications by Year')
            ax2.set_xlabel('Year')
            ax2.set_ylabel('Number of Studies')

        # Sample size distribution
        if 'sample_size' in data.columns:
            data['sample_size'].hist(ax=ax3, bins=20)
            ax3.set_title('Sample Size Distribution')
            ax3.set_xlabel('Sample Size')
            ax3.set_ylabel('Frequency')

        # Country distribution (top 10)
        if 'country' in data.columns:
            country_counts = data['country'].value_counts().head(10)
            ax4.barh(range(len(country_counts)), country_counts.values)
            ax4.set_yticks(range(len(country_counts)))
            ax4.set_yticklabels(country_counts.index)
            ax4.set_title('Top 10 Countries')

        plt.suptitle('Study Characteristics Overview', fontsize=16, fontweight='bold')
        plt.tight_layout()

        return fig

    def _create_temporal_trends(self, data: pd.DataFrame) -> plt.Figure:
        """Create temporal trends visualization"""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        if 'publication_year' in data.columns:
            # Cumulative publications
            yearly_counts = data['publication_year'].value_counts().sort_index()
            cumulative = yearly_counts.cumsum()

            ax1.plot(cumulative.index, cumulative.values, marker='o')
            ax1.set_title('Cumulative Publications Over Time')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Cumulative Count')
            ax1.grid(True, alpha=0.3)

            # Year-over-year growth
            if len(yearly_counts) > 1:
                yoy_growth = yearly_counts.pct_change() * 100
                ax2.bar(yoy_growth.index, yoy_growth.values)
                ax2.set_title('Year-over-Year Publication Growth (%)')
                ax2.set_xlabel('Year')
                ax2.set_ylabel('Growth (%)')
                ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
                ax2.grid(True, alpha=0.3)

        plt.suptitle('Publication Trends', fontsize=14, fontweight='bold')
        plt.tight_layout()

        return fig

    def _create_meta_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create meta-analysis summary statistics"""

        primary_results = results.get('primary_results', {})

        summary = {
            'overall_effect': primary_results.get('overall_effect', 0),
            'ci_lower': primary_results.get('ci_lower', 0),
            'ci_upper': primary_results.get('ci_upper', 0),
            'p_value': primary_results.get('p_value', 1),
            'heterogeneity_i2': primary_results.get('heterogeneity_test', {}).get('I2', 0),
            'heterogeneity_q': primary_results.get('heterogeneity_test', {}).get('Q', 0),
            'method_used': results.get('primary_method', 'unknown'),
            'total_studies': results.get('total_studies', 0)
        }

        # Effect size interpretation
        effect = summary['overall_effect']
        if abs(effect) < 0.2:
            summary['effect_magnitude'] = 'small'
        elif abs(effect) < 0.5:
            summary['effect_magnitude'] = 'medium'
        else:
            summary['effect_magnitude'] = 'large'

        # Statistical significance
        summary['significant'] = summary['p_value'] < 0.05

        return summary

    def _create_heterogeneity_plot(self, results: Dict[str, Any]) -> plt.Figure:
        """Create heterogeneity visualization"""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        het_test = results.get('primary_results', {}).get('heterogeneity_test', {})

        # I-squared plot
        i2 = het_test.get('I2', 0)
        bars = ax1.bar(['I²'], [i2], color='skyblue')
        ax1.set_ylabel('I² (%)', fontsize=12)
        ax1.set_title('Heterogeneity (I²)', fontsize=14, fontweight='bold')
        ax1.set_ylim(0, min(i2 + 10, 100))
        ax1.text(0, i2 + 1, '.1f', ha='center', va='bottom')

        # Interpret I-squared
        if i2 < 25:
            interpretation = "Low"
        elif i2 < 50:
            interpretation = "Moderate"
        elif i2 < 75:
            interpretation = "Substantial"
        else:
            interpretation = "Considerable"

        ax1.text(0.5, 0.9, f"Level: {interpretation}", ha='center', va='top',
                transform=ax1.transAxes, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

        # Q statistic
        q_stat = het_test.get('Q', 0)
        q_p = het_test.get('p_value', 1)

        color = 'red' if q_p < 0.05 else 'green'
        bars = ax2.bar(['Q'], [q_stat], color=color)
        ax2.set_ylabel('Q Statistic', fontsize=12)
        ax2.set_title('Cochran Q Test', fontsize=14, fontweight='bold')
        ax2.text(0, q_stat * 1.05, f"p = {q_p:.3f}", ha='center', va='bottom')

        plt.suptitle('Heterogeneity Assessment', fontsize=16, fontweight='bold')
        plt.tight_layout()

        return fig

    def _create_forest_plot(self, results: Dict[str, Any]) -> plt.Figure:
        """Create forest plot from meta-analysis results"""

        study_data = results.get('study_data', [])

        if not study_data:
            # Create empty plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No study data available', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Forest Plot - No Data')
            return fig

        # Convert to DataFrame for easier handling
        df = pd.DataFrame(study_data)

        # Create forest plot
        fig, ax = plt.subplots(figsize=(12, max(6, len(df) * 0.5)))

        y_positions = np.arange(len(df))

        # Plot individual studies
        for i, (_, study) in enumerate(df.iterrows()):
            effect = study.get('effect_size', 0)
            se = study.get('effect_se', 0.1)
            ci_lower = effect - 1.96 * se
            ci_upper = effect + 1.96 * se

            # Study effect point
            ax.plot(effect, i, 's', color='blue', markersize=6)

            # Confidence interval line
            ax.plot([ci_lower, ci_upper], [i, i], color='blue', linewidth=2)

        # Overall effect
        primary_results = results.get('primary_results', {})
        overall_effect = primary_results.get('overall_effect', 0)
        overall_ci_lower = primary_results.get('ci_lower', 0)
        overall_ci_upper = primary_results.get('ci_upper', 0)

        ax.plot(overall_effect, len(df), 'D', color='red', markersize=10)
        ax.plot([overall_ci_lower, overall_ci_upper], [len(df), len(df)], color='red', linewidth=3)

        # Vertical line at no effect
        ax.axvline(x=0, color='black', linestyle='--', alpha=0.7)

        # Labels
        ax.set_xlabel('Effect Size (95% CI)', fontsize=12, fontweight='bold')
        ax.set_title('Forest Plot', fontsize=14, fontweight='bold')
        ax.set_yticks(list(range(len(df))) + [len(df)])
        ax.set_yticklabels([study.get('study_id', f'Study {i+1}') for study in study_data] + ['Overall Effect'])
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def _create_funnel_plot(self, results: Dict[str, Any]) -> plt.Figure:
        """Create funnel plot for publication bias"""

        study_data = results.get('study_data', [])

        if not study_data:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, 'No study data available', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Funnel Plot - No Data')
            return fig

        df = pd.DataFrame(study_data)

        fig, ax = plt.subplots(figsize=(10, 8))

        # Individual studies
        effect_sizes = df.get('effect_size', pd.Series([0] * len(df)))
        se_values = df.get('effect_se', pd.Series([0.1] * len(df)))

        ax.scatter(effect_sizes, se_values, alpha=0.7, s=50, color='blue', edgecolors='black')

        # Pseudo-confidence intervals
        se_range = np.linspace(se_values.min(), se_values.max(), 100)
        ci_width = 1.96 * se_range

        ax.fill_between(se_range, -ci_width, ci_width, color='red', alpha=0.1)
        ax.plot(se_range, ci_width, '--', color='red', alpha=0.7, label='95% CI')
        ax.plot(se_range, -ci_width, '--', color='red', alpha=0.7)

        ax.set_xlabel('Effect Size', fontsize=12, fontweight='bold')
        ax.set_ylabel('Standard Error', fontsize=12, fontweight='bold')
        ax.set_title('Funnel Plot (Publication Bias Assessment)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Invert y-axis (convention)
        ax.invert_yaxis()

        plt.tight_layout()
        return fig

    def _create_quality_dashboard(self, quality_data: pd.DataFrame) -> plt.Figure:
        """Create quality assessment visualization"""

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Quality score distribution
        if 'overall_quality' in quality_data.columns:
            quality_data['overall_quality'].hist(ax=ax1, bins=10)
            ax1.set_title('Overall Quality Score Distribution')
            ax1.set_xlabel('Quality Score')
            ax1.set_ylabel('Frequency')

        # Risk of bias summary
        bias_columns = [col for col in quality_data.columns if 'bias' in col.lower()]
        if bias_columns:
            high_risk = quality_data[bias_columns].apply(lambda x: (x == 'High').sum())
            ax2.bar(range(len(high_risk)), high_risk.values)
            ax2.set_xticks(range(len(high_risk)))
            ax2.set_xticklabels(bias_columns, rotation=45, ha='right')
            ax2.set_title('High Risk of Bias Counts')
            ax2.set_ylabel('Number of Studies')

        # Quality components heatmap
        if len(bias_columns) > 1:
            quality_matrix = quality_data[bias_columns].apply(lambda x: x.map({'Low': 1, 'Unclear': 2, 'High': 3}))
            sns.heatmap(quality_matrix, ax=ax3, cmap='RdYlGn_r', cbar_kws={'label': 'Risk Level'})
            ax3.set_title('Quality Assessment Heatmap')
            ax3.set_ylabel('Studies')

        plt.suptitle('Quality Assessment Dashboard', fontsize=16, fontweight='bold')
        plt.tight_layout()

        return fig

    def _generate_html_dashboard(self, dashboard_data: Dict[str, Any], title: str) -> str:
        """Generate HTML dashboard"""

        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .dashboard-container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .dashboard-header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .dashboard-header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: 300;
                }}
                .dashboard-content {{
                    padding: 30px;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 40px;
                }}
                .stat-card {{
                    background: #f8f9fa;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    border-left: 4px solid #667eea;
                }}
                .stat-value {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #333;
                }}
                .stat-label {{
                    color: #666;
                    font-size: 0.9em;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .plot-container {{
                    background: white;
                    border-radius: 8px;
                    padding: 20px;
                    margin-bottom: 30px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }}
                .plot-title {{
                    font-size: 1.3em;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 15px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <h1>{title}</h1>
                    <p>Comprehensive Research Visualization Dashboard</p>
                </div>
                <div class="dashboard-content">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">{total_studies}</div>
                            <div class="stat-label">Total Studies</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{publication_years}</div>
                            <div class="stat-label">Publication Years</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{study_designs}</div>
                            <div class="stat-label">Study Designs</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{countries_covered}</div>
                            <div class="stat-label">Countries Covered</div>
                        </div>
                    </div>

                    <div id="literature-overview-plot" class="plot-container">
                        <div class="plot-title">Literature Overview</div>
                        <!-- Plot will be inserted here -->
                    </div>

                    <div id="study-characteristics-plot" class="plot-container">
                        <div class="plot-title">Study Characteristics</div>
                        <!-- Plot will be inserted here -->
                    </div>

                    <div id="temporal-trends-plot" class="plot-container">
                        <div class="plot-title">Publication Trends Over Time</div>
                        <!-- Plot will be inserted here -->
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        # Get data for stats
        literature_overview = dashboard_data.get('literature_overview', {})
        total_studies = literature_overview.get('total_studies', 0)
        publication_years = len(literature_overview.get('publication_years', {}))
        study_designs = len(literature_overview.get('study_designs', {}))
        countries_covered = len(literature_overview.get('countries', {}))

        return html_template.format(
            title=title,
            total_studies=total_studies,
            publication_years=publication_years,
            study_designs=study_designs,
            countries_covered=countries_covered
        )


class AutomatedVisualizationGenerator:
    """Main automated visualization generation system"""

    def __init__(self, output_dir: str = "research_visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.meta_visualizer = MetaAnalysisVisualizer()
        self.dashboard_generator = ResearchDashboardGenerator()

    def generate_comprehensive_visualizations(self,
                                           literature_data: pd.DataFrame = None,
                                           meta_results: Dict[str, Any] = None,
                                           quality_data: pd.DataFrame = None,
                                           project_type: str = "systematic_review") -> Dict[str, str]:
        """Generate comprehensive visualizations for a research project"""

        generated_files = {}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_output_dir = self.output_dir / f"{project_type}_{timestamp}"
        project_output_dir.mkdir(exist_ok=True)

        logger.info(f"Generating visualizations for {project_type} project")

        # Generate literature visualizations
        if literature_data is not None and not literature_data.empty:
            logger.info("Generating literature visualizations...")

            # Study characteristics plot
            study_char_fig = self.dashboard_generator._create_study_characteristics_plot(literature_data)
            study_char_path = project_output_dir / "study_characteristics.png"
            study_char_fig.savefig(study_char_path, dpi=300, bbox_inches='tight')
            generated_files['study_characteristics'] = str(study_char_path)

            # Temporal trends plot
            temporal_fig = self.dashboard_generator._create_temporal_trends(literature_data)
            temporal_path = project_output_dir / "temporal_trends.png"
            temporal_fig.savefig(temporal_path, dpi=300, bbox_inches='tight')
            generated_files['temporal_trends'] = str(temporal_path)

            plt.close('all')  # Close all figures to free memory

        # Generate meta-analysis visualizations
        if meta_results is not None:
            logger.info("Generating meta-analysis visualizations...")

            # Prepare study data for plots
            study_data = meta_results.get('study_data', [])
            if study_data:
                study_df = pd.DataFrame(study_data)

                # Add confidence intervals if not present
                if 'ci_lower' not in study_df.columns:
                    study_df['ci_lower'] = study_df['effect_size'] - 1.96 * study_df['effect_se']
                    study_df['ci_upper'] = study_df['effect_size'] + 1.96 * study_df['effect_se']

                if 'study_label' not in study_df.columns:
                    study_df['study_label'] = [f"Study {i+1}" for i in range(len(study_df))]

                # Forest plot
                forest_fig = self.meta_visualizer.forest_plot(study_df, save_path=str(project_output_dir / "forest_plot.png"))
                generated_files['forest_plot'] = str(project_output_dir / "forest_plot.png")

                # Funnel plot
                funnel_fig = self.meta_visualizer.funnel_plot(study_df, save_path=str(project_output_dir / "funnel_plot.png"))
                generated_files['funnel_plot'] = str(project_output_dir / "funnel_plot.png")

                # Heterogeneity plot
                het_fig = self.dashboard_generator._create_heterogeneity_plot(meta_results)
                het_path = project_output_dir / "heterogeneity_plot.png"
                het_fig.savefig(het_path, dpi=300, bbox_inches='tight')
                generated_files['heterogeneity_plot'] = str(het_path)

            plt.close('all')

        # Generate quality assessment visualizations
        if quality_data is not None and not quality_data.empty:
            logger.info("Generating quality assessment visualizations...")

            quality_fig = self.dashboard_generator._create_quality_dashboard(quality_data)
            quality_path = project_output_dir / "quality_assessment.png"
            quality_fig.savefig(quality_path, dpi=300, bbox_inches='tight')
            generated_files['quality_assessment'] = str(quality_path)

            plt.close('all')

        # Generate comprehensive dashboard
        if literature_data is not None:
            logger.info("Generating research dashboard...")

            dashboard_path = self.dashboard_generator.create_systematic_review_dashboard(
                literature_data, meta_results, quality_data
            )
            generated_files['dashboard'] = dashboard_path

        logger.info(f"Generated {len(generated_files)} visualization files")
        logger.info(f"Output directory: {project_output_dir}")

        return generated_files


# CLI Interface and utility functions
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automated Visualization Generation System")
    parser.add_argument("--literature-data", help="CSV file with literature data")
    parser.add_argument("--meta-results", help="JSON file with meta-analysis results")
    parser.add_argument("--quality-data", help="CSV file with quality assessment data")
    parser.add_argument("--project-type", default="systematic_review",
                       help="Type of research project")
    parser.add_argument("--output-dir", default="research_visualizations",
                       help="Output directory")

    args = parser.parse_args()

    generator = AutomatedVisualizationGenerator(args.output_dir)

    # Load data
    literature_data = pd.read_csv(args.literature_data) if args.literature_data else None
    meta_results = json.load(open(args.meta_results)) if args.meta_results else None
    quality_data = pd.read_csv(args.quality_data) if args.quality_data else None

    # Generate visualizations
    generated_files = generator.generate_comprehensive_visualizations(
        literature_data, meta_results, quality_data, args.project_type
    )

    print(f"Generated {len(generated_files)} visualization files:")
    for name, path in generated_files.items():
        print(f"  {name}: {path}")
