import os
from .enums import FileTypeEnums
from .exceptions import InvalidFormat, NoDownloader
from .extractors.base import DefaultExtractor
from .parser.html import ParserHandler
from .storage.base import DefaultStorage


class AppDownManger():
    parser_class = ParserHandler
    storage_class = DefaultStorage
    extractor_class = DefaultExtractor

    def __init__(self, file_type, url, output_path=None):
        self.file_type = file_type
        self.url = url
        self.output_path = output_path
        if not self._is_valid_format(file_type):
            raise InvalidFormat("Not a registered extension")
        self.setup()

    def _is_valid_format(self, format) -> bool:
        return format in [choice.value for choice in FileTypeEnums]

    def setup(self):
        self.storage = self.get_storage(output_path=self.output_path)
        self.downloader = self.extractor_class(self.url)

    def get_storage(self, output_path=None):
        return self.storage_class(output=output_path)

    def download(self):
        if self.downloader:
            raw_data = self.downloader.download()
            if raw_data:
                self.parse(raw_data)
            else:
                print(f"no {self.file_type} available on {self.url}")

    def parse(self, raw_data):
        self.parser = self.parser_class(raw_data, self.file_type).get_parser()
        self.links = self.parser.get_all_links(base=self.url)
        if not self.links:
            print(f"no {self.file_type} available on {self.url}")
            return
        for link in self.links:
            self.store(link)

    def store(self, link):
        self.storage.store(link)
