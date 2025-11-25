import requests
import pandas as pd
import time

from settings import Setting
from config.coins import Coins
from utils.coins_id_parser import id_parser

coins = Coins()

symbols = coins.get_symbol_list()
names = coins.get_name_list()

settings = Setting()

url = f"{settings.BASE_COINS_API_URL}{settings.COINS_MARKET_CHART}"

ids = id_parser(symbols, names)

df_coins_ids = pd.DataFrame({
    "coin_int_id": range(1, len(ids) + 1),
    "coin_api_id": ids
}).reset_index()


def get_market_data():
    dfs = []

    for count, id_ in enumerate(ids, start=1):
        try:
            response = requests.get(
                url.format(
                    id=  id_,
                    currency = "usd",
                    days = 10,
                    precision = 2
                )
            )
            response.raise_for_status()
            data = response.json()

            df_prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
            df_volumes = pd.DataFrame(data["total_volumes"], columns=["timestamp", "total_volumes"])

            df_coin = pd.concat([df_prices.set_index("timestamp"),
                                 df_volumes.set_index("timestamp")["total_volumes"]],
                                axis=1).reset_index()

            df_coin["coin_int_id"] = count
            dfs.append(df_coin)

        except Exception as e:
            print(f"Error for id {id_}: {e}")
        else:
            print(f"Processed id: {id_} ({count}/{len(ids)})")

        time.sleep(20)

    return pd.concat(dfs, ignore_index=True)


market_data = get_market_data()

market_data.to_csv("data/coins_market_data.csv", index=False)
# df_coins_ids.to_csv("data/coins_ids.csv", index=False)

print(market_data.head())
# print(df_coins_ids.head())