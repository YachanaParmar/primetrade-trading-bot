import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logger

BASE_URL = "https://testnet.binancefuture.com"
logger = setup_logger()


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json",
        })

    def _sign(self, params: Dict) -> Dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method: str, endpoint: str, params: Dict) -> Dict[str, Any]:
        url = f"{BASE_URL}{endpoint}"
        signed_params = self._sign(params)

        logger.debug(f"REQUEST  {method.upper()} {url} | params: {signed_params}")

        try:
            if method.upper() == "POST":
                response = self.session.post(url, params=signed_params, timeout=10)
            else:
                response = self.session.get(url, params=signed_params, timeout=10)

            logger.debug(f"RESPONSE {response.status_code} | body: {response.text}")
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e} | response: {response.text}")
            raise RuntimeError(f"API error {response.status_code}: {response.text}") from e
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network error: {e}")
            raise RuntimeError("Network connection failed. Check your internet.") from e
        except requests.exceptions.Timeout:
            logger.error("Request timed out.")
            raise RuntimeError("Request timed out. Try again.") from None

    def get_account_info(self) -> Dict:
        return self._request("GET", "/fapi/v2/account", {})

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        if order_type == "STOP_MARKET":
            params["stopPrice"] = stop_price

        return self._request("POST", "/fapi/v1/order", params)
