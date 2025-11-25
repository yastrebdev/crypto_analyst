class Coins:
    def __init__(self):
        self.coins = {
            "bitcoin": {
                "symbol": "btc",
                "ids": {}
            },
            "ethereum": {
                "symbol": "eth",
                "ids": {}
            },
            "tether": {
                "symbol": "usdt",
                "ids": {}
            },
            "xrp": {
                "symbol": "xrp",
                "ids": {}
            },
            "bnb": {
                "symbol": "bnb",
                "ids": {}
            },
            "solana": {
                "symbol": "sol",
                "ids": {}
            },
            "usd-coin": {
                "symbol": "usdc",
                "ids": {}
            },
            "tron": {
                "symbol": "trx",
                "ids": {}
            },
            "dogecoin": {
                "symbol": "doge",
                "ids": {}
            },
            "cardano": {
                "symbol": "ada",
                "ids": {}
            },
        }


    def all(self):
        return self.coins


    def add_id(self, coin_name, api_name, api_coin_id):
        key = coin_name.lower()
        if key not in self.coins:
            raise KeyError(f"Coin '{coin_name}' not found")
        self.coins[coin_name]["ids"][api_name] = api_coin_id
        return f"ID successfully added for {key} coin"


    def get_symbol_list(self):
        symbols = [value["symbol"] for _, value in self.coins.items()]
        return symbols


    def get_name_list(self):
        names = [key for key, _ in self.coins.items()]
        return names