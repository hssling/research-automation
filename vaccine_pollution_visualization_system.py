#!/usr/bin/env python3
"""
Vaccine Effectiveness in Polluted Urban Environments - Visualization System

This script generates publication-quality visualizations for the vaccine-pollution
ecological study, including:
- Dose-response curves for PM₂.₅ and vaccine effectiveness
- Regional pollution-vaccine maps
- Cost-benefit analysis charts
- Temporal trends and seasonal patterns
- Vaccine-specific effectiveness comparisons
- PAF (Population Attributable Fraction) visualizations

Author: Environmental Health Research Institute
Date: March 2025
Version: 1.0
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import pandas as pd
import numpy as np
import warnings

plt.style.use('seaborn-v0_8-white')
warnings.filterwarnings('ignore')

# Simulated study data
vaccine_data = {
    'pm25_levels': [15, 25, 35, 45, 55, 65, 75, 85],
    'measles_effectiveness': [95.2, 93.8, 87.4, 82.1, 76.3, 71.8, 66.9, 62.1],
    'dtp_effectiveness': [96.1, 95.2, 94.3, 92.1, 89.7, 88.3, 85.9, 83.1],
    'oral_polio_effectiveness': [94.7, 92.8, 86.2, 79.4, 73.6, 68.9, 63.1, 58.3],
    'hepatitis_effectiveness': [95.8, 95.1, 94.3, 93.2, 92.1, 91.4, 89.7, 88.3]
}

regional_data = {
    'Region': ['South Asia', 'East Asia', 'Southeast Asia', 'Middle East', 'Sub-Saharan Africa', 'Latin America', 'East Europe', 'West Europe'],
    'Mean_PM25': [62.1, 58.7, 32.4, 54.8, 28.3, 35.2, 29.1, 21.8],
    'Vaccine_Effect': [76.2, 81.3, 89.7, 82.6, 91.4, 88.8, 90.5, 93.1],
    'PAF_Percent': [34.2, 27.6, 18.1, 25.3, 12.1, 14.8, 11.6, 8.2]
}

temporal_data = {
    'Year': [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024],
    'PM25_Trend': [48.6, 52.1, 55.8, 59.7, 62.3, 68.9, 72.4, 76.8],
    'Vaccine_Effect': [91.2, 89.7, 87.8, 85.4, 83.1, 79.2, 76.8, 74.3],
    'Disease_Cases': [1.8, 2.1, 2.4, 2.8, 3.2, 3.9, 4.2, 4.6]
}

def create_dose_response_curves():
    """Create vaccine-specific dose-response curves showing PM₂.₅ effects."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12), dpi=300)

    df = pd.DataFrame(vaccine_data)
    x_smooth = np.linspace(15, 85, 100)

    # Measles Vaccine
    slope_mmr = np.polyfit(df['pm25_levels'], df['measles_effectiveness'], 2)
    y_smooth_mmr = np.polyval(slope_mmr, x_smooth)
    ax1.scatter(df['pm25_levels'], df['measles_effectiveness'], s=120, color='#e74c3c',
               edgecolor='black', linewidth=2, alpha=0.8)
    ax1.plot(x_smooth, y_smooth_mmr, '--', color='#e74c3c', linewidth=3, alpha=0.7)
    ax1.set_title('Measles Vaccine: PM₂.₅ Dose-Response\n(Live Attenuated)', fontweight='bold')
    ax1.set_ylabel('Vaccine Effectiveness (%)', fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # DTP Vaccine
    slope_dtp = np.polyfit(df['pm25_levels'], df['dtp_effectiveness'], 1)
    y_smooth_dtp = np.polyval(slope_dtp, x_smooth)
    ax2.scatter(df['pm25_levels'], df['dtp_effectiveness'], s=120, color='#27ae60',
               edgecolor='black', linewidth=2, alpha=0.8)
    ax2.plot(x_smooth, y_smooth_dtp, '--', color='#27ae60', linewidth=3, alpha=0.7)
    ax2.set_title('DTP Vaccine: PM₂.₅ Dose-Response\n(Inactivated Toxoids)', fontweight='bold')
    ax2.grid(True, alpha=0.3)

    # Oral Polio Vaccine
    slope_opv = np.polyfit(df['pm25_levels'], df['oral_polio_effectiveness'], 2)
    y_smooth_opv = np.polyval(slope_opv, x_smooth)
    ax3.scatter(df['pm25_levels'], df['oral_polio_effectiveness'], s=120, color='#f39c12',
               edgecolor='black', linewidth=2, alpha=0.8)
    ax3.plot(x_smooth, y_smooth_opv, '--', color='#f39c12', linewidth=3, alpha=0.7)
    ax3.set_title('Oral Polio Vaccine: PM₂.₅ Dose-Response\n(Live Attenuated)', fontweight='bold')
    ax3.set_xlabel('PM₂.₅ Concentration (µg/m³)', fontweight='bold')
    ax3.set_ylabel('Vaccine Effectiveness (%)', fontweight='bold')
    ax3.grid(True, alpha=0.3)

    # Hepatitis B Vaccine
    slope_hepb = np.polyfit(df['pm25_levels'], 100 - df['hepatitis_effectiveness'], 1)
    ax4.scatter(df['pm25_levels'], df['hepatitis_effectiveness'], s=120, color='#3498db',
               edgecolor='black', linewidth=2, alpha=0.8)
    ax4.axhline(y=95, color='gray', linestyle='--', alpha=0.5, label='Estimated Baseline')
    ax4.set_title('Hepatitis B Vaccine: PM₂.₅ Dose-Response\n(Recombinant)', fontweight='bold')
    ax4.set_xlabel('PM₂.₅ Concentration (µg/m³)', fontweight='bold')
    ax4.grid(True, alpha=0.3)

    # Add threshold line
    for ax in [ax1, ax3]:
        ax.axvline(x=35, color='red', linestyle='--', alpha=0.7, linewidth=2, label='35 µg/m³ Threshold')

    plt.tight_layout()
    plt.savefig('./results/vaccine_pollution_dose_response.png', dpi=300, bbox_inches='tight',
                pad_inches=0.2, facecolor='white')
    plt.close()

    print("✅ Vaccine dose-response curves saved to ./results/vaccine_pollution_dose_response.png")

def create_regional_effectiveness_map():
    """Create heatmap showing regional vaccine effectiveness patterns."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=300)

    df_regional = pd.DataFrame(regional_data)

    # Effectiveness Heatmap
    effectiveness_matrix = df_regional['Vaccine_Effect'].values.reshape(-1, 1)
    regions_formatted = [region.replace(' ', '\n') for region in df_regional['Region']]

    sns.heatmap(effectiveness_matrix, annot=[[f'{val:.1f}%'] for val in df_regional['Vaccine_Effect']],
               xticklabels=['Overall\nEffectiveness'], yticklabels=regions_formatted,
               cmap='RdYlGn', ax=ax1, cbar_kws={'label': 'Vaccine Effectiveness (%)'})
    ax1.set_title('Regional Vaccine Effectiveness in Polluted Environments\n(by PM₂.₅ burden)',
                 fontweight='bold')

    # PAF Heatmap
    paf_matrix = df_regional['PAF_Percent'].values.reshape(-1, 1)
    sns.heatmap(paf_matrix, annot=[[f'{val:.1f}%'] for val in df_regional['PAF_Percent']],
               xticklabels=['Population Attributable\nFraction'], yticklabels=regions_formatted,
               cmap='Reds', ax=ax2, cbar_kws={'label': 'PAF (%)'})
    ax2.set_title('Disease Burden Attributable to Pollution\n(Population Attributable Fraction)', fontweight='bold')

    # Add PM₂.₅ levels as annotations
    for i, (region, pm25) in enumerate(zip(df_regional['Region'], df_regional['Mean_PM25'])):
        ax1.text(0.5, i-0.3, f'Mean PM₂.₅: {pm25:.1f} µg/m³',
                ha='center', va='center', fontsize=8, color='black', weight='bold')
        ax2.text(0.5, i-0.3, f'Mean PM₂.₅: {pm25:.1f} µg/m³',
                ha='center', va='center', fontsize=8, color='black', weight='bold')

    plt.tight_layout()
    plt.savefig('./results/vaccine_pollution_regional_patterns.png', dpi=300, bbox_inches='tight',
                pad_inches=0.2, facecolor='white')
    plt.close()

    print("✅ Regional vaccine effectiveness map saved to ./results/vaccine_pollution_regional_patterns.png")

def create_temporal_trends_analysis():
    """Create temporal trends showing evolving pollution-vaccine relationships."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6), dpi=300)

    df_temporal = pd.DataFrame(temporal_data)

    # PM₂.₅ and Vaccine Effectiveness Trends
    ax1.plot(df_temporal['Year'], df_temporal['PM25_Trend'], marker='o', linewidth=3,
            markerfacecolor='red', markersize=8, color='#e74c3c', label='PM₂.₅ Concentration')
    ax1.set_ylabel('PM₂.₅ Concentration (µg/m³)', color='#e74c3c', fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='#e74c3c')

    ax1_twin = ax1.twinx()
    ax1_twin.plot(df_temporal['Year'], df_temporal['Vaccine_Effect'], marker='s', linewidth=3,
                markerfacecolor='blue', markersize=8, color='#3498db', label='Vaccine Effectiveness')
    ax1_twin.set_ylabel('Vaccine Effectiveness (%)', color='#3498db', fontsize=12, fontweight='bold')
    ax1_twin.tick_params(axis='y', labelcolor='#3498db')
    ax1.set_title('PM₂.₅ Pollution and Vaccine Effectiveness Trends\n(2010-2024)', fontweight='bold')

    # Fill area between lines for correlation visualization
    pm25_norm = (df_temporal['PM25_Trend'] - df_temporal['PM25_Trend'].min()) / (df_temporal['PM25_Trend'].max() - df_temporal['PM25_Trend'].min())
    vaccine_norm = (100 - df_temporal['Vaccine_Effect']) / (100 - df_temporal['Vaccine_Effect']).min()
    ax1.fill_between(df_temporal['Year'], pm25_norm * 20 + 45, vaccine_norm * 20 + 90,
                    alpha=0.1, color='#e74c3c')

    # Disease Cases vs Pollution
    ax2.scatter(df_temporal['PM25_Trend'], df_temporal['Disease_Cases'], s=100,
               color='#e74c3c', alpha=0.7, edgecolor='black', linewidth=2)
    slope, intercept = np.polyfit(df_temporal['PM25_Trend'], df_temporal['Disease_Cases'], 1)
    regression_line = slope * df_temporal['PM25_Trend'] + intercept
    ax2.plot(df_temporal['PM25_Trend'], regression_line, '--', color='#34495e',
            linewidth=2, alpha=0.8, label='.2f')
    ax2.set_xlabel('Annual Mean PM₂.₅ (µg/m³)', fontweight='bold')
    ax2.set_ylabel('Vaccine-Preventable Disease Cases\n(Millions, Annual)', fontweight='bold')
    ax2.set_title('PM₂.₅ Pollution vs Disease Burden Correlation\n(2010-2024)', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    # Seasonal Impact Analysis
    seasons = ['Winter', 'Spring', 'Summer', 'Fall']
    winter_effect = [0.143, 0.136, 0.147, 0.149, 0.158, 0.165, 0.172, 0.178]
    spring_effect = [0.087, 0.092, 0.085, 0.081, 0.089, 0.093, 0.096, 0.101]
    summer_effect = [0.045, 0.048, 0.043, 0.046, 0.042, 0.047, 0.051, 0.049]
    fall_effect = [0.073, 0.068, 0.075, 0.078, 0.074, 0.077, 0.082, 0.085]

    ax3.plot(range(2010, 2018), winter_effect[:8], 'o-', label='Winter (Dec-Feb)', color='#e74c3c', linewidth=2, markersize=6)
    ax3.plot(range(2010, 2018), spring_effect[:8], 's-', label='Spring (Mar-May)', color='#f39c12', linewidth=2, markersize=6)
    ax3.plot(range(2010, 2018), summer_effect[:8], '^-', label='Summer (Jun-Aug)', color='#27ae60', linewidth=2, markersize=6)
    ax3.plot(range(2010, 2018), fall_effect[:8], '+--', label='Fall (Sep-Nov)', color='#3498db', linewidth=2, markersize=6)

    ax3.set_xlabel('Year', fontweight='bold')
    ax3.set_ylabel('Pollution-Vaccine Effect Size\n(Effect per 10 µg/m³)', fontweight='bold')
    ax3.set_title('Seasonal Variations in Pollution-Vaccine Effects\n(2010-2017)', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('./results/vaccine_pollution_temporal_trends.png', dpi=300, bbox_inches='tight',
                pad_inches=0.2, facecolor='white')
    plt.close()

    print("✅ Temporal trends analysis saved to ./results/vaccine_pollution_temporal_trends.png")

def create_economic_cost_benefit():
    """Create cost-benefit analysis visualization."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 8), dpi=300)

    # Annual Economic Cost Categories
    categories = ['Medical Care\nCosts', 'Lost Productivity', 'Work/School\nDays Lost', 'Special Care\nCosts']
    costs = [1.87, 3.42, 0.78, 0.54]  # Billion USD

    bars = ax1.bar(range(len(categories)), costs, color=['#e74c3c', '#f39c12', '#f1c40f', '#3498db'],
                  edgecolor='black', linewidth=1.5, alpha=0.8)

    for bar, cost in zip(bars, costs):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'${cost:.2f}B', ha='center', va='bottom', fontweight='bold')

    ax1.set_ylabel('Annual Economic Cost (Billion USD)', fontweight='bold')
    ax1.set_title('Annual Economic Cost of Reduced Vaccine Effectiveness\n(Attributable to Air Pollution)', fontweight='bold')
    ax1.set_xticks(range(len(categories)))
    ax1.set_xticklabels(categories, rotation=45, ha='right')
    ax1.grid(True, axis='y', alpha=0.3)

    # Clean Air Intervention Benefits
    interventions = ['Electric Vehicle\nTransition', 'Natural Gas\nDistribution', 'Industrial Emission\nControl', 'Agricultural Burning\nBan']
    investment = [2.34, 1.87, 4.23, 0.78]
    benefit = [4.12, 3.24, 6.87, 1.94]
    net_return = [benefit[i] - investment[i] for i in range(len(investment))]
    roi = [(benefit[i]/investment[i] - 1) * 100 for i in range(len(investment))]

    x_pos = np.arange(len(interventions))
    width = 0.35

    ax2.bar(x_pos - width/2, investment, width, label='Investment Cost', color='#e74c3c', alpha=0.8, edgecolor='black')
    ax2.bar(x_pos + width/2, benefit, width, label='Health Benefit', color='#27ae60', alpha=0.8, edgecolor='black')

    for i, (inv, ben, rt, roi_val) in enumerate(zip(investment, benefit, net_return, roi)):
        ax2.text(x_pos[i] - width/2, inv + 0.2, f'-${inv:.1f}B', ha='center', va='bottom', fontweight='bold')
        ax2.text(x_pos[i] + width/2, ben + 0.2, f'+${ben:.1f}B', ha='center', va='bottom', fontweight='bold')
        ax2.text(x_pos[i], ben + 0.5, f'ROI: {roi_val:.0f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=10, color='#34495e')

    ax2.set_ylabel('Economic Impact (Billion USD)', fontweight='bold')
    ax2.set_title('Cost-Benefit Analysis: Clean Air Interventions\nAnnually Recovered Vaccine Effectiveness',
                 fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(interventions, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Total Impact Summary
    labels = ['Current Annual Cost', 'Maximum Clean Air Benefit', 'Net Economic Gain']
    sizes = [6.61, 16.17, 9.56]  # Billion USD
    colors = ['#e74c3c', '#3498db', '#27ae60']
    explode = (0.1, 0, 0)

    ax3.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=90)
    ax3.set_title('Total Annual Economic Impact\nPollution-Vaccine Effectiveness Relationship',
                 fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))

    # Add central annotation
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    ax3.text(0, 0, f'Total Impact:\n${sum(sizes):.2f} Billion\nUSD Annually',
            ha='center', va='center', fontweight='bold', fontsize=12)

    plt.tight_layout()
    plt.savefig('./results/vaccine_pollution_economic_analysis.png', dpi=300, bbox_inches='tight',
                pad_inches=0.2, facecolor='white')
    plt.close()

    print("✅ Economic cost-benefit analysis saved to ./results/vaccine_pollution_economic_analysis.png")

def create_vaccine_type_comparison():
    """Create comparative visualization of vaccine types by pollution sensitivity."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=300)

    # Radar Chart: Vaccine Sensitivity to Pollution
    vaccine_types = ['Measles', 'Oral Polio', 'Varicella', 'DTP', 'Hepatitis B', 'HPV']
    pollution_sensitivity = [1.0, 0.95, 0.85, 0.35, 0.28, 0.22]  # Normalized to measles
    immunological_factors = [0.8, 0.7, 0.6, 0.3, 0.2, 0.1]  # Relative immunological interference

    angles = np.linspace(0, 2 * np.pi, len(vaccine_types), endpoint=False).tolist()
    angles += angles[:1]

    poll_sens_full = pollution_sensitivity + pollution_sensitivity[:1]
    immun_full = immunological_factors + immunological_factors[:1]
    vaccine_types_full = vaccine_types + vaccine_types[:1]

    ax1.plot(angles, poll_sens_full, 'o-', linewidth=3, label='Pollution Sensitivity',
            markersize=8, color='#e74c3c')
    ax1.fill(angles, poll_sens_full, alpha=0.25, color='#e74c3c')
    ax1.plot(angles, immun_full, 's-', linewidth=3, label='Immunological Interference',
            markersize=8, color='#3498db')
    ax1.fill(angles, immun_full, alpha=0.25, color='#3498db')
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(vaccine_types)
    ax1.set_ylim(0, 1.1)
    ax1.set_title('Vaccine Sensitivity to Air Pollution by Type\n(Normalized to Measles Vaccine)',
                 fontweight='bold', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Bar Chart: PAF by Vaccine
    paf_by_vaccine = [8.3, 7.6, 6.4, 2.1, 1.7, 1.2]  # Annual PAF per vaccine
    annual_cases = [2.1, 1.9, 1.6, 0.5, 0.4, 0.3]    # Million attributable cases

    x = np.arange(len(vaccine_types))
    width = 0.35

    bars1 = ax2.bar(x - width/2, paf_by_vaccine, width, label='PAF (%)', color='#e74c3c', alpha=0.8)
    bars2 = ax2.bar(x + width/2, annual_cases, width, label='Attributable Cases\n(Millions)', color='#3498db', alpha=0.8)

    # Add value labels
    for bar1, bar2 in zip(bars1, bars2):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        ax2.text(bar1.get_x() + bar1.get_width()/2., height1 + 0.1,
                f'{height1:.1f}%', ha='center', va='bottom', fontweight='bold')
        ax2.text(bar2.get_x() + bar2.get_width()/2., height2 + 0.02,
                f'{height2:.1f}M', ha='center', va='bottom', fontweight='bold')

    ax2.set_xlabel('Vaccine Type', fontweight='bold')
    ax2.set_ylabel('Impact Measure', fontweight='bold')
    ax2.set_title('Disease Burden Attributable to Air Pollution\n(by Vaccine Type)',
                 fontweight='bold', fontsize=14)
    ax2.set_xticks(x)
    ax2.set_xticklabels(vaccine_types, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig('./results/vaccine_pollution_type_comparison.png', dpi=300, bbox_inches='tight',
                pad_inches=0.2, facecolor='white')
    plt.close()

    print("✅ Vaccine type comparison saved to ./results/vaccine_pollution_type_comparison.png")

def create_world_heatmaps():
    """Create world heatmaps showing PM₂.₅ pollution levels."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 8), dpi=300)

    # Simulated world data (simplified for demonstration)
    countries = [
        'India',       'China',       'Pakistan',    'Bangladesh',  'Nepal',
        'Afghanistan', 'Iran',        'Iraq',        'Saudi Arabia','Jordan',
        'Egypt',       'Indonesia',   'Malaysia',    'Vietnam',     'Thailand',
        'Philippines', 'South Korea', 'Japan',       'Taiwan',      'Hong Kong',
        'Singapore',   'Brazil',      'Mexico',      'Argentina',   'Colombia'
    ]

    pm25_levels = [
        62.1, 58.7, 45.2, 52.8, 49.6,    # South Asia
        48.9, 68.4, 65.7, 72.1, 58.3,    # Middle East
        34.7, 27.6, 41.8, 22.4, 23.9,    # Southeast Asia
        18.9, 14.6, 11.2, 29.8, 16.3,    # East Asia
        15.7, 23.4, 21.8, 34.2, 29.6     # Americas
    ]

    vaccine_loss = [23.4, 21.7, 18.9, 19.6, 18.3,     # Corresponding to PM₂.₅ levels
                   20.2, 28.7, 27.9, 32.1, 24.6,
                   15.3, 13.8, 17.6, 12.1, 11.9,
                   9.7, 8.2, 6.8, 14.3, 8.7]

    economic_impact = [42.3, 38.9, 33.2, 35.7, 32.1,
                      36.2, 49.8, 48.3, 52.9, 42.1,
                      28.7, 25.6, 31.7, 21.8, 22.3,
                      19.2, 16.7, 13.8, 26.2, 17.4]

    # Global transportation connectivity as proxy
    connectivity = np.random.normal(0.7, 0.15, len(countries))
    connectivity = np.clip(connectivity, 0.1, 1.0)

    # PM₂.₅ World Map (simplified visualization)
    ax1.scatter(range(len(countries)), [pm25] * len(countries), s=[pm25*2 for pm25 in pm25_levels],
               c=pm25_levels, cmap='Reds', alpha=0.7, edgecolors='black')
    ax1.set_xlabel('Countries (Indexed)', fontweight='bold')
    ax1.set_ylabel('PM₂.₅ Level Representation', fontweight='bold')
    ax1.set_title('Global PM₂.₅ Pollution Distribution\n(Urban Areas, 2024)', fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Vaccine Effectiveness Loss
    ax2.scatter(range(len(countries)), vaccine_loss, s=[loss*10 for loss in vaccine_loss],
               c=vaccine_loss, cmap='YlOrRd', alpha=0.8, edgecolors='black')
    ax2.plot(range(len(countries)), vaccine_loss, 'o-', alpha=0.3, color='orange', linewidth=1)
    ax2.set_xlabel('Countries (Indexed)', fontweight='bold')
    ax2.set_ylabel('Vaccine Effectiveness Loss (%)', fontweight='bold')
    ax2.set_title('Vaccine Effectiveness Impact of Air Pollution\n(by Country)', fontweight='bold')
    ax2.grid(True, alpha=0.3)

    # Economic Impact Bubble Plot
    ax3.scatter(range(len(countries)), economic_impact, s=[impact*3 for impact in economic_impact],
               c=connectivity, cmap='Blues', alpha=0.8, edgecolors='black')
    ax3.set_xlabel('Countries (Indexed)', fontweight='bold')
    ax3.set_ylabel('Annual Economic Impact (USD Billions)', fontweight='bold')
    ax3.set_title('Economic Cost of Pollution-Impacted Vaccine Effectiveness\n(Bubble size: Economic Impact)', fontweight='bold')
    ax3.grid(True, alpha=0.3)

    # Add country labels (simplified)
    for i, country in enumerate(countries):
        if i % 3 == 0:  # Label every 3rd country to avoid overcrowding
            for ax in [ax1, ax2, ax3]:
                if ax == ax1:
                    y_pos = pm25_levels[i] * 0.02
                elif ax == ax2:
                    y_pos = vaccine_loss[i] + 0.5
                else:
                    y_pos = economic_impact[i] - 2

                ax.text(i, y_pos, country[:3], ha='center', va='bottom',
                       fontsize=8, rotation=45, fontweight='bold')

    plt.tight_layout()
    plt.savefig('./results/vaccine_pollution_world_overview.png', dpi=300, bbox_inches='tight',
                pad_inches=0.2, facecolor='white')
    plt.close()

    print("✅ World overview heatmaps saved to ./results/vaccine_pollution_world_overview.png")

def main():
    """Main function to generate all vaccine-pollution visualization plots."""
    import os
    if not os.path.exists('./results'):
        os.makedirs('./results')
        print("📁 Created ./results directory")

    print("🎨 Generating Vaccine-Pollution Ecological Study Visualization Suite...")
    print("="*70)

    try:
        create_dose_response_curves()
        create_regional_effectiveness_map()
        create_temporal_trends_analysis()
        create_economic_cost_benefit()
        create_vaccine_type_comparison()
        create_world_heatmaps()

        print("\n" + "="*70)
        print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
        print("📊 Check ./results/ directory for all output files:")
        print("   - vaccine_pollution_dose_response.png")
        print("   - vaccine_pollution_regional_patterns.png")
        print("   - vaccine_pollution_temporal_trends.png")
        print("   - vaccine_pollution_economic_analysis.png")
        print("   - vaccine_pollution_type_comparison.png")
        print("   - vaccine_pollution_world_overview.png")
        print("="*70)
        print("🧬 SYSTEM STATUS: VACCINE-POLLUTION ECOLOGICAL STUDY COMPLETE!")
        print("📈 6 high-quality visualization panels generated for publication.")

    except Exception as e:
        print(f"❌ Error generating visualizations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
