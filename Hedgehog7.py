import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as ui_chart

# ---------------------------------------------------------
# 1. APP SETUP & CONTEXT
# ---------------------------------------------------------
st.set_page_config(page_title="The Hedgehog 7 Sandbox", layout="wide")
st.title("🦊 Foxes vs. 🦔 Hedgehogs: Macro Regime Performance Sandbox")
st.caption("Testing the Magnificent 7 against a low-volatility, dividend-compounding alternative index.")

# ---------------------------------------------------------
# 2. SIDEBAR USER INTERFACES (Timeline Filter Only)
# ---------------------------------------------------------
st.sidebar.header("Model Controls")
st.sidebar.markdown("Adjust the macro multi-year horizon to evaluate backtest performance.")

# Timeline selection slider
start_year, end_year = st.sidebar.slider(
    label="Adjust Macro Observation Window:",
    min_value=2010,
    max_value=2026,
    value=(2016, 2026),
    step=1
)
st.sidebar.markdown(f"**Current Window:** Jan 1, {start_year} to Dec 31, {end_year}")

# ---------------------------------------------------------
# 3. FIXED MOCK DATA INGESTION ENGINE
# ---------------------------------------------------------
@st.cache_data
def load_historical_macro_data():
    # Creating a clean historical timeline base
    dates = pd.date_range(start="2010-01-01", end="2025-12-31", freq="ME")
    
    # Simulating data curves to mimic market profiles
    np.random.seed(42)
    mag7_sim = 100 * np.exp(np.cumsum(np.random.normal(0.018, 0.06, len(dates))))
    hedge7_sim = 100 * np.exp(np.cumsum(np.random.normal(0.012, 0.03, len(dates))))
    sp500_sim = 100 * np.exp(np.cumsum(np.random.normal(0.014, 0.04, len(dates)))) # S&P 500 Baseline Curve
    
    # Simulating Fed Interest Rate cycles
    fed_rate_sim = np.sin(np.linspace(0, 10, len(dates))) * 2.25 + 2.5
    
    df = pd.DataFrame({
        "Mag7_Raw": mag7_sim,
        "Hedge7_Raw": hedge7_sim,
        "SP500_Raw": sp500_sim,
        "Fed_Rate": fed_rate_sim
    }, index=dates)
    
    df.index.name = "Date"
    return df

# Fetch and isolate dataset rows based on sidebar timeline parameters
raw_data = load_historical_macro_data()
filtered_df = raw_data.loc[f"{start_year}":f"{end_year}"].copy()

# ---------------------------------------------------------
# 4. DATA ENGINE: BASE 100 NORMALIZATION MATH
# ---------------------------------------------------------
if not filtered_df.empty:
    # Capture the raw starting price values on day one of the window
    baseline_row = filtered_df.iloc[0]
    
    # Force baseline metrics to normalize and anchor cleanly at 100.0
    filtered_df["Mag7_Indexed"] = (filtered_df["Mag7_Raw"] / baseline_row["Mag7_Raw"]) * 100
    filtered_df["Hedge7_Indexed"] = (filtered_df["Hedge7_Raw"] / baseline_row["Hedge7_Raw"]) * 100
    filtered_df["SP500_Indexed"] = (filtered_df["SP500_Raw"] / baseline_row["SP500_Raw"]) * 100
else:
    filtered_df["Mag7_Indexed"] = 100.0
    filtered_df["Hedge7_Indexed"] = 100.0
    filtered_df["SP500_Indexed"] = 100.0

# ---------------------------------------------------------
# 5. MULTI-AXIS CHART GRAPHICS (Plotly Engine)
# ---------------------------------------------------------
fig = ui_chart.Figure()

# Line 1: Mag 7 Asset Line (Red)
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index,
    y=filtered_df["Mag7_Indexed"],
    name="The Magnificent 7 (Foxes)",
    line=dict(color="#FF4B4B", width=3),
    hovertemplate="%{y:.2f}"
))

# Line 2: Hedgehog 7 Asset Line (Blue)
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index,
    y=filtered_df["Hedge7_Indexed"],
    name="The Hedgehog 7 (Hedgehogs)",
    line=dict(color="#1F77B4", width=3),
    hovertemplate="%{y:.2f}"
))

# NEW Line 3: S&P 500 Index Benchmark (Thin, Solid Black)
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index,
    y=filtered_df["SP500_Indexed"],
    name="S&P 500 Index Benchmark",
    line=dict(color="#000000", width=1.5, dash="solid"),
    hovertemplate="%{y:.2f}"
))

# Line 4: Federal Funds Rate (Thin, DASHED Green) mapped to secondary Y-axis
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index,
    y=filtered_df["Fed_Rate"],
    name="Fed Funds Rate (%)",
    line=dict(color="green", width=1.5, dash="dash"), # Updated styling to dash
    yaxis="y2",
    hovertemplate="%{y:.2f}%"
))

# Configure layout properties to visually support dual y-axes
fig.update_layout(
    title=f"Cumulative Growth Index (Base 100) vs. Fed Interest Rate Policy Horizon",
    xaxis=dict(title="Timeline Horizon"),
    yaxis=dict(title="Cumulative Growth Index (Base 100)"),
    yaxis2=dict(
        title="Fed Funds Rate (%)",
        overlaying="y",
        side="right",
        range=[0, 6]
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
    template="plotly_white",
    margin=dict(l=0, r=0, t=50, b=0)
)

# ---------------------------------------------------------
# 6. INSTITUTIONAL 3P CO-LOCATION LAYOUT MATRIX
# ---------------------------------------------------------
# Establish layout boundaries (75% width to keep layout neat and crisp)
left_chart_column, right_buffer_column = st.columns([0.75, 0.25])

with left_chart_column:
    # Render main index plot
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    
    # Split width into side-by-side equal column layout containers
    box_col1, box_col2 = st.columns(2)
    
    # Constructing clean dataframes with string-enforced Beta parameters
    mag7_data = pd.DataFrame({
        "Ticker": ["NVDA", "MSFT", "AAPL", "AMZN", "META", "GOOGL", "TSLA"],
        "Asset Name": ["NVIDIA Corp.", "Microsoft Corp.", "Apple Inc.", "Amazon.com Inc.", "Meta Platforms", "Alphabet Inc.", "Tesla Inc."],
        "Asset Classification": ["Semiconductors", "Systems Software", "Tech Hardware", "Broadline Retail", "Interactive Media", "Interactive Media", "Automobile Mfrs"],
        "Beta Risk": ["1.68", "1.11", "1.04", "1.16", "1.21", "1.03", "1.73"]
    })
    
    hedge7_data = pd.DataFrame({
        "Ticker": ["AVGO", "LLY", "MCD", "JNJ", "BRK.B", "V", "COST"],
        "Asset Name": ["Broadcom Inc.", "Eli Lilly & Co.", "McDonald's Corp.", "Johnson & Johnson", "Berkshire Hathaway", "Visa Inc.", "Costco Wholesale"],
        "Asset Classification": ["Semiconductors", "Pharmaceuticals", "Restaurants/Leisure", "Pharmaceuticals", "Multi-Sector Value", "Transaction/Payments", "Consumer Merchandise"],
        "Beta Risk": ["1.14", "0.42", "0.64", "0.53", "0.81", "0.94", "0.75"]
    })

    # Box A: The Magnificent 7 Container Box
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
                    "Beta Risk": st.column_config.TextColumn(help="Systematic Market Risk Coefficient")
                }
            )

    # Box B: The Hedgehog 7 Container Box
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
                    "Beta Risk": st.column_config.TextColumn(help="Systematic Market Risk Coefficient")
                }
            )
