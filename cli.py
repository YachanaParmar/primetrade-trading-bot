#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot
CLI entry point
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.orders import place_order
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_stop_price,
    validate_symbol,
)

load_dotenv()
logger = setup_logger()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--symbol",     required=True,  help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",       required=True,  help="BUY or SELL")
    parser.add_argument("--type",       required=True,  dest="order_type", help="MARKET, LIMIT, or STOP_MARKET")
    parser.add_argument("--quantity",   required=True,  help="Order quantity, e.g. 0.001")
    parser.add_argument("--price",      required=False, help="Limit price (required for LIMIT orders)")
    parser.add_argument("--stop-price", required=False, dest="stop_price", help="Stop price (required for STOP_MARKET)")
    parser.add_argument("--api-key",    required=False, help="Binance API key (or set BINANCE_API_KEY env var)")
    parser.add_argument("--api-secret", required=False, dest="api_secret", help="Binance API secret (or set BINANCE_API_SECRET env var)")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Resolve credentials
    api_key    = args.api_key    or os.getenv("BINANCE_API_KEY")
    api_secret = args.api_secret or os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("API credentials missing. Set --api-key/--api-secret or BINANCE_API_KEY/BINANCE_API_SECRET env vars.")
        sys.exit(1)

    # Validate inputs
    try:
        symbol     = validate_symbol(args.symbol)
        side       = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity   = validate_quantity(args.quantity)
        price      = validate_price(args.price, order_type)
        stop_price = validate_stop_price(args.stop_price, order_type)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        sys.exit(1)

    # Place order
    client = BinanceClient(api_key=api_key, api_secret=api_secret)

    try:
        response = place_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
        )
        print("\n✅ Order placed successfully!")
        print(f"   Order ID  : {response.get('orderId')}")
        print(f"   Status    : {response.get('status')}")
        print(f"   Exec Qty  : {response.get('executedQty')}")
        print(f"   Avg Price : {response.get('avgPrice', 'N/A')}")

    except RuntimeError as e:
        logger.error(f"Order failed: {e}")
        print(f"\n❌ Order failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
