from extractor import Extract
from download import Downloader
from random import randint
from collections import defaultdict
import logging
import time
from datetime import datetime, timedelta
import twitter_api
import os
from dotenv import load_dotenv

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
        self.technique = ""

    def download(self, name, media):
        downloader = Downloader(name, media)
        self.file_name = downloader.save_data()

    def extract_data(self):
        # get random technique name from the original techniques
        get_ran_technique_name = randint(0, len(self.techniques.keys()) - 1)
        technique_name = list(self.techniques.keys())[get_ran_technique_name]
        self.technique = technique_name

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

    def clean_up(self):
        if os.path.exists(f"{self.file_name}.gif"):
            os.remove(f"{main.file_name}.gif")
            os.remove(f"{main.file_name}.webp")

    def setup(self):
        extractor = Extract()
        extractor.extract()
        self.techniques = extractor.technique_names


main = Main()
main.setup()


def schedule_event(interval):
    next_time = datetime.now() + timedelta(seconds=interval)
    while True:
        current_time = datetime.now()
        pagination = (next_time - current_time).total_seconds()
        if pagination > 0:
            time.sleep(min(pagination, 5))
        else:
            main.repeat_event()
            twitter_api.post_media(technique=main.technique, file_name=main.file_name)
            main.clean_up()
            next_time = current_time + timedelta(seconds=interval)


schedule_event(20)
