from .api_client import Bit2c_client
from .Symbol import Symbol

import requests

# This is very important
# bit2c api knowns to work only with ip v4, this is how we force requests to use it
requests.packages.urllib3.util.connection.HAS_IPV6 = False
