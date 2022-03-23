from enum import Enum


class Symbol(Enum):

    BTC = "BTC"
    ETH = "ETH"
    LTC = "LTC"
    USDC = "USDC"

    @property
    def pair(self):
        return f"{self.value.capitalize()}Nis"
