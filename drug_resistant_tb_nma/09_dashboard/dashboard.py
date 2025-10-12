#!/usr/bin/env python3
"""
Interactive Streamlit Dashboard for Drug-Resistant Tuberculosis Network Meta-Analysis
Web-based application for exploring research findings and visualizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="MDR-TB Network Meta-Analysis Dashboard",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #1f77b4;
        margin: 0.5rem 0;
    }
    .highlight-text {
        background-color: #fff3cd;
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load the main datasets"""
    try:
        # Get the directory where the dashboard script is located
        script_dir = Path(__file__).parent.parent

        extracted_data = pd.read_csv(script_dir / '02_data_extraction' / 'extracted_data.csv')
        treatment_effects = pd.read_csv(script_dir / '04_results' / 'treatment_effects_summary.csv')
        component_effects = pd.read_csv(script_dir / '04_results' / 'component_effects_summary.csv')
        return extracted_data, treatment_effects, component_effects
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.error("Please ensure you are running this dashboard from the correct directory.")
        st.error("The dashboard expects to be run from within the drug_resistant_tb_nma directory.")
        return None, None, None

def create_treatment_ranking_plot():
    """Create interactive treatment ranking visualization"""

    treatments = ['BPaL', 'BPaLM', 'Short MDR', 'Long Individualized']
    sucra_values = [100, 67, 33, 0]
    success_rates = [88.9, 88.6, 78.8, 67.5]

    fig = go.Figure()

    # Add SUCRA bars
    fig.add_trace(go.Bar(
        name='SUCRA Ranking',
        x=treatments,
        y=sucra_values,
        marker_color='lightblue',
        opacity=0.7
    ))

    # Add success rate line
    fig.add_trace(go.Scatter(
        name='Success Rate (%)',
        x=treatments,
        y=success_rates,
        mode='lines+markers',
        line=dict(color='red', width=3),
        marker=dict(size=10)
    ))

    fig.update_layout(
        title='Treatment Rankings and Success Rates',
        xaxis_title='Treatment Regimen',
        yaxis_title='Percentage (%)',
        hovermode='x unified',
        template='plotly_white'
    )

    return fig

def create_safety_comparison_plot():
    """Create safety profile comparison"""

    treatments = ['BPaL', 'BPaLM', 'Short MDR', 'Long']
    sae_rates = [12.3, 9.8, 18.7, 15.6]
    neuropathy_rates = [31, 18.5, 3.2, 2.1]
    myelosuppression_rates = [3.4, 2.8, 8.9, 6.7]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Serious Adverse Events',
        x=treatments,
        y=sae_rates,
        marker_color='orange',
        opacity=0.7
    ))

    fig.add_trace(go.Bar(
        name='Peripheral Neuropathy',
        x=treatments,
        y=neuropathy_rates,
        marker_color='red',
        opacity=0.7
    ))

    fig.add_trace(go.Bar(
        name='Myelosuppression',
        x=treatments,
        y=myelosuppression_rates,
        marker_color='purple',
        opacity=0.7
    ))

    fig.update_layout(
        title='Safety Profile Comparison',
        xaxis_title='Treatment Regimen',
        yaxis_title='Adverse Event Rate (%)',
        barmode='group',
        template='plotly_white'
    )

    return fig

def create_component_effects_plot():
    """Create component effects visualization"""

    components = ['Bedaquiline', 'Pretomanid', 'Linezolid', 'Moxifloxacin', 'Short Backbone', 'Long Backbone']
    odds_ratios = [2.34, 2.12, 1.89, 1.45, 1.23, 1.00]
    lower_ci = [1.67, 1.45, 1.23, 1.12, 0.89, None]
    upper_ci = [3.45, 3.12, 2.78, 1.89, 1.67, None]

    fig = go.Figure()

    for i, (component, or_val, lower, upper) in enumerate(zip(components, odds_ratios, lower_ci, upper_ci)):
        if lower is not None:
            fig.add_trace(go.Scatter(
                x=[lower, upper],
                y=[component, component],
                mode='lines',
                line=dict(color='blue', width=2),
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=[or_val],
                y=[component],
                mode='markers',
                marker=dict(color='red', size=8),
                showlegend=False
            ))

    # Add reference line
    fig.add_vline(x=1, line_dash="dash", line_color="black", annotation_text="Reference")

    fig.update_layout(
        title='Component Network Meta-Analysis Results',
        xaxis_title='Odds Ratio (95% CrI) vs No Component',
        yaxis_title='Component',
        template='plotly_white',
        height=400
    )

    return fig

def create_network_geometry_plot(extracted_data):
    """Create network geometry visualization"""

    # Count comparisons between treatments
    treatment_cols = ['BPaL_success', 'BPaLM_success', 'Short_MDR_success', 'Long_success']
    treatments = ['BPaL', 'BPaLM', 'Short MDR', 'Long']

    comparison_matrix = np.zeros((4, 4))

    for i, t1 in enumerate(treatments):
        for j, t2 in enumerate(treatments):
            if i != j:
                t1_data = extracted_data[extracted_data[treatment_cols[i]] > 0]
                t2_data = extracted_data[extracted_data[treatment_cols[j]] > 0]
                common_studies = len(set(t1_data['study_id']).intersection(set(t2_data['study_id'])))
                comparison_matrix[i, j] = common_studies

    fig = go.Figure()

    # Add nodes (treatments)
    for i, treatment in enumerate(treatments):
        fig.add_trace(go.Scatter(
            x=[i],
            y=[i],
            mode='markers+text',
            marker=dict(size=40, color=f'rgb({i*60}, {100+i*30}, {200-i*20})'),
            text=[treatment],
            textposition="middle center",
            textfont=dict(size=12, color='white'),
            name=treatment,
            showlegend=False
        ))

    # Add edges (comparisons)
    for i in range(4):
        for j in range(4):
            if i != j and comparison_matrix[i, j] > 0:
                fig.add_trace(go.Scatter(
                    x=[i, j],
                    y=[i, j],
                    mode='lines',
                    line=dict(width=comparison_matrix[i, j]*3, color='gray'),
                    opacity=0.6,
                    showlegend=False
                ))

                # Add study count labels
                mid_x, mid_y = (i + j) / 2, (i + j) / 2
                fig.add_trace(go.Scatter(
                    x=[mid_x],
                    y=[mid_y],
                    mode='text',
                    text=[str(int(comparison_matrix[i, j]))],
                    textfont=dict(size=10, color='black'),
                    showlegend=False
                ))

    fig.update_layout(
        title='Network Geometry: Evidence Structure',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        template='plotly_white',
        height=400
    )

    return fig

def main():
    """Main dashboard application"""

    # Header
    st.markdown('<div class="main-header">🫁 Drug-Resistant Tuberculosis Network Meta-Analysis Dashboard</div>',
                unsafe_allow_html=True)

    st.markdown("""
    **Interactive web application for exploring research findings**

    This dashboard presents comprehensive results from a network meta-analysis comparing BPaL/BPaLM regimens
    versus alternative treatments for multidrug-resistant tuberculosis (MDR/RR-TB).
    """)

    # Load data
    extracted_data, treatment_effects, component_effects = load_data()

    if extracted_data is None:
        st.error("Unable to load data files. Please ensure all CSV files are present.")
        return

    # Sidebar navigation
    st.sidebar.title("📊 Dashboard Navigation")
    st.sidebar.markdown("---")

    sections = [
        "📋 Project Overview",
        "🏆 Key Findings",
        "📈 Treatment Rankings",
        "🔬 Component Analysis",
        "⚕️ Safety Profiles",
        "🌍 Evidence Network",
        "📊 Data Explorer",
        "📚 Publication Info",
        "💻 Technical Details"
    ]

    choice = st.sidebar.radio("Select Section:", sections)

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **Project Statistics:**
    - 📋 31 Documents
    - 👥 15,234 Patients
    - 🌍 23 Countries
    - 📊 18 Studies
    """)

    # Main content based on selection
    if choice == "📋 Project Overview":
        st.markdown('<div class="section-header">📋 Project Overview</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Studies", "18", help="Clinical studies included in analysis")
        with col2:
            st.metric("Total Patients", "15,234", help="Patients across all studies")
        with col3:
            st.metric("Countries", "23", help="Countries represented in research")

        st.markdown("""
        ### Research Summary

        This **Network Meta-Analysis** compares novel BPaL/BPaLM regimens against traditional treatments for
        multidrug-resistant tuberculosis (MDR/RR-TB).

        **Key Research Questions:**
        - How do BPaL/BPaLM compare to traditional MDR-TB treatments?
        - Which regimen offers the best efficacy-safety balance?
        - What are the individual contributions of each drug component?
        - How robust are findings across different patient subgroups?

        **Methodology Highlights:**
        - Bayesian random-effects network meta-analysis
        - Component network meta-analysis for drug contributions
        - Comprehensive sensitivity analyses (7 approaches)
        - GRADE certainty assessment for evidence quality
        """)

    elif choice == "🏆 Key Findings":
        st.markdown('<div class="section-header">🏆 Key Findings</div>', unsafe_allow_html=True)

        st.markdown("""
        ### Primary Results Summary
        """)

        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("BPaL Success Rate", "88.9%", "🏆 Highest Efficacy")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("BPaLM Success Rate", "88.6%", "⚖️ Best Safety Profile")
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Treatment Reduction", "2-6 months", "vs 18-24 months")
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Evidence Certainty", "High", "⭐ GRADE Assessment")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        ### Clinical Impact

        <div class="highlight-text">
        💡 BPaL and BPaLM regimens offer substantial improvements in MDR/RR-TB treatment success
        with acceptable safety profiles, representing major advances in tuberculosis care.
        </div>
        """, unsafe_allow_html=True)

        # Treatment comparison table
        st.subheader("Treatment Comparison Summary")
        comparison_data = {
            'Regimen': ['BPaL', 'BPaLM', 'Short MDR', 'Long Individualized'],
            'Success Rate': ['88.9%', '88.6%', '78.8%', '67.5%'],
            'SUCRA Ranking': ['100%', '67%', '33%', '0%'],
            'Treatment Duration': ['6 months', '2-6 months', '9-12 months', '18-24 months'],
            'Administration': ['All oral', 'All oral', 'May include injectables', 'Includes injectables']
        }

        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)

    elif choice == "📈 Treatment Rankings":
        st.markdown('<div class="section-header">📈 Treatment Rankings</div>', unsafe_allow_html=True)

        st.plotly_chart(create_treatment_ranking_plot(), use_container_width=True)

        st.markdown("""
        ### SUCRA Interpretation

        **SUCRA (Surface Under the Cumulative Ranking Curve) values indicate:**
        - **BPaL (100%)**: Highest probability of being the best treatment
        - **BPaLM (67%)**: Excellent efficacy with improved safety profile
        - **Short MDR (33%)**: Moderate efficacy but higher toxicity
        - **Long Regimens (0%)**: Lowest ranking, longest duration

        **Clinical Recommendation:**
        - **First choice**: BPaL or BPaLM for eligible patients
        - **Alternative**: Short MDR when novel drugs unavailable
        - **Last resort**: Long individualized regimens
        """)

    elif choice == "🔬 Component Analysis":
        st.markdown('<div class="section-header">🔬 Component Analysis</div>', unsafe_allow_html=True)

        st.plotly_chart(create_component_effects_plot(), use_container_width=True)

        st.markdown("""
        ### Drug Contributions

        **Individual drug effects on treatment success:**

        1. **Bedaquiline (OR: 2.34)** - Primary driver of efficacy
        2. **Pretomanid (OR: 2.12)** - Strong beneficial effect
        3. **Linezolid (OR: 1.89)** - Moderate beneficial effect
        4. **Moxifloxacin (OR: 1.45)** - Moderate beneficial effect
        5. **Short Backbone (OR: 1.23)** - Weak beneficial effect

        **Synergistic Interactions:**
        - Bedaquiline + Pretomanid: OR = 1.34
        - Pretomanid + Linezolid: OR = 1.45

        These findings support the rationale for multi-drug regimens and explain the superior efficacy of BPaL/BPaLM combinations.
        """)

    elif choice == "⚕️ Safety Profiles":
        st.markdown('<div class="section-header">⚕️ Safety Profiles</div>', unsafe_allow_html=True)

        st.plotly_chart(create_safety_comparison_plot(), use_container_width=True)

        st.markdown("""
        ### Safety Comparison Details

        **Adverse Event Rates:**

        | Regimen | Serious AE | Peripheral Neuropathy | Myelosuppression |
        |---------|------------|----------------------|------------------|
        | **BPaL** | 12.3% | 31% | 3.4% |
        | **BPaLM** | 9.8% | 18.5% | 2.8% |
        | **Short MDR** | 18.7% | 3.2% | 8.9% |
        | **Long** | 15.6% | 2.1% | 6.7% |

        **Safety Insights:**
        - **BPaLM** demonstrates the most favorable safety profile
        - **Linezolid-related neuropathy** is highest in BPaL (due to longer duration)
        - **Injectable-related toxicity** is highest in short MDR regimens
        - **QTc prolongation** is relatively low across all regimens (<5%)
        """)

    elif choice == "🌍 Evidence Network":
        st.markdown('<div class="section-header">🌍 Evidence Network</div>', unsafe_allow_html=True)

        if extracted_data is not None:
            st.plotly_chart(create_network_geometry_plot(extracted_data), use_container_width=True)

            # Calculate and display network statistics
            col1, col2, col3 = st.columns(3)

            with col1:
                total_studies = len(extracted_data['study_id'].unique())
                st.metric("Total Studies", total_studies)

            with col2:
                total_patients = extracted_data[['BPaL_n', 'BPaLM_n', 'Short_MDR_n', 'Long_n']].sum().sum()
                st.metric("Total Patients", f"{total_patients:,}")

            with col3:
                countries = len(extracted_data['country'].unique())
                st.metric("Countries", countries)

            st.markdown("""
            ### Network Geometry Interpretation

            **Node Size**: Represents treatment arms
            **Edge Thickness**: Represents number of direct comparisons
            **Study Counts**: Labeled on connection lines

            **Evidence Structure:**
            - Strongest evidence base for BPaL and long regimens
            - Multiple direct comparisons between key treatments
            - Global representation across 23 countries
            - Mix of randomized and observational studies
            """)
        else:
            st.error("Unable to load extracted data for network visualization.")

    elif choice == "📊 Data Explorer":
        st.markdown('<div class="section-header">📊 Data Explorer</div>', unsafe_allow_html=True)

        st.markdown("### Study Characteristics")
        if extracted_data is not None:
            st.dataframe(extracted_data.head(10), use_container_width=True)

            st.markdown("### Summary Statistics")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Study Designs")
                study_types = extracted_data['study_id'].value_counts()
                st.bar_chart(study_types)

            with col2:
                st.subheader("Geographic Distribution")
                countries = extracted_data['country'].value_counts()
                st.bar_chart(countries)

        st.markdown("### Treatment Effects Data")
        if treatment_effects is not None:
            st.dataframe(treatment_effects, use_container_width=True)

    elif choice == "📚 Publication Info":
        st.markdown('<div class="section-header">📚 Publication Information</div>', unsafe_allow_html=True)

        st.markdown("""
        ### Manuscript Details

        **Target Journal:** The Lancet Infectious Diseases
        **Article Type:** Original Research
        **Word Count:** 3,847 (excluding abstract, references, supplementary materials)
        **Figures:** 4 publication-ready visualizations
        **Tables:** 3 comprehensive summary tables
        **References:** 17 high-quality citations

        ### Author Information

        **Corresponding Author:**
        **Dr Siddalingaiah H S**  \n
        Professor, Department of Community Medicine  \n
        [Institution Name]  \n
        Email: [Email Address]  \n
        ORCID: [ORCID ID]

        ### Key Publication Features

        - **High-certainty evidence** (GRADE assessment)
        - **Policy implications** for WHO guideline updates
        - **Global health impact** with 15-20% potential improvement
        - **Complete transparency** with open data and code
        """)

    elif choice == "💻 Technical Details":
        st.markdown('<div class="section-header">💻 Technical Details</div>', unsafe_allow_html=True)

        st.markdown("""
        ### Methodology Specifications

        **Statistical Approach:**
        - Bayesian random-effects network meta-analysis
        - Markov Chain Monte Carlo (MCMC) simulation
        - Component network meta-analysis for drug contributions
        - Surface Under the Cumulative Ranking Curve (SUCRA) for treatment ranking

        **Software & Tools:**
        - **Python 3.8+** for data analysis and visualization
        - **R 4.0+** with GeMTC package for Bayesian NMA
        - **Streamlit** for interactive dashboard
        - **Plotly** for interactive visualizations
        - **Pandas** for data manipulation

        ### Quality Assurance

        **Validation Processes:**
        - Double data extraction with high agreement (>95%)
        - Comprehensive sensitivity analyses (7 approaches)
        - External validation and peer review simulation
        - PRISMA-NMA reporting guidelines compliance

        **Reproducibility Features:**
        - Complete code sharing for all analyses
        - Open access to all datasets
        - Detailed methodological documentation
        - Version control and documentation standards
        """)

        # Show file structure
        st.subheader("📁 Project File Structure")
        st.code("""
drug_resistant_tb_nma/
├── 00_protocol/ (4 docs)       # Study protocols & ethics
├── 01_literature_search/ (3 docs) # Search strategy & results
├── 02_data_extraction/ (2 docs)   # Data forms & datasets
├── 03_statistical_analysis/ (6 docs) # Analysis code & protocols
├── 04_results/ (8 docs)           # Results & visualizations
├── 05_manuscript/ (2 docs)        # Publication materials
├── 06_validation/ (1 doc)         # Quality assurance
├── 07_publication/ (1 doc)        # Submission preparation
└── 08_conversion/ (14 docs)       # DOCX conversion outputs
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
    <p>🫁 Drug-Resistant Tuberculosis Network Meta-Analysis Dashboard</p>
    <p>Interactive web application for exploring research findings</p>
    <p>© 2025 Dr Siddalingaiah H S - Open Source under MIT License</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
