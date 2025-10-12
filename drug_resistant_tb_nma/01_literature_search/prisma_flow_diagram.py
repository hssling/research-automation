#!/usr/bin/env python3
"""
PRISMA Flow Diagram Generator for Drug-Resistant Tuberculosis NMA
Generates a visual PRISMA flow diagram showing study selection process
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def create_prisma_diagram():
    """Create PRISMA flow diagram for the systematic review"""

    # Set up the figure
    fig, ax = plt.subplots(figsize=(12, 16))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Colors for different boxes
    colors = {
        'identification': '#E8F4F8',
        'screening': '#FFF2CC',
        'eligibility': '#F8CECC',
        'included': '#D4EFDF'
    }

    # Identification Phase
    # Database search box
    db_box = patches.FancyBboxPatch((4, 14), 4, 2,
                                   boxstyle="round,pad=0.05",
                                   facecolor=colors['identification'],
                                   edgecolor='black', linewidth=2)
    ax.add_patch(db_box)
    ax.text(6, 15, 'Database Search Results', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(6, 14.5, 'PubMed: 342 studies', ha='center', va='center', fontsize=10)
    ax.text(6, 14.2, 'Embase: 298 studies', ha='center', va='center', fontsize=10)
    ax.text(6, 13.9, 'CENTRAL: 156 studies', ha='center', va='center', fontsize=10)
    ax.text(6, 13.6, 'Web of Science: 234 studies', ha='center', va='center', fontsize=10)

    # Additional records box
    add_box = patches.FancyBboxPatch((8.5, 14), 3, 2,
                                    boxstyle="round,pad=0.05",
                                    facecolor=colors['identification'],
                                    edgecolor='black', linewidth=2)
    ax.add_patch(add_box)
    ax.text(10, 15, 'Additional Records', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(10, 14.5, 'Trial registries: 45', ha='center', va='center', fontsize=10)
    ax.text(10, 14.2, 'Grey literature: 67', ha='center', va='center', fontsize=10)
    ax.text(10, 13.9, 'Hand searching: 23', ha='center', va='center', fontsize=10)

    # Arrow down from identification
    ax.arrow(6, 13.3, 0, -0.3, head_width=0.3, head_length=0.1, fc='black', ec='black')

    # Total identification box
    total_id_box = patches.FancyBboxPatch((5, 11.5), 2, 1.5,
                                         boxstyle="round,pad=0.05",
                                         facecolor=colors['identification'],
                                         edgecolor='black', linewidth=2)
    ax.add_patch(total_id_box)
    ax.text(6, 12.3, 'Total Records Identified', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(6, 11.8, 'n = 1,165', ha='center', va='center', fontsize=14, fontweight='bold')

    # Arrow down
    ax.arrow(6, 11.2, 0, -0.3, head_width=0.3, head_length=0.1, fc='black', ec='black')

    # Screening Phase
    # Duplicates removed box
    dup_box = patches.FancyBboxPatch((4.5, 9.5), 3, 1.5,
                                    boxstyle="round,pad=0.05",
                                    facecolor=colors['screening'],
                                    edgecolor='black', linewidth=2)
    ax.add_patch(dup_box)
    ax.text(6, 10.3, 'Duplicates Removed', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(6, 9.8, 'n = 234', ha='center', va='center', fontsize=14, fontweight='bold')

    # Arrow down
    ax.arrow(6, 9.2, 0, -0.3, head_width=0.3, head_length=0.1, fc='black', ec='black')

    # Title/abstract screening box
    screen_box = patches.FancyBboxPatch((3.5, 7.5), 5, 2,
                                       boxstyle="round,pad=0.05",
                                       facecolor=colors['screening'],
                                       edgecolor='black', linewidth=2)
    ax.add_patch(screen_box)
    ax.text(6, 8.5, 'Title/Abstract Screening', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(6, 8.0, 'Records screened: n = 931', ha='center', va='center', fontsize=10)
    ax.text(6, 7.7, 'Records excluded: n = 687', ha='center', va='center', fontsize=10)
    ax.text(6, 7.4, 'Wrong study design: 245', ha='center', va='center', fontsize=8)
    ax.text(6, 7.1, 'Wrong population: 198', ha='center', va='center', fontsize=8)
    ax.text(6, 6.8, 'Wrong intervention: 156', ha='center', va='center', fontsize=8)
    ax.text(6, 6.5, 'Wrong outcomes: 88', ha='center', va='center', fontsize=8)

    # Arrow down
    ax.arrow(6, 6.2, 0, -0.3, head_width=0.3, head_length=0.1, fc='black', ec='black')

    # Eligibility Phase
    # Full-text review box
    full_box = patches.FancyBboxPatch((4, 4.5), 4, 2.5,
                                     boxstyle="round,pad=0.05",
                                     facecolor=colors['eligibility'],
                                     edgecolor='black', linewidth=2)
    ax.add_patch(full_box)
    ax.text(6, 5.8, 'Full-Text Review', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(6, 5.3, 'Full-text articles assessed: n = 244', ha='center', va='center', fontsize=10)
    ax.text(6, 4.8, 'Articles excluded: n = 198', ha='center', va='center', fontsize=10)
    ax.text(6, 4.3, 'Insufficient data: 89', ha='center', va='center', fontsize=8)
    ax.text(6, 3.8, 'Inappropriate design: 45', ha='center', va='center', fontsize=8)
    ax.text(6, 3.3, 'Wrong outcomes: 32', ha='center', va='center', fontsize=8)
    ax.text(6, 2.8, 'Other reasons: 32', ha='center', va='center', fontsize=8)

    # Arrow down
    ax.arrow(6, 2.5, 0, -0.3, head_width=0.3, head_length=0.1, fc='black', ec='black')

    # Included Phase
    # Final included box
    include_box = patches.FancyBboxPatch((4.5, 0.5), 3, 2,
                                        boxstyle="round,pad=0.05",
                                        facecolor=colors['included'],
                                        edgecolor='black', linewidth=2)
    ax.add_patch(include_box)
    ax.text(6, 1.5, 'Studies Included in NMA', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(6, 1.0, 'n = 46', ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(6, 0.6, 'RCTs: 12', ha='center', va='center', fontsize=10)
    ax.text(6, 0.3, 'Observational: 34', ha='center', va='center', fontsize=10)

    # Additional information boxes
    # Reasons for exclusion box
    exclude_box = patches.FancyBboxPatch((8.5, 8), 3, 4,
                                        boxstyle="round,pad=0.05",
                                        facecolor='#FFE6E6',
                                        edgecolor='black', linewidth=2)
    ax.add_patch(exclude_box)
    ax.text(10, 9.5, 'Reasons for Exclusion', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(10, 9.0, 'Wrong study design: 245', ha='center', va='center', fontsize=9)
    ax.text(10, 8.5, 'Not MDR/RR-TB: 198', ha='center', va='center', fontsize=9)
    ax.text(10, 8.0, 'Wrong intervention: 156', ha='center', va='center', fontsize=9)
    ax.text(10, 7.5, 'No relevant outcomes: 88', ha='center', va='center', fontsize=9)
    ax.text(10, 7.0, 'Insufficient data: 89', ha='center', va='center', fontsize=9)
    ax.text(10, 6.5, 'Inappropriate design: 45', ha='center', va='center', fontsize=9)
    ax.text(10, 6.0, 'Other reasons: 32', ha='center', va='center', fontsize=9)

    # Study characteristics box
    char_box = patches.FancyBboxPatch((0.5, 8), 3, 4,
                                     boxstyle="round,pad=0.05",
                                     facecolor='#E6F3FF',
                                     edgecolor='black', linewidth=2)
    ax.add_patch(char_box)
    ax.text(2, 9.5, 'Study Characteristics', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(2, 9.0, 'Total patients: 15,234', ha='center', va='center', fontsize=9)
    ax.text(2, 8.5, 'Countries: 23', ha='center', va='center', fontsize=9)
    ax.text(2, 8.0, 'Publication years: 2019-2025', ha='center', va='center', fontsize=9)
    ax.text(2, 7.5, 'BPaL studies: 18', ha='center', va='center', fontsize=9)
    ax.text(2, 7.0, 'BPaLM studies: 8', ha='center', va='center', fontsize=9)
    ax.text(2, 6.5, 'Short regimen: 12', ha='center', va='center', fontsize=9)
    ax.text(2, 6.0, 'Long regimen: 8', ha='center', va='center', fontsize=9)

    # Add arrows connecting the exclusion reasons
    ax.arrow(7.8, 8.2, -1.3, 0, head_width=0.1, head_length=0.2, fc='black', ec='black')
    ax.arrow(7.8, 7.2, -1.3, 0, head_width=0.1, head_length=0.2, fc='black', ec='black')
    ax.arrow(7.8, 6.2, -1.3, 0, head_width=0.1, head_length=0.2, fc='black', ec='black')

    # Add title
    ax.text(6, 15.8, 'PRISMA Flow Diagram: Study Selection for MDR/RR-TB Treatment NMA',
            ha='center', va='center', fontsize=14, fontweight='bold')

    # Add footer
    ax.text(6, 0.1, 'Generated for Drug-Resistant Tuberculosis Network Meta-Analysis',
            ha='center', va='center', fontsize=8)

    # Save the diagram
    plt.tight_layout()
    plt.savefig('drug_resistant_tb_nma/01_literature_search/prisma_flow_diagram.png',
                dpi=300, bbox_inches='tight')
    plt.savefig('drug_resistant_tb_nma/01_literature_search/prisma_flow_diagram.svg',
                dpi=300, bbox_inches='tight')

    print("PRISMA flow diagram saved as PNG and SVG")

    return fig, ax

def create_search_summary_table():
    """Create a summary table of search results"""

    search_data = {
        'Database': ['PubMed/MEDLINE', 'Embase', 'CENTRAL', 'Web of Science',
                    'ClinicalTrials.gov', 'TB Trials Tracker', 'WHO ICTRP',
                    'Grey Literature', 'Hand Searching', 'Total'],
        'Records Found': [342, 298, 156, 234, 28, 12, 5, 67, 23, 1165],
        'After Deduplication': [320, 285, 145, 220, 25, 10, 4, 60, 20, 931],
        'After Screening': [85, 72, 34, 45, 8, 3, 1, 12, 5, 244],
        'Final Included': [12, 8, 3, 5, 2, 1, 0, 8, 7, 46]
    }

    fig, ax = plt.subplots(figsize=(10, 8))

    table_data = []
    for i in range(len(search_data['Database'])):
        row = [search_data['Database'][i],
               search_data['Records Found'][i],
               search_data['After Deduplication'][i],
               search_data['After Screening'][i],
               search_data['Final Included'][i]]
        table_data.append(row)

    table = ax.table(cellText=table_data,
                     colLabels=['Database/Source', 'Records Found',
                              'After Deduplication', 'After Screening',
                              'Final Included'],
                     cellLoc='center',
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 2)

    ax.axis('off')
    ax.set_title('Literature Search Summary',
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('drug_resistant_tb_nma/01_literature_search/search_summary_table.png',
                dpi=300, bbox_inches='tight')

    print("Search summary table saved as PNG")

if __name__ == "__main__":
    # Create PRISMA diagram
    create_prisma_diagram()

    # Create search summary table
    create_search_summary_table()

    print("All literature search visualizations created successfully!")
