import os
from datetime import datetime
from loguru import logger
from notifiers.logging import NotificationHandler

notifiers_params = {
    "username": os.getenv('GMAIL_USERNAME'),
    "password":  os.getenv('GMAIL_PASSWORD'),
    "to":  os.getenv('NOFITY_TO')
}

FILEPATHS = {
    "info": "log/output.log",
}

class Logger:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            logger.remove()
            logger.add(FILEPATHS["info"], rotation="500 MB")

            # Custom sink function to create a new error log file with timestamp
            def error_sink(message):
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                with open(f"log/error_{timestamp}.log", "w") as error_file:
                    error_file.write(message)

            logger.add(error_sink, level="ERROR")

            # Add notifier handler so that it notifies me when errors occured
            handler = NotificationHandler("gmail", defaults=notifiers_params)
            logger.add(handler, level="ERROR")

        return cls._instance

    def info(self, msg):
        logger.info(msg)

    def debug(self, msg):
        logger.debug(msg)

    def error(self, msg):
        logger.exception(msg)
