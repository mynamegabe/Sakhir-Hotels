class Contact:
    count_id = 0
    def __init__(self,firstname,lastname,email,tel,msg):
        Contact.count_id += 1
        self.__contact_id = Contact.count_id
        self.__name = firstname + lastname
        self.__email = email
        self.__tel = tel
        self.__msg = msg
        self.__status = "Unresolved"

    def get_contact_id(self):
        return self.__contact_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_tel(self):
        return self.__tel

    def get_msg(self):
        return self.__msg

    def get_status(self):
        return self.__status

    def set_contact_id(self,contact_id):
        self.__contact_id = contact_id

    def set_name(self,name):
        self.__name = name

    def set_email(self,email):
        self.__email = email

    def set_tel(self,tel):
        self.__tel = tel

    def set_msg(self,msg):
        self.__msg = msg

    def set_status(self,status):
        self.__status = status


