import os
from urllib.request import urlopen
import requests
from .base import BaseDownloader



class PDFDownloader(BaseDownloader):

    def __init__(self, url) -> None:
        self.url = url

    def download(self):
        response = requests.get(self.url)
        return response.text
