from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from PIL import Image
from custom_logger import logger
import os


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
            logger.error(f"Please provide correct url {err}")
            raise Exception(err)
        except HTTPError as err:
            logger.error(f"Connection error {err}")
            raise Exception(err)

    def save_data(self):
        id = self.media_url.split("/")[-1].split(".")[0]
        file_name = f"data/{self.technique_name}-{id}"

        with open(f"{file_name}.webp", "wb") as fs:
            for data in self._get_data():
                fs.write(data)
        logger.info(f"File has downloaded: {file_name}.webp")
        self._convert_format(file_name)
        return file_name

    def _convert_format(self, file_name):

        im = Image.open(f"{file_name}.webp")
        im.info.pop("background", None)

        create_file = f"{file_name}.gif"
        im.save(create_file, "gif", save_all=True)
        logger.info(f"File has been converted to gif format from webp: {create_file}")

        info = os.stat(create_file).st_size
        bytes_to_mb = round(info * 10**-6)
        if bytes_to_mb >= 15:
            im.save(create_file, "gif", save_all=True, quality=50)
            logger.warning(
                f"reduced quality of {create_file} file due large size : {bytes_to_mb}mb size"
            )
