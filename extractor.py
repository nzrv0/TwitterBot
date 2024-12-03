import requests
from bs4 import BeautifulSoup


class Extract:
    def __init__(self) -> None:
        pass

    @property
    def base_url(self):
        return "https://eyecannndy.com/"

    def extract_techniques(self):
        url = self.base_url()
        if response := self.check_aviablitiy(url):
            extractor = self.extract_html(response)
            links = extractor.find_all(
                "a", attrs=lambda x: x and x[0].startswith("/technique")
            )

    def check_aviablitiy(self, url):
        try:
            response = requests.get(url=url)
        except requests.HTTPError as err:
            raise SystemExit(err)
        else:
            print(f"Succsesufly connected {response}")
            return response

    def check_tecnique(self):
        techniques = self.base_url() + "technique/"

        pass

    def extract_html(self, html_page):
        bs4 = BeautifulSoup(html_page, "html.parser")
        return bs4
