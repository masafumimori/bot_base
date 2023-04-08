from typing import Optional
import ccxt
import os

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

class ExchangeBase:

    _instance = None

    def __new__(cls, exchange_name):
        if exchange_name not in ccxt.exchanges:
            raise ValueError(f"Invalid exchange name '{exchange_name}'. Choose from: {', '.join(ccxt.exchanges)}")

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            exchange_class = getattr(ccxt, exchange_name)
            cls._instance.exchange = exchange_class({
                'apiKey': API_KEY,
                'secret': API_SECRET,
            })
        return cls._instance

    def fetch_balance(self, params={}):
        return self.exchange.fetch_balance(params=params)

    def create_order(self, symbol: str, type, side, amount, price=None, params={}):
        return self.exchange.create_order(symbol, type, side, amount, price, params)

    def cancel_order(self, id: str, symbol: Optional[str] = None, params={}):
        return self.exchange.cancel_order(id, symbol, params)