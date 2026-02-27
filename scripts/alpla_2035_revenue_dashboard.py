"""
ALPLA 2035 Revenue Projection Dashboard
Interactive tool for modeling regional revenue growth across 11-year horizon

Usage:
    streamlit run alpla_2035_revenue_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="ALPLA 2035 Revenue Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 ALPLA 2035 Revenue Projection Dashboard")
st.markdown("**Strategic revenue forecasting by region (2024-2035) with interactive scenario modeling**")
st.divider()

# ============================================================================
# DATA INITIALIZATION
# ============================================================================

# 2024 Baseline Revenue (€M)
BASELINE_2024 = {
    "Europe": 2200,
    "Asia-Pacific": 740,
    "South America": 980,
    "North America": 740,
    "Africa/Middle East": 240,
}

# Default CAGR by Region (%)
DEFAULT_CAGR = {
    "Europe": 2.5,
    "Asia-Pacific": 8.5,
    "South America": 6.5,
    "North America": 4.5,
    "Africa/Middle East": 8.0,
}

# Scenario Presets
SCENARIOS = {
    "Conservative": {
        "Europe": 2.0,
        "Asia-Pacific": 7.0,
        "South America": 5.0,
        "North America": 3.5,
        "Africa/Middle East": 6.0,
        "description": "Low growth across regions; regulatory compliance costs; competitive pressure increases"
    },
    "Base Case": {
        "Europe": 2.5,
        "Asia-Pacific": 8.5,
        "South America": 6.5,
        "North America": 4.5,
        "Africa/Middle East": 8.0,
        "description": "Sustainable Mix strategy succeeds; Asia-Pacific & Africa grow; Europe stable"
    },
    "Optimistic": {
        "Europe": 3.5,
        "Asia-Pacific": 10.0,
        "South America": 7.5,
        "North America": 5.5,
        "Africa/Middle East": 9.5,
        "description": "Scenario B outperformance; early-mover advantage in emerging markets; premium pricing"
    },
}

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================

st.sidebar.header("⚙️ Projection Controls")

# Scenario Selector
scenario_choice = st.sidebar.radio(
    "📍 Select Growth Scenario",
    options=list(SCENARIOS.keys()),
    help="Choose a predefined scenario or customize below"
)

st.sidebar.info(SCENARIOS[scenario_choice]["description"])

# Customize CAGRs
st.sidebar.subheader("Adjust Regional CAGR (%)")
st.sidebar.markdown("*Override scenario defaults if needed*")

custom_cagr = {}
for region in BASELINE_2024.keys():
    scenario_val = SCENARIOS[scenario_choice][region]
    custom_cagr[region] = st.sidebar.slider(
        f"{region}",
        min_value=0.0,
        max_value=15.0,
        value=scenario_val,
        step=0.5,
        key=f"cagr_{region}"
    )

st.sidebar.divider()

# Projection Range
st.sidebar.subheader("⏱️ Projection Period")
start_year = st.sidebar.number_input("Start Year", value=2024, min_value=2024, max_value=2025)
end_year = st.sidebar.number_input("End Year", value=2035, min_value=2026, max_value=2045)

st.sidebar.divider()

# Show assumptions
st.sidebar.subheader("📋 Current Assumptions")
for region, cagr in custom_cagr.items():
    st.sidebar.caption(f"**{region}**: {cagr:.1f}% CAGR")

total_2024 = sum(BASELINE_2024.values())
st.sidebar.metric("2024 Total Revenue", f"€{total_2024:,.0f}M")

# ============================================================================
# CALCULATION ENGINE
# ============================================================================

def project_revenue(baseline, cagr, start_year, end_year):
    """Project revenue for a region across years using CAGR"""
    years = np.arange(start_year, end_year + 1)
    years_offset = years - start_year
    projected = baseline * ((1 + cagr/100) ** years_offset)
    return dict(zip(years, projected))

# Calculate projections for all regions
projections = {}
for region, baseline_val in BASELINE_2024.items():
    projections[region] = project_revenue(
        baseline_val,
        custom_cagr[region],
        start_year,
        end_year
    )

# Build projection dataframe
years_list = list(range(start_year, end_year + 1))
df_projection = pd.DataFrame(projections)
df_projection.index = years_list
df_projection.index.name = "Year"

# ============================================================================
# KEY METRICS
# ============================================================================

col1, col2, col3, col4, col5 = st.columns(5)

total_2024 = df_projection.iloc[0].sum()
total_end = df_projection.iloc[-1].sum()
cagr_total = ((total_end / total_2024) ** (1 / (end_year - start_year)) - 1) * 100
growth_absolute = total_end - total_2024
growth_pct = ((total_end - total_2024) / total_2024) * 100

with col1:
    st.metric("2024 Total", f"€{total_2024:,.0f}M")

with col2:
    st.metric(f"{end_year} Total", f"€{total_end:,.0f}M", f"+€{growth_absolute:,.0f}M")

with col3:
    st.metric("Total Growth %", f"+{growth_pct:.1f}%")

with col4:
    st.metric("CAGR (Total)", f"{cagr_total:.2f}%")

with col5:
    st.metric("Years", f"{end_year - start_year}")

st.divider()

# ============================================================================
# VISUALIZATIONS
# ============================================================================

# 1. STACKED AREA CHART (Revenue over time by region)
st.subheader("📈 Revenue Trajectory by Region (2024-2035)")

fig_area = go.Figure()

colors = {
    "Europe": "#1f77b4",
    "Asia-Pacific": "#ff7f0e",
    "South America": "#2ca02c",
    "North America": "#d62728",
    "Africa/Middle East": "#9467bd",
}

for region in BASELINE_2024.keys():
    fig_area.add_trace(go.Scatter(
        x=df_projection.index,
        y=df_projection[region],
        name=region,
        mode='lines',
        stackgroup='one',
        fillcolor=colors[region],
        line=dict(width=0.5, color=colors[region]),
        hovertemplate=f"<b>{region}</b><br>Year: %{{x}}<br>Revenue: €%{{y:,.0f}}M<extra></extra>"
    ))

fig_area.update_layout(
    hovermode='x unified',
    xaxis_title="Year",
    yaxis_title="Revenue (€M)",
    height=450,
    template="plotly_white",
    font=dict(size=11)
)

st.plotly_chart(fig_area, use_container_width=True)

# ============================================================================

# 2. 2035 BREAKDOWN (Pie Chart)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🥧 2035 Revenue Breakdown by Region")

    final_year_data = df_projection.iloc[-1]

    fig_pie = go.Figure(data=[go.Pie(
        labels=final_year_data.index,
        values=final_year_data.values,
        marker=dict(colors=[colors[region] for region in final_year_data.index]),
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Revenue: €%{value:,.0f}M<br>Share: %{percent}<extra></extra>'
    )])

    fig_pie.update_layout(
        height=400,
        template="plotly_white",
        font=dict(size=10)
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# ============================================================================

with col_right:
    st.subheader("📊 Year-over-Year Growth Rates")

    # Calculate YoY growth for each region
    growth_rates = df_projection.pct_change() * 100

    # Latest year growth
    latest_growth = growth_rates.iloc[-1].sort_values(ascending=False)

    fig_bar = go.Figure(data=[
        go.Bar(
            x=latest_growth.index,
            y=latest_growth.values,
            marker=dict(color=[colors[r] for r in latest_growth.index]),
            text=[f"{v:.1f}%" for v in latest_growth.values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Growth: %{y:.1f}%<extra></extra>'
        )
    ])

    fig_bar.update_layout(
        title=f"YoY Growth Rate in {end_year}",
        xaxis_title="Region",
        yaxis_title="Growth Rate (%)",
        height=400,
        template="plotly_white",
        showlegend=False,
        font=dict(size=10)
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# ============================================================================

# 3. DETAILED PROJECTION TABLE
st.subheader("📋 Detailed Revenue Projections (€M)")

# Format for display
df_display = df_projection.copy()
for col in df_display.columns:
    df_display[col] = df_display[col].apply(lambda x: f"€{x:,.0f}")

# Add totals column
df_display['TOTAL'] = df_projection.sum(axis=1).apply(lambda x: f"€{x:,.0f}")

st.dataframe(df_display, use_container_width=True)

# ============================================================================

# 4. REGION COMPARISON & CAGR
st.subheader("🔍 Regional Performance Summary")

summary_data = []
for region in BASELINE_2024.keys():
    val_2024 = BASELINE_2024[region]
    val_end = df_projection[region].iloc[-1]
    region_growth = ((val_end / val_2024) ** (1 / (end_year - start_year)) - 1) * 100

    summary_data.append({
        "Region": region,
        "2024 Revenue": f"€{val_2024:,.0f}M",
        "2035 Revenue": f"€{val_end:,.0f}M",
        "Absolute Growth": f"€{val_end - val_2024:,.0f}M",
        "Growth %": f"+{((val_end - val_2024) / val_2024 * 100):.1f}%",
        "CAGR": f"{region_growth:.2f}%",
        "Target CAGR": f"{custom_cagr[region]:.1f}%"
    })

df_summary = pd.DataFrame(summary_data)
st.dataframe(df_summary, use_container_width=True, hide_index=True)

# ============================================================================

# 5. SENSITIVITY ANALYSIS
st.subheader("⚡ Sensitivity Analysis: CAGR Impact on 2035 Revenue")

st.markdown("*Adjust CAGR sliders below to see 2035 impact*")

sens_cols = st.columns(5)
sens_results = {}

for idx, (region, col) in enumerate(zip(BASELINE_2024.keys(), sens_cols)):
    with col:
        baseline = BASELINE_2024[region]
        current_cagr = custom_cagr[region]

        # Project with current CAGR
        revenue_2035 = baseline * ((1 + current_cagr/100) ** (end_year - start_year))

        # Calculate sensitivity: +/- 1% CAGR
        revenue_cagr_plus = baseline * ((1 + (current_cagr + 1)/100) ** (end_year - start_year))
        revenue_cagr_minus = baseline * ((1 + (current_cagr - 1)/100) ** (end_year - start_year))

        st.metric(
            region,
            f"€{revenue_2035:,.0f}M",
            f"±€{(revenue_cagr_plus - revenue_2035):,.0f}M per 1% CAGR"
        )

# ============================================================================

# 6. SCENARIO COMPARISON
st.divider()
st.subheader("🎯 Scenario Comparison")

scenario_comparison = []
for scenario_name, scenario_cagrs in SCENARIOS.items():
    total_2035 = 0
    for region, baseline in BASELINE_2024.items():
        cagr = scenario_cagrs[region]
        rev_2035 = baseline * ((1 + cagr/100) ** (end_year - start_year))
        total_2035 += rev_2035

    total_2024 = sum(BASELINE_2024.values())
    total_growth = total_2035 - total_2024
    total_growth_pct = (total_growth / total_2024) * 100
    scenario_cagr = ((total_2035 / total_2024) ** (1 / (end_year - start_year)) - 1) * 100

    scenario_comparison.append({
        "Scenario": scenario_name,
        "2035 Total": f"€{total_2035:,.0f}M",
        "Absolute Growth": f"€{total_growth:,.0f}M",
        "Growth %": f"+{total_growth_pct:.1f}%",
        "Implied CAGR": f"{scenario_cagr:.2f}%"
    })

df_scenarios = pd.DataFrame(scenario_comparison)
st.dataframe(df_scenarios, use_container_width=True, hide_index=True)

# ============================================================================

# 7. REGIONAL GROWTH TRENDS
st.divider()
st.subheader("📊 Regional CAGR Ranking")

region_ranking = []
for region in BASELINE_2024.keys():
    region_ranking.append({
        "Region": region,
        "CAGR": custom_cagr[region],
        "2024": BASELINE_2024[region],
        "2035": df_projection[region].iloc[-1]
    })

df_ranking = pd.DataFrame(region_ranking).sort_values("CAGR", ascending=False)

fig_rank = go.Figure(data=[
    go.Bar(
        x=df_ranking["Region"],
        y=df_ranking["CAGR"],
        marker=dict(color=[colors[r] for r in df_ranking["Region"]]),
        text=[f"{v:.1f}%" for v in df_ranking["CAGR"]],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>CAGR: %{y:.1f}%<extra></extra>'
    )
])

fig_rank.update_layout(
    title="Regional CAGR Rankings (Current Scenario)",
    xaxis_title="Region",
    yaxis_title="CAGR (%)",
    height=350,
    template="plotly_white",
    showlegend=False,
    font=dict(size=11)
)

st.plotly_chart(fig_rank, use_container_width=True)

# ============================================================================

# FOOTER
st.divider()
st.caption(
    "**Data Sources:** Alpla Official Reports (2024), SOCM Strategic Analysis, Regional Growth Assumptions | "
    "**Last Updated:** January 2026 | **Methodology:** Compound Annual Growth Rate (CAGR) projections"
)

# Download option
st.subheader("💾 Export Data")

csv_buffer = df_projection.to_csv()
st.download_button(
    label="📥 Download Projections as CSV",
    data=csv_buffer,
    file_name=f"alpla_2035_revenue_projections_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)
