from extractor import Extract
from download import Downloader
from random import randint
from collections import defaultdict
import logging
import time
from datetime import datetime, timedelta
import psutil
import twitter_api


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p",
    filename="app.log",
    filemode="a",
    encoding="utf-8",
)


class Main:
    def __init__(self) -> None:
        self.old_data = defaultdict(list)
        self.techniques = {}
        self.file_name = ""

    def download(self, name, media):
        downloader = Downloader(name, media)
        self.file_name = downloader.save_data()
        print(self.file_name)

    def extract_data(self):
        # get random technique name from the original techniques
        get_ran_technique_name = randint(0, len(self.techniques.keys()) - 1)
        technique_name = list(self.techniques.keys())[get_ran_technique_name]

        # get random media link from the original tehcnique
        technique_medias = self.techniques[technique_name]
        get_ran_technique_media = randint(0, len(technique_medias) - 1)
        media_link = technique_medias[get_ran_technique_media]

        return technique_name, media_link

    def repeat_event(self):
        technique_name, media_link = self.extract_data()
        # add to old data to check later for not getting same data twice
        if media_link not in self.old_data[technique_name]:
            self.download(name=technique_name, media=media_link)
            self.old_data[technique_name].append(media_link)

    def setup(self):
        extractor = Extract()
        extractor.extract()
        self.techniques = extractor.technique_names


main = Main()
main.setup()


def schedule_event(interval):
    while True:
        print("this works")
        # next_time = datetime.now() + timedelta(seconds=interval)
        # current_time = datetime.now()
        # if current_time >= next_time:
        main.repeat_event()
        twitter_api.post_media(name=main.file_name)
        # next_time = current_time + timedelta(seconds=interval)
        time.sleep(interval)


schedule_event(80)
