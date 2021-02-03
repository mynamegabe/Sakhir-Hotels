class SwabLog:
    count_id = 0

    def __init__(self, user_id, ic, first_name, last_name, swabcheck):
        SwabLog.count_id += 1
        self.__user_id = user_id
        self.__ic = ic
        self.__first_name = first_name
        self.__last_name = last_name
        self.__swabcheck = swabcheck

    def get_user_id(self):
        return self.__user_id

    def get_ic(self):
        return self.__ic

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_swabcheck(self):
        return self.__swabcheck

    def set_user_id(self,user_id):
        self.__user_id = user_id

    def set_ic(self,ic):
        self.__ic = ic

    def set_first_name(self,first_name):
        self.__first_name = first_name

    def set_last_name(self,last_name):
        self.__last_name = last_name

    def set_swabcheck(self, swabcheck):
        self.__swabcheck = swabcheck
