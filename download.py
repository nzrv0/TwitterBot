import requests


class Downloader:
    def __init__(self, media, title) -> None:
        """
        Get data :
            media has the value {title: str: [*url: str], }
            title is the original title which provided from the extractor
        """
        self.media = media
        self.title = title

    def _get_data(self, data):
        try:
            response = requests.get(data)
        except requests.ConnectionError as err:
            raise SystemExit(err)
        else:
            yield response

    def save_data(self):
        data = self._get_data(self.media[self.title][0])

        with open(f"/static/{self.title}", "wb") as fs:
            fs.write(data)
