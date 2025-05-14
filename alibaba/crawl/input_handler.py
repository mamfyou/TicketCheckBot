import re

from colorama import Fore


class UserInputHandler:
    def get_inputs(self):
        print(Fore.CYAN + 'Welcome to Alibaba Bot! 🚆')
        print(Fore.YELLOW + 'To use this bot, Chrome must be installed.')

        date = self.get_date_input()
        times = self.get_time_input()
        is_qom_to_teh = self.get_route_input()
        order = self.get_passenger_order()

        print(Fore.GREEN + "\n✅ Inputs are valid! Processing your request...")
        return date, times, is_qom_to_teh, order

    def get_date_input(self):
        while True:
            date_pattern = r'^(?:1[34]\d{2})-(?:0?[1-9]|1[0-2])-(?:[0-2]?[0-9]|3[0-1])$'
            date = input(Fore.BLUE + '📅 Enter the departure date (e.g., 1403-12-12): ').strip()
            if re.match(date_pattern, date):
                return date
            print(Fore.RED + "❌ Invalid date format. Use the format 1403-12-12.")

    def get_time_input(self):
        while True:
            time_str = input(
                Fore.BLUE + '⏰ Enter departure time (15:00) or leave empty (comma-separated for multiple times): '
            ).strip()
            if not time_str:
                return []

            times = [t.strip() for t in time_str.split(',')]
            time_pattern = r'^(?:[01]?\d|2[0-3]):[0-5]\d$'

            if all(re.match(time_pattern, t) for t in times):
                return times

            print(Fore.RED + "❌ Invalid time format. Use the format 15:00.")

    def get_route_input(self):
        while True:
            direction = input(Fore.BLUE + '🗺️ Enter the destination (Tehran or Qom): ').strip().lower()
            if direction in ['tehran', 'qom']:
                return direction == 'tehran'
            print(Fore.RED + "❌ Invalid destination. Choose either 'Tehran' or 'Qom'.")

    def get_passenger_order(self):
        while True:
            order = input(Fore.BLUE + 'Enter the order of your passenger: ')
            if order.isdigit():
                return int(order)
            print(Fore.RED + "Please enter a valid integer.")