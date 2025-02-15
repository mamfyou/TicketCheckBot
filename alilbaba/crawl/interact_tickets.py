import time

import winsound
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class InteractTickets:
    def __init__(self, scrapy, driver, departure_times: list = ()):
        self.scrapy = scrapy
        self.driver = driver
        self.departure_times = departure_times

    def notify_user(self):
        winsound.Beep(700, 1000)

    def choose_passenger(self, order: int = 1):
        passengers_list_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '/html/body/div[1]/div[1]/main/form/div[3]/div/div[1]/div[1]/div/button')
                                           ))
        passengers_list_button.click()

        passenger_choose_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            f'/html/body/div[1]/div[2]/div/div/div/div[3]/table/tbody/tr[{order}]/td[4]/button')
                                           ))

        passenger_choose_button.click()

    def submit_ticket(self):
        submit_button = self.driver.find_element(By.XPATH,
                                                 '/html/body/div[1]/div[1]/main/div/div/div/div/div[3]/button')
        submit_button.click()

    def get_tickets(self):
        time.sleep(1)
        tickets: list = self.scrapy.css('.last\\:mb-0')
        return tickets

    def choose_ticket(self, ticket_index):
        choose_ticket_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.last\\:mb-0 button'))
        )
        choose_ticket_button = choose_ticket_buttons[ticket_index]
        choose_ticket_button.click()

    def get_first_desired_ticket(self) -> bool:
        tickets = self.get_tickets()

        for index, ticket in enumerate(tickets):
            ticket_time = ticket.css('.md\\:flex-row:nth-child(1) .font-bold::text').extract_first()
            if ticket_time in self.departure_times:
                button = ticket.css('.last\\:mb-0 button').extract_first()
                if button:
                    self.choose_ticket(index)

                    self.choose_passenger(order=2)

                    self.submit_ticket()

                    self.notify_user()
                    return True

        return False
