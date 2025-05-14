import os
import time

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class AlibabaCrawler:
    def __init__(self, date_str: str, user_name: str = 'mamf', is_qom_to_teh: bool = True):
        self.username = user_name
        self.date_str = date_str
        route = 'QUM-THR' if is_qom_to_teh else 'THR-QUM'
        self.BASE_URL = (f'https://www.alibaba.ir/train/{route}'
                         f'?adult=1&child=0&infant=0&ticketType=Family&isExclusive=false&&departing={date_str}')

    def get_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir=C:/Users/{self.username}/AppData/Local/Google/Chrome/User Data/Profile 1")
        chrome_options.add_argument("profile-directory=Default")
        return chrome_options

    def get_chrome_driver(self):
        driver_path = ChromeDriverManager().install()
        os.system("taskkill /im chrome.exe /f")
        driver = webdriver.Chrome(service=Service(driver_path), options=self.get_chrome_options())
        return driver

    def scrapy_tickets_page(self) -> tuple[HtmlResponse, webdriver.Chrome]:
        driver = self.get_chrome_driver()
        driver.get(self.BASE_URL)
        time.sleep(30)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.last\\:mb-0'))
            )
        except Exception as e:
            print(e)

        url = self.BASE_URL
        scrapy = HtmlResponse(url=url, body=driver.page_source, encoding="utf-8")
        return scrapy, driver
