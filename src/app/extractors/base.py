from abc import abstractmethod, ABC

import requests


class BaseDownloader(ABC):

    @abstractmethod
    def download(self):
        pass



class DefaultExtractor(BaseDownloader):

    def __init__(self, url) -> None:
        self.url = url

    def download(self):
        response = requests.get(self.url)
        return response.text
