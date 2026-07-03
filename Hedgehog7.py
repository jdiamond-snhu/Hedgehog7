import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date

# ==============================================================================
# SECTION 1: GLOBAL UI SETTINGS & APP HEADER
# ==============================================================================
st.set_page_config(layout="wide", page_title="The Hedgehog 7 Dashboard")

st.title("🦔 The Hedgehog 7 Portfolio Matrix")
st.markdown("""
This institutional sandbox evaluates the structural performance of a low-beta, 
high-free-cash-flow alternative index against the concentrated weight of the 
traditional Magnificent 7 mega-caps across changing macroeconomic interest regimes.
""")

# ==============================================================================
# SECTION 2: THE DATA INGESTION ENGINE
# ==============================================================================
@st.cache_data
def load_portfolio_data():
    # Load your historical stock array file
    df = pd.read_csv("https://raw.githubusercontent.com/jdiamond-snhu/Hedgehog7/refs/heads/main/Hedgehog7_Data.csv")
    
    # Standardize the date tracking column right at the ingestion layer
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
    else:
        df.index = pd.to_datetime(df.index)
        
    return df

# Initialize the data frame globally under 'df' to prevent naming conflicts
df = load_portfolio_data()

# Establish baseline absolute calendar boundaries from your source file
min_date = df.index.min().date()
max_date = df.index.max().date()

# ==============================================================================
# SECTION 3: SIDEBAR CONTROL CENTER (DATE-WINDOW INTERACTION ONLY)
# ==============================================================================
st.sidebar.header("🕹️ Strategy Parameters")
st.sidebar.markdown("Adjust the macro multi-year horizon to evaluate backtest performance.")

# The single, unified date window slider control
start_date, end_date = st.sidebar.slider(
    "Select Evaluation Window:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_value),
    format="YYYY-MM-DD"
)

# ==============================================================================
# SECTION 4: DATA ENGINE, FILTERING, INDICES AND CHART GENERATION
# ==============================================================================
# Convert sidebar selections into clean timestamp matching formats
start_ts = pd.Timestamp(start_date)
end_ts = pd.Timestamp(end_date)

# Execute the structural time window slice cleanly
filtered_df = df[(df.index >= start_ts) & (df.index <= end_ts)].copy()

# Ensure the database layer returned viable data rows before proceeding
if not filtered_df.empty:
    # 1. Capture the raw starting baseline points on day one of selected window
    mag7_base_value = filtered_df["Mag7_Total"].iloc[0]
    hedge7_base_value = filtered_df["Hedge7_Total"].iloc[0]
    
    # 2. Re-calculate the dynamically normalized Base-100 column vectors 
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

# ==============================================================================
# SECTION 5: INSTITUTIONAL HORIZONTAL CONTAINER BOXES
# ==============================================================================
# 1. Establish the main 75% left boundary to match the chart width
left_chart_column, right_buffer_column = st.columns([0.75, 0.25])

with left_chart_column:
    # Render the performance index plot inside the left column space
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---") # Visual separator line under the chart
    
    # 2. Split the space into two equal side-by-side layout columns for the data tables
    box_col1, box_col2 = st.columns(2)
    
    # --- PORTFOLIO MATRIX DATA ASSETS ---
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

    # Box A: The Magnificent 7 (Foxes Table)
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

    # Box B: The Hedgehog 7 (Hedgehogs Table)
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
