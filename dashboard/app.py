# ============================================================
#   🏭 End-to-End Supply Chain Analytics Dashboard
#   Author: Duong Quy Vu (Dave)
#   Description:
#       Interactive Python Streamlit dashboard for simulation-based
#       performance and scenario analytics across a multi-echelon
#       supply chain network.
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------------
# 0️⃣ Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Supply Chain Simulation Dashboard",
    page_icon="🏭",
    layout="wide"
)
st.title("🏭 End-to-End Supply Chain Simulation Dashboard")
st.caption("Built entirely in Python – powered by Streamlit, Pandas, and Matplotlib")

# ----------------------------
# 1️⃣ Load Data
# ----------------------------
data_dir = Path("../data/processed")

@st.cache_data
def load_data():
    try:
        shipments = pd.read_csv(data_dir / "shipments_simulated.csv")
        demand = pd.read_csv(data_dir / "demand_simulated.csv")
        lanes = pd.read_csv(data_dir / "lanes_generated.csv")
        whatif = pd.read_csv(data_dir / "whatif_comparison.csv")
    except FileNotFoundError as e:
        st.error(f"Missing data file: {e}")
        st.stop()
    return shipments, demand, lanes, whatif

shipments, demand, lanes, whatif = load_data()

# ----------------------------
# 2️⃣ Sidebar Controls
# ----------------------------
st.sidebar.header("⚙️ Control Panel")

scenario = st.sidebar.selectbox(
    "Select Scenario",
    options=["Baseline", "LowReliability_HighFuel"],
    index=0
)

show_trend = st.sidebar.checkbox("Show weekly performance trend", value=True)
show_tradeoff = st.sidebar.checkbox("Show cost vs reliability chart", value=True)
show_table = st.sidebar.checkbox("Show detailed table", value=True)

st.sidebar.markdown("---")
st.sidebar.write("Data source: simulation outputs (Steps 5–7)")
st.sidebar.info("All computations are generated dynamically from CSV outputs.")

# ----------------------------
# 3️⃣ KPI Calculation Functions
# ----------------------------
def compute_kpis(df):
    kpis = {
        "avg_lead_days": df["realized_lead_days"].mean(),
        "on_time_rate": df["delivered_on_time"].mean() * 100,
        "total_cost": df["transport_cost"].sum()
    }
    return kpis

baseline_kpi = compute_kpis(shipments)
if scenario == "Baseline":
    scenario_kpi = baseline_kpi
else:
    scenario_kpi = {
        "avg_lead_days": whatif.loc[whatif.metric=="avg_lead_days","scenario"].values[0],
        "on_time_rate": whatif.loc[whatif.metric=="on_time_rate","scenario"].values[0],
        "total_cost": whatif.loc[whatif.metric=="total_cost","scenario"].values[0]
    }

# ----------------------------
# 4️⃣ KPI Display Section
# ----------------------------
st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

lead_delta = scenario_kpi["avg_lead_days"] - baseline_kpi["avg_lead_days"]
otd_delta = scenario_kpi["on_time_rate"] - baseline_kpi["on_time_rate"]
cost_delta = scenario_kpi["total_cost"] - baseline_kpi["total_cost"]

col1.metric("Average Lead Time (days)", f"{scenario_kpi['avg_lead_days']:.2f}", f"{lead_delta:+.2f}")
col2.metric("On-Time Delivery (%)", f"{scenario_kpi['on_time_rate']:.2f}%", f"{otd_delta:+.2f}%")
col3.metric("Total Transport Cost (AUD)", f"${scenario_kpi['total_cost']:,.0f}", f"${cost_delta:,.0f}")

st.markdown("---")

# ----------------------------
# 5️⃣ Weekly Trend Visualization
# ----------------------------
if show_trend:
    st.subheader("📈 Weekly Operational Trends")
    weekly = shipments.groupby("week").agg({
        "realized_lead_days": "mean",
        "delivered_on_time": "mean"
    }).reset_index()
    weekly["delivered_on_time"] *= 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,4))
    ax1.plot(weekly["week"], weekly["delivered_on_time"], marker="o", color="tab:blue")
    ax1.set_title("On-Time Delivery % by Week")
    ax1.set_xlabel("Week")
    ax1.set_ylabel("OTD %")

    ax2.plot(weekly["week"], weekly["realized_lead_days"], marker="o", color="tab:orange")
    ax2.set_title("Average Lead Time by Week")
    ax2.set_xlabel("Week")
    ax2.set_ylabel("Days")

    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# ----------------------------
# 6️⃣ Cost vs Reliability Trade-Off
# ----------------------------
if show_tradeoff:
    st.subheader("⚖️ Cost vs Reliability Scatter Plot")

    fig2, ax3 = plt.subplots(figsize=(8,5))
    scatter = ax3.scatter(
        shipments["realized_lead_days"],
        shipments["transport_cost"],
        c=shipments["delivered_on_time"],
        cmap="coolwarm",
        alpha=0.7,
        edgecolor="k"
    )
    plt.colorbar(scatter, ax=ax3, label="Delivered On-Time (1=True)")
    ax3.set_xlabel("Lead Time (days)")
    ax3.set_ylabel("Transport Cost (AUD)")
    ax3.set_title("Cost vs Lead Time (colored by reliability)")
    st.pyplot(fig2)

st.markdown("---")

# ----------------------------
# 7️⃣ Scenario Comparison Table
# ----------------------------
if show_table:
    st.subheader("🧾 What-If Scenario Comparison")
    comparison = whatif.copy()
    comparison["impact_%"] = ((comparison["scenario"] - comparison["baseline"]) / comparison["baseline"]) * 100
    st.dataframe(comparison.round(2))

    st.download_button(
        "📥 Download What-If Results (CSV)",
        data=comparison.to_csv(index=False).encode("utf-8"),
        file_name="whatif_comparison.csv",
        mime="text/csv"
    )

# ----------------------------
# 8️⃣ Business Interpretation
# ----------------------------
st.markdown("---")
st.subheader("💡 Insight & Business Interpretation")
st.markdown("""
When supplier reliability drops from **0.93 → 0.85** and fuel surcharge increases by **+15%**, 
average lead time increases by **~10%**, on-time delivery rate declines by **~9.6%**, 
and total logistics cost rises by **~15%**.  

This highlights the **trade-off between cost efficiency and service reliability**.  
Such insights support **data-driven sourcing and transportation planning decisions**, 
helping supply chain managers balance risk, cost, and service level.
""")

st.markdown("📌 *Dashboard powered by Streamlit + Matplotlib + Pandas*")