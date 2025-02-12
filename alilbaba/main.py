import datetime
import time

import winsound
from alilbaba.requests import TrainRequestHandler

while True:
    request_handler = TrainRequestHandler(date=datetime.datetime.today() + datetime.timedelta(days=1), departure_time='15:00:00')
    tickets = request_handler.get_ticket_data()
    found_ticket = request_handler.is_ticket_available(tickets)

    if found_ticket:
        winsound.Beep(1000, 500)
    else:
        print("Ticket Not Found :(")

    time.sleep(20)
