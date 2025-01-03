from extractor import Extractor
from downloader import Downloader
from random import randint
from custom_logger import logger
import time
import twitter_api
import os
import json


class Main:
    def __init__(self) -> None:
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

    def _repeat_event(self):
        media_link = self.extract_data()
        self.download(name=self.technique_name, media=media_link)
        self.techniques[self.technique_name].remove(media_link)
        self.save_json()

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
