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
st.caption("Testing the Magnificent 7 against a low-volatility, dividend-compounding alternative index.")

# ---------------------------------------------------------
# 2. USER INTERFACE & SIDEBAR NAVIGATION CONTROLS
# ---------------------------------------------------------
st.sidebar.header("Model Parameters")

# A. Build structural parameters for the non-linear investment slider
low_range = list(range(100, 1000, 100))          # Micro scaling [$100 to $900]
high_range = list(range(1000, 101000, 1000))     # Macro scaling [$1,000 to $100,000]
custom_investment_steps = low_range + high_range  # Comprehensive array mapping

# B. Render index slider control mapping to our non-linear value list
selected_index = st.sidebar.slider(
    label="Initial Investment Amount ($):",
    min_value=0,
    max_value=len(custom_investment_steps) - 1,
    value=9,  # Default selection index pointing straight to $1,000
    step=1
)

# Extract working numeric scalar for math computations
initial_investment = custom_investment_steps[selected_index]
st.sidebar.markdown(f"**Principal Capital Baseline:** ${initial_investment:,.0f}")

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

# Execute mathematical base transformation normalization to dynamic investment principal
filtered_df["Mag7_Indexed"] = (filtered_df["Mag7_Raw"] / baseline_row["Mag7_Raw"]) * initial_investment
filtered_df["Hedgehog7_Indexed"] = (filtered_df["Hedge7_Raw"] / baseline_row["Hedge7_Raw"]) * initial_investment
filtered_df["SP500_Indexed"] = (filtered_df["SP500_Raw"] / baseline_row["SP500_Raw"]) * initial_investment

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
    yaxis="y2"  # Explicit layout configuration directive assignment
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
        showgrid=False  # Clean output separation grid elimination
    ),
    hovermode="x unified",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Pipe graphic object into the active layout framework surface
st.plotly_chart(fig, use_container_width=True)
