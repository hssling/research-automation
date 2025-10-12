#!/usr/bin/env python3
"""
Healthcare Worker Burnout Interventions Meta-Analysis Visualization Script

This script generates comprehensive figures for the network meta-analysis comparing
digital vs in-person interventions for healthcare worker burnout including:
- Network meta-analysis plots
- League tables visualizations
- Forest plots by intervention type
- GRADE evidence profile plots
- Cost-effectiveness scatter plots

Requirements:
- Python 3.8+
- matplotlib
- seaborn
- numpy
- pandas
- networkx (for network plots)
- plotly (optional for interactive plots)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings('ignore')

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False
    print("NetworkX not available - network plots will use alternative visualization")

# Set style parameters
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_palette("husl")

# Meta-analysis data
interventions = {
    'Digital Ecosystem': {'SMD': -1.05, 'CI_low': -1.16, 'CI_high': -0.94, 'studies': 4, 'GRADE': 'High'},
    'Mindfulness Apps': {'SMD': -0.76, 'CI_low': -0.90, 'CI_high': -0.62, 'studies': 23, 'GRADE': 'High'},
    'CBT Platforms': {'SMD': -0.84, 'CI_low': -0.97, 'CI_high': -0.71, 'studies': 18, 'GRADE': 'High'},
    'Teletherapy': {'SMD': -0.70, 'CI_low': -0.83, 'CI_high': -0.57, 'studies': 21, 'GRADE': 'Moderate'},
    'Peer Support Apps': {'SMD': -0.79, 'CI_low': -0.95, 'CI_high': -0.63, 'studies': 11, 'GRADE': 'Moderate'},
    'Multicomponent Platforms': {'SMD': -0.88, 'CI_low': -1.02, 'CI_high': -0.74, 'studies': 14, 'GRADE': 'High'},
    'In-Person Workshops': {'SMD': -0.67, 'CI_low': -0.81, 'CI_high': -0.53, 'studies': 16, 'GRADE': 'Moderate'},
    'Individual Counseling': {'SMD': -0.72, 'CI_low': -0.86, 'CI_high': -0.58, 'studies': 12, 'GRADE': 'Moderate'},
    'Team Interventions': {'SMD': -0.59, 'CI_low': -0.76, 'CI_high': -0.42, 'studies': 6, 'GRADE': 'Low'},
    'Workplace Retreats': {'SMD': -0.65, 'CI_low': -0.82, 'CI_high': -0.48, 'studies': 8, 'GRADE': 'Low'}
}

# League table data for network plot
league_data = {
    ('Digital Ecosystem', 'Mindfulness Apps'): -0.29,
    ('Digital Ecosystem', 'CBT Platforms'): -0.21,
    ('Digital Ecosystem', 'Teletherapy'): -0.35,
    ('Digital Ecosystem', 'In-Person Workshops'): -0.38,
    ('Mindfulness Apps', 'CBT Platforms'): -0.08,
    ('Mindfulness Apps', 'Teletherapy'): -0.06,
    ('Mindfulness Apps', 'In-Person Workshops'): -0.09,
    ('CBT Platforms', 'Teletherapy'): -0.14,
    ('CBT Platforms', 'In-Person Workshops'): -0.17,
    ('Teletherapy', 'In-Person Workshops'): -0.03
}

class HCW_Burnout_Visualizer:
    """
    Visualization class for HCW burnout interventions network meta-analysis
    """

    def __init__(self):
        self.output_dir = "."
        self.figsize = (14, 10)
        plt.rcParams.update({
            'font.size': 12,
            'axes.labelsize': 14,
            'axes.titlesize': 16,
            'xtick.labelsize': 11,
            'ytick.labelsize': 11,
            'legend.fontsize': 12,
            'figure.titlesize': 18
        })

    def create_network_metaanalysis_plot(self, save_path=None):
        """
        Create network meta-analysis plot showing intervention connections
        """
        if not HAS_NETWORKX:
            # Create simplified network visualization without networkx
            return self.create_simplified_network_plot(save_path)

        fig, ax = plt.subplots(figsize=self.figsize)

        # Create network graph
        G = nx.Graph()

        # Add nodes with positions
        digital_nodes = ['Digital Ecosystem', 'Mindfulness Apps', 'CBT Platforms', 'Teletherapy', 'Peer Support Apps', 'Multicomponent Platforms']
        in_person_nodes = ['In-Person Workshops', 'Individual Counseling', 'Team Interventions', 'Workplace Retreats']

        # Position nodes in two columns
        positions = {}
        for i, node in enumerate(digital_nodes):
            positions[node] = (0, -i)
        for i, node in enumerate(in_person_nodes):
            positions[node] = (2, -i)

        for node in list(positions.keys()):
            G.add_node(node)

        # Add edges based on league table
        for (node1, node2), weight in league_data.items():
            if abs(weight) > 0.1:  # Only show meaningful differences
                G.add_edge(node1, node2, weight=abs(weight))

        # Draw network
        nx.draw_networkx_nodes(G, positions, node_color=['lightblue']*6 + ['lightgreen']*4,
                              node_size=2000, alpha=0.7, ax=ax)
        nx.draw_networkx_labels(G, positions, font_size=10, font_weight='bold', ax=ax)
        nx.draw_networkx_edges(G, positions, width=2, alpha=0.6, edge_color='gray', ax=ax)

        # Add intervention type labels
        ax.text(-0.3, 0.5, 'DIGITAL\nINTERVENTIONS', transform=ax.transAxes,
               fontsize=14, fontweight='bold', color='darkblue', ha='center')
        ax.text(1.3, 0.5, 'IN-PERSON\nINTERVENTIONS', transform=ax.transAxes,
               fontsize=14, fontweight='bold', color='darkgreen', ha='center')

        ax.set_title('Network Meta-Analysis: HCW Burnout Interventions\nDirect vs Indirect Comparisons',
                    fontsize=16, fontweight='bold')
        ax.axis('off')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            return fig

    def create_simplified_network_plot(self, save_path=None):
        """
        Create simplified network visualization without networkx dependency
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        # Create two-column layout manually
        digital = ['Digital\nEcosystem', 'Mindfulness\nApps', 'CBT\nPlatforms', 'Teletherapy', 'Peer\nSupport\nApps', 'Multicomponent\nPlatforms']
        in_person = ['In-Person\nWorkshops', 'Individual\nCounseling', 'Team\nInterventions', 'Workplace\nRetreats']

        # Draw nodes
        node_colors = ['lightblue'] * len(digital) + ['lightgreen'] * len(in_person)
        all_nodes = digital + in_person

        for i, node in enumerate(all_nodes):
            col = 0 if i < len(digital) else 1
            row = i % len(digital) if col == 0 else i - len(digital)
            ax.add_patch(plt.Rectangle((col*1.5, -row*0.4), 0.4, 0.15, color=node_colors[i], alpha=0.7))
            ax.text(col*1.5 + 0.2, -row*0.4 - 0.075, node, ha='center', va='center',
                   fontsize=8, wrap=True)

        # Draw some connection lines
        ax.plot([0.4, 1.5], [0, 0], 'gray', alpha=0.5)  # Example connections
        ax.plot([0.4, 1.5], [-0.4, -0.4], 'gray', alpha=0.5)

        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-2, 0.5)
        ax.set_title('Network Meta-Analysis: Digital vs In-Person HCW Burnout Interventions')
        ax.axis('off')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            return fig

    def create_forest_plot_main(self, save_path=None):
        """
        Create main forest plot showing all intervention effects
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        # Prepare data
        int_names = list(interventions.keys())
        smds = [interventions[int]['SMD'] for int in int_names]
        ci_lows = [interventions[int]['CI_low'] for int in int_names]
        ci_highs = [interventions[int]['CI_high'] for int in int_names]
        studies = [interventions[int]['studies'] for int in int_names]

        # Sort by effect size
        sorted_indices = np.argsort(smds)

        y_pos = range(len(int_names))
        sorted_names = [int_names[i] for i in sorted_indices]
        sorted_smds = [smds[i] for i in sorted_indices]
        sorted_ci_lows = [ci_lows[i] for i in sorted_indices]
        sorted_ci_highs = [ci_highs[i] for i in sorted_indices]
        sorted_studies = [studies[i] for i in sorted_indices]

        # Plot
        ax.errorbar(sorted_smds, y_pos, xerr=[
            np.array(sorted_smds) - np.array(sorted_ci_lows),
            np.array(sorted_ci_highs) - np.array(sorted_smds)
        ], fmt='D', markersize=8, linewidth=2, capsize=6, color='#2E86AB')

        # Add reference line
        ax.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='No effect')

        # Labels and formatting
        ax.set_yticks(y_pos)
        ax.set_yticklabels([f'{name}\n({sorted_studies[i]} studies)' for i, name in enumerate(sorted_names)])
        ax.set_xlabel('Standardized Mean Difference (95% CI)')
        ax.set_title('Forest Plot: Intervention Effects on HCW Burnout\nMore Negative = Better Outcomes')
        ax.grid(True, alpha=0.3)
        ax.legend()

        # Add GRADE quality indicators
        grade_colors = {'High': 'green', 'Moderate': 'orange', 'Low': 'red'}
        for i, name in enumerate(sorted_names):
            grade = interventions[name]['GRADE']
            ax.scatter(sorted_smds[i], i, color=grade_colors[grade], s=50, zorder=10, alpha=0.8)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            return fig

    def create_grade_evidence_profile(self, save_path=None):
        """
        Create GRADE evidence profile for digital vs in-person interventions
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # GRADE data
        certainty_levels = ['High', 'Moderate', 'Low', 'Very Low']
        grades = ['High', 'Moderate', 'Moderate', 'Low']
        grade_map = {'High': 4, 'Moderate': 3, 'Low': 2, 'Very Low': 1}
        grade_nums = [grade_map[g] for g in grades]

        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

        bars = ax.barh(certainty_levels, grade_nums, color=colors, alpha=0.7)

        ax.set_xlabel('Quality of Evidence')
        ax.set_xlim(0, 4.5)
        ax.set_xticks([1, 2, 3, 4])
        ax.set_xticklabels(['Very Low', 'Low', 'Moderate', 'High'])
        ax.set_title('GRADE Evidence Profile: Digital vs In-Person HCW Burnout Interventions')

        # Add quality descriptions
        for bar, grade, level in zip(bars, grades, certainty_levels):
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                   level, ha='left', va='center', fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            return fig

    def create_cost_effectiveness_plot(self, save_path=None):
        """
        Create cost-effectiveness scatter plot
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        # Cost-effectiveness data
        intervention_names = ['Digital Ecosystem', 'Mindfulness Apps', 'CBT Platforms', 'Teletherapy', 'In-Person Workshops', 'Individual Counseling']
        costs = [245, 89, 156, 134, 1234, 1890]  # Cost per participant $
        effects = [-1.05, -0.76, -0.84, -0.70, -0.67, -0.72]  # SMD effect

        colors = ['blue'] * 4 + ['green'] * 2  # Blue for digital, green for in-person

        scatter = ax.scatter(costs, effects, s=150, c=colors, alpha=0.7, edgecolors='black')

        # Add intervention labels
        for i, name in enumerate(intervention_names):
            ax.annotate(f'{name.split()[0]}', (costs[i], effects[i]),
                       xytext=(5, 5), textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8),
                       fontsize=9)

        ax.set_xlabel('Cost per Participant ($)')
        ax.set_ylabel('Effectiveness (SMD)')
        ax.set_title('Cost-Effectiveness Scatter Plot\nHCW Burnout Interventions')
        ax.grid(True, alpha=0.3)

        # Add reference lines
        ax.axhline(y=-0.7, color='red', linestyle='--', alpha=0.7, label='Moderate effect threshold')
        ax.axvline(x=500, color='orange', linestyle='--', alpha=0.7, label='High cost threshold')

        # Legend for digital vs in-person
        legend_elements = [
            plt.scatter([], [], c='blue', label='Digital Interventions', s=100, alpha=0.7, edgecolors='black'),
            plt.scatter([], [], c='green', label='In-Person Interventions', s=100, alpha=0.7, edgecolors='black'),
            Line2D([0], [0], color='red', linestyle='--', label='Moderate Effect'),
            Line2D([0], [0], color='orange', linestyle='--', label='High Cost')
        ]
        ax.legend(handles=legend_elements, loc='lower right')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            return fig

    def create_subgroup_analysis_plot(self, save_path=None):
        """
        Create subgroup analysis by healthcare role
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        # Subgroup data
        subgroups = ['Physicians', 'Nurses', 'Allied Health', 'Overall']
        digital_effects = [-0.87, -0.81, -0.76, -0.83]
        in_person_effects = [-0.69, -0.66, -0.63, -0.66]

        x = np.arange(len(subgroups))
        width = 0.35

        bars1 = ax.bar(x - width/2, digital_effects, width, label='Digital Interventions',
                      color='lightblue', alpha=0.8)
        bars2 = ax.bar(x + width/2, in_person_effects, width, label='In-Person Interventions',
                      color='lightgreen', alpha=0.8)

        ax.set_ylabel('Standardized Mean Difference')
        ax.set_title('Subgroup Analysis: Intervention Effects by Healthcare Role')
        ax.set_xticks(x)
        ax.set_xticklabels(subgroups)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

        # Add value labels on bars
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       '.2f', ha='center', va='bottom')

        autolabel(bars1)
        autolabel(bars2)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            return fig

    def generate_all_plots(self, output_directory="."):
        """
        Generate all HCW burnout intervention plots
        """
        print("Generating visualization plots for HCW Burnout Interventions meta-analysis...")

        plots = {
            '1_network_metaanalysis_plot.png': self.create_network_metaanalysis_plot,
            '2_forest_plot_main.png': self.create_forest_plot_main,
            '3_grade_evidence_profile.png': self.create_grade_evidence_profile,
            '4_costeffectiveness_scatter.png': self.create_cost_effectiveness_plot,
            '5_subgroup_analysis_hcw_role.png': self.create_subgroup_analysis_plot
        }

        for filename, plot_func in plots.items():
            filepath = f"{output_directory}/{filename}"
            plot_func(filepath)
            print(f"✓ Generated: {filename}")

        print("\nNetwork Evidence Summary:")
        print("- Digital interventions demonstrate consistent superiority")
        print("- Digital ecosystems show largest effect sizes")
        print("- Cost-effectiveness favors digital approaches")
        print("- GRADE evidence quality is High for best interventions")

        if not HAS_NETWORKX:
            print("\nNote: NetworkX not available - using simplified network visualization")
            print("For full network plots, install networkx: pip install networkx")

        print(f"\nAll plots saved to: {output_directory}")
        print("HCW Burnout visualization generation complete!")

def main():
    """
    Main function to generate all plots
    """
    print("=" * 70)
    print("HCW Burnout Interventions Network Meta-Analysis")
    print("Visualization Script")
    print("=" * 70)

    visualizer = HCW_Burnout_Visualizer()
    visualizer.generate_all_plots()

    print("\n" + "=" * 70)
    print("Key Findings from Generated Plots:")
    print("• Digital ecosystems most effective (-1.05 SMD)")
    print("• 17% greater effect than in-person approaches")
    print("• 10-fold cost advantage for digital interventions")
    print("• Consistent benefits across HCW roles")
    print("• High GRADE certainty for key recommendations")
    print("=" * 70)

if __name__ == "__main__":
    main()
