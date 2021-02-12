class Restaurant:
    def __init__(self,name,cuisine,description,opening_hours,menu,lunch_menu,dinner_menu,staff_list):
        self.__name = name
        self.__cuisine = cuisine
        self.__description = description
        self.__opening_hours = opening_hours
        self.__menu = menu
        self.__lunch_menu = lunch_menu
        self.__dinner_menu = dinner_menu
        self.__staff_list = staff_list
        self.__order_list = {}
        self.__complete_order_list = {}

    def get_name(self):
        return self.__name

    def get_cuisine(self):
        return self.__cuisine

    def get_description(self):
        return self.__description

    def get_opening_hours(self):
        return self.__opening_hours

    def get_menu(self):
        return self.__menu

    def get_lunch_menu(self):
        return self.__lunch_menu

    def get_dinner_menu(self):
        return self.__dinner_menu

    def get_staff_list(self):
        return self.__staff_list

    def get_order_list(self):
        return self.__order_list

    def get_complete_order_list(self):
        return self.__complete_order_list

    def set_name(self,name):
        self.__name = name

    def set_cuisine(self, cuisine):
        self.__cuisine = cuisine

    def set_description(self,description):
        self.__description = description

    def set_opening_hours(self,opening_hours):
        self.__opening_hours = opening_hours

    def set_menu(self,menu):
        self.__menu = menu

    def set_lunch_menu(self,lunch_menu):
        self.__lunch_menu = lunch_menu

    def set_dinner_menu(self,dinner_menu):
        self.__dinner_menu = dinner_menu

    def set_staff_list(self,staff_list):
        self.__staff_list = staff_list

    def set_order_list(self,order_list):
        self.__order_list = order_list

    def set_complete_order_list(self,complete_order_list):
        self.__complete_order_list = complete_order_list