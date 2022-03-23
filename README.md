# Bit2cAPI

Python API for interacting with the israeli crypto trading platform [bit2c](https://bit2c.co.il/).

## USAGE

```python
import os
from Bit2capi.api_client import Bit2c_client

key, secret = os.getenv(BIT2CKEY), os.getenv(BIT2C_SECRET)

client = Bit2c_client(key, secret)

balance = client.fetch_balance()

order_response = client.add_stop_limit_order(
    amount=0.5, price=730, stop=750, isBid=True, symbol=Symbol.LTC.pair
)

```
