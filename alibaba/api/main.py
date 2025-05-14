import datetime
import time

import winsound
from alibaba.api.requests import TrainRequestHandler


def main():
    while True:
        request_handler = TrainRequestHandler(date=datetime.datetime.today() + datetime.timedelta(days=1),
                                              departure_time='15:00:00')
        tickets = request_handler.get_ticket_data()
        found_ticket = request_handler.is_ticket_available(tickets)

        if found_ticket:
            print("Found the ticket :)")
            winsound.Beep(800, 2000)
        else:
            print("Ticket Not Found :(")

        time.sleep(20)


if __name__ == '__main__':
    main()
