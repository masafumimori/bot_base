from typing import Optional
import ccxt
import os

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')


class ExchangeBase:
    """
    Provides a base abstraction for interacting with an exchange through the CCXT library.
    """

    def __init__(self, exchange_name: str) -> None:
        """
        Initializes the exchange instance using the given name.

        Parameters:
        - `exchange_name`: The name of the exchange to connect to.
        """
        if exchange_name not in ccxt.exchanges:
            raise ValueError(f"Invalid exchange name '{exchange_name}'. Choose from: {', '.join(ccxt.exchanges)}")
        exchange_class = getattr(ccxt, exchange_name)
        self.exchange = exchange_class({
            'apiKey': API_KEY,
            'secret': API_SECRET,
        })

    def fetch_balance(self, params: dict = {}) -> dict:
        """
        Retrieves the balance information for the connected account.

        Parameters:
        - `params`: Additional parameters to pass to the CCXT library.

        Returns:
        - A dictionary of balance information for the connected account.
        """
        return self.exchange.fetch_balance(params=params)

    def create_order(self, symbol: str, type: str, side: str, amount: float, price: Optional[float] = None, params: dict = {}) -> dict:
        """
        Creates an order on the exchange.

        Parameters:
        - `symbol`: The trading pair (e.g. 'BTC/USDT') to trade.
        - `type`: The type of order to create (e.g. 'limit', 'market', etc.).
        - `side`: The side of the order (e.g. 'buy' or 'sell').
        - `amount`: The amount of the asset to trade.
        - `price`: The price at which to place the order (optional for market orders).
        - `params`: Additional parameters to pass to the CCXT library.

        Returns:
        - A dictionary containing information about the created order.
        """
        return self.exchange.create_order(symbol, type, side, amount, price, params)

    def cancel_order(self, id: str, symbol: Optional[str] = None, params: dict = {}) -> dict:
        """
        Cancels an order on the exchange.

        Parameters:
        - `id`: The ID of the order to cancel.
        - `symbol`: The trading pair associated with the order (optional).
        - `params`: Additional parameters to pass to the CCXT library.

        Returns:
        - A dictionary containing information about the cancelled order.
        """
        return self.exchange.cancel_order(id, symbol, params)