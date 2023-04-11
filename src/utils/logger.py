import os
from datetime import datetime
from typing import Callable, Dict, List, Optional
from loguru import logger
from notifiers.logging import NotificationHandler
from notifier import Discord, LINE, Notifier

GMAIL_NOTIFIER_PARAMS = {
    "username": os.getenv('GMAIL_USERNAME'),
    "password":  os.getenv('GMAIL_PASSWORD'),
    "to":  os.getenv('NOFITY_TO')
}

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

FILEPATHS = {
    "info": "log/output.log",
}

class Logger:

    _instance = None
    _notifiers: List[Notifier] = []

    @classmethod
    def instance(cls, notifiers: Optional[List[str]] = None) -> 'Logger':
        """
        Returns the singleton instance of the `Logger` class.

        If the `notifiers` config list is specified and is different from the previously set configuration,
        the `Logger` instance is recreated with the new list.

        Parameters:
            `notifiers` (optional): list of notifiers to set. Possible values are `"gmail"`, `"discord"`, `"line"`.

        Returns:
            The singleton instance of the `Logger` class.
        """
        if notifiers is None:
            notifiers = ["discord"]

        if not cls._instance:
            cls._instance = cls(notifiers)
        else:
            instance_notifiers_classes = [n.__class__.__name__.lower() for n in cls._instance.notifiers]
            if set(instance_notifiers_classes) != set(notifiers):
                cls._instance._notifiers = cls._instance.__set_notifiers(notifiers)
        return cls._instance
    
    def __init__(self, notifiers: Optional[List[str]] = None) -> None:
        """
        Initializes the Logger instance with the given notifiers configuration.

        Parameters:
            `notifiers` (optional): list of notifiers to set. Possible values are `"gmail"`, `"discord"`, `"line"`.
        """
        if notifiers is None:
            notifiers = ["discord"]

        self.__setup_logger()
        self._notifiers = self.__set_notifiers(notifiers)

    def __setup_logger(self):
        logger.remove()
        logger.add(FILEPATHS["info"], rotation="500 MB")

        # Custom sink function to create a new error log file with timestamp
        def error_sink(message):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with open(f"log/error_{timestamp}.log", "w") as error_file:
                error_file.write(message)

        logger.add(error_sink, level="ERROR")

    def __set_notifiers(self, notifiers) -> List[Notifier]:
        notifier_setup_funcs: Dict[str, Callable[[], Optional[Notifier]]] = {
            "gmail": self.__set_gmail_notifier,
            "discord": self.__get_discord_notifier,
            "line": self.__get_line_notifier
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
        handler = NotificationHandler("gmail", defaults=GMAIL_NOTIFIER_PARAMS)
        logger.add(handler, level="ERROR")
    
    def __get_discord_notifier(self) -> Notifier:
        return Discord(DISCORD_WEBHOOK_URL)
    
    def __get_line_notifier(self) -> Notifier:
        return LINE(LINE_NOTIFY_TOKEN)

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