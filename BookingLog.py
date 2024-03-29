class BookingLog:
    count_id = 0

    def __init__(self, customer_id, customer_name, room_type, startDate, endDate):
        BookingLog.count_id += 1
        self.__bookinglog_id = BookingLog.count_id
        self.__customer_id = customer_id
        self.__customer_name = customer_name
        self.__room_type = room_type
        self.__startDate = startDate
        self.__endDate = endDate

    def get_bookinglog_id(self):
        return self.__bookinglog_id

    def get_customer_id(self):
        return self.__customer_id

    def get_customer_name(self):
        return self.__customer_name

    def get_room_type(self):
        return self.__room_type

    def get_startDate(self):
        return self.__startDate

    def get_endDate(self):
        return self.__endDate

    def set_bookinglog_id(self,bookinglog_id):
        self.__bookinglog_id = bookinglog_id

    def set_customer_id(self,customer_id):
        self.__customer_id = customer_id

    def set_customer_name(self,customer_name):
        self.__customer_name = customer_name

    def set_room_type(self,room_type):
        self.__room_type = room_type

    def set_startDate(self,startDate):
        self.__startDate = startDate

    def set_endDate(self,endDate):
        self.__endDate = endDate

