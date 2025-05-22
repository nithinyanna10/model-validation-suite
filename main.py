import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fix relative imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils.report_generator import generate_validation_report, fig_to_base64

# -------------------- Load Data --------------------
vol_surface_path = "data/vol_surface.csv"
yield_curve_path = "data/yield_curve.csv"

if not os.path.exists(vol_surface_path) or not os.path.exists(yield_curve_path):
    raise FileNotFoundError("Required data files not found in /data")

vol_surface = pd.read_csv(vol_surface_path, index_col=0)
yield_curve = pd.read_csv(yield_curve_path)

# -------------------- Simulated Input Parameters --------------------
spot = 100
strike = 100
rate = 0.05
volatility = 0.2
maturity = 1
option_type = "call"
mc_paths = 500
mc_steps = 30
exposure = np.linspace(0, 50, mc_steps + 1)  # Fake data for now

# -------------------- Generate Plots and Convert to Base64 --------------------
plots = {}

# Volatility Surface
fig1, ax1 = plt.subplots()
sns.heatmap(vol_surface, ax=ax1, cmap="viridis")
ax1.set_title("Volatility Surface")
plots["Volatility Surface"] = fig_to_base64(fig1)

# Yield Curve
fig2, ax2 = plt.subplots()
ax2.plot(yield_curve["Term"], yield_curve["Rate"], marker="o")
ax2.set_title("Yield Curve")
plots["Yield Curve"] = fig_to_base64(fig2)

# Expected Exposure
fig3, ax3 = plt.subplots()
ax3.plot(np.linspace(0, maturity, mc_steps + 1), exposure)
ax3.set_title("Expected Exposure")
plots["Expected Exposure"] = fig_to_base64(fig3)

# Greeks (simulated for now)
greek_strikes = np.linspace(50, 150, 50)
fig4, ax4 = plt.subplots()
for greek in ["delta", "gamma", "vega"]:
    ax4.plot(greek_strikes, np.random.rand(50), label=greek)
ax4.set_title("Greeks")
ax4.legend()
plots["Greeks"] = fig_to_base64(fig4)

# -------------------- Generate Report --------------------
config = {
    "Spot": spot,
    "Strike": strike,
    "Rate": rate,
    "Volatility": volatility,
    "Maturity": maturity,
    "Option Type": option_type,
    "Paths": mc_paths,
    "Steps": mc_steps
}

generate_validation_report({"config": config, "plots": plots})
print("✅ Report generated in /reports")
