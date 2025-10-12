#!/usr/bin/env python3
"""
Python Network Meta-Analysis Visualization for Type 2 Diabetes Drug Sequencing
Creates publication-ready visualizations using matplotlib, seaborn, and plotly
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

# Set style for publication-ready plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DiabetesNMAAnalysis:
    """Main class for diabetes drug sequencing NMA analysis and visualization"""

    def __init__(self):
        self.treatments = [
            'SGLT2i', 'GLP-1RA', 'DPP-4i', 'TZD',
            'Tirzepatide', 'SGLT2i+DPP-4i', 'TZD+SGLT2i+Metformin'
        ]

        self.outcomes = [
            'Cardiovascular', 'Renal', 'HbA1c_Reduction', 'Weight_Change', 'Hypoglycemia'
        ]

        # SUCRA rankings from the analysis
        self.sucra_data = {
            'Cardiovascular': [92, 78, 45, 35, 85, 68, 55],
            'Renal': [95, 68, 40, 30, 75, 72, 50],
            'HbA1c_Reduction': [58, 78, 35, 45, 92, 65, 75],
            'Weight_Change': [75, 82, 45, 25, 95, 68, 35],
            'Hypoglycemia': [88, 55, 72, 45, 65, 78, 40]
        }

        # Treatment effects data
        self.effects_data = {
            'Cardiovascular_HR': [0.76, 0.78, 0.99, 0.95, 0.74, 0.82, 0.85],
            'Renal_HR': [0.62, 0.83, 1.05, 1.02, 0.75, 0.78, 0.88],
            'HbA1c_Change': [-0.35, -1.45, -0.50, -0.65, -1.85, -0.80, -1.15],
            'Weight_Change': [-2.8, -3.8, -0.2, 1.2, -5.2, -1.8, -0.5],
            'Hypoglycemia_RR': [0.92, 1.05, 1.05, 1.15, 0.95, 0.98, 1.08]
        }

    def create_sucra_heatmap(self):
        """Create SUCRA ranking heatmap"""
        fig, ax = plt.subplots(figsize=(12, 8))

        sucra_df = pd.DataFrame(self.sucra_data, index=self.treatments)

        sns.heatmap(sucra_df, annot=True, cmap='RdYlBu_r', center=50,
                   square=True, ax=ax, cbar_kws={'shrink': 0.8})

        ax.set_title('SUCRA Rankings Across Outcomes\nType 2 Diabetes Drug Sequencing NMA',
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Outcomes', fontsize=12)
        ax.set_ylabel('Treatments', fontsize=12)

        plt.tight_layout()
        plt.savefig('type_2_diabetes_drug_sequencing/09_python_visualization/sucra_heatmap.png',
                   dpi=300, bbox_inches='tight')
        return fig

    def create_rank_plot(self):
        """Create treatment ranking plot"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()

        colors = plt.cm.Set3(np.linspace(0, 1, len(self.treatments)))

        for i, (outcome, sucra_values) in enumerate(self.sucra_data.items()):
            if i < 5:  # Only first 5 subplots
                treatment_sucra = list(zip(self.treatments, sucra_values))
                treatment_sucra.sort(key=lambda x: x[1], reverse=True)

                treatments_sorted = [t[0] for t in treatment_sucra]
                sucra_sorted = [t[1] for t in treatment_sucra]

                bars = axes[i].bar(range(len(treatments_sorted)), sucra_sorted,
                                 color=colors, alpha=0.8)

                axes[i].set_title(f'{outcome.replace("_", " ")}', fontsize=14, fontweight='bold')
                axes[i].set_xlabel('Treatments', fontsize=10)
                axes[i].set_ylabel('SUCRA Value (%)', fontsize=10)
                axes[i].set_xticks(range(len(treatments_sorted)))
                axes[i].set_xticklabels(treatments_sorted, rotation=45, ha='right', fontsize=8)

                # Add value labels on bars
                for bar, value in zip(bars, sucra_sorted):
                    axes[i].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                               f'{value:.1f}', ha='center', va='bottom', fontsize=9)

        plt.suptitle('Treatment Rankings Across Outcomes (SUCRA Values)\nHigher values indicate better performance',
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.savefig('type_2_diabetes_drug_sequencing/09_python_visualization/treatment_rankings.png',
                   dpi=300, bbox_inches='tight')
        return fig

    def create_forest_plot(self):
        """Create forest plot for treatment effects"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.flatten()

        outcomes_to_plot = [
            ('Cardiovascular_HR', 'Cardiovascular Outcomes (HR vs Placebo)'),
            ('Renal_HR', 'Renal Outcomes (HR vs Placebo)'),
            ('HbA1c_Change', 'HbA1c Reduction (%)'),
            ('Weight_Change', 'Weight Change (kg)')
        ]

        for i, (outcome_key, title) in enumerate(outcomes_to_plot):
            effects = self.effects_data[outcome_key]
            errors = [0.15, 0.12, 0.08, 0.10, 0.11, 0.13, 0.09]  # Placeholder CI

            y_pos = np.arange(len(self.treatments))

            axes[i].errorbar(effects, y_pos, xerr=errors, fmt='o',
                           capsize=5, capthick=2, markersize=8, alpha=0.8)

            axes[i].set_yticks(y_pos)
            axes[i].set_yticklabels(self.treatments, fontsize=10)
            axes[i].set_xlabel('Effect Size', fontsize=11)
            axes[i].set_title(title, fontsize=12, fontweight='bold')
            axes[i].axvline(x=0, color='red', linestyle='--', alpha=0.7, linewidth=1)
            axes[i].grid(True, alpha=0.3)

        plt.suptitle('Forest Plot: Treatment Effects Across Outcomes\nType 2 Diabetes Drug Sequencing NMA',
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.savefig('type_2_diabetes_drug_sequencing/09_python_visualization/forest_plots.png',
                   dpi=300, bbox_inches='tight')
        return fig

    def create_interactive_dashboard(self):
        """Create interactive Plotly dashboard"""
        # SUCRA radar chart
        fig = go.Figure()

        for i, treatment in enumerate(self.treatments):
            sucra_values = [self.sucra_data[outcome][i] for outcome in self.outcomes]

            fig.add_trace(go.Scatterpolar(
                r=sucra_values,
                theta=self.outcomes,
                fill='toself',
                name=treatment,
                opacity=0.7
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickangle=0,
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    tickfont=dict(size=11)
                )
            ),
            title=dict(
                text='Treatment Performance Radar Chart (SUCRA Values)<br>Type 2 Diabetes Drug Sequencing NMA',
                x=0.5,
                font=dict(size=16)
            ),
            showlegend=True,
            legend=dict(
                x=1.1,
                y=0.5,
                font=dict(size=10)
            )
        )

        fig.write_html('type_2_diabetes_drug_sequencing/09_python_visualization/interactive_sucra_radar.html')
        return fig

    def create_network_geometry(self):
        """Create network geometry plot"""
        # Simplified network based on available comparisons
        treatments = ['Placebo', 'SGLT2i', 'GLP-1RA', 'DPP-4i', 'Tirzepatide']

        # Create connections based on available evidence
        edges = [
            ('Placebo', 'SGLT2i'), ('Placebo', 'GLP-1RA'), ('Placebo', 'DPP-4i'),
            ('SGLT2i', 'GLP-1RA'), ('SGLT2i', 'Tirzepatide'), ('GLP-1RA', 'Tirzepatide'),
            ('DPP-4i', 'SGLT2i'), ('DPP-4i', 'GLP-1RA')
        ]

        # Create positions for nodes
        pos = {
            'Placebo': (0.5, 0.8),
            'SGLT2i': (0.2, 0.5),
            'GLP-1RA': (0.8, 0.5),
            'DPP-4i': (0.5, 0.2),
            'Tirzepatide': (0.5, 0.5)
        }

        fig, ax = plt.subplots(figsize=(10, 8))

        # Draw edges
        for edge in edges:
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.6, linewidth=2)

        # Draw nodes
        for treatment, (x, y) in pos.items():
            size = 2000 if treatment == 'Placebo' else 1500
            color = 'red' if treatment == 'Placebo' else 'blue'
            ax.scatter(x, y, s=size, c=color, alpha=0.8, edgecolors='black', linewidth=2)
            ax.text(x, y + 0.05, treatment, ha='center', va='center',
                   fontsize=11, fontweight='bold')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title('Evidence Network Geometry\nType 2 Diabetes Drug Sequencing NMA',
                    fontsize=14, fontweight='bold', pad=20)
        ax.axis('off')

        plt.tight_layout()
        plt.savefig('type_2_diabetes_drug_sequencing/09_python_visualization/network_geometry.png',
                   dpi=300, bbox_inches='tight')
        return fig

    def create_summary_dashboard(self):
        """Create comprehensive summary dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('SUCRA Rankings Heatmap', 'Treatment Effects Forest Plot',
                          'Network Geometry', 'Interactive Radar Chart'),
            specs=[[{"type": "heatmap"}, {"type": "xy"}],
                   [{"type": "scatter"}, {"type": "polar"}]]
        )

        # Add SUCRA heatmap data
        sucra_df = pd.DataFrame(self.sucra_data, index=self.treatments)
        fig.add_trace(
            go.Heatmap(z=sucra_df.values, x=self.outcomes, y=self.treatments,
                      colorscale='RdYlBu_r', showscale=True),
            row=1, col=1
        )

        # Add sample forest plot data (simplified)
        treatments_subset = self.treatments[:5]
        effects_subset = [self.effects_data['HbA1c_Change'][i] for i in range(5)]
        errors_subset = [0.2, 0.15, 0.18, 0.12, 0.16]

        fig.add_trace(
            go.Scatter(x=effects_subset, y=treatments_subset, mode='markers',
                      error_x=dict(type='data', array=errors_subset, visible=True),
                      marker=dict(size=10), showlegend=False),
            row=1, col=2
        )

        # Add network geometry (simplified)
        nodes_x = [0.5, 0.2, 0.8, 0.5, 0.5]
        nodes_y = [0.8, 0.5, 0.5, 0.2, 0.5]
        node_names = ['Placebo', 'SGLT2i', 'GLP-1RA', 'DPP-4i', 'Tirzepatide']

        fig.add_trace(
            go.Scatter(x=nodes_x, y=nodes_y, mode='markers+text',
                      text=node_names, textposition="middle right",
                      marker=dict(size=20), showlegend=False),
            row=2, col=1
        )

        # Add radar chart data
        for i, treatment in enumerate(self.treatments[:3]):  # Show only first 3 for clarity
            sucra_values = [self.sucra_data[outcome][i] for outcome in self.outcomes]
            fig.add_trace(
                go.Scatterpolar(r=sucra_values, theta=self.outcomes, name=treatment),
                row=2, col=2
            )

        fig.update_layout(
            title_text="Comprehensive Diabetes Drug Sequencing NMA Dashboard",
            title_x=0.5,
            height=800,
            showlegend=True
        )

        fig.write_html('type_2_diabetes_drug_sequencing/09_python_visualization/nma_dashboard.html')
        return fig

    def run_all_visualizations(self):
        """Run all visualization functions"""
        print("Creating SUCRA heatmap...")
        self.create_sucra_heatmap()

        print("Creating treatment ranking plots...")
        self.create_rank_plot()

        print("Creating forest plots...")
        self.create_forest_plot()

        print("Creating network geometry...")
        self.create_network_geometry()

        print("Creating interactive dashboard...")
        self.create_interactive_dashboard()

        print("Creating summary dashboard...")
        self.create_summary_dashboard()

        print("All visualizations completed!")
        print("Files saved in: type_2_diabetes_drug_sequencing/09_python_visualization/")

# Main execution
if __name__ == "__main__":
    analysis = DiabetesNMAAnalysis()
    analysis.run_all_visualizations()
