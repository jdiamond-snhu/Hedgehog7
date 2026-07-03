import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as ui_chart

# ---------------------------------------------------------
# 1. APP SETUP & CONTEXT
# ---------------------------------------------------------
st.set_page_config(page_title="The Hedgehog 7 Sandbox", layout="wide")
st.title("🦊 Foxes vs. 🦔 Hedgehogs: Macro Regime Performance Sandbox")
st.caption("Testing the Magnificent 7 against a low-volatility, dividend-compounding alternative.")

# ---------------------------------------------------------
# 2. SIDEBAR USER INTERFACES
# ---------------------------------------------------------
st.sidebar.header("Model Controls")

# Create a non-linear list of options using a list comprehension
low_range = list(range(100, 1000, 100))          # [$100, $200 ... $900]
high_range = list(range(1000, 101000, 1000))     # [$1000, $2000 ... $100000]
custom_investment_steps = low_range + high_range  # Total of 109 steps

# Render a slider that maps to the index positions of our custom list
selected_index = st.sidebar.slider(
    label="Initial Investment Amount ($):",
    min_value=0,
    max_value=len(custom_investment_steps) - 1,
    value=9,  # Defaults to index 9, which is exactly $1,000
    step=1
)

# Extract the actual dollar value chosen by the user
initial_investment = custom_investment_steps[selected_index]

# Display the cleanly formatted dollar selection to the user
st.sidebar.markdown(f"**Principal Capital:** ${initial_investment:,.0f}")

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
# 3. MOCK DATA INGESTION ENGINE (Replace with your CSV/API data)
# ---------------------------------------------------------
@st.cache_data
def load_historical_macro_data():
    # Creating a dummy date range for structural testing
    dates = pd.date_range(start="2010-01-01", end="2025-12-31", freq="M")
    
    # ---------------------------------------------------------
# MATH: THE DYNAMIC RE-INDEXING MATRIX
# ---------------------------------------------------------
# Pulling the first available row in our filtered slice to serve as our index base
baseline_row = filtered_df.iloc[0]

# Normalize stock tracking arrays to start at the user's custom principal amount
filtered_df["Mag7_Indexed"] = (filtered_df["Mag7_Raw"] / baseline_row["Mag7_Raw"]) * initial_investment
filtered_df["Hedge7_Indexed"] = (filtered_df["Hedge7_Raw"] / baseline_row["Hedge7_Raw"]) * initial_investment

    
    # Simulating Fed Interest Rate cycle
fed_rate_sim = np.sin(np.linspace(0, 10, len(dates))) * 2.25 + 2.5
    
    df = pd.DataFrame({
        "Date": dates,
        "Mag7_Avg": mag7_sim,
        "Hedge7_Avg": hedge7_sim,
        "Fed_Rate": fed_rate_sim
    })
    df.set_index("Date", inplace=True)
    return df

# Fetch and filter dataset based on your sidebar slider choices
raw_data = load_historical_macro_data()
filtered_df = raw_data.loc[f"{start_year}":f"{end_year}"]

# ---------------------------------------------------------
# 4. MULTI-AXIS CHART GRAPHICS (Plotly Engine)
# ---------------------------------------------------------
fig = ui_chart.Figure()

# Line 1: Mag 7 Asset Line (Purple)
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index, 
    y=filtered_df["Mag7_Avg"],
    name="Magnificent 7 Avg (Foxes)",
    line=dict(color="purple", width=3)
))

# Line 2: Hedgehog 7 Asset Line (Orange)
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index, 
    y=filtered_df["Hedge7_Avg"],
    name="Hedgehog 7 Avg (Hedgehogs)",
    line=dict(color="orange", width=3)
))

# Line 3: Federal Funds Rate (Thin, Solid Green) mapped to a secondary Y-axis
fig.add_trace(ui_chart.Scatter(
    x=filtered_df.index, 
    y=filtered_df["Fed_Rate"],
    name="Fed Funds Rate (%)",
    line=dict(color="green", width=1.5, dash="solid"),
    yaxis="y2" 
))

# Configure layout properties to visually support dual y-axes
fig.update_layout(
    title="Relative Asset Price Movement vs. Macro Rate Environment",
        title=f"Growth of ${initial_investment:,.0f} Investment (Starting Jan {start_year}) vs. Fed Interest Rate Policy",
    xaxis=dict(title="Timeline"),
    yaxis=dict(title=f"Portfolio Growth Value ($)"),

    yaxis2=dict(
        title="Fed Funds Rate (%)",
        overlaying="y",
        side="right",
        range=[0, 6] # Lock macro rate display space
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
    template="plotly_white"
)

# Render output element directly inside core layout view
st.plotly_chart(fig, use_container_width=True)

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
