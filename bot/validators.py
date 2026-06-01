from typing import Optional

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol or len(symbol) < 3:
        raise ValueError(f"Invalid symbol: '{symbol}'. Example: BTCUSDT")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side: '{side}'. Must be one of {VALID_SIDES}")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type: '{order_type}'. Must be one of {VALID_ORDER_TYPES}")
    return order_type


def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError
        return qty
    except (ValueError, TypeError):
        raise ValueError(f"Invalid quantity: '{quantity}'. Must be a positive number.")


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError
            return p
        except (ValueError, TypeError):
            raise ValueError(f"Invalid price: '{price}'. Must be a positive number.")
    return None


def validate_stop_price(stop_price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "STOP_MARKET":
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_MARKET orders.")
        try:
            sp = float(stop_price)
            if sp <= 0:
                raise ValueError
            return sp
        except (ValueError, TypeError):
            raise ValueError(f"Invalid stop price: '{stop_price}'. Must be a positive number.")
    return None
