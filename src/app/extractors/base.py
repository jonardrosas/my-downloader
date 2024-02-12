from abc import abstractmethod, ABC

import requests
from ..exceptions import NoUrlProvided


class BaseDownloader(ABC):

    @abstractmethod
    def download(self):
        pass



class DefaultExtractor(BaseDownloader):

    def __init__(self, url=None) -> None:
        self.url = url

    def get_request(self, url=None):
        if not url:
            url = self.url
        if not url:
            raise NoUrlProvided('No url provided')
        return requests.get(url)

    def download(self):
        return self.get_request().text
