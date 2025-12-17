from flight_search import FlightSearch


class FlightData:
    # This class is responsible for structuring the flight data.
    def formatCheapFlight(self, x):
        offers = x["data"]

        if not offers:
            return "No sales found."

        for i in offers:
            currency = i['price']['currency']
            available_seats = i['numberOfBookableSeats']
            one_way = "round" if i['oneWay'] is False else "one way"
            grand_total = i['price']['grandTotal']

        cheapest = min(
            offers,
            key=lambda o: float(o["price"]["grandTotal"])
        )

        cheapest_price = cheapest["price"]["grandTotal"]
        cheapest_origin = cheapest["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        cheapest_dest = cheapest["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
        cheapest_type = cheapest["travelerPricings"][0]["fareDetailsBySegment"][0]["cabin"]
        print(f"For {cheapest_price}, there is a flight from {cheapest_origin} to {cheapest_dest}. {cheapest_type}.")
        return cheapest["price"]["grandTotal"]


instanttt = FlightData()
searcher = FlightSearch()
instanttt.formatCheapFlight(searcher.find_sales('EZE', 'IST', '2026-01-11', 1))
