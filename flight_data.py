class FlightData:
    def __init__(self, origin_city, origin_airport, destination_city, destination_airport, date_from, date_to, price,
                 stop_over=0, via_city=""):
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.date_from = date_from
        self.date_to = date_to
        self.price = price
        self.stop_over = stop_over
        self.via_city = via_city
