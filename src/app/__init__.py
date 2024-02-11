import os
from .enums import FileTypeEnums
from .exceptions import InvalidFormat, NoDownloader
from .downloaders.pdf import PDFDownloader
from .parser.html import HtmlParser
from .storage.base import DefaultStorage


class Handler:

    def __init__(self, file_type):
        self._file_type = file_type

    def get_downloader_class(self):
        if self._file_type == FileTypeEnums.PDF.value:
            return PDFDownloader
        raise NoDownloader(f"No downloader class available for {self._file_type} format")


class AppBase:
    storage_class = DefaultStorage


    def __init__(self, file_type, url, output_path=None):
        self.file_type = file_type
        self.url = url
        if not self.is_valid:
            raise InvalidFormat("Not a registered extension")
        self.storage = self.get_storage(output_path=output_path)

    def get_storage(self, output_path=None):
        return self.storage_class(output=output_path)

    def _is_valid_format(self, format):
        for _format in FileTypeEnums:
            if _format.value == format:
                return True
        return False


class AppDownloader(AppBase):
    handler_class = Handler
    parser_class = HtmlParser

    def __init__(self, file_type, url, output_path=None):
        super().__init__(file_type, url, output_path=output_path)
        self.is_valid = self._is_valid_format(file_type)
        self.setup()

    def setup(self):
        self._downloader_class = self.handler_class(self.file_type).get_downloader_class()
        self.downloader = self._downloader_class(self.url)

    def download(self):
        if self.downloader:
            raw_data = self.downloader.download()
            if raw_data:
                self.parse(raw_data)
            else:
                print(f"no {self.file_type} available on {self.url}")

    def parse(self, raw_data):
        self.parser = self.parser_class(raw_data, self.file_type)
        self.links = self.parser.get_all_links(base=self.url)
        if not self.links:
            print(f"no {self.file_type} available on {self.url}")
            return
        for link in self.links:
            self.store(link)

    def store(self, link):
        self.storage.store(link)
