from abc import abstractmethod, ABC


class BaseDownloader(ABC):

    def __init__(self, url) -> None:
        self.url = url

    @abstractmethod
    def download(self):
        pass