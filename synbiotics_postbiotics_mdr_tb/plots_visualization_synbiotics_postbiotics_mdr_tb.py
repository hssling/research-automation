#!/usr/bin/env python3
"""
Plots and Visualization Script for Synbiotics and Postbiotics in MDR-TB Meta-Analysis

This script generates forest plots, funnel plots, and other visualizations
for the systematic review and meta-analysis.

Requirements:
- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- statsmodels (for meta-analysis)
- forestplot (for forest plots)
- plotly (for interactive plots)

Install dependencies:
pip install pandas numpy matplotlib seaborn scipy statsmodels forestplot plotly
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.meta_analysis import (
    combine_effects,
    effectsize_smd,
    effectsize_2proportions
)
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class MDRTBVisualizations:
    """
    Visualization class for MDR-TB synbiotics/postbiotics meta-analysis
    """

    def __init__(self, data_path=None):
        """
        Initialize with data path

        Parameters:
        data_path (str): Path to cleaned data file
        """
        self.data_path = data_path
        self.data = None

        if data_path:
            self.load_data()

    def load_data(self):
        """Load and preprocess data"""
        try:
            self.data = pd.read_csv(self.data_path)
            print(f"Data loaded successfully. Shape: {self.data.shape}")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = None

    def create_forest_plot(self, outcome='treatment_success',
                          title="Forest Plot: Treatment Success Rate",
                          save_path=None):
        """
        Create forest plot for specified outcome

        Parameters:
        outcome (str): Column name for outcome data
        title (str): Plot title
        save_path (str): Path to save figure
        """
        if self.data is None:
            print("No data loaded")
            return

        # Prepare data for forest plot
        forest_data = self.data[['study_id', f'{outcome}_rr', f'{outcome}_ci_low',
                               f'{outcome}_ci_high', 'weight']].copy()

        forest_data.columns = ['study', 'RR', 'ci_low', 'ci_high', 'weight']

        # Create forest plot
        fig, ax = plt.subplots(figsize=(12, len(forest_data) * 0.5 + 2))

        # Plot individual studies
        y_pos = np.arange(len(forest_data))

        # Error bars
        ax.errorbar(forest_data['RR'], y_pos,
                   xerr=[forest_data['RR'] - forest_data['ci_low'],
                        forest_data['ci_high'] - forest_data['RR']],
                   fmt='o', color='blue', capsize=3)

        # Vertical line at 1.0
        ax.axvline(x=1.0, color='red', linestyle='--', alpha=0.7)

        # Study labels
        ax.set_yticks(y_pos)
        ax.set_yticklabels(forest_data['study'])
        ax.set_xlabel('Risk Ratio (95% CI)')
        ax.set_title(title)

        # Add weights as text
        for i, weight in enumerate(forest_data['weight']):
            ax.text(0.1, y_pos[i], '.1f', ha='left', va='center')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Forest plot saved to {save_path}")

        plt.show()

    def create_funnel_plot(self, outcome='treatment_success',
                          title="Funnel Plot: Publication Bias Assessment",
                          save_path=None):
        """
        Create funnel plot for publication bias assessment

        Parameters:
        outcome (str): Column name for outcome data
        title (str): Plot title
        save_path (str): Path to save figure
        """
        if self.data is None:
            print("No data loaded")
            return

        # Prepare data
        funnel_data = self.data[[f'{outcome}_rr', 'se']].copy()
        funnel_data.columns = ['effect_size', 'se']

        fig, ax = plt.subplots(figsize=(8, 6))

        # Scatter plot
        ax.scatter(funnel_data['effect_size'], 1/funnel_data['se'],
                  alpha=0.6, s=50)

        # Funnel boundaries (95% CI)
        x_vals = np.linspace(min(funnel_data['effect_size']) - 0.5,
                           max(funnel_data['effect_size']) + 0.5, 100)
        se_vals = np.linspace(min(funnel_data['se']), max(funnel_data['se']), 100)

        # Upper and lower bounds
        y_upper = 1/se_vals * 1.96 / se_vals
        y_lower = 1/se_vals * (-1.96) / se_vals

        # Plot funnel
        ax.plot(x_vals, np.interp(x_vals, funnel_data['effect_size'],
                                1/funnel_data['se']), 'r--', alpha=0.5)

        ax.set_xlabel('Effect Size (Risk Ratio)')
        ax.set_ylabel('Precision (1/SE)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Funnel plot saved to {save_path}")

        plt.show()

    def create_subgroup_forest_plots(self, subgroup_var='intervention_type',
                                    outcome='treatment_success',
                                    save_path=None):
        """
        Create subgroup forest plots

        Parameters:
        subgroup_var (str): Column name for subgroup variable
        outcome (str): Outcome variable
        save_path (str): Path to save figure
        """
        if self.data is None:
            print("No data loaded")
            return

        subgroups = self.data[subgroup_var].unique()

        fig, axes = plt.subplots(len(subgroups), 1,
                                figsize=(12, 6 * len(subgroups)))

        if len(subgroups) == 1:
            axes = [axes]

        for i, subgroup in enumerate(subgroups):
            subgroup_data = self.data[self.data[subgroup_var] == subgroup]

            if len(subgroup_data) > 0:
                # Prepare forest plot for subgroup
                y_pos = np.arange(len(subgroup_data))

                axes[i].errorbar(subgroup_data[f'{outcome}_rr'], y_pos,
                               xerr=[subgroup_data[f'{outcome}_rr'] - subgroup_data[f'{outcome}_ci_low'],
                                    subgroup_data[f'{outcome}_ci_high'] - subgroup_data[f'{outcome}_rr']],
                               fmt='o', color='blue', capsize=3)

                axes[i].axvline(x=1.0, color='red', linestyle='--', alpha=0.7)
                axes[i].set_yticks(y_pos)
                axes[i].set_yticklabels(subgroup_data['study_id'])
                axes[i].set_xlabel('Risk Ratio (95% CI)')
                axes[i].set_title(f'{subgroup}: {outcome.replace("_", " ").title()}')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Subgroup forest plots saved to {save_path}")

        plt.show()

    def create_interactive_dashboard(self, html_path="mdr_tb_dashboard.html"):
        """
        Create interactive dashboard with Plotly

        Parameters:
        html_path (str): Path to save HTML dashboard
        """
        if self.data is None:
            print("No data loaded")
            return

        # Create subplot figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Treatment Success Forest Plot',
                          'Culture Conversion Time',
                          'Publication Bias Funnel',
                          'Subgroup Analysis'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )

        # Forest plot for treatment success
        fig.add_trace(
            go.Scatter(x=self.data['treatment_success_rr'],
                      y=self.data['study_id'],
                      mode='markers',
                      error_x=dict(
                          type='data',
                          symmetric=False,
                          array=self.data['treatment_success_ci_high'] - self.data['treatment_success_rr'],
                          arrayminus=self.data['treatment_success_rr'] - self.data['treatment_success_ci_low']
                      ),
                      name='Treatment Success'),
            row=1, col=1
        )

        # Add line at RR = 1
        fig.add_vline(x=1, line_dash="dash", line_color="red", row=1, col=1)

        # Culture conversion scatter
        fig.add_trace(
            go.Scatter(x=self.data['conversion_time_md'],
                      y=self.data['study_id'],
                      mode='markers',
                      error_x=dict(
                          type='data',
                          symmetric=False,
                          array=self.data['conversion_time_ci_high'] - self.data['conversion_time_md'],
                          arrayminus=self.data['conversion_time_md'] - self.data['conversion_time_ci_low']
                      ),
                      name='Conversion Time'),
            row=1, col=2
        )

        # Funnel plot
        fig.add_trace(
            go.Scatter(x=self.data['treatment_success_rr'],
                      y=1/self.data['treatment_success_se'],
                      mode='markers',
                      name='Studies'),
            row=2, col=1
        )

        # Subgroup bar chart
        subgroup_means = self.data.groupby('intervention_type')['treatment_success_rr'].mean()
        fig.add_trace(
            go.Bar(x=subgroup_means.index,
                  y=subgroup_means.values,
                  name='Subgroup Means'),
            row=2, col=2
        )

        fig.update_layout(height=800, title_text="MDR-TB Synbiotics/Postbiotics Meta-Analysis Dashboard")
        fig.write_html(html_path)
        print(f"Interactive dashboard saved to {html_path}")

    def create_summary_visualizations(self, save_path_prefix="mdr_tb_summary"):
        """
        Create summary visualizations for manuscript

        Parameters:
        save_path_prefix (str): Prefix for saved files
        """
        if self.data is None:
            print("No data loaded")
            return

        # Summary statistics plot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

        # Study characteristics
        study_types = self.data['study_design'].value_counts()
        ax1.pie(study_types.values, labels=study_types.index, autopct='%1.1f%%')
        ax1.set_title('Study Design Distribution')

        # Geographic distribution
        regions = self.data['country'].value_counts().head(10)
        regions.plot(kind='barh', ax=ax2)
        ax2.set_title('Geographic Distribution (Top 10)')
        ax2.set_xlabel('Number of Studies')

        # Intervention types
        intervention_types = self.data['intervention_type'].value_counts()
        intervention_types.plot(kind='bar', ax=ax3)
        ax3.set_title('Intervention Types')
        ax3.set_ylabel('Number of Studies')
        ax3.tick_params(axis='x', rotation=45)

        # Effect sizes distribution
        ax4.hist(self.data['treatment_success_rr'], bins=10, alpha=0.7, edgecolor='black')
        ax4.axvline(x=1.0, color='red', linestyle='--', label='No Effect')
        ax4.set_title('Distribution of Treatment Success Risk Ratios')
        ax4.set_xlabel('Risk Ratio')
        ax4.set_ylabel('Frequency')
        ax4.legend()

        plt.tight_layout()

        summary_path = f"{save_path_prefix}_study_characteristics.png"
        plt.savefig(summary_path, dpi=300, bbox_inches='tight')
        print(f"Summary visualizations saved to {summary_path}")
        plt.show()

# Example usage
if __name__ == "__main__":
    # Initialize visualizer
    viz = MDRTBVisualizations()

    # Example with dummy data for demonstration
    np.random.seed(42)
    dummy_data = pd.DataFrame({
        'study_id': [f'Study_{i}' for i in range(1, 11)],
        'treatment_success_rr': np.random.uniform(0.8, 1.5, 10),
        'treatment_success_ci_low': np.random.uniform(0.6, 0.9, 10),
        'treatment_success_ci_high': np.random.uniform(1.2, 2.0, 10),
        'weight': np.random.uniform(5, 15, 10),
        'se': np.random.uniform(0.1, 0.3, 10),
        'conversion_time_md': np.random.uniform(-2, 2, 10),
        'conversion_time_ci_low': np.random.uniform(-3, -1, 10),
        'conversion_time_ci_high': np.random.uniform(1, 3, 10),
        'study_design': np.random.choice(['RCT', 'Cohort'], 10),
        'country': np.random.choice(['China', 'India', 'South Africa', 'Russia'], 10),
        'intervention_type': np.random.choice(['Synbiotic', 'Postbiotic'], 10)
    })

    viz.data = dummy_data

    # Generate plots
    print("Generating forest plot...")
    viz.create_forest_plot(save_path="forest_plot_treatment_success.png")

    print("Generating funnel plot...")
    viz.create_funnel_plot(save_path="funnel_plot_publication_bias.png")

    print("Generating subgroup plots...")
    viz.create_subgroup_forest_plots(save_path="subgroup_forest_plots.png")

    print("Generating summary visualizations...")
    viz.create_summary_visualizations(save_path_prefix="mdr_tb_summary")

    print("Generating interactive dashboard...")
    viz.create_interactive_dashboard(html_path="mdr_tb_interactive_dashboard.html")

    print("\nAll visualizations generated successfully!")
    print("\nFiles created:")
    print("- forest_plot_treatment_success.png")
    print("- funnel_plot_publication_bias.png")
    print("- subgroup_forest_plots.png")
    print("- mdr_tb_summary_study_characteristics.png")
    print("- mdr_tb_interactive_dashboard.html")
