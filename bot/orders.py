from typing import Optional

from bot.client import BinanceClient
from bot.logging_config import setup_logger

logger = setup_logger()


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
) -> dict:
    """Place an order and return structured result."""

    summary = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "price": price if order_type == "LIMIT" else "N/A",
        "stop_price": stop_price if order_type == "STOP_MARKET" else "N/A",
    }

    logger.info("=" * 55)
    logger.info("ORDER REQUEST SUMMARY")
    for k, v in summary.items():
        logger.info(f"  {k.upper():12}: {v}")
    logger.info("=" * 55)

    response = client.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
        stop_price=stop_price,
    )

    logger.info("ORDER RESPONSE")
    logger.info(f"  Order ID     : {response.get('orderId', 'N/A')}")
    logger.info(f"  Status       : {response.get('status', 'N/A')}")
    logger.info(f"  Executed Qty : {response.get('executedQty', 'N/A')}")
    logger.info(f"  Avg Price    : {response.get('avgPrice', 'N/A')}")
    logger.info("=" * 55)

    return response
