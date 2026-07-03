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

# ==============================================================================
# SECTION 4: DATA ENGINE, FILTERING, INDICES AND CHART GENERATION
# ==============================================================================

# Execute loading mechanics and apply core time window crops
# Convert the dataframe index to explicit pandas datetime elements to fix the crash
    df.index = pd.to_datetime(df.index)

# Apply the structural time window slice using standard timestamp values 
filtered_df = df[(df.index >= pd.Timestamp(start_date)) & (df.index <= pd.Timestamp(end_date))].copy() 

# Ensure the database layer returned viable data rows before proceeding 
if not filtered_df.empty: 
    # 1. Capture the raw starting price/value base points on day one of selected window 
    mag7_base_value = filtered_df["Mag7_Total"].iloc[0] 
    hedge7_base_value = filtered_df["Hedge7_Total"].iloc[0] 
    
    # 2. Re-calculate the dynamically normalized Base-100 column vectors 
    # This divides each date's aggregate value by the base price and roots at 100 
    filtered_df["Mag7_Indexed"] = (filtered_df["Mag7_Total"] / mag7_base_value) * 100 
    filtered_df["Hedge7_Indexed"] = (filtered_df["Hedge7_Total"] / hedge7_base_value) * 100 
else: 
    # Bulletproof fallback arrays to prevent layout breakage if window crops empty 
    filtered_df["Mag7_Indexed"] = 100.0 
    filtered_df["Hedge7_Indexed"] = 100.0 

# Build the interactive structural macro comparison chart with Plotly 
fig = go.Figure() 

# Plot Line A: The Magnificent 7 Portfolio Vector (The Foxes) 
fig.add_trace( 
    go.Scatter( 
        x=filtered_df.index, 
        y=filtered_df["Mag7_Indexed"], 
        name="The Magnificent 7 (Foxes)", 
        line=dict(color="#FF4B4B", width=2.5), 
        hovertemplate="%{y:.2f}" 
    ) 
) 

# Plot Line B: The Hedgehog 7 Portfolio Vector (The Hedgehogs) 
fig.add_trace( 
    go.Scatter( 
        x=filtered_df.index, 
        y=filtered_df["Hedge7_Indexed"], 
        name="The Hedgehog 7 (Hedgehogs)", 
        line=dict(color="#1F77B4", width=2.5), 
        hovertemplate="%{y:.2f}" 
    ) 
) 

# Inject structural layout formatting to enforce an institutional style grid 
fig.update_layout( 
    xaxis_title="Timeline Multi-Year Horizon", 
    yaxis_title="Cumulative Growth Index (Base 100)", 
    hovermode="x unified", 
    margin=dict(l=0, r=0, t=10, b=0), 
    legend=dict( 
        orientation="h", 
        yanchor="bottom", 
        y=1.02, 
        xanchor="right", 
        x=1 
    ), 
    template="plotly_white" 
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
    # Note: Beta metrics are wrapped as strings to lock in flush-left layout alignment
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
                    "Beta Risk": st.column_config.TextColumn(help="Systematic Market Risk Coefficient") 
                } 
            )
