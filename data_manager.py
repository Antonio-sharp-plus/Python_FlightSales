from pprint import pprint
import requests

from flight_search import FlightSearch
from flight_data import FlightData

import os
from dotenv import load_dotenv

load_dotenv()


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_header = os.getenv('SHEETY_BASICAUTHORIZATION_HEADER')
        self.sheety_bearer = os.getenv('SHEETY_BEARER')
        self.url = "https://api.sheety.co/12659492d89ac84c788d62902763dfd0/flightDeals/prices"

        self.flight_search = FlightSearch()
        self.flight_data = FlightData()

    def read_sheet(self):
        headers = {
            'Authorization': self.sheety_bearer
        }

        response = requests.get(self.url, headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP errors

        data = response.json()
        return data['prices']

    def update_iata_codes(self):
        flight_data = self.read_sheet()
        city_name = [item['city'] for item in flight_data]


        iata_codes = []
        for i in city_name:
            search_result = self.flight_search.find_iata_codes(keyword=i)
            iata_codes.append(search_result)
        print(iata_codes)

        row = 2

        headers = {
            'Authorization': self.sheety_bearer,
            "Content-Type": "application/json"
        }
        print(self.sheety_bearer)
        payload = {
            "price": {
                "iataCode": ''
            }
        }

        for i in iata_codes:
            new_url = f"https://api.sheety.co/12659492d89ac84c788d62902763dfd0/flightDeals/prices/{row}"
            payload["price"]["iataCode"] = i

            response = requests.put(new_url, json=payload, headers=headers)
            response.raise_for_status()  # Raises an exception for HTTP errors

            row += 1

        flight_data = self.read_sheet()
        pprint(flight_data)

    def update_prices(self):
        flight_data = self.read_sheet()
        iata_codes = [item['iataCode'] for item in flight_data]
        cheapest_found = []

        for i in iata_codes:
            search_result = self.flight_search.find_sales("EZE", i, '2026-01-10', 1)
            lowest_price = self.flight_data.formatCheapFlight(search_result)
            cheapest_found.append(lowest_price)
        print(cheapest_found)

        row = 2

        headers = {
            'Authorization': self.sheety_bearer,
            "Content-Type": "application/json"
        }
        print(self.sheety_bearer)
        payload = {
            "price": {
                "lowestPrice": ''
            }
        }

        for i in cheapest_found:
            new_url = f"https://api.sheety.co/12659492d89ac84c788d62902763dfd0/flightDeals/prices/{row}"
            payload["price"]["lowestPrice"] = i

            response = requests.put(new_url, json=payload, headers=headers)
            response.raise_for_status()  # Raises an exception for HTTP errors

            row += 1

        flight_data = self.read_sheet()
        pprint(flight_data)
    def small_test(self):
        headers = {
            'Authorization': self.sheety_bearer,
            "Content-Type": "application/json"
        }

        json = {
            "price": {
                "iataCode": 'PAR'
            }
        }

        new_url = f"https://api.sheety.co/12659492d89ac84c788d62902763dfd0/flightDeals/prices/2"
        response = requests.put(new_url, json=json, headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP errors


datas = DataManager()
datas.update_prices()

