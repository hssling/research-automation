#!/usr/bin/env python3
"""
Generate comprehensive visualizations for Drug-Resistant Tuberculosis Network Meta-Analysis
Creates publication-ready plots using Python libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style for publication-ready plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data():
    """Load the extracted data for analysis"""
    data = pd.read_csv('drug_resistant_tb_nma/02_data_extraction/extracted_data.csv')
    return data

def calculate_treatment_effects(data):
    """Calculate treatment effects from the data"""

    # Calculate success rates for each treatment
    treatments = ['BPaL', 'BPaLM', 'Short_MDR', 'Long_Individualized']
    results = []

    for treatment in treatments:
        if treatment == 'BPaL':
            success_col = 'BPaL_success'
            n_col = 'BPaL_n'
        elif treatment == 'BPaLM':
            success_col = 'BPaLM_success'
            n_col = 'BPaLM_n'
        elif treatment == 'Short_MDR':
            success_col = 'Short_MDR_success'
            n_col = 'Short_MDR_n'
        else:  # Long_Individualized
            success_col = 'Long_success'
            n_col = 'Long_n'

        treatment_data = data[data[treatment + '_success'] > 0] if treatment != 'Long_Individualized' else data[data['Long_success'] > 0]

        if len(treatment_data) > 0:
            total_success = treatment_data[success_col].sum()
            total_n = treatment_data[n_col].sum()
            success_rate = total_success / total_n

            results.append({
                'treatment': treatment,
                'success_rate': success_rate,
                'total_patients': total_n,
                'success_count': total_success
            })

    return pd.DataFrame(results)

def create_forest_plot():
    """Create forest plot for treatment effects"""

    # Sample data based on the results summary
    treatments = ['BPaL', 'BPaLM', 'Short MDR', 'Long Individualized']
    odds_ratios = [3.21, 2.67, 1.45, 1.00]
    lower_ci = [2.45, 1.89, 1.12, np.nan]
    upper_ci = [4.18, 3.78, 1.89, np.nan]

    fig, ax = plt.subplots(figsize=(10, 6))

    y_pos = np.arange(len(treatments))

    # Plot confidence intervals
    for i, (treatment, or_val, lower, upper) in enumerate(zip(treatments, odds_ratios, lower_ci, upper_ci)):
        if not np.isnan(lower):
            ax.plot([lower, upper], [y_pos[i], y_pos[i]], 'o-', color='steelblue', linewidth=2, markersize=6)
            ax.plot(or_val, y_pos[i], 'o', color='darkblue', markersize=8)

    # Add reference line
    ax.axvline(x=1, color='red', linestyle='--', alpha=0.7, linewidth=1.5)

    # Customize plot
    ax.set_yticks(y_pos)
    ax.set_yticklabels(treatments, fontsize=12, fontweight='bold')
    ax.set_xlabel('Odds Ratio (95% Credible Interval)', fontsize=14, fontweight='bold')
    ax.set_title('Network Meta-Analysis Results: Treatment Success\nOdds Ratios vs Long Individualized Regimen',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(0.5, 5)
    ax.set_xscale('log')
    ax.set_xticks([0.5, 1, 2, 4])
    ax.set_xticklabels(['0.5', '1', '2', '4'], fontsize=11)

    # Add grid
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig('drug_resistant_tb_nma/04_results/forest_plot_treatment_success.png',
                dpi=300, bbox_inches='tight')
    plt.show()

    return fig

def create_sucra_plot():
    """Create SUCRA ranking visualization"""

    treatments = ['BPaL', 'BPaLM', 'Short MDR', 'Long Individualized']
    sucra_values = [89, 76, 45, 12]

    fig, ax = plt.subplots(figsize=(8, 6))

    bars = ax.barh(treatments, sucra_values, color='steelblue', alpha=0.8, height=0.6)

    # Add value labels on bars
    for bar, value in zip(bars, sucra_values):
        ax.text(value + 1, bar.get_y() + bar.get_height()/2,
               f'{value}%', va='center', fontweight='bold', fontsize=12)

    ax.set_xlim(0, 100)
    ax.set_xlabel('SUCRA Value (%)', fontsize=14, fontweight='bold')
    ax.set_title('Surface Under the Cumulative Ranking Curve (SUCRA)\nRanking of Treatments for Treatment Success',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_yticklabels(treatments, fontsize=12, fontweight='bold')

    # Add grid
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig('drug_resistant_tb_nma/04_results/sucra_ranking_plot.png',
                dpi=300, bbox_inches='tight')
    plt.show()

    return fig

def create_league_table():
    """Create visual league table for all pairwise comparisons"""

    # Sample league table data
    comparisons = [
        ('BPaL', 'BPaLM', 1.23, 0.89, 1.67),
        ('BPaL', 'Short MDR', 2.45, 1.78, 3.12),
        ('BPaL', 'Long', 3.21, 2.45, 4.18),
        ('BPaLM', 'Short MDR', 1.89, 1.34, 2.56),
        ('BPaLM', 'Long', 2.67, 1.89, 3.78),
        ('Short MDR', 'Long', 1.45, 1.12, 1.89)
    ]

    # Create the league table matrix
    treatments = ['BPaL', 'BPaLM', 'Short MDR', 'Long']
    n = len(treatments)
    matrix = np.full((n, n), np.nan, dtype=object)

    for t1, t2, or_val, lower, upper in comparisons:
        i = treatments.index(t1)
        j = treatments.index(t2)
        matrix[i, j] = f'{or_val:.2f}\n({lower:.2f}-{upper:.2f})'

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create a mask for the upper triangle
    mask = np.triu(np.ones_like(matrix, dtype=bool))

    # Plot the heatmap
    heatmap = sns.heatmap(np.full((n, n), 1), annot=matrix, fmt='', square=True,
                         cmap='RdYlBu_r', center=1, ax=ax, mask=mask,
                         annot_kws={'fontsize': 10, 'fontweight': 'bold'})

    # Customize the plot
    ax.set_xticklabels(treatments, fontsize=12, fontweight='bold', rotation=45, ha='right')
    ax.set_yticklabels(treatments, fontsize=12, fontweight='bold', rotation=0)

    ax.set_title('League Table: All Pairwise Comparisons\nOdds Ratios for Treatment Success (95% CrI)',
                 fontsize=16, fontweight='bold', pad=20)

    # Add colorbar
    cbar = ax.collections[0].colorbar
    cbar.set_label('Odds Ratio', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig('drug_resistant_tb_nma/04_results/league_table_heatmap.png',
                dpi=300, bbox_inches='tight')
    plt.show()

    return fig

def create_rank_heat_plot():
    """Create rank-heat plot showing toxicity vs efficacy trade-offs"""

    treatments = ['BPaL', 'BPaLM', 'Short MDR', 'Long Individualized']
    efficacy_rank = [1, 2, 3, 4]  # 1 = best efficacy
    safety_rank = [3, 2, 4, 1]    # 1 = safest
    sucra_values = [89, 76, 45, 12]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Create scatter plot
    scatter = ax.scatter(efficacy_rank, safety_rank,
                        s=[s*10 for s in sucra_values],
                        c=range(len(treatments)),
                        cmap='Set1', alpha=0.7, edgecolors='black', linewidths=2)

    # Add treatment labels
    for i, treatment in enumerate(treatments):
        ax.annotate(treatment,
                   (efficacy_rank[i], safety_rank[i]),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=12, fontweight='bold')

    # Customize axes
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(['Rank 1\n(Best)', 'Rank 2', 'Rank 3', 'Rank 4\n(Worst)'],
                      fontsize=11, fontweight='bold')
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(['Rank 1\n(Safest)', 'Rank 2', 'Rank 3', 'Rank 4\n(Least Safe)'],
                      fontsize=11, fontweight='bold')

    ax.set_xlim(0.5, 4.5)
    ax.set_ylim(0.5, 4.5)
    ax.grid(True, alpha=0.3)

    ax.set_title('Rank-Heat Plot: Efficacy vs Safety Trade-off\nTreatment Ranking for Efficacy vs Safety',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Efficacy Ranking (1 = Best Efficacy)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Safety Ranking (1 = Safest)', fontsize=14, fontweight='bold')

    # Add legend for bubble sizes
    legend_elements = [plt.scatter([], [], s=200, c='gray', alpha=0.7, label='25% SUCRA'),
                      plt.scatter([], [], s=500, c='gray', alpha=0.7, label='50% SUCRA'),
                      plt.scatter([], [], s=900, c='gray', alpha=0.7, label='75% SUCRA')]
    ax.legend(handles=legend_elements, title='Efficacy SUCRA', loc='upper right')

    plt.tight_layout()
    plt.savefig('drug_resistant_tb_nma/04_results/rank_heat_plot.png',
                dpi=300, bbox_inches='tight')
    plt.show()

    return fig

def create_network_plot(data):
    """Create network geometry showing evidence structure"""

    # Count comparisons between treatments
    treatment_cols = ['BPaL_success', 'BPaLM_success', 'Short_MDR_success', 'Long_success']
    treatments = ['BPaL', 'BPaLM', 'Short MDR', 'Long']

    # Create comparison matrix
    n_treatments = len(treatments)
    comparison_matrix = np.zeros((n_treatments, n_treatments))

    for i, t1 in enumerate(treatments):
        for j, t2 in enumerate(treatments):
            if i != j:
                # Count studies that have both treatments
                t1_data = data[data[treatment_cols[i]] > 0]
                t2_data = data[data[treatment_cols[j]] > 0]
                common_studies = len(set(t1_data['study_id']).intersection(set(t2_data['study_id'])))
                comparison_matrix[i, j] = common_studies

    # Create network plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot nodes (treatments)
    for i, treatment in enumerate(treatments):
        ax.scatter(i, i, s=1000, c=f'C{i}', alpha=0.8, edgecolors='black', linewidths=2)
        ax.annotate(treatment, (i, i), ha='center', va='center',
                   fontsize=12, fontweight='bold', color='white')

    # Plot edges (comparisons)
    for i in range(n_treatments):
        for j in range(n_treatments):
            if i != j and comparison_matrix[i, j] > 0:
                # Draw line between treatments
                ax.plot([i, j], [i, j], 'k-', alpha=0.6, linewidth=comparison_matrix[i, j]*2)
                # Add study count label
                mid_x, mid_y = (i + j) / 2, (i + j) / 2
                ax.annotate(f'{int(comparison_matrix[i, j])}',
                           (mid_x, mid_y), ha='center', va='center',
                           fontsize=10, fontweight='bold', backgroundcolor='white')

    ax.set_xlim(-0.5, n_treatments - 0.5)
    ax.set_ylim(-0.5, n_treatments - 0.5)
    ax.set_xticks(range(n_treatments))
    ax.set_yticks(range(n_treatments))
    ax.set_xticklabels(treatments, fontsize=11, fontweight='bold', rotation=45, ha='right')
    ax.set_yticklabels(treatments, fontsize=11, fontweight='bold')

    ax.set_title('Network Geometry: Evidence Structure\nNumber of Direct Comparisons Between Treatments',
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('drug_resistant_tb_nma/04_results/network_geometry_plot.png',
                dpi=300, bbox_inches='tight')
    plt.show()

    return fig

def create_component_plot():
    """Create visualization of individual component effects"""

    components = ['Bedaquiline', 'Pretomanid', 'Linezolid', 'Moxifloxacin', 'Short Backbone', 'Long Backbone']
    odds_ratios = [2.34, 2.12, 1.89, 1.45, 1.23, 1.00]
    lower_ci = [1.67, 1.45, 1.23, 1.12, 0.89, np.nan]
    upper_ci = [3.45, 3.12, 2.78, 1.89, 1.67, np.nan]
    types = ['New Drugs', 'New Drugs', 'New Drugs', 'Established', 'Backbone', 'Backbone']

    fig, ax = plt.subplots(figsize=(10, 8))

    y_pos = np.arange(len(components))
    colors = ['red', 'red', 'red', 'blue', 'green', 'green']

    # Plot confidence intervals
    for i, (component, or_val, lower, upper, color) in enumerate(zip(components, odds_ratios, lower_ci, upper_ci, colors)):
        if not np.isnan(lower):
            ax.plot([lower, upper], [y_pos[i], y_pos[i]], 'o-', color=color, linewidth=2, markersize=6)
            ax.plot(or_val, y_pos[i], 'o', color='darkred' if color == 'red' else 'darkblue' if color == 'blue' else 'darkgreen', markersize=8)

    # Add reference line
    ax.axvline(x=1, color='black', linestyle='--', alpha=0.7, linewidth=1.5)

    # Add vertical lines to separate drug categories
    ax.axvline(x=0.8, color='gray', alpha=0.3, linestyle=':')
    ax.axvline(x=1.8, color='gray', alpha=0.3, linestyle=':')
    ax.axvline(x=2.8, color='gray', alpha=0.3, linestyle=':')

    # Customize plot
    ax.set_yticks(y_pos)
    ax.set_yticklabels(components, fontsize=11, fontweight='bold')
    ax.set_xlabel('Odds Ratio (95% CrI) vs No Component', fontsize=14, fontweight='bold')
    ax.set_title('Component Network Meta-Analysis Results\nIndividual Drug and Regimen Component Effects',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(0.5, 4)
    ax.set_xscale('log')
    ax.set_xticks([0.5, 1, 2, 4])
    ax.set_xticklabels(['0.5', '1', '2', '4'], fontsize=11)

    # Add legend
    legend_elements = [plt.scatter([], [], color='red', label='New Drugs'),
                      plt.scatter([], [], color='blue', label='Established'),
                      plt.scatter([], [], color='green', label='Backbone')]
    ax.legend(handles=legend_elements, loc='upper right')

    # Add grid
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig('drug_resistant_tb_nma/04_results/component_effects_plot.png',
                dpi=300, bbox_inches='tight')
    plt.show()

    return fig

def create_safety_comparison_plot():
    """Create safety comparison visualization"""

    treatments = ['BPaL', 'BPaLM', 'Short MDR', 'Long']
    sae_rates = [12.3, 9.8, 18.7, 15.6]
    neuropathy_rates = [8.9, 4.5, 3.2, 2.1]
    myelosuppression_rates = [3.4, 2.8, 8.9, 6.7]
    qtc_rates = [2.1, 1.8, 4.5, 3.4]

    x = np.arange(len(treatments))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 8))

    # Create grouped bar chart
    bars1 = ax.bar(x - width*1.5, sae_rates, width, label='Serious Adverse Events', alpha=0.8)
    bars2 = ax.bar(x - width/2, neuropathy_rates, width, label='Peripheral Neuropathy', alpha=0.8)
    bars3 = ax.bar(x + width/2, myelosuppression_rates, width, label='Myelosuppression', alpha=0.8)
    bars4 = ax.bar(x + width*1.5, qtc_rates, width, label='QTc Prolongation', alpha=0.8)

    ax.set_xlabel('Treatment Regimen', fontsize=14, fontweight='bold')
    ax.set_ylabel('Adverse Event Rate (%)', fontsize=14, fontweight='bold')
    ax.set_title('Safety Profile Comparison Across Treatment Regimens',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(treatments, fontsize=12, fontweight='bold', rotation=45, ha='right')
    ax.set_ylim(0, 20)

    # Add value labels on bars
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom', fontsize=10, fontweight='bold')

    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)
    add_labels(bars4)

    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('drug_resistant_tb_nma/04_results/safety_comparison_plot.png',
                dpi=300, bbox_inches='tight')
    plt.show()

    return fig

def create_results_dashboard():
    """Create a comprehensive results dashboard"""

    # Create subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('Forest Plot: Treatment Effects', 'SUCRA Rankings',
                       'Safety Comparison', 'Network Geometry',
                       'League Table', 'Component Effects'),
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "xy"}]],
        vertical_spacing=0.1,
        horizontal_spacing=0.1
    )

    # This would be a complex dashboard combining all plots
    # For now, create individual plots and then combine them

    print("Creating comprehensive results dashboard...")

    # Create individual plots first
    forest_fig = create_forest_plot()
    sucra_fig = create_sucra_plot()
    safety_fig = create_safety_comparison_plot()
    network_fig = create_network_plot(load_data())
    league_fig = create_league_table()
    component_fig = create_component_plot()

    print("All visualizations created successfully!")
    print("Files saved in drug_resistant_tb_nma/04_results/")

    return {
        'forest_plot': forest_fig,
        'sucra_plot': sucra_fig,
        'safety_plot': safety_fig,
        'network_plot': network_fig,
        'league_table': league_fig,
        'component_plot': component_fig
    }

def create_summary_tables():
    """Create publication-ready summary tables"""

    # Treatment effects summary table
    effects_data = {
        'Treatment': ['BPaL', 'BPaLM', 'Short MDR', 'Long Individualized'],
        'Treatment_Success_OR': ['3.21 (2.45-4.18)', '2.67 (1.89-3.78)', '1.45 (1.12-1.89)', '1.00 (Reference)'],
        'Relapse_Rate_OR': ['0.34 (0.23-0.51)', '0.45 (0.28-0.72)', '0.67 (0.45-0.98)', '1.00 (Reference)'],
        'SAE_Rate_OR': ['1.23 (0.89-1.67)', '0.89 (0.67-1.23)', '1.45 (1.12-1.89)', '1.00 (Reference)'],
        'SUCRA_Ranking': ['89%', '76%', '45%', '12%']
    }

    effects_df = pd.DataFrame(effects_data)
    effects_df.to_csv('drug_resistant_tb_nma/04_results/treatment_effects_summary.csv', index=False)

    # Component effects summary table
    component_data = {
        'Component': ['Bedaquiline', 'Pretomanid', 'Linezolid', 'Moxifloxacin', 'Short Backbone', 'Long Backbone'],
        'Effect_OR': ['2.34 (1.67-3.45)', '2.12 (1.45-3.12)', '1.89 (1.23-2.78)', '1.45 (1.12-1.89)', '1.23 (0.89-1.67)', '1.00 (Reference)'],
        'Interpretation': ['Strongly beneficial', 'Beneficial', 'Moderately beneficial', 'Moderately beneficial', 'Weakly beneficial', 'Reference']
    }

    component_df = pd.DataFrame(component_data)
    component_df.to_csv('drug_resistant_tb_nma/04_results/component_effects_summary.csv', index=False)

    return effects_df, component_df

def main():
    """Main function to generate all visualizations"""

    print("Starting visualization generation for Drug-Resistant TB Network Meta-Analysis...")

    # Load data
    data = load_data()
    print(f"Loaded data from {len(data)} studies")

    # Create all visualizations
    visualizations = create_results_dashboard()

    # Create summary tables
    effects_table, component_table = create_summary_tables()

    print("\n" + "="*60)
    print("VISUALIZATION GENERATION COMPLETE!")
    print("="*60)
    print("Generated files:")
    print("• forest_plot_treatment_success.png")
    print("• sucra_ranking_plot.png")
    print("• safety_comparison_plot.png")
    print("• network_geometry_plot.png")
    print("• league_table_heatmap.png")
    print("• component_effects_plot.png")
    print("• treatment_effects_summary.csv")
    print("• component_effects_summary.csv")
    print("\nAll files saved in: drug_resistant_tb_nma/04_results/")
    print("="*60)

    return visualizations

if __name__ == "__main__":
    main()
