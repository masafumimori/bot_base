import os
import unittest
from unittest.mock import MagicMock, patch
from utils.exchange_base import ExchangeBase

class TestExchangeBase(unittest.TestCase):

    def setUp(self):
        self.exchange_name = 'bybit'

    def test_invalid_exchange_name(self):
        invalid_exchange_name = 'invalid_exchange'
        self.assertRaises(ValueError, ExchangeBase, invalid_exchange_name)

    def test_fetch_balance(self):
        mocked_balance = {"BTC": {"free": 0.1, "used": 0, "total": 0.1}}

        with patch("ccxt.bybit") as mock_exchange_class:
            mock_exchange = MagicMock()
            mock_exchange.fetch_balance.return_value = mocked_balance
            mock_exchange_class.return_value = mock_exchange

            exchange_base = ExchangeBase(self.exchange_name)
            balance = exchange_base.fetch_balance()

            self.assertEqual(balance, mocked_balance, "Balance should be fetched correctly")
            mock_exchange.fetch_balance.assert_called_once()

    def test_create_order(self):
        symbol = 'BTC/USDT'
        order_type = 'limit'
        side = 'buy'
        amount = 0.01
        price = 30000

        mocked_order = {
            'id': '12345',
            'info': {},
            'symbol': symbol,
            'type': order_type,
            'side': side,
            'price': price,
            'amount': amount,
        }

        with patch("ccxt.bybit") as mock_exchange_class:
            mock_exchange = MagicMock()
            mock_exchange.create_order.return_value = mocked_order
            mock_exchange_class.return_value = mock_exchange

            exchange_base = ExchangeBase(self.exchange_name)
            order = exchange_base.create_order(symbol, order_type, side, amount, price)

            self.assertEqual(order, mocked_order, "Order should be created correctly")
            mock_exchange.create_order.assert_called_once_with(symbol, order_type, side, amount, price, {})

    def test_cancel_order(self):
        order_id = '12345'
        symbol = 'BTC/USDT'

        mocked_cancel = {
            'id': order_id,
            'symbol': symbol,
        }

        with patch("ccxt.bybit") as mock_exchange_class:
            mock_exchange = MagicMock()
            mock_exchange.cancel_order.return_value = mocked_cancel
            mock_exchange_class.return_value = mock_exchange

            exchange_base = ExchangeBase(self.exchange_name)
            cancel = exchange_base.cancel_order(order_id, symbol)

            self.assertEqual(cancel, mocked_cancel, "Order should be canceled correctly")
            mock_exchange.cancel_order.assert_called_once_with(order_id, symbol, {})

if __name__ == "__main__":
    unittest.main()
