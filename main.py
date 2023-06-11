from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
f_search = FlightSearch()
notification = NotificationManager()

origin_city = "LON"

tomorrow_date = datetime.now() + timedelta(days=1)
six_month_after = tomorrow_date + timedelta(days=180)

for data in sheet_data:
    # if destination code in not in google sheet
    if data['iataCode'] == '':
        # getting the destination code from FlightSearch class
        destination_code = f_search.get_iata_code(c_name=data['city'])
        # saving the destination code to the Google sheet
        data_manager.update_destination_code(data['id'], destination_code)
    else:
        all_flight = f_search.check_flight(origin_city, data['iataCode'], tomorrow_date, six_month_after)
        message = f"Low price alert! only £{all_flight.price} to fly from {all_flight.departure_city}-{all_flight.departure_iata} " \
                  f" to {all_flight.arrival_city}-{all_flight.arrival_iata},from {all_flight.date_from} to {all_flight.date_to}"
        # if any price lower than our desired price send msg
        if all_flight.price < data["lowestPrice"]:
            notification.seng_msg(message)
