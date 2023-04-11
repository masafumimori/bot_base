from abc import ABC, abstractmethod
import json
import requests

class Notifier(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def send(self, msg: str):
        pass

class Discord(Notifier):

    def __init__(self, url) -> None:
        self.__webhookurl = url
    
    def send(self, msg):
        content = {'content': msg}
        headers = {'Content-Type': 'application/json'}

        requests.post(self.__webhookurl, json.dumps(content), headers=headers)


class Line(Notifier):
    """
    Notifier object that sends messages to a LINE user or group.
    """

    BASE_URL = 'https://notify-api.line.me/api/notify'

    def __init__(self, token: str) -> None:
        """
        Initializes the Line notifier instance with an access token.

        Parameters:
        - `token`: The Line access token to use.
        """
        self.token = token

    def send(self, msg: str) -> None:
        """
        Sends a message to the Line user or group.

        Parameters:
        - `msg`: The message to send.
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + self.token
        }
        requests.post(self.BASE_URL, headers=headers, data={"message": self._safe_msg(msg)})

    def _safe_msg(self, msg: str) -> str:
        """
        Returns a truncated message if it exceeds the maximum allowable length for a Line message.

        Parameters:
        - `msg`: The message to truncate, if necessary.

        Returns:
        - The original message, truncated to fit within the Line message character limit.
        """
        # Only allows 1000 chars
        return msg[:1000]