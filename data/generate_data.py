"""
Generate synthetic vendor order data for the Vendor Consistency Predictor demo.

Usage:
    python data/generate_data.py

Output:
    data/vendor_orders.csv
"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)

N_ORDERS = 10_000
N_VENDORS = 200

# Vendor-level characteristics (some vendors are consistently slower)
vendor_base_delay = {vid: round(np.random.exponential(3.0), 2) for vid in range(1, N_VENDORS + 1)}

# Hour-of-day probability distribution (peaks at lunch & dinner)
HOUR_PROBS = np.array([
    0.01, 0.005, 0.005, 0.005, 0.005, 0.01, 0.02, 0.03,   # 0-7
    0.04, 0.04, 0.05, 0.07, 0.09, 0.07, 0.05, 0.04,        # 8-15
    0.05, 0.06, 0.08, 0.09, 0.07, 0.05, 0.03, 0.02          # 16-23
])
HOUR_PROBS = HOUR_PROBS / HOUR_PROBS.sum()  # normalize to sum to 1

PEAK_HOURS = {12, 13, 18, 19, 20, 21}

records = []
for _ in range(N_ORDERS):
    vendor_id = np.random.randint(1, N_VENDORS + 1)
    order_hour = int(np.random.choice(range(24), p=HOUR_PROBS))
    day_of_week = np.random.randint(0, 7)
    item_count = np.random.randint(1, 12)
    is_peak_hour = 1 if order_hour in PEAK_HOURS else 0
    historical_delay_avg = max(0, vendor_base_delay[vendor_id] + np.random.normal(0, 1))

    # Realistic target with known dependencies
    prep_time = (
        8.0                                           # base prep time
        + item_count * 1.8                            # per-item cost
        + is_peak_hour * np.random.uniform(2, 6)      # rush hour penalty
        + historical_delay_avg * 0.7                  # vendor reliability
        + (1 if day_of_week >= 5 else 0) * 2.5        # weekend surge
        + np.random.normal(0, 3)                      # noise
    )
    prep_time = max(3.0, prep_time)

    records.append({
        "vendor_id": vendor_id,
        "order_hour": order_hour,
        "day_of_week": day_of_week,
        "item_count": item_count,
        "is_peak_hour": is_peak_hour,
        "historical_delay_avg": round(historical_delay_avg, 2),
        "prep_time_minutes": round(prep_time, 2),
    })

df = pd.DataFrame(records)

# Save
out_path = os.path.join(os.path.dirname(__file__), "vendor_orders.csv")
df.to_csv(out_path, index=False)

print(f"Generated {len(df):,} orders across {df['vendor_id'].nunique()} vendors")
print(f"Saved to: {out_path}")
print(f"\nSample stats:")
print(df.describe().round(2))
