class User:
    count_id = 0

    def __init__(self, first_name, last_name, gender, birthdate, membership, remarks, password, swabcheck):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__birthdate = birthdate
        self.__membership = membership
        self.__remarks = remarks
        self.__username = first_name + last_name
        self.__password = password
        self.__swabcheck = swabcheck

    def get_user_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_birthdate(self):
        return self.__birthdate

    def get_membership(self):
        return self.__membership

    def get_remarks(self):
        return self.__remarks

    def get_password(self):
        return self.__password

    def get_swabcheck(self):
        return self.__swabcheck

    def set_user_id(self,user_id):
        self.__user_id = user_id

    def set_first_name(self,first_name):
        self.__first_name = first_name

    def set_last_name(self,last_name):
        self.__last_name = last_name

    def set_gender(self,gender):
        self.__gender = gender

    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate

    def set_membership(self,membership):
        self.__membership = membership

    def set_remarks(self,remarks):
        self.__remarks = remarks

    def set_password(self,password):
        self.__password = password

    def set_swabcheck(self, swabcheck):
        self.__swabcheck = swabcheck
