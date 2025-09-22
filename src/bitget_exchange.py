# src/bitget_exchange.py
import json
import time
import hmac
import hashlib
import base64
import httpx


class BitgetExchange:
    def __init__(self, keys_file: str = "keys.json"):
        with open(keys_file, "r") as f:
            keys = json.load(f)
        self.api_key = keys["bitget"]["api_key"]
        self.api_secret = keys["bitget"]["api_secret"]
        self.passphrase = keys["bitget"]["passphrase"]
        self.base_url = "https://api.bitget.com"
        self.client = httpx.Client()

    def _sign(self, method: str, path: str, params: str = ""):
        timestamp = str(int(time.time() * 1000))
        pre_sign = f"{timestamp}{method}{path}{params}"
        sign = hmac.new(
            self.api_secret.encode("utf-8"),
            pre_sign.encode("utf-8"),
            hashlib.sha256
        ).digest()
        sign_b64 = base64.b64encode(sign).decode()
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": sign_b64,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
        }
        return headers

    def _get_balances(self, endpoint):
        """Méthode générique pour requêter un endpoint de balance"""
        headers = self._sign("GET", endpoint)
        url = self.base_url + endpoint
        r = self.client.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_spot_balances(self):
        """Récupère les soldes Spot"""
        data = self._get_balances("/api/v2/spot/account/assets")
        balances = []
        if data["code"] == "00000":
            for b in data.get("data", []):
                available = float(b.get("available", 0))
                frozen = float(b.get("frozen", 0))
                locked = float(b.get("locked", 0))
                total = available + frozen + locked
                if total > 0:
                    balances.append({
                        "asset": b["coin"],
                        "available": available,
                        "frozen": frozen,
                        "locked": locked,
                        "total": total,
                        "type": "spot"
                    })
        return balances

    def get_earn_balances(self):
        """Récupère les soldes Earn"""
        data = self._get_balances("/api/v2/earn/account/assets")
        balances = []
        if data["code"] == "00000":
            for b in data.get("data", []):
                amount = float(b.get("amount", 0))
                if amount > 0:
                    balances.append({
                        "asset": b["coin"],
                        "available": amount,
                        "frozen": 0.0,
                        "locked": 0.0,
                        "total": amount,
                        "type": "earn"
                    })
        return balances

    def get_all_balances(self):
        """Récupère Spot + Earn"""
        return self.get_spot_balances() + self.get_earn_balances()    
