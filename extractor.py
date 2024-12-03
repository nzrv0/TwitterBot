import requests
from bs4 import BeautifulSoup


class Extract:
    def __init__(self) -> None:
        self.base_url = "https://eyecannndy.com/"

    def extract_technique_names(self):
        if response := self._check_availability(self.base_url):
            extractor = self._extract_html(response)
            all_techniques = extractor.find_all(
                "a", attrs=lambda x: x and x[0].startswith("/technique")
            )
            all_techniques = [link.get_text().lower() for link in all_techniques]
            return all_techniques

    def _check_availability(self, url):
        try:
            response = requests.get(url=url)
        except requests.HTTPError as err:
            raise SystemExit(err)
        else:
            print(f"Succsesufly connected {response}")
            return response

    def extract_technique_media(self, technique):
        assets = "https://asset.eyecannndy.com/"
        if extractor := self._check_tecnique(technique):
            extracted = extractor.find_all(
                "img", attrs=lambda x: x and x[0].startswith(assets)
            )
            return extracted

    def _check_tecnique(self, technique):
        technique_url = self.base_url + f"technique/{technique}"
        if response := self._check_availability(technique_url):
            extractor = self._extract_html(response)
            return extractor

    def _extract_html(self, html_page):
        bs4 = BeautifulSoup(html_page, "html.parser")
        return bs4
