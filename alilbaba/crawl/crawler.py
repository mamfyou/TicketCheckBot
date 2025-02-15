import datetime
import os

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from persiantools.jdatetime import JalaliDate


class AlibabaCrawler:
    def __init__(self, username='mamf',
                 date_str: str = datetime.datetime.now().strftime('%Y-%m-%d'),
                 QToT: bool = True):
        self.username = username
        self.date_str = date_str
        date = self.get_jalali_date_from_gregorian()
        route = 'QUM-THR' if QToT else 'THR-QUM'
        self.BASE_URL = f'https://www.alibaba.ir/train/{route}?adult=1&child=0&infant=0&ticketType=Family&isExclusive=false&&departing={date}'

    def get_jalali_date_from_gregorian(self):
        year, month, day = map(int, self.date_str.split("-"))
        jalali_date = JalaliDate.to_jalali(year, month, day)
        return jalali_date

    def get_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir=C:/Users/{self.username}/AppData/Local/Google/Chrome/User Data")
        chrome_options.add_argument("profile-directory=Default")
        return chrome_options

    def get_chrome_driver(self):
        os.system("taskkill /im chrome.exe /f")
        driver = webdriver.Chrome(options=self.get_chrome_options())
        return driver

    def scrapy_tickets_page(self) -> tuple[HtmlResponse, WebDriver]:
        driver = self.get_chrome_driver()
        driver.get(self.BASE_URL)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.last\\:mb-0'))
            )
        except Exception as e:
            print(e)

        url = self.BASE_URL
        scrapy = HtmlResponse(url=url, body=driver.page_source, encoding="utf-8")
        return scrapy, driver
