import requests
from dotenv import dotenv_values
from flight_data import FlightData

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
            "curr": "GBP"
        }
        result = requests.get("https://api.tequila.kiwi.com/v2/search", params=params, headers=headers).json()['data'][
            0]

        # passing the response to the flight data class
        flight_data = FlightData(
            origin_city=result["cityFrom"],
            origin_airport=result["flyFrom"],
            destination_city=result['cityTo'],
            destination_airport=result['flyTo'],
            date_from=result['local_departure'].split("T")[0],
            date_to=result['local_arrival'].split("T")[0],
            price=result['conversion']["GBP"]
        )

        return flight_data
