import base64
import json
from datetime import datetime

import httpx


class TrainRequestHandler:
    def __init__(self, date=datetime.today(), from_city=1, to_city=161, departure_time=None):
        self.date = date
        self.from_city = from_city
        self.to_city = to_city
        self.departure_time = departure_time

    def prepare_request_data(self):
        data = {'From': self.from_city,
                'To': self.to_city,
                'DepartureDate': self.date.strftime('%Y-%m-%d') + 'T00:00:00',
                'TicketType': 1,
                'IsExclusiveCompartment': False,
                'PassengerCount': 1,
                'ReturnDate': None,
                'ServiceType': None,
                'Channel': 1,
                'AvailableTargetType': None,
                'Requester': None,
                'UserId': 501936975,
                'OnlyWithHotel': False,
                'ForceUpdate': None
                }
        json_data = json.dumps(data)
        encoded_data = base64.b64encode(json_data.encode('utf-8'))
        return encoded_data.decode()

    def get_request_headers(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        return headers

    def get_ticket_data(self):
        data = self.prepare_request_data()
        url = 'https://ws.alibaba.ir/api/v2/train/available/' + data
        print(url)
        response = httpx.get(url, headers=self.get_request_headers(), timeout=15)
        try:
            return response.json()['result']['departing']
        except Exception as e:
            print(response.text)
            return []

    def get_date_from_date_string(self, date_str):
        datetime_obj = datetime.fromisoformat(date_str)
        return datetime_obj

    def is_ticket_available(self, tickets):
        for ticket in tickets:
            if ticket['seat'] > 0:
                if self.departure_time:
                    if self.get_date_from_date_string(ticket['departureDateTime']).time() == self.departure_time:
                        return ticket
                else:
                    return ticket
        return None
