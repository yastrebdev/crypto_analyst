import time
from dotenv import load_dotenv
import os

import pandas as pd
import requests

from settings import Setting

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

EVERYTHING, = Setting().get_news_api_endpoints()

coin_ids = pd.read_csv("data/coins_ids.csv")
coin_api_ids = coin_ids["coin_api_id"].tolist()
coin_int_ids = coin_ids["coin_int_id"].tolist()


def get_news():
    all_news = []

    for count, id_ in enumerate(coin_api_ids):
        try:
            response = requests.get(
                url=f"{EVERYTHING}"
                    f"?q={id_}"
                    f"&from=2025-11-9"
                    f"&to=2025-11-19"
                    f"&sortBy=relevancy"
                    f"&language=en"
                    f"&apiKey={NEWSAPI_KEY}")

            data = response.json()
            articles = data["articles"]

            news_by_id = []
            for article in articles:

                news_by_id.append({
                    "coin_int_id": coin_int_ids[count],
                    "source": article["source"]["name"],
                    "author": article["author"],
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "publishedAt": article["publishedAt"]
                })

            df = pd.DataFrame(news_by_id)
            all_news.append(df)
        except Exception as e:
            print(f"Error for id {id_}: {e}")
        else:
            print(f"Processed id: {id_} ({count + 1}/{len(coin_api_ids)})")

        time.sleep(10)

    return pd.concat(all_news, ignore_index=True)


news = get_news()
news.to_csv("data/news_from_newsapi.csv", index=False)