class Dish:
    count_id = 0
    def __init__(self,name,description,price):
        Dish.count_id += 1
        self.__dish_id = Dish.count_id
        self.__name = name
        self.__description = description
        self.__price = price

    def get_dish_id(self):
        return self.__dish_id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def set_dish_id(self,id):
        self.__dish_id = id

    def set_name(self,name):
        self.__name = name

    def set_description(self,desc):
        self.__description = desc

    def set_price(self,price):
        self.__price = price
