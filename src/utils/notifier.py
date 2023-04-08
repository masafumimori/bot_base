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