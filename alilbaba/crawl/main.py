import time

from colorama import init, Fore
from scrapy.http import HtmlResponse

from alilbaba.crawl.crawler import AlibabaCrawler
from alilbaba.crawl.helper import Notifier
from alilbaba.crawl.input_handler import UserInputHandler
from alilbaba.crawl.interact_tickets import InteractTickets

init(autoreset=True)


def search_for_ticket(username, t_date, t_time, is_qom_to_teh, order):
    crawler = AlibabaCrawler(is_qom_to_teh=is_qom_to_teh, date_str=t_date, user_name=username)
    scrapy, driver = crawler.scrapy_tickets_page()

    while True:
        scrapy = HtmlResponse(url='', body=driver.page_source, encoding="utf-8")
        interactor = InteractTickets(driver=driver, scrapy=scrapy, departure_times=t_time, order_of_passenger=order)
        is_done = interactor.get_first_desired_ticket()

        if is_done:
            time.sleep(15 * 60)
            break

        time.sleep(10)
        driver.refresh()


if __name__ == '__main__':
    inputs = UserInputHandler()
    username, t_date, t_time, is_qom_to_teh, order = inputs.get_inputs()

    print(Fore.MAGENTA + 'Attention:')
    time.sleep(1)
    print(Fore.YELLOW + 'Whenever the desired ticket is found, this sound will play for you:')
    time.sleep(1)
    Notifier.beep()
    time.sleep(1)

    print(Fore.CYAN + 'Searching for your ticket...')
    time.sleep(1)
    print(Fore.GREEN + f'Date: {t_date}')
    print(Fore.GREEN + f'Time: {t_time}')
    print(Fore.BLUE + ('Qom-Tehran' if is_qom_to_teh else 'Tehran-Qom'))

    print(Fore.YELLOW + 'Please wait...')
    time.sleep(1)
    print(Fore.GREEN + 'Bot Waits for 30 seconds for you to login to website')
    print(Fore.GREEN + 'And after that the crawling will begin')
    time.sleep(3)

    search_for_ticket(username=username, t_date=t_date, t_time=t_time, is_qom_to_teh=is_qom_to_teh, order=order)
