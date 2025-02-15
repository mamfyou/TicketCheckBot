import time

from alilbaba.crawl.crawler import AlibabaCrawler
from alilbaba.crawl.interact_tickets import InteractTickets


def search_for_ticket(QToT=True):
    channels_list = set()

    crawler = AlibabaCrawler(QToT=QToT)
    scrapy, driver = crawler.scrapy_tickets_page()

    interactor = InteractTickets(driver=driver, scrapy=scrapy)

    while True:
        is_done = interactor.get_first_desired_ticket()
        if is_done:
            break
        else:
            time.sleep(10)
            driver.refresh()


if __name__ == '__main__':
    search_for_ticket(QToT=False)
