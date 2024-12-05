from selenium.webdriver.common.by import By
from selenium import webdriver, common
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from random import randint


class Extract:
    def __init__(self) -> None:
        self.base_url = "https://eyecannndy.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Content-Type": "application/json",
        }
        self.proxies = {"http": "http://131.0.226.198:9898"}

    def extract_technique_names(self):
        if driver := self._check_availability(self.base_url):
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "nav-animate-in"))
                )
                links = driver.find_elements(
                    By.XPATH, "//li[@class='nav-animate-in']/a"
                )
            except common.NoSuchElementException as err:
                raise Exception(err)
            else:
                techniques = [ll.get_attribute("href") for ll in links]
                return techniques

    def _check_availability(self, url):
        driver = self.get_driver()
        try:
            driver.get(url)
        except common.InvalidArgumentException as err:
            raise SystemExit(err)
        else:
            print(f"{url} page was found ")
            return driver

    def extract_technique_media(self):
        if driver := self.check_tecnique():
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "grid-item"))
                )
                links = driver.find_elements(
                    By.XPATH, "//*[contains(@class, 'grid-item')]/img"
                )
            except common.NoSuchElementException as err:
                raise Exception(err)
            else:
                media_links = [link.get_attribute("src") for link in links]
                return media_links

    def check_tecnique(self):
        techniques = self.extract_technique_names()
        get_random_num = randint(0, len(techniques))
        technique = techniques[get_random_num]

        if driver := self._check_availability(technique):
            return driver

    def get_driver(self):
        options = self._setup_driver_options()
        try:
            driver = webdriver.Chrome(options=options)
        except common.NoSuchDriverException as err:
            raise RuntimeError(err)
        else:
            return driver

    def _setup_driver_options(self):
        options = webdriver.ChromeOptions()

        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")

        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        return options
