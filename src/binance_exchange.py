# src/binance_exchange.py
from binance.client import Client
import json


class BinanceExchange:
    def __init__(self, keys_file: str = "keys.json"):
        with open(keys_file, "r") as f:
            keys = json.load(f)
        self.api_key = keys["binance"]["api_key"]
        self.api_secret = keys["binance"]["api_secret"]
        self.client = Client(self.api_key, self.api_secret)

    def get_account_info(self):
        """Retourne les infos du compte (balances, etc.)"""
        return self.client.get_account()

    def get_balances(self):
        """Retourne uniquement les balances non nulles"""
        account = self.get_account_info()
        balances = account["balances"]
        return [b for b in balances if float(b["free"]) > 0 or float(b["locked"]) > 0]
