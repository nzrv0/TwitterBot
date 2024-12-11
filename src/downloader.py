from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from PIL import Image
import logging


class Downloader:
    def __init__(self, technique_name, media_url) -> None:
        self.technique_name = technique_name
        self.media_url = media_url

    def _get_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
        req = Request(url=self.media_url, method="GET", headers=headers)
        try:
            with urlopen(req) as res:
                yield res.read()

        except URLError as err:
            logging.error(f"Please provide correct url {err}")
            raise Exception(err)
        except HTTPError as err:
            logging.error(f"Connection error {err}")
            raise Exception(err)

    def save_data(self):
        id = self.media_url.split("/")[-1].split(".")[0]
        file_name = f"data/{self.technique_name}-{id}"

        with open(f"{file_name}.webp", "wb") as fs:
            for data in self._get_data():
                fs.write(data)
        logging.info(f"File has downloaded: {file_name}")
        self._convert_format(file_name)
        return file_name

    def _convert_format(self, file_name):
        im = Image.open(f"{file_name}.webp")
        im.info.pop("background", None)
        im.save(f"{file_name}.gif", "gif", save_all=True)
        logging.info(f"File has been converted to gif format from webp")
