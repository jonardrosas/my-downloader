import os
from ..extractors.base import DefaultExtractor

from abc import ABC, abstractmethod
import requests


class StorageAbstract(ABC):
    @abstractmethod
    def store(self):
        pass



class DefaultStorage(StorageAbstract):
    _output_path = "output"
    chunk_size = 128
    extractor_class = DefaultExtractor

    def __init__(self, output=None):
        if output:
            self._output = output
        self.setup()

    def setup(self):
        self.extractor = self.extractor_class()

    def get(self, link):
        return self.extractor.get_request(link)

    def store(self, link):
        if not link:
            return

        path, file = os.path.split(link)
        folder_name = path.split("/")[-1]
        output_folder = os.path.join(self._output_path, folder_name)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = os.path.join(output_folder, file)
        with open(output_path, "wb") as output_file:
            response = self.get(link)
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                output_file.write(chunk)

