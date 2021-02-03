class Room:
    count_id = 0
    def __init__(self, category, name, rooms, avail_rooms, price, capacitylist, detaillist):
        Room.count_id += 1
        self.__room_id = Room.count_id
        self.__category = category
        self.__room_name = name
        self.__rooms = rooms
        self.__avail_rooms = avail_rooms
        self.__price = price
        self.__capacity_list = capacitylist
        self.__detail_list = detaillist

    def get_room_id(self):
        return self.__room_id

    def get_category(self):
        return self.__category

    def get_room_name(self):
        return self.__room_name

    def get_rooms(self):
        return self.__rooms

    def get_avail_rooms(self):
        return self.__avail_rooms

    def get_price(self):
        return self.__price

    def get_capacity_list(self):
        return self.__capacity_list

    def get_detail_list(self):
        return self.__detail_list

    def set_room_name(self, name):
        self.__room_name = name

    def set_rooms(self, rooms):
        self.__rooms = rooms

    def set_avail_rooms(self, avail_rooms):
        self.__avail_rooms = avail_rooms

    def set_price(self, price):
        self.__price = price

    def set_capacity_list(self, capacitylist):
        self.__capacity_list = capacitylist

    def set_detail_list(self, detaillist):
        self.__detail_list = detaillist


