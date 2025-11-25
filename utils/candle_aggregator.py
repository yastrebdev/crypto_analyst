import pandas as pd

hours = "4h"

df = pd.read_csv("data/coins_market_data.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

df = df.sort_values(["coin_id", "timestamp"])

df["volume_diff"] = df.groupby("coin_id")["total_volumes"].diff()
df["volume_diff"] = df["volume_diff"].abs()

agg = (
    df
    .groupby("coin_id")
    .resample(hours, on="timestamp")
    .agg({
        "price": "ohlc",
        "volume_diff": "sum"
    })
    .reset_index()
    .sort_values(["coin_id", "timestamp"])
    .rename(columns={"volume_diff": "volume"})
)

agg.columns = [
    col[1] if isinstance(col, tuple) and col[1] else col[0] if isinstance(col, tuple) else col
    for col in agg.columns
]

if "volume_diff" in agg.columns:
    agg = agg.rename(columns={"volume_diff": "volume"})

agg.to_csv(f"data/candles_{hours}.csv", index=False)