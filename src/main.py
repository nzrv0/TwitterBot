from extractor import Extractor
from downloader import Downloader
from random import randint
from collections import defaultdict
from custom_logger import logger
import time
from datetime import datetime, timedelta
import twitter_api
import os
import asyncio


class Main:
    def __init__(self) -> None:
        self.old_data = defaultdict(list)
        self.techniques = {}
        self.file_name = ""
        self.technique_name = ""

    def download(self, name, media):
        downloader = Downloader(name, media)
        self.file_name = downloader.save_data()

    def extract_data(self):
        # get random technique name from the original techniques
        get_ran_technique_name = randint(0, len(self.techniques.keys()) - 1)
        technique_name = list(self.techniques.keys())[get_ran_technique_name]
        self.technique_name = technique_name

        # get random media link from the original tehcnique
        technique_medias = self.techniques[technique_name]
        get_ran_technique_media = randint(0, len(technique_medias) - 1)
        media_link = technique_medias[get_ran_technique_media]

        return media_link

    def _repeat_event(self):
        media_link = self.extract_data()

        # add to old data to check later for not getting same data twice
        if media_link not in self.old_data[self.technique_name]:
            self.download(name=self.technique_name, media=media_link)
            self.old_data[self.technique_name].append(media_link)

    async def schedule_event(self, interval):
        next_time = datetime.now() + timedelta(seconds=interval)
        while True:
            current_time = datetime.now()
            pagination = (next_time - current_time).total_seconds()
            if pagination > 0:
                time.sleep(min(pagination, 5))
            else:
                self._repeat_event()

                post_media = await twitter_api.post_media(
                    technique=self.technique_name, file_name=self.file_name
                )
                clean_up = await self._clean_up()
                await asyncio.gather(post_media, clean_up)
                logger.info(f"Next twitte post in {interval} hours")
                next_time = current_time + timedelta(seconds=interval)

    async def _clean_up(self):
        await asyncio.sleep(2)
        if os.path.exists(f"{self.file_name}.gif"):
            os.remove(f"{self.file_name}.gif")
            os.remove(f"{self.file_name}.webp")

    def setup(self):
        try:
            logger.info("Extractor has been started")
            extractor = Extractor()
            extractor.extract()
            self.techniques = extractor.technique_names
            # await self.schedule_event(20)
            asyncio.run(self.schedule_event(20))
        except RuntimeError as err:
            logger.error(f"Stopped due to: {err}")
        except KeyboardInterrupt as err:
            logger.error(f"User stopped program")


Main().setup()
