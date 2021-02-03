class ChatLog:
    count_id = 0

    def __init__(self, name, email, phone, query):
        ChatLog.count_id += 1
        self.__chatlog_id = ChatLog.count_id
        self.__name = name
        self.__email = email
        self.__phone = phone
        self.__query = query
        self.__chat = []
        self.__status = "Incomplete"

    def get_chatlog_id(self):
        return self.__chatlog_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_chat(self):
        return self.__chat

    def get_query(self):
        return self.__query

    def get_status(self):
        return self.__status

    def set_chat_id(self,chatlog_id):
        self.__chatlog_id = chatlog_id

    def set_name(self,name):
        self.__name = name

    def set_email(self,email):
        self.__email = email

    def set_phone(self,phone):
        self.__phone = phone

    def set_chat(self, chat):
        self.__chat = chat

    def set_query(self, query):
        self.__query = query

    def set_status(self, status):
        self.__status = status



