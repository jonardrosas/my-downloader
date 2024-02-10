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
    _output_path = "output"

    def __init__(self, file_type, url, output_path=None):
        self.file_type = file_type
        self.url = url
        if output_path:
            self._output_path = output_path
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
            folder_name = path.split('/')[-1]
            output_folder = os.path.join(self._output_path, folder_name)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            output_path = os.path.join(output_folder, file)
            with open(output_path, 'wb') as output_file:
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
    parser.add_argument('--output', help="Ouput path where you want to store")
    args = parser.parse_args()
    ext = args.input
    url = args.url
    output_path = args.output
    app = AppDownloader(ext, url, output_path=output_path)
    app.download()


if __name__ == '__main__':
    run()