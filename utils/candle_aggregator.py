import pandas as pd

df = pd.read_csv("data/coins_market_data.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

df = df.sort_values(["coin_int_id", "timestamp"])

df["volume_diff"] = df.groupby("coin_int_id")["total_volumes"].diff()
df["volume_diff"] = df["volume_diff"].abs()

agg = (
    df
    .groupby("coin_int_id")
    .resample("4h", on="timestamp")
    .agg({
        "price": "ohlc",
        "volume_diff": "sum"
    })
    .reset_index()
    .sort_values(["coin_int_id", "timestamp"])
    .rename(columns={"volume_diff": "volume"})
)

print(agg)