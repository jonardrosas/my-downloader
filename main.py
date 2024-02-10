import argparse
import os
from src.enums import FileTypeEnums
from src.exceptions import InvalidFormat, NoDownloader
from src.downloaders.pdf import PDFDownloader
from src.parser.html import HtmlParser

import requests



class Handler():

    def __init__(self, file_type):
        self._file_type = file_type
        
    def handle(self, url):
        if self._file_type == FileTypeEnums.PDF.value:
            return PDFDownloader(url)
        raise NoDownloader(f"No downloader for specified {self._file_type} format")


class AppDownloader():
    downloader = None
    handler = Handler
    parser_class =  HtmlParser
    output = "output"

    def __init__(self, file_type, url):
        self.file_type = file_type
        self.url = url
        self.is_valid = self._is_valid_format(file_type)
        if not self.is_valid:
            raise InvalidFormat('Not a registered extension')
        self.handle()

    def handle(self):
        self.downloader = self.handler(self.file_type).handle(self.url)

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
            path, file = os.path.split(link)
            output_file = os.path.join(self.output, file)
            with open(output_file, 'wb') as output_file:
                r = requests.get(link)
                for chunk in r.iter_content(chunk_size=128):
                    output_file.write(chunk)
            print(self.links)

    def _is_valid_format(self, format):
        for _format in FileTypeEnums:
            if _format.value == format:
                return True
        return False

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="Input file extension you want to download", choices=[FileTypeEnums.PDF.value])
    parser.add_argument('url', help="Url link", type=str)
    args = parser.parse_args()
    ext = args.input
    url = args.url
    app = AppDownloader(ext, url)
    app.download()


if __name__ == '__main__':
    run()