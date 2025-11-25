import pandas as pd


def id_parser(symbols, names):
    df = pd.read_csv("data/coins_list.csv")
    df["symbol"] = df["symbol"].str.lower()
    df["name"] = df["name"].str.lower()

    filtered = df[df["symbol"].isin(symbols) & df["name"].isin(names)]

    list_ids = filtered["id"].tolist()

    return list_ids