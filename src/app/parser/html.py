from bs4 import BeautifulSoup
from ..enums import FileTypeEnums


class BaseParser:
    _links = []
    parser = BeautifulSoup
    _parser_type = 'html.parser'
    _file_type = None
 
    def __init__(self, raw_data) -> None:
        self._parse(raw_data)

    def _parse(self, raw_data):
        return

    def get_all_links(self, base=None):
        links = []
        for link in self._links:
            if 'http' not in link and base:
                links.append(f"{base}{link}")
            else:
                links.append(link)
        return links


class LinkedParser(BaseParser):
    _file_type = FileTypeEnums.PDF.value

    def _parse(self, raw_data):
        if not self._file_type:
            return
        self.soup = self.parser(raw_data, self._parser_type)
        for link in  self.soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith(self._file_type) and href not in self._links:
                self._links.append(link.get('href'))


class ImageParser(BaseParser):
    elements = ['img', 'source']
    attributes = ['src', 'data-src', 'srcset']
    _file_type = [FileTypeEnums.PNG.value, FileTypeEnums.JPG.value, FileTypeEnums.WEBP.value]

    def _parse(self, raw_data):
        if not self._file_type:
            return
        self.soup = self.parser(raw_data, self._parser_type)
        for element in self.elements:
            for link in self.soup.find_all(element):
                for attribute in self.attributes:
                    if not link.get(attribute):
                        continue
                    href = link.get(attribute)
                    if isinstance(self._file_type, list):
                        for ext in self._file_type:
                            if href and href not in self._links:
                                self._links.append(href)
                    else:
                        if href and href.endswith(self._file_type) and href not in self._links:
                            self._links.append(href)


class PngParser(ImageParser):
    _file_type = FileTypeEnums.PNG.value


class JpgParser(ImageParser):
    _file_type = FileTypeEnums.JPG.value


class DefaultParser(BaseParser):

    def get_all_links(self, base=None):
        return []


class ParserHandler:

    def __init__(self, raw_data, type) -> None:
        self.type = type
        self.raw_data = raw_data

    def get_parser(self):
        if self.type == FileTypeEnums.PDF.value:
            return LinkedParser(self.raw_data)
        elif self.type == FileTypeEnums.PNG.value:
            return PngParser(self.raw_data)
        elif self.type == FileTypeEnums.JPG.value:
            return JpgParser(self.raw_data)
        elif self.type == FileTypeEnums.IMG.value:
            return ImageParser(self.raw_data)
        else:
            return DefaultParser(self.raw_data)
