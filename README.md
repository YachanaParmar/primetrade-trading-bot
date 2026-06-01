# Binance Futures Testnet Trading Bot

A clean, structured Python CLI application for placing orders on Binance Futures Testnet (USDT-M).

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Structured logging setup
├── cli.py                 # CLI entry point (argparse)
├── logs/                  # Auto-created log files
├── .env.example           # Sample env file
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Get Testnet API Credentials

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Log in with your GitHub account
3. Click **"API Key"** → Generate a new API key and secret
4. Save both — the secret is shown only once

### 2. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/trading-bot.git
cd trading-bot
pip install -r requirements.txt
```

### 3. Configure Credentials

```bash
cp .env.example .env
# Edit .env and add your actual API key and secret
```

Or pass credentials directly via CLI flags (see below).

---

## How to Run

### Market Order (BUY)

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Market Order (SELL)

```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01
```

### Limit Order (SELL)

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 68000
```

### Limit Order (BUY)

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 65000
```

### Stop-Market Order (Bonus)

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 66000
```

### Pass Credentials Inline (no .env)

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 \
  --api-key YOUR_KEY --api-secret YOUR_SECRET
```

---

## Sample Output

```
INFO: =====================================================
INFO: ORDER REQUEST SUMMARY
INFO:   SYMBOL      : BTCUSDT
INFO:   SIDE        : BUY
INFO:   TYPE        : MARKET
INFO:   QUANTITY    : 0.001
INFO: =====================================================
INFO: ORDER RESPONSE
INFO:   Order ID     : 3279841
INFO:   Status       : FILLED
INFO:   Executed Qty : 0.001
INFO:   Avg Price    : 67342.10
INFO: =====================================================

✅ Order placed successfully!
   Order ID  : 3279841
   Status    : FILLED
   Exec Qty  : 0.001
   Avg Price : 67342.10
```

---

## Logging

Logs are saved to `logs/trading_bot_YYYYMMDD.log`.

Each log includes:
- Full request params (excluding secret)
- Raw API response
- Order summary (symbol, side, type, qty, price)
- Errors with context

---

## Assumptions

- Testnet base URL: `https://testnet.binancefuture.com`
- USDT-M Futures only
- `timeInForce` defaults to `GTC` for LIMIT orders
- Credentials loaded from `.env` or CLI flags
- Minimum quantity depends on the symbol (Binance testnet enforces lot size rules)

---

## Bonus Features Implemented

- ✅ **STOP_MARKET** order type support (`--type STOP_MARKET --stop-price XXXX`)
- ✅ Structured code with separate client/validation/order layers
- ✅ Dual logging (console + rotating daily log file)

---

## Requirements

- Python 3.8+
- `requests`
- `python-dotenv`
