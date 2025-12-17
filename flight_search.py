import os
from dotenv import load_dotenv
import requests

from pprint import pprint

load_dotenv()


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_API_SECRET"]
        self.bearer_authorization = self.get_new_token()

    def get_new_token(self):
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        answer = f"{token_data['token_type']} {token_data['access_token']}"
        return answer

    def find_iata_codes(self, keyword):
        search_url = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'

        params = {
            "keyword": keyword,
            "max": 1,
        }

        headers = {
            "accept": "application/vnd.amadeus+json",
            "Authorization": self.bearer_authorization,
        }

        response = requests.get(search_url, params=params, headers=headers)

        response.raise_for_status()  # Raises an exception for 4xx/5xx responses

        data = response.json()

        processed = data['data'][0]['iataCode']
        print(f"IATA code found for {keyword}: {processed}")
        return processed

    def find_sales(self, origin, destiny, dDate, adults):
        sales_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            "accept": "application/vnd.amadeus+json",
            "Authorization": self.bearer_authorization,
        }
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destiny,
            "departureDate": dDate,
            "adults": adults,
            "currencyCode": "USD",
            "max": 5
        }
        response = requests.get(sales_url, params=params, headers=headers)

        if response.status_code != 200:
            print(response.status_code)
            print(response.text)

        data = response.json()
        return data
flighter = FlightSearch()
flighter.find_sales('EZE', 'PAR', '2026-01-11', 1)