class TempLog:
    count_id = 0

    def __init__(self, user_id, username, temperature, swabcheck):
        TempLog.count_id += 1
        self.__templog_id = TempLog.count_id
        self.__username = username
        self.__user_id = user_id
        self.__temperature = temperature
        self.__swabcheck = swabcheck

    def get_user_id(self):
        return self.__user_id

    def get_templog_id(self):
        return self.__templog_id

    def get_username(self):
        return self.__username

    def get_temperature(self):
        return self.__temperature

    def get_swabcheck(self):
        return self.__swabcheck

    def set_user_id(self,id):
        self.__user_id = id

    def set_username(self,username):
        self.__username = username

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def set_swabcheck(self, swabcheck):
        self.__swabcheck = swabcheck