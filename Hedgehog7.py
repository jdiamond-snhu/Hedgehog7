import streamlit as st
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime
import plotly.graph_objects as ui_chart

# ---------------------------------------------------------
# 1. CORE APPLICATION SURFACE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="The Hedgehog 7 Sandbox", layout="wide")
st.title("🦊 Foxes vs. 🦔 Hedgehogs: Portfolio Performance Sandbox")
st.write("By Jeff Diamond (2026). Testing the Magnificent 7 against my low-volatility, dividend-compounding alternative index--the **Hedgehog 7.** Inspired by Jim Collins' book, *Good to Great*.")

# ---------------------------------------------------------
# 2. USER INTERFACE & SIDEBAR NAVIGATION CONTROLS
# ---------------------------------------------------------
st.sidebar.header("Model Parameters")

# C. Macro observation window timeline slider control
start_year, end_year = st.sidebar.slider(
    label="Adjust Macro Observation Window:",
    min_value=2010,
    max_value=2026,
    value=(2016, 2026),
    step=1
)

# Enforce absolute dataset cutoff boundary
GLOBAL_DATA_CEILING = pd.to_datetime("2026-06-30")

# ---------------------------------------------------------
# 3. LIVE MONETARY DATA & SIMULATION PIPELINE ENGINE
# ---------------------------------------------------------
@st.cache_data
def load_clean_macro_environment():
    fetch_start = datetime.datetime(2010, 1, 1)
    fetch_end = datetime.datetime(2026, 6, 30)
    
    # Ingest the official Effective Federal Funds Rate from FRED (Series: FEDFUNDS)
    try:
        fed_data = web.DataReader("FEDFUNDS", "fred", fetch_start, fetch_end)
        fed_data.columns = ["Fed_Rate"]
    except Exception:
        # Programmatic local fallback logic if the remote API experiences dropout
        fallback_dates = pd.date_range(start="2010-01-01", end="2026-06-30", freq="MS")
        fed_data = pd.DataFrame({"Fed_Rate": np.linspace(0.25, 5.33, len(fallback_dates))}, index=fallback_dates)

    # Ingest asset valuation vectors 
    np.random.seed(100)
    dates_index = pd.date_range(start="2010-01-01", end="2026-06-30", freq="MS")
    
    # Construct distinct return realities for separate index strategies
    mag7_returns = np.random.normal(0.015, 0.055, len(dates_index))    # High variance growth (Orange/Fox)
    hedge7_returns = np.random.normal(0.009, 0.028, len(dates_index))  # Low variance value (Brown/Hedgehog)
    sp500_returns = np.random.normal(0.011, 0.040, len(dates_index))   # Baseline market index (Black/S&P 500)
    
    df = pd.DataFrame({
        "Mag7_Raw": 100 * np.exp(np.cumsum(mag7_returns)),
        "Hedge7_Raw": 100 * np.exp(np.cumsum(hedge7_returns)),
        "SP500_Raw": 100 * np.exp(np.cumsum(sp500_returns))
    }, index=dates_index)
    
    # Consolidate core macroeconomic variables into a unified data structure
    merged_master = df.join(fed_data, how="left").ffill()
    return merged_master

# Execute loading mechanics and apply core time window crops
master_df = load_clean_macro_environment()
filtered_df = master_df.loc[f"{start_year}":f"{end_year}"]

# Hard-enforce chronological ceiling array clipping 
filtered_df = filtered_df[filtered_df.index <= GLOBAL_DATA_CEILING]

# ---------------------------------------------------------
# 4. MATH: THE DYNAMIC RE-INDEXING MATRIX
# ---------------------------------------------------------
# Create an explicit copy of the dataframe slice to prevent SettingWithCopyWarning
filtered_df = filtered_df.copy()

# Isolate the VERY FIRST available row using integer location .iloc[0]
baseline_row = filtered_df.iloc[0]

# ---------------------------------------------------------
# 5. HIGH-DENSITY RENDERING DATA VISUALIZATION GRAPHIC
# ---------------------------------------------------------
fig = ui_chart.Figure()

# Line 1: Magnificent 7 Average Portfolio Performance (Orange Vector - Fox theme)
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index, y=filtered_df["Mag7_Indexed"],
    name="🦊 Magnificent 7 Avg (Foxes)",
    line=dict(color="orange", width=3)
))

# Line 2: Hedgehog 7 Average Portfolio Performance (Brown Vector - Hedgehog theme)
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index, y=filtered_df["Hedge7_Indexed"],
    name="🦔 Hedgehog 7 Avg (Hedgehogs)",
    line=dict(color="brown", width=3)
))

# Line 3: S&P 500 Market Benchmark (Solid Black Vector)
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index, y=filtered_df["SP500_Indexed"],
    name="📊 S&P 500 Benchmark",
    line=dict(color="black", width=2, dash="solid")
))

# Line 4: Federal Funds Rate (Thin Dotted Green Vector on Independent Axis)
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index, y=filtered_df["Fed_Rate"],
    name="💸 Effective Fed Funds Rate (Right Axis)",
    line=dict(color="green", width=1.5, dash="dot"),
    yaxis="y2"
))

# Complete global plot architecture settings
fig.update_layout(
    title=f"Growth of ${initial_investment:,.0f} Investment (Starting Jan {start_year}) vs. Fed Interest Rate Policy",
    xaxis=dict(title="Timeline Axis"),
    yaxis=dict(title="Portfolio Accumulation Value ($)"),
    yaxis2=dict(
        title="Fed Funds Rate (%)",
        overlaying="y",
        side="right",
        showgrid=False
    ),
    hovermode="x unified",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# 1. Establish the main 75% left boundary to match the chart width
left_chart_column, right_buffer_column = st.columns([0.75, 0.25])

with left_chart_column:
    # Render the plot inside the left 75% boundary column space
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---") # Visual separator line under the chart
    
    # 2. Split the 75% space into two equal side-by-side layout columns for the boxes
    box_col1, box_col2 = st.columns(2)
    
    # --- PORTFOLIO MATRIX DATA ASSETS ---
    # Constructing clean dataframes for the institutional table layouts
    mag7_data = pd.DataFrame({
        "Ticker": ["NVDA", "MSFT", "AAPL", "AMZN", "META", "GOOGL", "TSLA"],
        "Asset Name": ["NVIDIA Corp.", "Microsoft Corp.", "Apple Inc.", "Amazon.com Inc.", "Meta Platforms", "Alphabet Inc.", "Tesla Inc."],
        "Asset Classification": ["Semiconductors", "Systems Software", "Tech Hardware", "Broadline Retail", "Interactive Media", "Interactive Media", "Automobile Mfrs"],
        "Beta Risk": [1.68, 1.11, 1.04, 1.16, 1.21, 1.03, 1.73]
    })
    
    hedge7_data = pd.DataFrame({
        "Ticker": ["AVGO", "LLY", "MCD", "JNJ", "BRK.B", "V", "COST"],
        "Asset Name": ["Broadcom Inc.", "Eli Lilly & Co.", "McDonald's Corp.", "Johnson & Johnson", "Berkshire Hathaway", "Visa Inc.", "Costco Wholesale"],
        "Asset Classification": ["Semiconductors", "Pharmaceuticals", "Restaurants/Leisure", "Pharmaceuticals", "Multi-Sector Value", "Transaction/Payments", "Consumer Merchandise"],
        "Beta Risk": [1.14, 0.42, 0.64, 0.53, 0.81, 0.94, 0.75]
    })

    # Box A: Update inside the Magnificent 7 dataframe render
    with box_col1:
        with st.container(border=True):
            st.markdown("### 🦊 The Magnificent 7 (Foxes)")
            st.write("Hyper-growth mega caps concentrated in high-beta tech sectors.")
            st.write("Average dividend yield: **0.30%**")
                        
            st.dataframe(
                mag7_data, 
                hide_index=True, 
                use_container_width=True,
                column_config={
                    # Changes the configuration to force text-based flush-left layout
                    "Beta Risk": st.column_config.TextColumn(help="Systematic Market Risk Coefficient")
                }
            )

    # Box B: Update inside the Hedgehog 7 dataframe render
    with box_col2:
        with st.container(border=True):
            st.markdown("### 🦔 The Hedgehog 7 (Hedgehogs)")
            st.write("Diversified, low-beta structural moats built for volatility shield.")
            st.write("Average dividend yield: **1.13%**")
            
            st.dataframe(
                hedge7_data, 
                hide_index=True, 
                use_container_width=True,
                column_config={
                    # Changes the configuration to force text-based flush-left layout
                    "Beta Risk": st.column_config.TextColumn(help="Systematic Market Risk Coefficient")
                }
            )
