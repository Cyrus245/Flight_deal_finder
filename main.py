from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager
import pprint

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
        # getting the destination code from FlightSearch class get_iata_code method
        destination_code = f_search.get_iata_code(c_name=data['city'])

        # saving the destination code to the Google sheet
        data_manager.update_destination_code(data['id'], destination_code)
    else:
        all_flight = f_search.check_flight(origin_city, data['iataCode'], tomorrow_date, six_month_after)

        # if no direct flights found
        if all_flight is None:
            continue

        # if any price lower than our desired price send msg
        if all_flight.price < data["lowestPrice"]:

            # getting the customers email
            users = data_manager.get_customers_email()
            emails = [user['email'] for user in users]
            names = [user['firstName'] for user in users]

            message = f"Low price alert! only £{all_flight.price} to fly from {all_flight.origin_city}-{all_flight.origin_airport} " \
                      f" to {all_flight.destination_city}-{all_flight.destination_airport},from {all_flight.date_from} to {all_flight.date_to}."

            if all_flight.stop_over > 0:
                # if flight has stopover
                message += f"flight has {all_flight.stop_over} stopover, via {all_flight.via_city} City."
            link = f"https://www.google.co.uk/flights?hl=en#flt={all_flight.origin_airport}.{all_flight.destination_airport}.{all_flight.date_from}*{all_flight.origin_airport}.{all_flight.destination_airport}.{all_flight.date_to}"
            # sending email
            notification.send_emails(emails=emails, message=message, link=link)
