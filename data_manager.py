from pprint import pprint
import requests
from datetime import datetime

from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

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
        self.twilio_helper = NotificationManager()

        self.sheet_info = self.read_sheet()

    def read_sheet(self):
        headers = {
            'Authorization': self.sheety_bearer
        }

        response = requests.get(self.url, headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP errors

        data = response.json()
        for i, value in enumerate(data['prices']):
            print(f"i: {i} - value: {value}")
        return data['prices']

    def update_iata_codes(self):
        city_name = [item['city'] for item in self.sheet_info]

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
        iata_codes = [item['iataCode'] for item in self.sheet_info]
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

        updated_data = self.read_sheet()
        pprint(updated_data)

    def check_for_deals(self):
        iata_codes = [item['iataCode'] for item in self.sheet_info]

        for i, value in enumerate(self.sheet_info):
            search_result = self.flight_search.find_sales("EZE", value['iataCode'], '2026-01-10', 1)
            new_price = self.flight_data.formatCheapFlight(search_result)
            stored_price = self.sheet_info[i]['lowestPrice']

            try:
                new_price = float(new_price)
                stored_price = float(stored_price)
            except (TypeError, ValueError):
                continue

            if new_price < stored_price:
                segments = search_result["data"][0]["itineraries"][0]["segments"]

                def fmt(ts):
                    return datetime.fromisoformat(ts).strftime("%d %b %Y %H:%M")

                message = (
                    f"Sale found for {self.sheet_info[i]['city']}.\n"
                    f"Price found: {new_price}\n"
                    f"Price in sheets file: {stored_price}\n"
                    f"From: EZE\n"
                    f"To: {value['iataCode']}\n"
                    f"Departure: {fmt(segments[0]['departure']['at'])}\n"
                    f"Arrival: {fmt(segments[-1]['arrival']['at'])}"
                )

                print(message)
                self.twilio_helper.send_message(message)

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

# datas = DataManager()
# datas.check_for_deals()