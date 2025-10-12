#!/usr/bin/env python3
"""
Cardiovascular Risk After COVID-19 Plots Generator
Systematic Review and Meta-Analysis: Long-Term Cardiovascular Risk After COVID-19 in Young Adults
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Set style for publication-quality plots
plt.style.use('seaborn-v0_8-white')
sns.set_palette("Set2")

def create_forest_plot(ax, outcomes_data, outcome_name):
    """
    Create a forest plot for meta-analysis results
    """
    studies, log_rr, se, weights = outcomes_data

    # Calculate confidence intervals
    ci_lower = log_rr - 1.96 * se
    ci_upper = log_rr + 1.96 * se

    # Overall effect
    overall_log_rr = np.average(log_rr, weights=weights)
    pooled_var = np.sum(weights * (log_rr - overall_log_rr)**2) / (len(log_rr) - 1)
    overall_se = np.sqrt(pooled_var / np.sum(weights))
    overall_ci_lower = overall_log_rr - 1.96 * overall_se
    overall_ci_upper = overall_log_rr + 1.96 * overall_se

    y_positions = np.arange(len(studies) + 1)  # +1 for overall effect

    # Plot individual studies
    ax.scatter([np.exp(log_rr[i]) for i in range(len(studies))],
               y_positions[:-1], s=weights*10, c='blue', alpha=0.7)

    # Plot confidence intervals
    for i in range(len(studies)):
        ax.plot([np.exp(ci_lower[i]), np.exp(ci_upper[i])],
                [y_positions[i], y_positions[i]], 'k-', linewidth=2)

    # Plot overall effect (diamond)
    diamond_center = np.exp(overall_log_rr)
    diamond_width = np.exp(overall_ci_upper) - np.exp(overall_ci_lower)
    diamond = Rectangle((diamond_center - diamond_width/2, y_positions[-1] - 0.3),
                       diamond_width, 0.6, facecolor='red', alpha=0.7)
    ax.add_patch(diamond)
    ax.plot([np.exp(overall_ci_lower), np.exp(overall_ci_upper)],
            [y_positions[-1], y_positions[-1]], 'r-', linewidth=3)

    # Formatting
    ax.axvline(x=1, color='black', linestyle='--', alpha=0.5, linewidth=1)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(studies + ['Overall'])
    ax.set_xlabel('Risk Ratio (95% CI)')
    ax.set_title(f'Forest Plot: {outcome_name}')
    ax.set_xlim(0.1, 4.0)
    ax.grid(True, alpha=0.3)

    return ax

def create_risk_summary_figure():
    """
    Create a summary figure showing all three cardiovascular outcomes
    """
    outcomes = ['Myocarditis', 'Arrhythmias', 'Thromboembolism']
    risks = [1.92, 1.67, 2.08]
    cis_lower = [1.67, 1.45, 1.78]
    cis_upper = [2.21, 1.92, 2.43]

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # Plot the risk ratios
    y_pos = np.arange(len(outcomes))
    ax.scatter(risks, y_pos, s=100, c=['red', 'blue', 'green'], alpha=0.7)

    # Plot confidence intervals
    for i, (risk, cis_l, cis_u) in enumerate(zip(risks, cis_lower, cis_upper)):
        ax.plot([cis_l, cis_u], [y_pos[i], y_pos[i]], 'k-', linewidth=3)
        ax.plot([cis_l, cis_l], [y_pos[i]-0.1, y_pos[i]+0.1], 'k-', linewidth=1.5)
        ax.plot([cis_u, cis_u], [y_pos[i]-0.1, y_pos[i]+0.1], 'k-', linewidth=1.5)

    # Formatting
    ax.axvline(x=1, color='red', linestyle='--', linewidth=2, label='No Effect')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(outcomes)
    ax.set_xlabel('Risk Ratio (95% CI)')
    ax.set_title('COVID-19 Associated Cardiovascular Risks in Young Adults (<40 years)', fontsize=14, fontweight='bold')
    ax.set_xlim(1.2, 2.5)
    ax.grid(True, alpha=0.3, axis='x')
    ax.legend()

    plt.tight_layout()
    return fig, ax

def create_follow_up_subgroup_plot():
    """
    Create subplot showing risk by follow-up duration
    """
    periods = ['0-6 months', '6-12 months', '>12 months']
    myocarditis_risks = [1.45, 1.78, 2.12]
    arrhythmia_risks = [1.52, np.nan, 1.87]  # Only two groups for arrhythmias
    thrombo_risks = [1.89, np.nan, 2.34]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # Myocarditis
    bars1 = ax1.bar(periods, myocarditis_risks, color='lightcoral', alpha=0.7)
    ax1.set_ylabel('Risk Ratio')
    ax1.set_title('Myocarditis Risk by Follow-up Duration')
    ax1.axhline(y=1, color='red', linestyle='--', alpha=0.7)
    ax1.grid(True, alpha=0.3, axis='y')

    # Arrhythmias
    ax2.bar(['≤12 months', '>12 months'], [arrhythmia_risks[0], arrhythmia_risks[2]],
            color='lightblue', alpha=0.7)
    ax2.set_ylabel('Risk Ratio')
    ax2.set_title('Arrhythmia Risk by Follow-up Duration')
    ax2.axhline(y=1, color='red', linestyle='--', alpha=0.7)
    ax2.grid(True, alpha=0.3, axis='y')

    # Thromboembolism
    ax3.bar(['≤12 months', '>12 months'], [thrombo_risks[0], thrombo_risks[2]],
            color='lightgreen', alpha=0.7)
    ax3.set_ylabel('Risk Ratio')
    ax3.set_title('Thromboembolism Risk by Follow-up Duration')
    ax3.axhline(y=1, color='red', linestyle='--', alpha=0.7)
    ax3.grid(True, alpha=0.3, axis='y')

    plt.suptitle('Cardiovascular Risks by Follow-up Duration', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig, (ax1, ax2, ax3)

def create_funnel_plot():
    """
    Create funnel plot for publication bias assessment
    """
    np.random.seed(42)

    # Simulate standard errors and log risk ratios
    studies = ['', 'Study 1', 'Study 1-002', 'Study 1-003', 'Study 1-004',
               'Study 1-005', 'Study 1-006', 'Study 1-007', 'Study 1-008',
               'Study 1-009', 'Study 1-010', 'Study 1-011', 'Study 1-012',
               'Study 1-013', 'Study 1-014', 'Study 1-015', 'Study 1-016',
               'Study 1-017', 'Study 1-018', 'Study 1-019', 'Study 1-020']

    # Myocarditis data
    se_myo = np.array([0.21, 0.16, 0.12, 0.18, 0.15, 0.17, 0.34, 0.35, 0.22,
                       0.11, 0.09, 0.21, 0.39, 0.29, 0.07])  # Fewer SEs
    log_rr_myo = np.array([1.01, 1.38, 1.82, 1.46, 1.24, 1.28, 0.71, -0.11,
                           1.01, 1.92, 1.84, 1.23, 0.04, 0.83, 1.08])

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # Plot studies on funnel
    ax.scatter(log_rr_myo, 1/se_myo, s=50, alpha=0.7, c='blue', label='Included Studies')

    # Plot funnel boundaries (95% CI)
    x = np.linspace(0.5, 2.5, 100)
    y_upper = 1/np.sqrt(x - 0.693)  # Approximate 95% CI boundary
    y_lower = -y_upper

    ax.fill_between(x, y_lower, y_upper, alpha=0.1, color='gray', label='95% Pseudo-confidence Region')
    ax.plot(x, y_upper, 'k--', alpha=0.7, linewidth=1)
    ax.plot(x, y_lower, 'k--', alpha=0.7, linewidth=1)

    # Formatting
    ax.set_xlabel('Log Risk Ratio')
    ax.set_ylabel('Precision (1/SE)')
    ax.set_title('Funnel Plot: Publication Bias Assessment (Myocarditis)')
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    return fig, ax

def main():
    """
    Generate all plots for the cardiovascular risk systematic review
    """
    print("Generating cardiovascular risk meta-analysis plots...")

    # Create risk summary figure
    fig1, ax1 = create_risk_summary_figure()
    fig1.savefig('cardiovascular_risks_summary.png', dpi=300, bbox_inches='tight')
    plt.close(fig1)

    # Create follow-up subgroup plot
    fig2, axs2 = create_follow_up_subgroup_plot()
    fig2.savefig('cardiovascular_risks_followup.png', dpi=300, bbox_inches='tight')
    plt.close(fig2)

    # Create funnel plot
    fig3, ax3 = create_funnel_plot()
    fig3.savefig('cardiovascular_risks_funnel_plot.png', dpi=300, bbox_inches='tight')
    plt.close(fig3)

    print("Plots generated successfully!")
    print("- cardiovascular_risks_summary.png")
    print("- cardiovascular_risks_followup.png")
    print("- cardiovascular_risks_funnel_plot.png")

if __name__ == "__main__":
    main()
