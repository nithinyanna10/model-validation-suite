import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys

# 🔧 Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.black_scholes import BlackScholesModel
from models.monte_carlo_xva import MonteCarloXVA

# -------------------- Page Setup --------------------
st.set_page_config(page_title="Model Validation Dashboard", layout="wide")
st.title("📊 Model Validation Dashboard")

# -------------------- Load Market Data --------------------
VOL_PATH = "data/vol_surface.csv"
YIELD_PATH = "data/yield_curve.csv"

@st.cache_data
def load_vol_surface():
    if os.path.exists(VOL_PATH):
        return pd.read_csv(VOL_PATH, index_col=0)
    else:
        st.error("Volatility surface not found.")
        return pd.DataFrame()

@st.cache_data
def load_yield_curve():
    if os.path.exists(YIELD_PATH):
        return pd.read_csv(YIELD_PATH)
    else:
        st.error("Yield curve not found.")
        return pd.DataFrame()

vol_surface = load_vol_surface()
yield_curve = load_yield_curve()

# -------------------- Tabs --------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🟡 Volatility Surface",
    "📉 Yield Curve",
    "💵 Black-Scholes Pricing",
    "📉 Greeks",
    "📊 Expected Exposure"
])

# -------------------- Tab 1: Volatility Surface --------------------
with tab1:
    st.subheader("Volatility Surface")
    if not vol_surface.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(vol_surface, cmap="viridis", xticklabels=5, yticklabels=5, ax=ax)
        plt.title("Implied Volatility Surface")
        plt.xlabel("Strike")
        plt.ylabel("Maturity (Years)")
        st.pyplot(fig)
    else:
        st.warning("Volatility surface data not available.")

# -------------------- Tab 2: Yield Curve --------------------
with tab2:
    st.subheader("Yield Curve")
    if not yield_curve.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(yield_curve["Term"], yield_curve["Rate"], marker='o')
        plt.title("Simulated Yield Curve")
        plt.xlabel("Term (Years)")
        plt.ylabel("Rate")
        plt.grid(True)
        st.pyplot(fig)
    else:
        st.warning("Yield curve data not available.")

# -------------------- Tab 3: Black-Scholes Pricing --------------------
with tab3:
    st.subheader("Black-Scholes Pricing Visualizer")

    col1, col2, col3 = st.columns(3)
    with col1:
        spot = st.number_input("Spot Price (S₀)", 50.0, 200.0, 100.0, key="spot_price")
    with col2:
        rate = st.number_input("Risk-Free Rate (r)", 0.0, 0.2, 0.05, key="risk_free_rate")
    with col3:
        option_type = st.selectbox("Option Type", ["call", "put"], key="option_type")

    strike = st.slider("Strike (K)", 50.0, 150.0, 100.0, key="strike_slider")
    maturity = st.slider("Maturity (T in years)", 0.1, 5.0, 1.0, key="maturity_slider")
    volatility = st.slider("Volatility (σ)", 0.01, 1.0, 0.2, key="bs_vol_slider")

    model = BlackScholesModel(spot, strike, maturity, rate, volatility, option_type)
    price = model.price()

    st.metric(label=f"💵 {option_type.capitalize()} Price", value=f"${price:.2f}")

# -------------------- Tab 4: Greeks Viewer --------------------
with tab4:
    st.subheader("Greeks vs Strike")

    greek_strikes = np.linspace(50, 150, 50)
    greek_values = {"delta": [], "gamma": [], "vega": [], "theta": [], "rho": []}

    for k in greek_strikes:
        m = BlackScholesModel(spot, k, maturity, rate, volatility, option_type)
        greeks = m.greeks()
        for g in greek_values:
            greek_values[g].append(greeks[g])

    fig, ax = plt.subplots(figsize=(10, 4))
    for g, values in greek_values.items():
        ax.plot(greek_strikes, values, label=g)
    ax.set_title("Greeks vs Strike")
    ax.set_xlabel("Strike")
    ax.set_ylabel("Greek Value")
    ax.legend()
    st.pyplot(fig)

# -------------------- Tab 5: Monte Carlo Exposure --------------------
with tab5:
    st.subheader("Expected Exposure (Monte Carlo)")

    col1, col2, col3 = st.columns(3)
    with col1:
        mc_sigma = st.slider("Volatility (σ)", 0.01, 1.0, 0.2, key="mc_vol_slider")
    with col2:
        mc_paths = st.slider("Paths", 100, 2000, 500, step=100, key="mc_paths_slider")
    with col3:
        mc_steps = st.slider("Steps", 10, 100, 30, key="mc_steps_slider")

    mc_model = MonteCarloXVA(S0=spot, r=rate, sigma=mc_sigma, T=maturity, steps=mc_steps, paths=mc_paths)
    exposure = mc_model.expected_exposure()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(np.linspace(0, maturity, mc_steps + 1), exposure)
    ax.set_title("Expected Exposure Over Time")
    ax.set_xlabel("Time (Years)")
    ax.set_ylabel("Exposure ($)")
    st.pyplot(fig)
