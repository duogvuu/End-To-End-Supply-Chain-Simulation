import numpy as np
import pandas as pd
import yaml
from pathlib import Path

# --- Load config ---
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

weeks = cfg["time"]["weeks"]
params = cfg["demand"]
n_retailers = cfg["network"]["retailers"]
n_skus = cfg["network"]["skus"]

# --- Function to generate demand ---
def generate_weekly_demand(base, weeks, seasonality_amp, trend_per_year, noise_sd, promo_weeks, uplift_pct):
    t = np.arange(weeks)
    seasonality = 1 + seasonality_amp * np.sin(2 * np.pi * t / 52)
    trend = 1 + trend_per_year * (t / 52)
    noise = np.random.normal(0, noise_sd, size=weeks)
    demand = base * seasonality * trend * (1 + noise)
    demand = np.clip(demand, 0, None)

    # Add promotion uplift
    promo_mask = np.zeros(weeks)
    promo_indices = np.random.choice(weeks, size=promo_weeks, replace=False)
    promo_mask[promo_indices] = 1 + uplift_pct
    demand = demand * (1 + (promo_mask - 1))

    return pd.DataFrame({"week": np.arange(1, weeks + 1), "demand_units": demand})


# --- Generate full dataset ---
rows = []
for r in range(n_retailers):
    for s in range(n_skus):
        base = np.random.randint(params["base_range_per_sku"][0], params["base_range_per_sku"][1])
        df = generate_weekly_demand(
            base=base,
            weeks=weeks,
            seasonality_amp=params["seasonality_amp_pct"],
            trend_per_year=params["trend_pct_per_year"],
            noise_sd=params["noise_sd_pct"],
            promo_weeks=params["promo"]["weeks_per_store"],
            uplift_pct=params["promo"]["uplift_pct"],
        )
        df["retailer_id"] = f"RET_{r+1}"
        df["sku_id"] = f"SKU_{s+1}"
        rows.append(df)

final_df = pd.concat(rows, ignore_index=True)

# --- Save output ---
output_path = Path("data/processed/demand_simulated.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
final_df.to_csv(output_path, index=False)

print(f"✅ Demand simulation dataset saved to {output_path}")