import requests
from dotenv import dotenv_values

config = {
    **dotenv_values('.env')
}

sheet_url = config['sheety_url']


class DataManager:
    def __init__(self):
        self.get_url = sheet_url

    def get_destination_data(self):
        """this method getting data from Google sheet using sheet api"""
        result = requests.get(self.get_url).json()[
            'prices']
        return result

    def update_destination_code(self, r_id, msg):
        """this method update destination(IATA) code  in google sheet"""
        params = {
            "price": {
                "iataCode": msg
            }
        }
        result = requests.put(
            f'{self.get_url}/{r_id}', json=params)
