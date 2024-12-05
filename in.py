import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless mode (no UI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

driver = webdriver.Chrome(options=options)

url = "https://eyecannndy.com/"

driver.get(url)

try:
    ll = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "nav-animate-in"))
    )

    elements = driver.find_elements(By.XPATH, "//li[@class='nav-animate-in']/a")
    links = [ll.get_attribute("href") for ll in elements]
    print(links)
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.save_screenshot("headless_debug_screenshot.png")
    driver.quit()
