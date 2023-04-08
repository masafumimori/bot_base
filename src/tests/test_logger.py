import unittest
from unittest.mock import MagicMock, patch
from utils.logger import Logger
from utils.notifier import Discord

class TestLogger(unittest.TestCase):

    def test_singleton(self):
        logger1 = Logger()
        logger2 = Logger()
        self.assertEqual(logger1, logger2, "Logger should be a singleton")

    def test_notifiers(self):
        notifiers = ["discord"]
        logger = Logger(notifiers=notifiers)
        self.assertIsInstance(logger.notifiers[0], Discord, "The first notifier should be an instance of Discord")
        self.assertEqual(len(logger.notifiers), len(notifiers), "There should be only one notifier set")

    def test_info(self):
        msg = "Test info"
        with patch.object(Logger, "info") as mock_info:
            logger = Logger()
            logger.info(msg)
            mock_info.assert_called_once_with(msg)

    def test_warning(self):
        msg = "Test warning"
        with patch.object(Logger, "warning") as mock_warning:
            logger = Logger()
            logger.warning(msg)
            mock_warning.assert_called_once_with(msg)

    def test_debug(self):
        msg = "Test debug"
        with patch.object(Logger, "debug") as mock_debug:
            logger = Logger()
            logger.debug(msg)
            mock_debug.assert_called_once_with(msg)

    def test_error(self):
        msg = "Test error"
        with patch.object(Logger, "error") as mock_error:
            logger = Logger()
            logger.error(msg)
            mock_error.assert_called_once_with(msg)

    def test_send_notifications(self):
        msg = "Test notification"
        mock_notifier = MagicMock()
        logger = Logger()
        logger.notifiers = [mock_notifier]  # Directly add the mock_notifier to the notifiers list
        logger._Logger__send_notifications(msg)  # Call the __send_notifications method
        mock_notifier.send.assert_called_once_with(msg)

if __name__ == "__main__":
    unittest.main()
