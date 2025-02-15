import time

from scrapy.http import HtmlResponse

from alilbaba.crawl.crawler import AlibabaCrawler
from alilbaba.crawl.interact_tickets import InteractTickets

DEPARTURE_TIMES = ['15:00']
DATE = '1403-12-10'


def search_for_ticket(QToT=True):
    crawler = AlibabaCrawler(QToT=QToT, date_str=DATE)
    scrapy, driver = crawler.scrapy_tickets_page()

    while True:
        scrapy = HtmlResponse(url='', body=driver.page_source, encoding="utf-8")
        interactor = InteractTickets(driver=driver, scrapy=scrapy, departure_times=DEPARTURE_TIMES)
        is_done = interactor.get_first_desired_ticket()
        if is_done:
            print('done')
            time.sleep(15 * 60)
            break
        else:
            time.sleep(10)
            driver.refresh()


if __name__ == '__main__':
    search_for_ticket(QToT=False)
