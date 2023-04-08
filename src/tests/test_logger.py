import os
import unittest
from unittest.mock import MagicMock, patch
from utils.logger import Logger

class TestLogger(unittest.TestCase):

    def test_singleton(self):
        logger1 = Logger()
        logger2 = Logger()
        self.assertEqual(logger1, logger2, "Logger should be a singleton")

    def test_notifiers(self):
        with patch("your_module.Logger.__set_notifiers", return_value=["test_notifier"]):
            logger = Logger()
            self.assertEqual(len(logger.notifiers), 1, "There should be only one notifier set")

    def test_info(self):
        msg = "Test info"
        with patch("your_module.logger.info") as mock_info:
            logger = Logger()
            logger.info(msg)
            mock_info.assert_called_once_with(msg)

    def test_warning(self):
        msg = "Test warning"
        with patch("your_module.logger.warning") as mock_warning:
            logger = Logger()
            logger.warning(msg)
            mock_warning.assert_called_once_with(msg)

    def test_debug(self):
        msg = "Test debug"
        with patch("your_module.logger.debug") as mock_debug:
            logger = Logger()
            logger.debug(msg)
            mock_debug.assert_called_once_with(msg)

    def test_error(self):
        msg = "Test error"
        with patch("your_module.logger.exception") as mock_exception:
            logger = Logger()
            logger.error(msg)
            mock_exception.assert_called_once_with(msg)

    def test_send_notifications(self):
        msg = "Test notification"
        mock_notifier = MagicMock()
        with patch("your_module.Logger.__set_notifiers", return_value=[mock_notifier]):
            logger = Logger()
            logger._Logger__send_notifications(msg)
            mock_notifier.send.assert_called_once_with(msg)

if __name__ == "__main__":
    unittest.main()
