from extractor import Extract
from download import Downloader
from random import randint


class Main:
    def __init__(self) -> None:
        self.techniques = {}
        self.extractor = Extract()

    def download(self, media, name):
        Downloader(media, name)

    def extract(self):
        names = self.extractor.extract_technique_names()
        random_name = names[randint(0, len(names) - 1)]
        media = self.extractor.extract_technique_media(technique=random_name)
        self.download(media, random_name)


test1 = Main().extract()
