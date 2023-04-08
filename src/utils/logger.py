import os
from datetime import datetime
from typing import Callable, Dict, Optional, List
from loguru import logger
from notifiers.logging import NotificationHandler
from .notifier import Discord, Notifier

gmail_notofier_params = {
    "username": os.getenv('GMAIL_USERNAME'),
    "password":  os.getenv('GMAIL_PASSWORD'),
    "to":  os.getenv('NOFITY_TO')
}

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
FILEPATHS = {
    "info": "log/output.log",
}

class Logger:

    _instance = None
    notifiers: List[Notifier] = []

    def __new__(cls, notifiers=["discord"]):
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
            cls._instance.notifiers = cls._instance.__set_notifiers(notifiers)

        return cls._instance

    def __set_notifiers(self, notifiers) -> List[Notifier]:
        notifier_setup_funcs: Dict[str, Callable[[], Optional[Notifier]]] = {
            "gmail": self.__set_gmail_notifier,
            "discord": self._get_discord_notifier
            # Add other notifiers and their setup functions here
        }

        notifiers_set = []
        for notifier in notifiers:
            setup_func = notifier_setup_funcs.get(notifier)
            if setup_func:
                instance = setup_func()
                if instance:
                    notifiers_set.append(instance)
            else:
                raise ValueError(f"Invalid notifier '{notifier}'. Choose from: {', '.join(notifier_setup_funcs.keys())}")

        return notifiers_set

    def __set_gmail_notifier(self) -> None:
        handler = NotificationHandler("gmail", defaults=gmail_notofier_params)
        logger.add(handler, level="ERROR")

    def _get_discord_notifier(self) -> Notifier:
        return Discord(DISCORD_WEBHOOK_URL)

    def info(self, msg):
        self.__send_notifications(msg)
        logger.info(msg)

    def warning(self, msg):
        logger.warning(msg)

    def debug(self, msg):
        logger.debug(msg)

    def error(self, msg):
        self.__send_notifications(msg)
        logger.exception(msg)

    def __send_notifications(self, msg):
        for notifier in self.notifiers:
            try:
                notifier.send(msg)
            except:
                logger.info(f"ERROR: Failed to send notification to {notifier.__name__}")