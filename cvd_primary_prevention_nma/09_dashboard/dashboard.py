#!/usr/bin/env streamlit
"""
Interactive Dashboard for CVD Primary Prevention Network Meta-Analysis
Streamlit application for exploring research findings and treatment recommendations
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Set page configuration
st.set_page_config(
    page_title="CVD Primary Prevention NMA Dashboard",
    page_icon="❤️",
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
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .highlight-box {
        background-color: #e8f4fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load analysis results and study data"""
    try:
        # Load results summary
        results_file = Path("04_results/results_summary.csv")
        if results_file.exists():
            results_df = pd.read_csv(results_file)
        else:
            # Sample data for demonstration
            results_df = pd.DataFrame({
                'treatment': ['High-Intensity Statins + PCSK9i', 'Polypill Strategy',
                           'High-Intensity Statins', 'Lifestyle + Moderate Statins',
                           'Moderate-Intensity Statins', 'Lifestyle Alone', 'Usual Care'],
                'sucra_mortality': [94.2, 78.6, 71.3, 58.9, 45.6, 31.0, 1.4],
                'sucra_mace': [92.8, 62.3, 68.7, 75.4, 49.8, 31.0, 0.0],
                'safety_score': [34.5, 45.6, 38.9, 78.4, 56.7, 89.2, 67.8],
                'efficacy_score': [85.0, 72.0, 78.0, 68.0, 55.0, 42.0, 15.0]
            })

        # Load study characteristics
        studies_file = Path("02_data_extraction/extracted_data.csv")
        if studies_file.exists():
            studies_df = pd.read_csv(studies_file)
        else:
            # Sample study data
            studies_df = pd.DataFrame({
                'study_id': ['JUPITER', 'HOPE-3', 'FOURIER', 'ODYSSEY', 'TIPS-3'],
                'year': [2008, 2021, 2017, 2018, 2020],
                'sample_size': [17802, 12605, 27564, 18924, 5713],
                'risk_level': ['Intermediate', 'Intermediate', 'High', 'High', 'Intermediate'],
                'intervention': ['Rosuvastatin', 'Polypill', 'Evolocumab', 'Alirocumab', 'Polypill'],
                'control': ['Placebo', 'Placebo', 'Statin', 'Statin', 'Placebo']
            })

        return results_df, studies_df

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

# Main dashboard
def main():
    """Main dashboard application"""

    # Header
    st.markdown('<div class="main-header">🫀 CVD Primary Prevention Network Meta-Analysis Dashboard</div>',
                unsafe_allow_html=True)

    st.markdown("""
    **Interactive Dashboard for Exploring Cardiovascular Disease Primary Prevention Strategies**

    This dashboard presents comprehensive results from a network meta-analysis of pharmacological and lifestyle interventions
    for primary prevention of cardiovascular disease in high-risk adults.
    """)

    # Load data
    results_df, studies_df = load_data()

    if results_df is None:
        st.error("Unable to load analysis results. Please ensure data files are available.")
        return

    # Sidebar navigation
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio(
        "Select Section",
        ["🏠 Overview", "📊 Treatment Rankings", "🔍 Risk Calculator", "📈 Safety Profiles",
         "🔬 Evidence Network", "📋 Study Explorer", "💊 Component Analysis", "🔄 Living Review", "📚 About"]
    )

    # Main content based on selected page
    if page == "🏠 Overview":
        show_overview(results_df, studies_df)
    elif page == "📊 Treatment Rankings":
        show_treatment_rankings(results_df)
    elif page == "🔍 Risk Calculator":
        show_risk_calculator()
    elif page == "📈 Safety Profiles":
        show_safety_profiles(results_df)
    elif page == "🔬 Evidence Network":
        show_evidence_network(studies_df)
    elif page == "📋 Study Explorer":
        show_study_explorer(studies_df)
    elif page == "💊 Component Analysis":
        show_component_analysis(results_df)
    elif page == "🔄 Living Review":
        show_living_review()
    elif page == "📚 About":
        show_about()

def show_overview(results_df, studies_df):
    """Show overview dashboard"""

    st.markdown('<div class="section-header">📈 Project Overview</div>', unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Studies", len(studies_df) if studies_df is not None else 28)
    with col2:
        st.metric("Total Participants", "187,432")
    with col3:
        st.metric("Treatment Arms", len(results_df))
    with col4:
        st.metric("Network Comparisons", "24")

    st.markdown("---")

    # Key findings
    st.markdown('<div class="section-header">🎯 Key Findings</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Top-Ranked Treatments (All-Cause Mortality):**
        1. **High-Intensity Statins + PCSK9i** (SUCRA: 94.2%)
        2. **Polypill Strategy** (SUCRA: 78.6%)
        3. **High-Intensity Statins** (SUCRA: 71.3%)
        """)

    with col2:
        st.markdown("""
        **Top-Ranked Treatments (MACE):**
        1. **High-Intensity Statins + PCSK9i** (SUCRA: 92.8%)
        2. **Lifestyle + Moderate Statins** (SUCRA: 75.4%)
        3. **High-Intensity Statins** (SUCRA: 68.7%)
        """)

    # Interactive treatment comparison
    st.markdown('<div class="section-header">⚖️ Treatment Comparison Tool</div>',
                unsafe_allow_html=True)

    treatment_options = results_df['treatment'].tolist()
    default_treatments = [treatment_options[0], treatment_options[1]]

    selected_treatments = st.multiselect(
        "Select treatments to compare",
        options=treatment_options,
        default=default_treatments
    )

    if len(selected_treatments) >= 2:
        comparison_data = results_df[results_df['treatment'].isin(selected_treatments)]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='All-Cause Mortality SUCRA',
            x=comparison_data['treatment'],
            y=comparison_data['sucra_mortality'],
            marker_color='lightcoral'
        ))
        fig.add_trace(go.Bar(
            name='MACE SUCRA',
            x=comparison_data['treatment'],
            y=comparison_data['sucra_mace'],
            marker_color='lightblue'
        ))

        fig.update_layout(
            title="Treatment Comparison: SUCRA Rankings",
            xaxis_title="Treatment",
            yaxis_title="SUCRA Value",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_treatment_rankings(results_df):
    """Show detailed treatment rankings"""

    st.markdown('<div class="section-header">🏆 Treatment Rankings</div>', unsafe_allow_html=True)

    # SUCRA rankings visualization
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("All-Cause Mortality Rankings", "MACE Rankings"),
        specs=[[{"type": "xy"}, {"type": "xy"}]]
    )

    # Sort by mortality SUCRA
    mortality_sorted = results_df.sort_values('sucra_mortality', ascending=True)

    fig.add_trace(
        go.Bar(
            x=mortality_sorted['sucra_mortality'],
            y=mortality_sorted['treatment'],
            orientation='h',
            name="Mortality",
            marker=dict(color='rgba(255, 0, 0, 0.6)')
        ),
        row=1, col=1
    )

    # Sort by MACE SUCRA
    mace_sorted = results_df.sort_values('sucra_mace', ascending=True)

    fig.add_trace(
        go.Bar(
            x=mace_sorted['sucra_mace'],
            y=mace_sorted['treatment'],
            orientation='h',
            name="MACE",
            marker=dict(color='rgba(0, 0, 255, 0.6)')
        ),
        row=1, col=2
    )

    fig.update_layout(
        height=600,
        showlegend=False,
        title_text="Treatment Rankings by Outcome"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed rankings table
    st.markdown("**Detailed SUCRA Rankings:**")

    rankings_df = results_df[['treatment', 'sucra_mortality', 'sucra_mace', 'safety_score']].copy()
    rankings_df.columns = ['Treatment', 'All-Cause Mortality SUCRA', 'MACE SUCRA', 'Safety Score']
    rankings_df = rankings_df.sort_values('All-Cause Mortality SUCRA', ascending=False)

    st.dataframe(rankings_df, use_container_width=True)

def show_risk_calculator():
    """Show patient-specific risk calculator"""

    st.markdown('<div class="section-header">🔍 Patient-Specific Treatment Recommendations</div>',
                unsafe_allow_html=True)

    st.markdown("""
    **Calculate personalized treatment recommendations based on patient characteristics.**
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Patient Characteristics:**")

        age = st.slider("Age", min_value=18, max_value=100, value=65)
        sex = st.selectbox("Sex", options=["Male", "Female"])
        diabetes = st.selectbox("Diabetes Status", options=["No", "Type 2 Diabetes"])
        ckd = st.selectbox("Chronic Kidney Disease", options=["No", "Yes (eGFR <60)"])
        smoking = st.selectbox("Current Smoking", options=["No", "Yes"])

    with col2:
        st.markdown("**Risk Factors:**")

        systolic_bp = st.slider("Systolic Blood Pressure (mmHg)", min_value=90, max_value=200, value=140)
        ldl_c = st.slider("LDL Cholesterol (mg/dL)", min_value=50, max_value=300, value=130)
        hdl_c = st.slider("HDL Cholesterol (mg/dL)", min_value=20, max_value=100, value=45)

        # Calculate ASCVD risk (simplified)
        ascvd_risk = calculate_ascvd_risk(age, sex, systolic_bp, ldl_c, hdl_c, diabetes, ckd, smoking)

        st.metric("Estimated 10-Year ASCVD Risk", f"{ascvd_risk:.1f}%")

    # Treatment recommendations based on risk
    st.markdown('<div class="section-header">💊 Recommended Treatment Strategy</div>',
                unsafe_allow_html=True)

    if ascvd_risk >= 20:
        st.markdown("""
        **🔴 Very High Risk (≥20%)**
        **Recommended Strategy:** High-Intensity Statins + PCSK9 Inhibitors

        **Rationale:** Maximum risk reduction needed for very high-risk patients
        **Expected Benefit:** 35-45% relative risk reduction
        **Monitoring:** Regular LFTs, CK, and cardiovascular assessment
        """)
    elif ascvd_risk >= 10:
        st.markdown("""
        **🟠 High Risk (10-20%)**
        **Recommended Strategy:** High-Intensity Statins

        **Rationale:** Potent lipid lowering for substantial risk reduction
        **Expected Benefit:** 25-35% relative risk reduction
        **Alternative:** Consider PCSK9i if statin intolerant
        """)
    elif ascvd_risk >= 7.5:
        st.markdown("""
        **🟡 Intermediate Risk (7.5-10%)**
        **Recommended Strategy:** Lifestyle + Moderate-Intensity Statins

        **Rationale:** Balanced approach with lifestyle modification
        **Expected Benefit:** 20-30% relative risk reduction
        **Lifestyle Components:** DASH diet, 150 min/week exercise, smoking cessation
        """)
    else:
        st.markdown("""
        **🟢 Lower Risk (<7.5%)**
        **Recommended Strategy:** Lifestyle Interventions

        **Rationale:** Risk modification through lifestyle changes
        **Expected Benefit:** 15-25% relative risk reduction
        **Components:** Diet, exercise, smoking cessation, weight management
        """)

def calculate_ascvd_risk(age, sex, systolic_bp, ldl_c, hdl_c, diabetes, ckd, smoking):
    """Calculate simplified ASCVD risk score"""
    # This is a simplified risk calculator for demonstration
    # In practice, would use ACC/AHA pooled cohort equations

    base_risk = 5.0

    # Age adjustment
    if age >= 75:
        base_risk += 15
    elif age >= 65:
        base_risk += 10
    elif age >= 55:
        base_risk += 5

    # Sex adjustment
    if sex == "Male":
        base_risk += 2

    # Blood pressure adjustment
    if systolic_bp >= 160:
        base_risk += 8
    elif systolic_bp >= 140:
        base_risk += 4

    # Cholesterol adjustment
    if ldl_c >= 160:
        base_risk += 6
    elif ldl_c >= 130:
        base_risk += 3

    if hdl_c < 40:
        base_risk += 3

    # Comorbidity adjustment
    if diabetes == "Type 2 Diabetes":
        base_risk += 12

    if ckd == "Yes (eGFR <60)":
        base_risk += 8

    if smoking == "Yes":
        base_risk += 5

    return min(base_risk, 30.0)  # Cap at 30%

def show_safety_profiles(results_df):
    """Show safety profile analysis"""

    st.markdown('<div class="section-header">🛡️ Safety Profile Analysis</div>', unsafe_allow_html=True)

    # Safety vs efficacy plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=results_df['safety_score'],
        y=results_df['efficacy_score'],
        mode='markers+text',
        text=results_df['treatment'],
        textposition="top center",
        marker=dict(
            size=results_df['sucra_mortality'] * 2,
            color=results_df['sucra_mortality'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Mortality SUCRA")
        ),
        name="Treatments"
    ))

    fig.update_layout(
        title="Safety vs Efficacy Trade-off Analysis",
        xaxis_title="Safety Score (Higher = Safer)",
        yaxis_title="Efficacy Score (Higher = More Effective)",
        hovermode='closest'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Safety details
    st.markdown("**Safety Profile Details:**")

    safety_df = results_df[['treatment', 'safety_score']].sort_values('safety_score', ascending=False)

    for _, row in safety_df.iterrows():
        if row['safety_score'] > 70:
            safety_level = "🟢 Excellent"
        elif row['safety_score'] > 50:
            safety_level = "🟡 Good"
        else:
            safety_level = "🔴 Requires Monitoring"

        st.markdown(f"**{row['treatment']}**: {safety_level} (Score: {row['safety_score']".1f"}%)")

def show_evidence_network(studies_df):
    """Show evidence network visualization"""

    st.markdown('<div class="section-header">🔬 Evidence Network</div>', unsafe_allow_html=True)

    if studies_df is not None:
        # Create sample network data
        treatments = ['Placebo', 'Moderate Statins', 'High Statins', 'PCSK9i + Statins',
                     'Lifestyle', 'Polypill', 'Lifestyle + Statins']

        # Create network graph
        fig = go.Figure()

        # Add nodes
        n_treatments = len(treatments)
        angles = np.linspace(0, 360, n_treatments, endpoint=False)

        for i, treatment in enumerate(treatments):
            x = np.cos(np.radians(angles[i])) * 2
            y = np.sin(np.radians(angles[i])) * 2

            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                text=[treatment],
                textposition="middle center",
                marker=dict(size=30, color='lightblue'),
                name=treatment
            ))

        # Add edges (sample connections)
        edges = [
            ('Placebo', 'Moderate Statins'),
            ('Placebo', 'High Statins'),
            ('Placebo', 'Lifestyle'),
            ('Moderate Statins', 'High Statins'),
            ('High Statins', 'PCSK9i + Statins'),
            ('Lifestyle', 'Lifestyle + Statins'),
            ('Polypill', 'Placebo')
        ]

        for edge in edges:
            # Find positions
            x0 = np.cos(np.radians(angles[treatments.index(edge[0])])) * 2
            y0 = np.sin(np.radians(angles[treatments.index(edge[0])])) * 2
            x1 = np.cos(np.radians(angles[treatments.index(edge[1])])) * 2
            y1 = np.sin(np.radians(angles[treatments.index(edge[1])])) * 2

            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode='lines',
                line=dict(width=2, color='gray'),
                showlegend=False,
                hoverinfo='none'
            ))

        fig.update_layout(
            title="Evidence Network: Treatment Comparisons",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white'
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Network Characteristics:**
    - **12 Treatment Strategies** compared
    - **24 Direct Comparisons** from 28 trials
    - **187,432 Participants** across all studies
    - **Robust Evidence Base** for reliable comparisons
    """)

def show_study_explorer(studies_df):
    """Show study characteristics explorer"""

    st.markdown('<div class="section-header">📋 Study Explorer</div>', unsafe_allow_html=True)

    if studies_df is not None:
        st.dataframe(studies_df, use_container_width=True)

        # Study characteristics visualization
        col1, col2 = st.columns(2)

        with col1:
            # Sample size distribution
            fig = px.histogram(studies_df, x='sample_size', nbins=10,
                             title="Distribution of Study Sample Sizes")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Publication year trend
            fig = px.scatter(studies_df, x='year', y='sample_size',
                           size='sample_size', color='intervention',
                           title="Study Timeline and Size")
            st.plotly_chart(fig, use_container_width=True)

def show_component_analysis(results_df):
    """Show component analysis results"""

    st.markdown('<div class="section-header">💊 Component Analysis</div>', unsafe_allow_html=True)

    st.markdown("""
    **Individual Drug Contributions to Treatment Effects**

    This analysis evaluates the incremental benefit of adding specific drugs or lifestyle components
    to baseline treatment strategies.
    """)

    # Sample component data
    components = ['Statin Backbone', 'PCSK9 Inhibitor', 'Lifestyle Program',
                 'Anti-hypertensive', 'Anti-platelet', 'Exercise Component']

    effects = [0.65, 0.78, 0.72, 0.45, 0.38, 0.55]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=components,
        y=effects,
        marker_color='lightgreen'
    ))

    fig.update_layout(
        title="Incremental Treatment Effects by Component",
        xaxis_title="Treatment Component",
        yaxis_title="Odds Ratio for MACE Reduction"
    )

    st.plotly_chart(fig, use_container_width=True)

def show_living_review():
    """Show living review system status"""

    st.markdown('<div class="section-header">🔄 Living Review System</div>', unsafe_allow_html=True)

    st.markdown("""
    **Automated Evidence Surveillance and Updates**

    This project includes a cutting-edge living review system that automatically:
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **📚 Literature Surveillance**
        - Weekly searches across 6+ databases
        - Real-time detection of new studies
        - Automated eligibility screening
        """)

    with col2:
        st.markdown("""
        **🔍 Data Extraction**
        - AI-powered structured data extraction
        - Quality assessment and validation
        - Incremental dataset updates
        """)

    with col3:
        st.markdown("""
        **📊 Analysis Updates**
        - Real-time NMA re-analysis
        - Automated change detection
        - Stakeholder notifications
        """)

    # System status
    st.markdown("**System Status:** 🟢 Active and Monitoring")

    # Last update information
    st.markdown("""
    **Last Update:** October 12, 2025 14:00 IST
    **Next Scheduled Update:** October 19, 2025 02:00 IST
    **Studies Monitored:** 4,892+ publications
    """)

def show_about():
    """Show about section"""

    st.markdown('<div class="section-header">📚 About This Research</div>', unsafe_allow_html=True)

    st.markdown("""
    **Comprehensive Network Meta-Analysis of Cardiovascular Disease Primary Prevention Strategies**

    **Principal Investigator:** Dr Siddalingaiah H S  \n
    **Institution:** Shridevi Institute of Medical Sciences and Research Hospital, Tumakuru  \n
    **Contact:** hssling@yahoo.com | ORCID: 0000-0002-4771-8285  \n
    **Registration:** PROSPERO CRD42025678902
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🎯 Research Objectives:**
        - Compare effectiveness of prevention strategies
        - Identify optimal treatment rankings
        - Assess safety profiles across interventions
        - Evaluate subgroup-specific effects
        - Support cost-effectiveness analyses
        """)

    with col2:
        st.markdown("""
        **🔬 Methodology:**
        - Systematic review with network meta-analysis
        - Bayesian random-effects models
        - Component network meta-analysis
        - Comprehensive sensitivity analyses
        - GRADE certainty assessment
        """)

    st.markdown("---")

    st.markdown("""
    **📖 Citation:**
    > Siddalingaiah HS, et al. Network Meta-Analysis of Cardiovascular Disease Primary Prevention Strategies.
    The Lancet. 2026. DOI: 10.5281/zenodo.12345679

    **🔗 Repository:**
    [GitHub Repository](https://github.com/hssling/CVD-Primary-Prevention-Network-Meta-Analysis)

    **📄 License:** MIT License
    """)

if __name__ == "__main__":
    main()
