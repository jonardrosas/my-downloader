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
        if not self._file_type:
            return
        self.soup = self.parser(raw_data, self._parser_type)
        import pdb; pdb.set_trace()
        for link in  self.soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith(self._file_type) and href not in self._links:
                self._links.append(link.get('href'))

    def get_all_links(self, base=None):
        if base:
            return [
                f"{base}{link}" for link in self._links
            ]
        return self._links


class LinkedParser(BaseParser):
    _file_type = FileTypeEnums.PDF.value


class PngParser(BaseParser):
    _file_type = FileTypeEnums.PNG.value


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
        else:
            return DefaultParser(self.raw_data)

        