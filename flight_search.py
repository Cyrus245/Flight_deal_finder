import requests
from dotenv import dotenv_values
from flight_data import FlightData
import pprint

config = {
    **dotenv_values('.env')
}
api_key = config['tequila_api_key']


class FlightSearch:

    def get_iata_code(self, c_name):
        """this method will get the iata code from tequila api"""
        req_header = {
            'apikey': api_key,
        }
        params = {
            "term": c_name
        }
        result = requests.get("https://api.tequila.kiwi.com/locations/query", params=params, headers=req_header).json()[
            'locations']

        return result[0]['code']

    def check_flight(self, origin_place, to_place, date_from, date_to):
        """this method check the available flight and send the response
        to the flight data class """

        headers = {
            "apikey": api_key
        }

        params = {
            "fly_from": origin_place,
            "fly_to": to_place,
            "dateFrom": date_from.strftime("%d/%m/%Y"),
            "dateTo": date_to.strftime("%d/%m/%Y"),
            "flight_type": "round",
            "max_stopovers": 0,
            "one_for_city": 1,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "curr": "GBP"

        }
        try:
            # requesting for direct flights
            result = \
                requests.get("https://api.tequila.kiwi.com/v2/search", params=params, headers=headers).json()['data'][0]

        except IndexError:
            # this block will execute if no direct flight found for a destination
            params["max_stopovers"] = 1
            data = requests.get("https://api.tequila.kiwi.com/v2/search", params=params, headers=headers)
            try:
                response = data.json()['data'][0]
            except IndexError:
                print(f"No flights found for {to_place}.")
                return None
            else:
                # flight with stopover
                flight_data = FlightData(
                    origin_city=response["cityFrom"],
                    origin_airport=response["flyFrom"],
                    destination_city=response['cityTo'],
                    destination_airport=response['flyTo'],
                    date_from=response['local_departure'].split("T")[0],
                    date_to=response['local_arrival'].split("T")[0],
                    price=response['price'],
                    stop_over=1,
                    via_city=response["route"][0]["cityTo"]

                )
                return flight_data

        else:
            # passing the response to the flight data class and creating a flight data obj
            flight_data = FlightData(
                origin_city=result["cityFrom"],
                origin_airport=result["flyFrom"],
                destination_city=result['cityTo'],
                destination_airport=result['flyTo'],
                date_from=result['local_departure'].split("T")[0],
                date_to=result['local_arrival'].split("T")[0],
                price=result['price'],

            )
            # print(f"{flight_data.destination_city}:{flight_data.price}")

            return flight_data
