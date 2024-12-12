from selenium.webdriver.common.by import By
from selenium import webdriver, common
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from custom_logger import logger


class Extractor:
    def __init__(self) -> None:
        self.base_url = "https://eyecannndy.com"
        self.technique_names = {}

    def extract_technique_names(self):
        driver = self._check_availability(self.base_url)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "nav-animate-in"))
            )
            links = driver.find_elements(
                By.XPATH,
                "//li[@class='nav-animate-in']/a[contains(@href, '/technique')]",
            )
        except common.NoSuchElementException as err:
            logger.error(f"Element not found {err}")
            raise Exception(err)
        else:
            for link in links[:1]:
                technique = link.get_attribute("href").split("/")[-1]
                self.technique_names[technique] = [] + self.technique_names.get(
                    technique, []
                )
            logger.debug(
                f"Technique names has beend added: {list(self.technique_names.keys())}"
            )

    def _check_availability(self, url):
        driver = self.get_driver()
        try:
            driver.get(url)
            logger.debug(f"Connected to {url}")
        except common.InvalidArgumentException as err:
            logger.error(f"Url not found {err}")
            raise SystemExit(err)
        except common.TimeoutException as err:
            logger.error(f"Read timout error in {url}")
        else:
            return driver

    def extract_technique_media(self, technique_name):
        driver = self._check_availability(f"{self.base_url}/technique/{technique_name}")
        try:
            WebDriverWait(driver, 5, 1).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[contains(@class, 'grid-item')]/img[contains(@class, 'show-it')]",
                    )
                )
            )
            links = driver.find_elements(
                By.XPATH,
                "//*[contains(@class, 'grid-item')]/img[contains(@class, 'show-it')]",
            )
        except common.NoSuchElementException as err:
            logger.error(f"Element not found {err}")
            raise Exception(err)
        else:
            for link in links:
                media_link = link.get_attribute("src")
                self.technique_names[technique_name].append(media_link)

    def get_driver(self):
        options = self._setup_driver_options()
        try:
            driver = webdriver.Chrome(options=options)
        except common.NoSuchDriverException as err:
            logger.error(f"Driver not found {err}")
            raise RuntimeError(err)
        else:
            return driver

    def _setup_driver_options(self):
        options = webdriver.ChromeOptions()

        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")

        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        return options

    def extract(self):
        # get names of technique names
        self.extract_technique_names()

        # extranct the media links from the technique names
        for technique_name in self.technique_names.keys():
            self.extract_technique_media(technique_name)

        items_count = 0

        for value in self.technique_names.values():
            items_count += len(value)

        logger.info(
            f"Everything was worked fine: {len(self.technique_names.keys())} technique names was found and {items_count} media elements has getted."
        )
