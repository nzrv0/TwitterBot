from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


class Downloader:
    def __init__(
        self,
        name,
        media,
    ) -> None:
        """
        Get data :
            media has the value {name: [*url: str], }
            name is the original technique name which provided from the extractor
        """
        self.name = name
        self.media = media

    def _get_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
        req = Request(url=self.media, method="GET", headers=headers)
        try:
            with urlopen(req) as res:
                yield res.read()
        except URLError as err:
            raise Exception(err)

    def save_data(self):
        id = self.media.split("/")[-1].split(".")[0]
        # data = self._get_data()
        file_name = f"static/{self.name}-{id}.webp"
        with open(f"{file_name}", "wb") as fs:
            for data in self._get_data():
                fs.write(data)
        return file_name
