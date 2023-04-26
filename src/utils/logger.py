import os
from datetime import datetime
from typing import Callable, Dict, List, Optional
from loguru import logger
from notifiers.logging import NotificationHandler
from .notifier import Discord, LINE, Notifier

GMAIL_NOTIFIER_PARAMS = {
    "username": os.getenv('GMAIL_USERNAME'),
    "password":  os.getenv('GMAIL_PASSWORD'),
    "to":  os.getenv('NOFITY_TO')
}

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

class Logger:
    """
    A custom Logger class that uses the loguru library for logging and supports sending notifications through
    various notifiers like Gmail, Discord, and LINE. It follows the Singleton design pattern.
    """
    _instance = None
    _notifiers: List[Notifier] = []

    @classmethod
    def instance(cls, notifiers: Optional[List[str]] = None) -> 'Logger':
        """
        Returns the singleton instance of the Logger class.

        If the notifiers config list is specified and is different from the previously set configuration,
        the Logger instance is recreated with the new list.

        Args:
            notifiers (Optional[List[str]], optional): List of notifiers to set. Possible values are "gmail", "discord", "line".

        Returns:
            Logger: The singleton instance of the Logger class.
        """
        if notifiers is None:
            notifiers = ["discord"]

        if not cls._instance:
            cls._instance = cls(notifiers)
        else:
            instance_notifiers_classes = [n.__class__.__name__.lower() for n in cls._instance._notifiers]
            if set(instance_notifiers_classes) != set(notifiers):
                cls._instance._notifiers = cls._instance.__set_notifiers(notifiers)
        return cls._instance
    
    def __init__(self, notifiers: Optional[List[str]] = None) -> None:
        """
        Initializes the Logger instance with the given notifiers configuration.

        Args:
            notifiers (Optional[List[str]], optional): List of notifiers to set. Possible values are "gmail", "discord", "line".
        """
        if notifiers is None:
            notifiers = ["discord"]

        self.__setup_logger()
        self._notifiers = self.__set_notifiers(notifiers)

    def __setup_logger(self) -> None:
        """
        Sets up the logger configurations by removing any existing handlers and adding new handlers for logging to a file and for logging errors.
        """
        logger.remove()
        logger.add("logs/output.log", rotation="500 MB")

        def error_sink(message: str) -> None:
            """
            Custom sink function to create a new error log file with a timestamp.

            Args:
                message (str): The error message to be written to the file.
            """
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with open(f"logs/error_{timestamp}.log", "w") as error_file:
                error_file.write(message)

        logger.add(error_sink, level="ERROR")

    def __set_notifiers(self, notifiers: List[str]) -> List[Notifier]:
        """
        Sets up the notifiers based on the given configuration.

        Args:
            notifiers (List[str]): A list of notifiers to set.

        Returns:
            List[Notifier]: A list of configured Notifier instances.
        """
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
        """
        Sets up the Gmail notifier using the NotificationHandler and adds it to the logger for error-level notifications.
        """
        handler = NotificationHandler("gmail", defaults=GMAIL_NOTIFIER_PARAMS)
        logger.add(handler, level="ERROR")

    def __get_discord_notifier(self) -> Notifier:
        """
        Returns a Discord notifier instance.

        Returns:
            Notifier: The Discord notifier instance.
        """
        return Discord(DISCORD_WEBHOOK_URL)

    def __get_line_notifier(self) -> Notifier:
        """
        Returns a LINE notifier instance.

        Returns:
            Notifier: The LINE notifier instance.
        """
        return LINE(LINE_NOTIFY_TOKEN)

    def info(self, msg: str, notify: bool = False) -> None:
        """
        Logs an info-level message and sends notifications if the notify parameter is set to True.

        Args:
            msg (str): The message to log.
            notify (bool): If True, sends notifications. Defaults to False.
        """
        if notify:
            self.__send_notifications(msg)
        logger.info(msg)

    def success(self, msg: str, notify: bool = False) -> None:
        """
        Logs an success-level message and sends notifications if the notify parameter is set to True.

        Args:
            msg (str): The message to log.
            notify (bool): If True, sends notifications. Defaults to False.
        """
        if notify:
            self.__send_notifications(msg)
        logger.success(msg)

    def warning(self, msg: str, notify: bool = False) -> None:
        """
        Logs a warning-level message and sends notifications if the notify parameter is set to True.

        Args:
            msg (str): The message to log.
            notify (bool): If True, sends notifications. Defaults to False.
        """
        if notify:
            self.__send_notifications(msg)
        logger.warning(msg)

    def debug(self, msg: str, notify: bool = False) -> None:
        """
        Logs a debug-level message and sends notifications if the notify parameter is set to True.

        Args:
            msg (str): The message to log.
            notify (bool): If True, sends notifications. Defaults to False.
        """
        if notify:
            self.__send_notifications(msg)
        logger.debug(msg)

    def error(self, msg: str, notify: bool = True) -> None:
        """
        Logs an error-level message and sends notifications if the notify parameter is set to True.

        Args:
            msg (str): The message to log.
            notify (bool): If True, sends notifications. Defaults to True.
        """
        if notify:
            self.__send_notifications(msg)

        # exception() : Convenience method for logging an 'ERROR' with exception information.
        logger.exception(msg)
    
    def critical(self, msg: str, notify: bool = True) -> None:
        """
        Logs an critical-level message and sends notifications if the notify parameter is set to True.

        Args:
            msg (str): The message to log.
            notify (bool): If True, sends notifications. Defaults to True.
        """
        if notify:
            self.__send_notifications(msg)
        logger.critical(msg)

    def __send_notifications(self, msg: str) -> None:
        """
        Sends notifications using the configured notifiers.

        Args:
            msg (str): The message to send as a notification.
        """
        for notifier in self._notifiers:
            try:
                notifier.send(msg)
            except:
                logger.warning(f"Failed to send notification to {notifier.__class__.__name__}")
