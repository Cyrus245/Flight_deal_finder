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
        result = requests.get(f'{self.get_url}/prices').json()[
            'prices']

        return result

    def update_destination_code(self, r_id, msg):
        """this method update destination(IATA) code  in google sheet"""
        params = {
            "price": {
                "iataCode": msg
            }
        }
        result = requests.put(f'{self.get_url}/prices/{r_id}', json=params)

    def get_customers_email(self):
        """This method will get the users data from Google sheet"""
        result = requests.get(f"{self.get_url}/users").json()
        users = result['users']
        return users
