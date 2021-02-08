class Staff:
    count_id = 0
    def __init__(self,name,restaurant,position,salary,birthday):
        Staff.count_id += 1
        self.__staff_id = Staff.count_id
        self.__name = name
        self.__restaurant = restaurant
        self.__position = position
        self.__salary = salary
        self.__birthday = birthday

    def get_staff_id(self):
        return self.__staff_id

    def get_staff_name(self):
        return self.__name

    def get_restaurant(self):
        return self.__restaurant

    def get_position(self):
        return self.__position

    def get_salary(self):
        return self.__salary

    def get_birthday(self):
        return self.__birthday

    def set_staff_id(self,id):
        self.__staff_id = id

    def set_staff_name(self,name):
        self.__staff_name = name

    def set_restaurant(self,restaurant):
        self.__restaurant = restaurant

    def set_position(self,position):
        self.__position = position

    def set_salary(self,salary):
        self.__salary = salary

    def set_birthday(self,birthday):
        self.__birthday = birthday