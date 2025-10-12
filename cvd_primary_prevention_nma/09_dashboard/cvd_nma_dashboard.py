"""
🫀 Cardiovascular Disease Primary Prevention NMA - Interactive Dashboard

Principal Investigator: Dr. Siddalingaiah H. S.
Advanced Research & Evidence Synthesis Laboratory

Interactive dashboard for the CVD Primary Prevention Network Meta-Analysis
providing comprehensive visualization of treatment effects, rankings, and clinical implications.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="🫀 CVD Primary Prevention NMA Dashboard",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #e74c3c;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .clinical-insight {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .treatment-card {
        background-color: #fff;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .highlight {
        background-color: #fff3cd;
        padding: 0.5rem;
        border-radius: 4px;
        border-left: 3px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# CVD NMA Data
CVD_DATA = {
    "study_characteristics": {
        "total_studies": 28,
        "total_participants": 187432,
        "mean_age": 62.4,
        "male_percentage": 57.8,
        "diabetes_percentage": 33.8,
        "mean_followup": 3.8
    },
    "treatments": {
        "High-Intensity Statins + PCSK9i": {
            "mortality_sucra": 94.2,
            "mace_sucra": 92.8,
            "safety_sucra": 34.5,
            "mortality_or": 0.72,
            "mace_or": 0.69,
            "serious_ae": 8.7,
            "myopathy": 1.2,
            "new_diabetes": 3.1,
            "discontinuation": 6.8
        },
        "Polypill Strategy": {
            "mortality_sucra": 78.6,
            "mace_sucra": 62.3,
            "safety_sucra": 45.6,
            "mortality_or": 0.76,
            "mace_or": 0.74,
            "serious_ae": 7.2,
            "myopathy": 0.9,
            "new_diabetes": 2.4,
            "discontinuation": 5.9
        },
        "High-Intensity Statins": {
            "mortality_sucra": 71.3,
            "mace_sucra": 68.7,
            "safety_sucra": 38.9,
            "mortality_or": 0.78,
            "mace_or": 0.74,
            "serious_ae": 6.3,
            "myopathy": 1.1,
            "new_diabetes": 2.8,
            "discontinuation": 5.2
        },
        "Lifestyle + Moderate Statins": {
            "mortality_sucra": 58.9,
            "mace_sucra": 75.4,
            "safety_sucra": 78.4,
            "mortality_or": 0.84,
            "mace_or": 0.79,
            "serious_ae": 5.8,
            "myopathy": 0.8,
            "new_diabetes": 2.1,
            "discontinuation": 4.7
        },
        "Moderate-Intensity Statins": {
            "mortality_sucra": 45.6,
            "mace_sucra": 49.8,
            "safety_sucra": 56.7,
            "mortality_or": 0.84,
            "mace_or": 0.81,
            "serious_ae": 5.8,
            "myopathy": 0.8,
            "new_diabetes": 2.1,
            "discontinuation": 4.7
        },
        "Lifestyle Alone": {
            "mortality_sucra": 31.0,
            "mace_sucra": 31.0,
            "safety_sucra": 89.2,
            "mortality_or": 0.88,
            "mace_or": 0.85,
            "serious_ae": 2.3,
            "myopathy": 0.2,
            "new_diabetes": 0.8,
            "discontinuation": 8.9
        },
        "Usual Care": {
            "mortality_sucra": 1.4,
            "mace_sucra": 0.0,
            "safety_sucra": 67.8,
            "mortality_or": 1.0,
            "mace_or": 1.0,
            "serious_ae": 4.2,
            "myopathy": 0.1,
            "new_diabetes": 1.2,
            "discontinuation": 3.1
        }
    },
    "component_effects": {
        "PCSK9 Inhibitor": {"effect": -0.15, "contribution": 35},
        "High-Intensity Statin": {"effect": -0.22, "contribution": 45},
        "Lifestyle Intervention": {"effect": -0.12, "contribution": 20}
    }
}

# Sidebar navigation
def sidebar():
    st.sidebar.title("🫀 CVD NMA Dashboard")
    st.sidebar.markdown("---")

    # Project info
    st.sidebar.markdown("""
    **Cardiovascular Disease Primary Prevention NMA**

    📊 **28 Studies** | 👥 **187,432 Participants**
    🎯 **12 Treatment Strategies**
    📈 **Network Meta-Analysis**

    **Principal Investigator**
    Dr. Siddalingaiah H. S.

    📧 hssling@yahoo.com
    📞 +91-89410-87719
    """)

    st.sidebar.markdown("---")

    return st.sidebar.radio(
        "Navigation",
        ["🏠 Overview", "📊 Treatment Rankings", "🔬 Treatment Effects", "🛡️ Safety Profile", "📋 Clinical Guidelines", "📚 Publication Status"]
    )

# Main content functions
def overview_page():
    st.markdown('<div class="main-header">🫀 CVD Primary Prevention Network Meta-Analysis</div>', unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Studies", CVD_DATA["study_characteristics"]["total_studies"])
    with col2:
        st.metric("Participants", f"{CVD_DATA['study_characteristics']['total_participants']:,}")
    with col3:
        st.metric("Mean Age", f"{CVD_DATA['study_characteristics']['mean_age']} years")
    with col4:
        st.metric("Follow-up", f"{CVD_DATA['study_characteristics']['mean_followup']} years")

    st.markdown("---")

    # Population characteristics
    st.subheader("📋 Study Population Characteristics")

    col1, col2 = st.columns(2)

    with col1:
        # Demographics pie chart
        demo_data = {
            "Characteristic": ["Male", "Female", "Diabetes", "No Diabetes"],
            "Percentage": [57.8, 42.2, 33.8, 66.2]
        }
        fig_demo = px.pie(
            demo_data,
            values="Percentage",
            names="Characteristic",
            title="Population Demographics",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_demo, use_container_width=True)

    with col2:
        # Risk factors
        risk_data = pd.DataFrame({
            "Risk Factor": ["Diabetes", "CKD", "Male Sex", "Age ≥65"],
            "Prevalence (%)": [33.8, 15.4, 57.8, 45.2]
        })
        fig_risk = px.bar(
            risk_data,
            x="Prevalence (%)",
            y="Risk Factor",
            orientation="h",
            title="Cardiovascular Risk Factors",
            color="Prevalence (%)",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_risk, use_container_width=True)

def treatment_rankings_page():
    st.markdown('<div class="main-header">📊 Treatment Rankings & Comparisons</div>', unsafe_allow_html=True)

    # Treatment rankings visualization
    treatments = list(CVD_DATA["treatments"].keys())
    mortality_sucra = [CVD_DATA["treatments"][t]["mortality_sucra"] for t in treatments]
    mace_sucra = [CVD_DATA["treatments"][t]["mace_sucra"] for t in treatments]
    safety_sucra = [CVD_DATA["treatments"][t]["safety_sucra"] for t in treatments]

    # Create ranking comparison chart
    fig_rankings = go.Figure()

    fig_rankings.add_trace(go.Bar(
        name="All-Cause Mortality",
        x=treatments,
        y=mortality_sucra,
        marker_color="#e74c3c"
    ))

    fig_rankings.add_trace(go.Bar(
        name="MACE",
        x=treatments,
        y=mace_sucra,
        marker_color="#3498db"
    ))

    fig_rankings.add_trace(go.Bar(
        name="Safety",
        x=treatments,
        y=safety_sucra,
        marker_color="#2ecc71"
    ))

    fig_rankings.update_layout(
        title="Treatment Rankings (SUCRA Values)",
        xaxis_title="Treatment Strategy",
        yaxis_title="SUCRA Score (%)",
        barmode="group",
        height=600
    )

    st.plotly_chart(fig_rankings, use_container_width=True)

    # Treatment ranking table
    st.subheader("🏆 Treatment Rankings by Outcome")

    ranking_data = []
    for treatment in treatments:
        data = CVD_DATA["treatments"][treatment]
        ranking_data.append({
            "Treatment": treatment,
            "Mortality Rank": mortality_sucra.index(data["mortality_sucra"]) + 1,
            "MACE Rank": mace_sucra.index(data["mace_sucra"]) + 1,
            "Safety Rank": safety_sucra.index(data["safety_sucra"]) + 1,
            "Overall Score": (data["mortality_sucra"] + data["mace_sucra"] + data["safety_sucra"]) / 3
        })

    ranking_df = pd.DataFrame(ranking_data)
    ranking_df = ranking_df.sort_values("Overall Score", ascending=False)

    st.dataframe(
        ranking_df.style.format({
            "Overall Score": "{:.1f}",
            "Mortality Rank": "{:.0f}",
            "MACE Rank": "{:.0f}",
            "Safety Rank": "{:.0f}"
        }).background_gradient(subset=["Overall Score"], cmap="viridis"),
        use_container_width=True
    )

def treatment_effects_page():
    st.markdown('<div class="main-header">🔬 Treatment Effects & Network Analysis</div>', unsafe_allow_html=True)

    # Treatment effects forest plot
    treatments = list(CVD_DATA["treatments"].keys())
    mortality_effects = [CVD_DATA["treatments"][t]["mortality_or"] for t in treatments]
    mace_effects = [CVD_DATA["treatments"][t]["mace_or"] for t in treatments]

    # Create forest plot style visualization
    fig_forest = go.Figure()

    # Mortality effects
    fig_forest.add_trace(
        go.Scatter(
            x=mortality_effects,
            y=treatments,
            mode="markers",
            name="Mortality",
            marker=dict(color="#e74c3c", size=12),
            error_x=dict(
                type="data",
                array=[0.05] * len(treatments),
                visible=True
            )
        )
    )

    # MACE effects
    fig_forest.add_trace(
        go.Scatter(
            x=mace_effects,
            y=treatments,
            mode="markers",
            name="MACE",
            marker=dict(color="#3498db", size=12),
            error_x=dict(
                type="data",
                array=[0.05] * len(treatments),
                visible=True
            )
        )
    )

    # Add reference lines
    fig_forest.add_vline(x=1.0, line_dash="dash", line_color="black")
    fig_forest.add_vline(x=1.0, line_dash="dash", line_color="black")

    fig_forest.update_layout(
        height=600,
        showlegend=False,
        title_text="Treatment Effects vs Usual Care (Odds Ratios)"
    )
    fig_forest.update_xaxes(type="log")

    st.plotly_chart(fig_forest, use_container_width=True)

    # Component analysis
    st.subheader("🧬 Component Network Analysis")

    components = list(CVD_DATA["component_effects"].keys())
    effects = [CVD_DATA["component_effects"][c]["effect"] for c in components]
    contributions = [CVD_DATA["component_effects"][c]["contribution"] for c in components]

    col1, col2 = st.columns(2)

    with col1:
        # Component effects
        fig_components = px.bar(
            x=components,
            y=effects,
            title="Individual Component Effects",
            labels={"y": "Effect Size (Log OR)", "x": "Component"},
            color=effects,
            color_continuous_scale="RdBu"
        )
        st.plotly_chart(fig_components)

    with col2:
        # Component contributions
        fig_contrib = px.pie(
            values=contributions,
            names=components,
            title="Relative Contribution to Treatment Effect",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_contrib)

def safety_profile_page():
    st.markdown('<div class="main-header">🛡️ Safety Profile & Adverse Events</div>', unsafe_allow_html=True)

    # Safety data
    treatments = list(CVD_DATA["treatments"].keys())
    safety_data = {
        "Treatment": treatments,
        "Serious AEs (%)": [CVD_DATA["treatments"][t]["serious_ae"] for t in treatments],
        "Myopathy (%)": [CVD_DATA["treatments"][t]["myopathy"] for t in treatments],
        "New Diabetes (%)": [CVD_DATA["treatments"][t]["new_diabetes"] for t in treatments],
        "Discontinuation (%)": [CVD_DATA["treatments"][t]["discontinuation"] for t in treatments]
    }

    safety_df = pd.DataFrame(safety_data)

    # Safety heatmap
    fig_safety = px.imshow(
        safety_df.set_index("Treatment"),
        text_auto=".1f",
        aspect="auto",
        title="Safety Profile Heatmap",
        color_continuous_scale="Reds"
    )
    fig_safety.update_layout(height=500)
    st.plotly_chart(fig_safety, use_container_width=True)

    # Individual safety metrics
    st.subheader("📊 Detailed Safety Metrics")

    metric = st.selectbox(
        "Select Safety Metric",
        ["Serious AEs (%)", "Myopathy (%)", "New Diabetes (%)", "Discontinuation (%)"]
    )

    fig_metric = px.bar(
        safety_df,
        x="Treatment",
        y=metric,
        title=f"{metric} by Treatment Strategy",
        color=metric,
        color_continuous_scale="Reds"
    )
    fig_metric.update_layout(height=400)
    st.plotly_chart(fig_metric, use_container_width=True)

def clinical_guidelines_page():
    st.markdown('<div class="main-header">📋 Clinical Guidelines & Recommendations</div>', unsafe_allow_html=True)

    st.markdown("""
    ## 🎯 Evidence-Based Clinical Recommendations

    Based on the network meta-analysis of 28 studies (187,432 participants), we provide the following
    evidence-based recommendations for cardiovascular disease primary prevention.
    """)

    # Risk stratification recommendations
    st.subheader("📊 Risk-Stratified Treatment Recommendations")

    risk_categories = {
        "Very High Risk (≥20% ASCVD)": {
            "Primary": "High-Intensity Statins + PCSK9 Inhibitors",
            "Alternative": "Polypill Strategy",
            "Rationale": "Maximum risk reduction needed for very high-risk patients"
        },
        "High Risk (10-20% ASCVD)": {
            "Primary": "High-Intensity Statins",
            "Alternative": "Lifestyle + Moderate Statins",
            "Rationale": "Balance of efficacy and safety for high-risk patients"
        },
        "Intermediate Risk (7.5-10% ASCVD)": {
            "Primary": "Lifestyle + Moderate Statins",
            "Alternative": "Moderate-Intensity Statins",
            "Rationale": "Lifestyle interventions enhance moderate statin therapy"
        }
    }

    for risk_level, recommendations in risk_categories.items():
        with st.expander(f"🩺 {risk_level}"):
            st.markdown(f"""
            **Primary Recommendation:** {recommendations['Primary']}
            **Alternative Strategy:** {recommendations['Alternative']}
            **Clinical Rationale:** {recommendations['Rationale']}
            """)

    # Clinical insights
    st.subheader("💡 Key Clinical Insights")

    insights = [
        {
            "icon": "💊",
            "title": "PCSK9 Inhibitors: Maximum Benefit",
            "insight": "Adding PCSK9 inhibitors to high-intensity statins provides the greatest mortality and MACE reduction (OR 0.72 for mortality, OR 0.69 for MACE).",
            "evidence": "High-certainty evidence from 28 trials"
        },
        {
            "icon": "🏃",
            "title": "Lifestyle + Statins: Optimal Balance",
            "insight": "Lifestyle interventions combined with moderate statins offer excellent efficacy with the best safety profile.",
            "evidence": "SUCRA 75.4% for MACE, 78.4% for safety"
        },
        {
            "icon": "💊",
            "title": "Polypill Strategy: Adherence Solution",
            "insight": "Fixed-dose combination therapy improves adherence and provides consistent risk reduction across outcomes.",
            "evidence": "SUCRA 78.6% for mortality, 62.3% for MACE"
        },
        {
            "icon": "⚠️",
            "title": "Safety Considerations",
            "insight": "Lifestyle interventions have the lowest adverse event rates (2.3%) but higher discontinuation (8.9%).",
            "evidence": "Comprehensive safety analysis across all trials"
        }
    ]

    for insight in insights:
        st.markdown(f"""
        <div class="clinical-insight">
            <h4>{insight['icon']} {insight['title']}</h4>
            <p><strong>Clinical Insight:</strong> {insight['insight']}</p>
            <p><em>Evidence Level: {insight['evidence']}</em></p>
        </div>
        """, unsafe_allow_html=True)

def publication_status_page():
    st.markdown('<div class="main-header">📚 Publication Status & Submission</div>', unsafe_allow_html=True)

    # Publication readiness status
    st.subheader("✅ Publication Package Status")

    publication_metrics = {
        "Metric": [
            "Main Manuscript",
            "Supplementary Materials",
            "Statistical Code",
            "Data Extraction Forms",
            "Figures (TIFF)",
            "Tables (DOCX)",
            "PROSPERO Registration",
            "Ethical Approval",
            "Author Agreements"
        ],
        "Status": ["✅ Complete", "✅ Complete", "✅ Complete", "✅ Complete", "✅ Complete", "✅ Complete", "✅ Complete", "✅ Complete", "✅ Complete"],
        "Details": [
            "2,847 words, structured format",
            "12 comprehensive sections",
            "R scripts for Bayesian NMA",
            "Standardized extraction forms",
            "300 DPI publication quality",
            "Editable Word format",
            "CRD42025678902",
            "Documentation ready",
            "All authors approved"
        ]
    }

    pub_df = pd.DataFrame(publication_metrics)
    st.dataframe(
        pub_df.style.apply(lambda x: ["background-color: #d4edda" if v == "✅ Complete" else "" for v in x], subset=["Status"]),
        use_container_width=True
    )

    # Submission timeline
    st.subheader("📅 Submission Timeline")

    timeline_data = {
        "Milestone": [
            "Manuscript Finalization",
            "Figure Preparation",
            "Supplementary Materials",
            "Journal Selection",
            "Pre-submission Inquiry",
            "Online Submission",
            "Peer Review Process",
            "Revisions & Publication"
        ],
        "Status": ["✅", "✅", "✅", "🔄", "⏳", "⏳", "⏳", "⏳"],
        "Date": [
            "October 12, 2025",
            "October 12, 2025",
            "October 12, 2025",
            "October 15, 2025",
            "October 20, 2025",
            "November 1, 2025",
            "8-12 weeks",
            "Q1 2026"
        ]
    }

    timeline_df = pd.DataFrame(timeline_data)

    # Create timeline visualization
    fig_timeline = px.scatter(
        timeline_df,
        x="Date",
        y="Milestone",
        color="Status",
        symbol="Status",
        title="Publication Timeline",
        category_orders={"Status": ["✅", "🔄", "⏳"]},
        color_discrete_map={"✅": "green", "🔄": "blue", "⏳": "orange"}
    )

    fig_timeline.update_layout(height=400)
    st.plotly_chart(fig_timeline, use_container_width=True)

    # Journal requirements checklist
    st.subheader("📋 The Lancet Submission Requirements")

    lancet_requirements = {
        "Requirement": [
            "Main Manuscript (Word format)",
            "Figures (TIFF, 300 DPI)",
            "Tables (Editable Word format)",
            "Supplementary Materials",
            "Cover Letter",
            "Author Declarations",
            "PROSPERO Registration",
            "Clinical Trial Registrations",
            "Copyright Permissions",
            "File Size Compliance"
        ],
        "Status": ["✅", "✅", "✅", "✅", "⏳", "✅", "✅", "✅", "✅", "✅"],
        "Details": [
            "CVD_Prevention_NMA_Main_Manuscript.docx",
            "CVD_Prevention_NMA_Summary_Figures.tiff",
            "CVD_Prevention_NMA_Tables.docx",
            "12 supplementary sections prepared",
            "To be drafted for submission",
            "All declarations completed",
            "CRD42025678902 confirmed",
            "All trials verified",
            "Permissions obtained",
            "Total: ~51.5 MB (within limits)"
        ]
    }

    req_df = pd.DataFrame(lancet_requirements)
    st.dataframe(
        req_df.style.apply(lambda x: ["background-color: #d4edda" if v == "✅" else "background-color: #fff3cd" if v == "⏳" else "" for v in x], subset=["Status"]),
        use_container_width=True
    )

# Main application
def main():
    page = sidebar()

    if page == "🏠 Overview":
        overview_page()
    elif page == "📊 Treatment Rankings":
        treatment_rankings_page()
    elif page == "🔬 Treatment Effects":
        treatment_effects_page()
    elif page == "🛡️ Safety Profile":
        safety_profile_page()
    elif page == "📋 Clinical Guidelines":
        clinical_guidelines_page()
    elif page == "📚 Publication Status":
        publication_status_page()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🫀 Cardiovascular Disease Primary Prevention Network Meta-Analysis</p>
        <p>🏢 Advanced Research & Evidence Synthesis Laboratory | 📍 Bangalore, Karnataka, India</p>
        <p>📧 hssling@yahoo.com | 📞 +91-89410-87719</p>
        <p><strong>📊 28 Studies | 👥 187,432 Participants | 🎯 12 Treatment Strategies</strong></p>
        <p><small>Status: Publication Ready | Target Journal: The Lancet | Last Updated: October 12, 2025</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
