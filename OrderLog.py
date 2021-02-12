class OrderLog:
    count_id = 0
    def __init__(self,dish,restaurant,roomno):
        OrderLog.count_id += 1
        self.__order_id = OrderLog.count_id
        self.__dish = dish
        self.__restaurant = restaurant
        self.__roomno = roomno

    def get_order_id(self):
        return self.__order_id

    def get_dish(self):
        return self.__dish

    def get_restaurant(self):
        return self.__restaurant

    def get_roomno(self):
        return self.__roomno

    def set_dish(self,dish):
        self.__dish = dish

    def set_restaurant(self,restaurant):
        self.__restaurant = restaurant

    def set_roomno(self,roomno):
        self.__roomno = roomno
