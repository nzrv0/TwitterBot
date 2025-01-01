from extractor import Extractor
from downloader import Downloader
from random import randint
from collections import defaultdict
from custom_logger import logger
import time
from datetime import datetime, timedelta
import twitter_api
import os
import json


class Main:
    def __init__(self) -> None:
        self.old_data = defaultdict(list)
        self.techniques = {}
        self.file_name = ""
        self.technique_name = ""
        self.json_file_name = "extracted.json"

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

    def save_json(self):
        try:
            with open("extracted.json", "w") as fs:
                json.dump(self.techniques, fs)
        except Exception as err:
            raise Exception(err)
        else:
            logger.debug("Data converted to json file")

    def save_old_to_json(self):
        try:
            with open("old_uploads.json", "w") as fs:
                json.dump(self.old_data, fs)
        except Exception as err:
            raise Exception(err)
        else:
            logger.debug("Old uploded data has been inserted to json file")

    def _repeat_event(self):
        try:
            with open("old_uploads.json") as fs:
                self.old_data = json.load(fs)
        except Exception as err:
            raise Exception(err)
        else:
            media_link = self.extract_data()

            # add to old data to check later for not getting same data twice
            if media_link not in self.old_data[self.technique_name]:
                self.download(name=self.technique_name, media=media_link)
                self.old_data[self.technique_name].append(media_link)
                self.save_old_to_json()

    # def schedule_event(self, interval):
    #     next_time = datetime.now() + timedelta(seconds=interval)
    #     while True:
    #         current_time = datetime.now()
    #         pagination = (next_time - current_time).total_seconds()
    #         if pagination < 0:
    #             self._repeat_event()

    #             twitter_api.post_media(
    #                 technique=self.technique_name, file_name=self.file_name
    #             )
    #             self._clean_up()
    #             logger.info(f"Next twitte post in {interval} hours")
    #             next_time = current_time + timedelta(seconds=interval)
    #         else:

    #             time.sleep(min(pagination, 5))

    def schedule_event(self):
        self._repeat_event()
        twitter_api.post_media(technique=self.technique_name, file_name=self.file_name)
        self._clean_up()

    def _clean_up(self):
        time.sleep(3)
        if os.path.exists(f"{self.file_name}.gif"):
            os.remove(f"{self.file_name}.gif")
            os.remove(f"{self.file_name}.webp")
            logger.debug(
                f"File {self.file_name}.gif and {self.file_name}.webp has been deleted"
            )

    def _clean_all(self):
        media_elements = os.listdir("data")
        if len(media_elements) > 0:
            for elem in os.listdir("data"):
                os.remove(f"data/{elem}")
            logger.warning("Every data cleaned due to uncompleated program execution")

    def setup(self):
        try:
            if not os.path.exists(self.json_file_name):
                logger.info("Extractor has been started")
                extractor = Extractor()
                extractor.extract()
                self.techniques = extractor.technique_names
                self.save_json()
            else:
                with open(self.json_file_name) as fs:
                    self.techniques = json.load(fs)

        except RuntimeError as err:
            logger.error(f"Stopped due to: {err}")

        except Exception as err:
            logger.error(f"Program stopped running {err}")

        except:
            self._clean_all()

        else:
            self.schedule_event()


Main().setup()
