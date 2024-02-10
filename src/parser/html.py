from bs4 import BeautifulSoup


class HtmlParser():
    parser = BeautifulSoup
    _links = []
    _parser_type = 'html.parser'

    def __init__(self, raw_data, file_type) -> None:
        self._file_type = file_type
        self._parse(raw_data)

    def _parse(self, raw_data):
        self.soup = self.parser(raw_data, self._parser_type)
        for link in  self.soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith(self._file_type) and href not in self._links:
                self._links.append(link.get('href'))

    def get_parsed_data(self):
        return self.soup.title

    def get_all_links(self, base=None):
        if base:
            return [
                f"{base}{link}" for link in self._links
            ]
        return self._links


        