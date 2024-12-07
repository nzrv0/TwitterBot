from extractor import Extract
from download import Downloader
from random import randint
from collections import defaultdict
import logging
import time
from datetime import datetime, timedelta
import asyncio

logging.basicConfig()
schedule_logger = logging.getLogger("schedule")
schedule_logger.setLevel(level=logging.DEBUG)


class Main:
    def __init__(self) -> None:
        self.old_data = defaultdict(list)
        self.extractor = Extract()
        self.downloader = Downloader

    def download(self, name, media):
        nn = self.downloader(name, media)
        nn.save_data()

    def extract_data(self):
        techniques = self.extractor.technique_names
        # get random technique name from the original techniques
        get_ran_technique_name = randint(0, len(techniques.keys()) - 1)
        technique_name = list(techniques.keys())[get_ran_technique_name]

        # get random media link from the original tehcnique
        technique_medias = techniques[technique_name]
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
        self.extractor.extract()


main = Main()
main.setup()


async def schedule_event(interval):

    while True:
        await asyncio.sleep(5)
        main.repeat_event()

    # main.repeat_event()
    # next_time = datetime.now() + timedelta(seconds=interval)

    # while True:

    #     current_time = datetime.now()
    #     if current_time >= next_time:
    #         main.repeat_event()
    #         next_time = current_time + timedelta(seconds=interval)

    #     time.sleep(20)


asyncio.run(schedule_event(2))
