import os
import re
import subprocess
import time

from colorama import init, Fore
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def beep():
    try:
        os.system('beep -f 700 -l 1000')
    except Exception:
        print('\a')


class AlibabaCrawler:
    def __init__(self, date_str: str, username='mamf', QToT: bool = True):
        self.username = username
        self.date_str = date_str
        route = 'QUM-THR' if QToT else 'THR-QUM'
        self.BASE_URL = f'https://www.alibaba.ir/train/{route}?adult=1&child=0&infant=0&ticketType=Family&isExclusive=false&&departing={date_str}'

    def get_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument(
            f"user-data-dir=/home/{self.username}/.config/google-chrome"
        )
        chrome_options.add_argument("profile-directory=Default")
        return chrome_options

    def get_chrome_driver(self):
        # Automatically download and install the correct version of ChromeDriver
        driver_path = ChromeDriverManager().install()
        subprocess.call(["pkill", "chrome"])

        # Use the Service class to specify the driver path
        driver = webdriver.Chrome(service=Service(driver_path), options=self.get_chrome_options())
        return driver

    def scrapy_tickets_page(self) -> tuple[HtmlResponse, webdriver.Chrome]:
        driver = self.get_chrome_driver()
        driver.get(self.BASE_URL)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.last\\:mb-0'))
            )
        except Exception as e:
            print(e)

        url = self.BASE_URL
        scrapy_response = HtmlResponse(url=url, body=driver.page_source, encoding="utf-8")
        return scrapy_response, driver


class InteractTickets:
    def __init__(self, scrapy_response, driver, departure_times: list = (), order=1):
        self.scrapy = scrapy_response
        self.driver = driver
        self.departure_times = departure_times
        self.order = order

    def notify_user(self):
        beep()

    def choose_passenger(self):
        passengers_list_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '/html/body/div[1]/div[1]/main/form/div[3]/div/div[1]/div[1]/div/button'))
        )
        passengers_list_button.click()

        passenger_choose_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 f'/html/body/div[1]/div[2]/div/div/div/div[3]/table/tbody/tr[{self.order}]/td[4]/button'))
        )
        passenger_choose_button.click()

    def submit_ticket(self):
        submit_button = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div[1]/main/div/div/div/div/div[3]/button'
        )
        submit_button.click()

    def get_tickets(self):
        time.sleep(1)
        tickets: list = self.scrapy.css('.last\\:mb-0')
        return tickets

    def choose_ticket(self, ticket_index):
        choose_ticket_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.last\\:mb-0 button'))
        )
        choose_ticket_buttons[ticket_index].click()

    def get_first_desired_ticket(self) -> bool:
        tickets = self.get_tickets()

        for index, ticket in enumerate(tickets):
            ticket_time = ticket.css('.md\\:flex-row:nth-child(1) .font-bold::text').extract_first()
            print(ticket_time, 'ticket time')
            print(self.departure_times)
            if ticket_time in self.departure_times or len(self.departure_times) == 0:
                button = ticket.css('.last\\:mb-0 button').extract_first()
                if button:
                    self.choose_ticket(index)
                    self.choose_passenger()
                    self.submit_ticket()
                    self.notify_user()
                    return True
        return False


# Initialize colorama
init(autoreset=True)


def get_inputs_from_user():
    print(Fore.CYAN + 'Welcome to Alibaba Bot! 🚆')
    print(Fore.YELLOW + 'To use this bot, Chrome must be installed.')

    while True:
        date_pattern = r'^(?:1[34]\d{2})-(?:0?[1-9]|1[0-2])-(?:[0-2]?[0-9]|3[0-1])$'
        train_date = input(Fore.BLUE + '📅 Enter the departure date (e.g., 1403-12-12): ').strip()
        if not re.match(date_pattern, train_date):
            print(Fore.RED + "❌ Invalid date format. Use the format 1403-12-12.")
            continue

        time_pattern = r'^(?:[01]?\d|2[0-3]):[0-5]\d$'
        train_time = input(
            Fore.BLUE + '⏰ Enter departure time (15:00) or leave empty (comma-separated for multiple times): '
        ).strip()
        if train_time:
            times = [t.strip() for t in train_time.split(',')]
            if not all(re.match(time_pattern, t) for t in times):
                print(Fore.RED + "❌ Invalid time format. Use the format 15:00.")
                continue
        else:
            times = []

        qom_to_teh = input(Fore.BLUE + '🗺️ Enter the destination (Tehran or Qom): ').strip().lower()
        if qom_to_teh not in ['tehran', 'qom']:
            print(Fore.RED + "❌ Invalid destination. Choose either 'Tehran' or 'Qom'.")
            continue

        order = input(Fore.BLUE + 'Enter the order of your passenger: ')
        if order.isdigit():
            order = int(order)
        else:
            print(Fore.RED + "Please enter a valid integer.")
            continue

        username = input(Fore.MAGENTA + '👤 Enter your system username (e.g., ali): ').strip()
        qtot = (qom_to_teh == "tehran")
        print(Fore.GREEN + "\n✅ Inputs are valid! Processing your request...")
        return username, train_date, times, qtot, order


def search_for_ticket(username, t_date, t_times, QToT, order):
    crawler = AlibabaCrawler(QToT=QToT, date_str=t_date, username=username)
    scrapy_response, driver = crawler.scrapy_tickets_page()

    while True:
        scrapy_response = HtmlResponse(url='', body=driver.page_source, encoding="utf-8")
        interactor = InteractTickets(
            driver=driver, scrapy_response=scrapy_response, departure_times=t_times, order=order
        )
        is_done = interactor.get_first_desired_ticket()
        if is_done:
            # Wait 15 minutes before ending or re-checking
            time.sleep(15 * 60)
            break
        else:
            time.sleep(10)
            driver.refresh()


if __name__ == '__main__':
    username, t_date, t_times, qtot, order = get_inputs_from_user()

    print(Fore.MAGENTA + 'Attention:')
    time.sleep(1)
    print(Fore.YELLOW + 'Whenever the desired ticket is found, this sound will play for you:')
    time.sleep(1)
    beep()
    time.sleep(1)

    print(Fore.CYAN + 'Searching for your ticket...')
    time.sleep(1)
    print(Fore.GREEN + f'Date: {t_date}')
    print(Fore.GREEN + f'Time(s): {t_times}')
    print(Fore.BLUE + ('Qom-Tehran' if qtot else 'Tehran-Qom'))

    print(Fore.YELLOW + 'Please wait...')
    time.sleep(1)

    search_for_ticket(username=username, t_date=t_date, t_times=t_times, QToT=qtot, order=order)
