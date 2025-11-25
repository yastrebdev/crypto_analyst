class Setting:
    def __init__(self):
        self.BASE_COINS_API_URL = "https://api.coingecko.com/api/v3"
        self.COINS_LIST = "/coins/list"
        self.COINS_MARKET_CHART = ("/coins/{id}/market_chart"
                                   "?vs_currency={currency}"
                                   "&days={days}"
                                   "&precision={precision}")

        self.NEWS_API_BASE_URL = "https://newsapi.org/v2"
        self.NEWS_API_EVERYTHING = "/everything"


    def get_news_api_endpoints(self):
        """
        **everything**: search every article published
        :return: tuple(str):
        """
        everything = f"{self.NEWS_API_BASE_URL}{self.NEWS_API_EVERYTHING}"

        return (everything,)