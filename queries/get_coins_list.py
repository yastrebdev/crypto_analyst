import requests
import pandas as pd

import os
from io import StringIO

from settings import Setting

setting = Setting()

url = f"{setting.BASE_COINS_API_URL}{setting.COINS_LIST}"

response = requests.get(url)


def create_csv(data, status):
    path = f"data/coins_list.csv"

    if status == 200:
        df = pd.read_json(StringIO(data))

        if not os.path.exists("data"):
            os.mkdir("data")

        df.to_csv(path, index=False)

        return f"Make file to dir: {path}"
    else:
        return f"Error: {status}"


res = create_csv(response.text, response.status_code)

print(res)