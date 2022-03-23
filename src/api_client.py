import math
import requests
import hmac
import hashlib
import base64
import json
from datetime import datetime
from json.decoder import JSONDecodeError


from src.Symbol import Symbol


class Bit2c_client:
    """class for accessing private methods of bit2c.co.il api"""

    def __init__(self, key: str, secret: str) -> None:
        self.__key = key
        self.__secret = secret

    def create_hash(self, hash_key: str) -> bytes:
        sign = base64.b64encode(
            hmac.new(self.__secret.encode(), hash_key.encode(), hashlib.sha512).digest()
        )
        return sign

    def query(self, url: str, method: str, data: dict = {}) -> requests.Response:
        BASE_URL = "https://bit2c.co.il/"
        # params to hash should be param1=x&param2=y...&nonce=number
        params_string = ""
        for item in data.items():
            params_string += "=".join([str(i) for i in list(item)]) + "&"

        nonce = self.nonce
        params_string += f"{nonce=}"

        url = BASE_URL + url
        sign = self.create_hash(params_string)
        headers = {
            "Key": self.__key,
            "Sign": sign,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        if method == "GET":
            url = f"{url}?{params_string}"
            return requests.get(url, headers=headers)

        if method == "POST":
            data["nonce"] = nonce
            return requests.post(url, headers=headers, data=data)

    @property
    @staticmethod
    def nonce(*args):
        return math.ceil(datetime.timestamp(datetime.now()))

    @staticmethod
    def _json(data: str) -> dict:
        try:
            return json.loads(data)
        except JSONDecodeError as e:
            print(e)
            print(data)
            return

    def fetch_balance(self) -> str:
        url = "Account/Balance"
        res = self.query(url, "GET")
        return self._json(res.text)

    def fetch_my_orders(self, symbol) -> str:
        url = "Order/MyOrders"
        data = {"pair": symbol.pair} if symbol else {}
        res = self.query(url, "GET", data)
        return self._json(res.text)

    def fetch_order_by_id(self, id: int) -> str:
        url = "Order/GetById"
        data = {"id": id}
        res = self.query(url, "GET", data)
        return self._json(res.text)

    def fetch_account_history(self, from_time: str | int, to_time: str | int) -> str:
        url = "Order/AccountHistory"
        data = {"fromTime": from_time, "toTime": to_time}
        res = self.query(url, "GET", data)
        return self._json(res.text)

    def fetch_order_history(
        self,
        from_time: str | int,
        to_time: str | int,
        symbol: Symbol,
        take: int = 1000,
    ) -> str:
        url = "Order/OrderHistory"
        data = {
            "fromTime": from_time,
            "toTime": to_time,
            "take": take,
            "pair": symbol.pair,
        }
        res = self.query(url, "GET", data)
        return self._json(res.text)

    def fetch_order_history_by_id(self, id: int) -> str:
        url = "Order/HistoryByOrderId"
        data = {"id": id}
        res = self.query(url, "GET", data)
        return self._json(res.text)

    def add_order(
        self, amount: float, price: float, is_bid: bool, symbol: Symbol
    ) -> str:
        """isbid true is buy, false is sell"""
        url = "Order/AddOrder"
        data = {
            "Amount": amount,
            "Price": price,
            "IsBid": str(is_bid).lower(),
            "Pair": symbol.pair,
        }
        res = self.query(url, "POST", data)
        return self._json(res.text)

    def cancel_order(self, id: int) -> str:
        url = "Order/CancelOrder"
        data = {"id": id}
        res = self.query(url, "POST", data)
        return self._json(res.text)

    def buy_market_price(self, total: float, symbol: Symbol) -> str:
        url = "Order/AddOrderMarketPriceBuy"
        data = {"Total": total, "Pair": symbol.pair}
        res = self.query(url, "POST", data)
        return self._json(res.text)

    def sell_market_price(self, amount: float, pair: float) -> str:
        url = "Order/AddOrderMarketPriceSell"
        data = {"Amount": amount, "Pair": pair}
        res = self.query(url, "POST", data)
        return self._json(res.text)

    def add_stop_limit_order(
        self, amount: float, price: float, stop: float, isbid: bool, symbol: Symbol
    ) -> str:
        url = "Order/AddStopOrder"
        data = {
            "Amount": amount,
            "Price": price,
            "Stop": stop,
            "IsBid": str(isbid).lower(),
            "Pair": symbol.pair,
        }
        res = self.query(url, "POST", data)
        return self._json(res.text)
