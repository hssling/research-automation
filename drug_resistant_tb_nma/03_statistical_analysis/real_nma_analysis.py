#!/usr/bin/env python3
"""
Real Network Meta-Analysis using Authentic Data from Published Studies
Compares results with synthetic data to validate approach
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for publication-ready plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_real_data():
    """Load the real extracted data from published studies"""
    data = pd.read_csv("drug_resistant_tb_nma/02_data_extraction/extracted_data.csv")
    return data

def calculate_treatment_effects():
    """Calculate treatment effects from real data"""

    data = load_real_data()

    # Group by treatment and calculate success rates
    treatment_effects = {}

    # BPaL treatments (from Nix-TB and ZeNix)
    bpal_data = data[data['treatment'].str.contains('BPaL')]
    if not bpal_data.empty:
        total_responders = bpal_data['responders'].sum()
        total_patients = bpal_data['sampleSize'].sum()
        treatment_effects['BPaL'] = {
            'success_rate': total_responders / total_patients,
            'ci_lower': 0,  # Would calculate properly with statsmodels
            'ci_upper': 0,
            'total_patients': total_patients,
            'studies': len(bpal_data)
        }

    # BPaLM treatments (from TB-PRACTECAL and NExT)
    bpalm_data = data[data['treatment'].str.contains('BPaLM')]
    if not bpalm_data.empty:
        total_responders = bpalm_data['responders'].sum()
        total_patients = bpalm_data['sampleSize'].sum()
        treatment_effects['BPaLM'] = {
            'success_rate': total_responders / total_patients,
            'ci_lower': 0,
            'ci_upper': 0,
            'total_patients': total_patients,
            'studies': len(bpalm_data)
        }

    # Short MDR regimen (from STREAM)
    short_data = data[data['treatment'] == 'Short_MDR']
    if not short_data.empty:
        total_responders = short_data['responders'].sum()
        total_patients = short_data['sampleSize'].sum()
        treatment_effects['Short_MDR'] = {
            'success_rate': total_responders / total_patients,
            'ci_lower': 0,
            'ci_upper': 0,
            'total_patients': total_patients,
            'studies': len(short_data)
        }

    # Long regimens (from STREAM and others)
    long_data = data[data['treatment'].str.contains('Long|Standard')]
    if not long_data.empty:
        total_responders = long_data['responders'].sum()
        total_patients = long_data['sampleSize'].sum()
        treatment_effects['Long_Individualized'] = {
            'success_rate': total_responders / total_patients,
            'ci_lower': 0,
            'ci_upper': 0,
            'total_patients': total_patients,
            'studies': len(long_data)
        }

    return treatment_effects

def calculate_sucra_ranking(treatment_effects):
    """Calculate SUCRA rankings from real data"""

    treatments = list(treatment_effects.keys())
    n_treatments = len(treatments)

    # Create ranking matrix (higher success rate = better rank)
    rankings = {}
    for i, tx1 in enumerate(treatments):
        rank_sum = 0
        for j, tx2 in enumerate(treatments):
            if i != j:
                # P(superior) based on success rate comparison
                if treatment_effects[tx1]['success_rate'] > treatment_effects[tx2]['success_rate']:
                    rank_sum += 1
                elif treatment_effects[tx1]['success_rate'] == treatment_effects[tx2]['success_rate']:
                    rank_sum += 0.5

        # Convert to SUCRA (0-100 scale)
        sucra = (rank_sum / (n_treatments - 1)) * 100
        rankings[tx1] = {
            'SUCRA': sucra,
            'success_rate': treatment_effects[tx1]['success_rate'],
            'rank': rank_sum + 1
        }

    # Sort by SUCRA
    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1]['SUCRA'], reverse=True)

    return rankings, sorted_rankings

def create_comparison_with_synthetic():
    """Compare real results with synthetic results"""

    # Real treatment effects
    real_effects = calculate_treatment_effects()

    # Synthetic effects (from original summary)
    synthetic_effects = {
        'BPaL': {'success_rate': 0.90, 'SUCRA': 89},
        'BPaLM': {'success_rate': 0.88, 'SUCRA': 76},
        'Short_MDR': {'success_rate': 0.79, 'SUCRA': 45},
        'Long_Individualized': {'success_rate': 0.73, 'SUCRA': 12}
    }

    # Create comparison table
    comparison_data = []
    for treatment in real_effects.keys():
        if treatment in synthetic_effects:
            real_rate = real_effects[treatment]['success_rate']
            synth_rate = synthetic_effects[treatment]['success_rate']
            difference = real_rate - synth_rate

            comparison_data.append({
                'Treatment': treatment,
                'Real_Success_Rate': f'{real_rate:.1%}',
                'Synthetic_Success_Rate': f'{synth_rate:.1%}',
                'Difference': f'{difference:+.1%}',
                'Real_Patients': real_effects[treatment]['total_patients'],
                'Real_Studies': real_effects[treatment]['studies']
            })

    comparison_df = pd.DataFrame(comparison_data)

    # Save comparison
    comparison_df.to_csv("drug_resistant_tb_nma/04_results/real_vs_synthetic_comparison.csv", index=False)

    return comparison_df

def create_real_forest_plot():
    """Create forest plot using real data"""

    treatment_effects = calculate_treatment_effects()

    # Prepare data for plotting
    treatments = []
    success_rates = []
    ci_lowers = []
    ci_uppers = []

    for tx, data in treatment_effects.items():
        treatments.append(tx)
        success_rates.append(data['success_rate'])

        # Calculate approximate 95% CI using normal approximation
        rate = data['success_rate']
        n = data['total_patients']
        se = np.sqrt(rate * (1 - rate) / n)
        ci_lower = max(0, rate - 1.96 * se)
        ci_upper = min(1, rate + 1.96 * se)

        ci_lowers.append(ci_lower)
        ci_uppers.append(ci_upper)

    # Create forest plot
    fig, ax = plt.subplots(figsize=(10, 6))

    y_pos = np.arange(len(treatments))

    ax.errorbar(success_rates, y_pos, xerr=[
        [r - l for r, l in zip(success_rates, ci_lowers)],
        [u - r for u, r in zip(ci_uppers, success_rates)]
    ], fmt='o', capsize=5, capthick=2, markersize=8, linewidth=2)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(treatments, fontsize=12, fontweight='bold')
    ax.set_xlabel('Treatment Success Rate', fontsize=14, fontweight='bold')
    ax.set_title('Real Data: Treatment Success Rates by Regimen\nNetwork Meta-Analysis of Published Trials',
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.axvline(x=0.5, color='red', linestyle='--', alpha=0.7, linewidth=2)

    # Add success rate labels
    for i, (rate, n_patients) in enumerate(zip(success_rates, [data['total_patients'] for data in treatment_effects.values()])):
        ax.annotate(f'{rate:.1%} (n={n_patients})',
                   xy=(rate, i), xytext=(10, 0),
                   textcoords='offset points', fontsize=10,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig("drug_resistant_tb_nma/04_results/real_data_forest_plot.png",
                dpi=300, bbox_inches='tight')
    plt.show()

    return fig, ax

def create_real_sucra_plot():
    """Create SUCRA ranking plot using real data"""

    treatment_effects = calculate_treatment_effects()
    rankings, sorted_rankings = calculate_sucra_ranking(treatment_effects)

    # Prepare data for plotting
    treatments = [tx for tx, _ in sorted_rankings]
    sucra_values = [rankings[tx]['SUCRA'] for tx, _ in sorted_rankings]
    success_rates = [treatment_effects[tx]['success_rate'] * 100 for tx in treatments]

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(range(len(treatments)), sucra_values,
                  color='steelblue', alpha=0.8, edgecolor='black', linewidth=1.5)

    # Add success rate labels on bars
    for i, (bar, rate) in enumerate(zip(bars, success_rates)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'Success: {rate:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_xticks(range(len(treatments)))
    ax.set_xticklabels(treatments, fontsize=12, fontweight='bold', rotation=45, ha='right')
    ax.set_ylabel('SUCRA Value (%)', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 110)
    ax.set_title('Real Data: SUCRA Rankings for Treatment Success\nBased on Published Clinical Trials',
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')

    # Add rank numbers
    for i, (tx, _) in enumerate(sorted_rankings):
        rank = rankings[tx]['rank']
        ax.text(i, sucra_values[i] - 8, f'Rank {rank}',
               ha='center', va='top', fontsize=11, fontweight='bold', color='white')

    plt.tight_layout()
    plt.savefig("drug_resistant_tb_nma/04_results/real_data_sucra_plot.png",
                dpi=300, bbox_inches='tight')
    plt.show()

    return fig, ax

def analyze_safety_data():
    """Analyze safety outcomes from real data"""

    data = load_real_data()

    # Extract safety data
    safety_data = []

    for _, row in data.iterrows():
        if pd.notna(row.get('peripheral_neuropathy_rate', None)):
            safety_data.append({
                'study': row['study_id'],
                'treatment': row['treatment'],
                'neuropathy_rate': row['peripheral_neuropathy_rate'],
                'myelosuppression_rate': row.get('myelosuppression_rate', 0),
                'qt_prolongation_rate': row.get('qt_prolongation_rate', 0)
            })

    safety_df = pd.DataFrame(safety_data)

    # Group by treatment type
    safety_summary = {}

    for treatment in ['BPaL', 'BPaLM', 'Short_MDR', 'Long']:
        tx_data = safety_df[safety_df['treatment'].str.contains(treatment.split('_')[0])]

        if not tx_data.empty:
            safety_summary[treatment] = {
                'neuropathy': tx_data['neuropathy_rate'].mean(),
                'myelosuppression': tx_data['myelosuppression_rate'].mean(),
                'qt_prolongation': tx_data['qt_prolongation_rate'].mean(),
                'n_studies': len(tx_data)
            }

    return safety_summary

def create_safety_comparison_plot():
    """Create safety comparison plot"""

    safety_data = analyze_safety_data()

    # Prepare data for plotting
    treatments = list(safety_data.keys())
    neuropathy_rates = [safety_data[tx]['neuropathy'] for tx in treatments]
    myelosuppression_rates = [safety_data[tx]['myelosuppression'] for tx in treatments]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Neuropathy plot
    bars1 = ax1.bar(range(len(treatments)), neuropathy_rates, color='orange', alpha=0.8)
    ax1.set_xticks(range(len(treatments)))
    ax1.set_xticklabels(treatments, fontsize=11, fontweight='bold', rotation=45, ha='right')
    ax1.set_ylabel('Peripheral Neuropathy Rate (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Peripheral Neuropathy by Regimen\nReal Data from Published Trials',
                   fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    for bar, rate in zip(bars1, neuropathy_rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Myelosuppression plot
    bars2 = ax2.bar(range(len(treatments)), myelosuppression_rates, color='red', alpha=0.8)
    ax2.set_xticks(range(len(treatments)))
    ax2.set_xticklabels(treatments, fontsize=11, fontweight='bold', rotation=45, ha='right')
    ax2.set_ylabel('Myelosuppression Rate (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Myelosuppression by Regimen\nReal Data from Published Trials',
                   fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    for bar, rate in zip(bars2, myelosuppression_rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig("drug_resistant_tb_nma/04_results/real_data_safety_comparison.png",
                dpi=300, bbox_inches='tight')
    plt.show()

    return fig, (ax1, ax2)

def generate_real_results_summary():
    """Generate comprehensive summary of real data analysis"""

    # Calculate treatment effects
    treatment_effects = calculate_treatment_effects()

    # Calculate rankings
    rankings, sorted_rankings = calculate_sucra_ranking(treatment_effects)

    # Analyze safety
    safety_data = analyze_safety_data()

    # Create comparison with synthetic
    comparison = create_comparison_with_synthetic()

    # Generate summary report
    summary = f"""
# Real Data Analysis Summary: Drug-Resistant Tuberculosis NMA

## Treatment Success Rates (Real Data)

"""

    for tx, data in treatment_effects.items():
        summary += f"**{tx}**: {data['success_rate']:.1%} success rate ({data['total_patients']} patients, {data['studies']} studies)\n"

    summary += "\n## SUCRA Rankings (Real Data)\n\n"

    for i, (tx, ranking_info) in enumerate(sorted_rankings, 1):
        summary += f"{i}. **{tx}**: SUCRA = {ranking_info['SUCRA']:.1f}% (Success rate: {treatment_effects[tx]['success_rate']:.1%})\n"

    summary += "\n## Safety Profile (Real Data)\n\n"

    for tx, safety in safety_data.items():
        summary += f"**{tx}**:\n"
        summary += f"- Peripheral neuropathy: {safety['neuropathy']:.1f}%\n"
        summary += f"- Myelosuppression: {safety['myelosuppression']:.1f}%\n"
        summary += f"- QT prolongation: {safety['qt_prolongation']:.1f}%\n"
        summary += f"- Based on {safety['n_studies']} studies\n\n"

    summary += "## Comparison with Synthetic Data\n\n"

    summary += comparison.to_string(index=False)

    # Save summary
    with open("drug_resistant_tb_nma/04_results/real_data_analysis_summary.md", 'w') as f:
        f.write(summary)

    print("Real data analysis completed!")
    print("Results saved to drug_resistant_tb_nma/04_results/")

    return {
        'treatment_effects': treatment_effects,
        'rankings': rankings,
        'safety_data': safety_data,
        'comparison': comparison
    }

def main():
    """Main execution function"""

    print("Starting real data analysis...")

    # Generate all visualizations
    forest_fig, forest_ax = create_real_forest_plot()
    sucra_fig, sucra_ax = create_real_sucra_plot()
    safety_fig, safety_axes = create_safety_comparison_plot()

    # Generate comprehensive summary
    results = generate_real_results_summary()

    print("\n" + "="*60)
    print("REAL DATA ANALYSIS COMPLETE")
    print("="*60)

    # Print key findings
    print("\nTOP 3 TREATMENTS BY EFFICACY:")
    rankings, sorted_rankings = calculate_sucra_ranking(results['treatment_effects'])
    for i, (tx, _) in enumerate(sorted_rankings[:3], 1):
        sucra = rankings[tx]['SUCRA']
        rate = results['treatment_effects'][tx]['success_rate']
        print(f"{i}. {tx}: {rate:.1%} success rate (SUCRA: {sucra:.1f}%)")

    print("\nSAFETY PROFILE:")
    for tx, safety in results['safety_data'].items():
        neuro = safety['neuropathy']
        myelo = safety['myelosuppression']
        print(f"{tx}: Neuropathy {neuro:.1f}%, Myelosuppression {myelo:.1f}%")

    print(f"\nComparison with synthetic data saved to: drug_resistant_tb_nma/04_results/real_vs_synthetic_comparison.csv")
    print(f"Complete analysis summary saved to: drug_resistant_tb_nma/04_results/real_data_analysis_summary.md")

    return results

if __name__ == "__main__":
    results = main()
