class OpeningHours:
    def __init__(self,monday,tuesday,wednesday,thursday,friday,saturday,sunday,publichols):
        self.__monday = monday
        self.__tuesday = tuesday
        self.__wednesday = wednesday
        self.__thursday = thursday
        self.__friday = friday
        self.__saturday = saturday
        self.__sunday = sunday
        self.__publichols = publichols

    def monday(self):
        return self.__monday

    def tuesday(self):
        return self.__tuesday

    def wednesday(self):
        return self.__wednesday

    def thursday(self):
        return self.__thursday

    def friday(self):
        return self.__friday

    def saturday(self):
        return self.__saturday

    def sunday(self):
        return self.__sunday

    def publichols(self):
        return self.__publichols

    def set_monday(self,monday):
        self.__monday = monday

    def set_tuesday(self,tuesday):
        self.__tuesday = tuesday

    def set_wednesday(self,wednesday):
        self.__wednesday = wednesday

    def set_thursday(self,thursday):
        self.__thursday = thursday

    def set_friday(self,friday):
        self.__friday = friday

    def set_saturday(self,saturday):
        self.__saturday = saturday

    def set_sunday(self,sunday):
        self.__sunday = sunday

    def set_publichols(self,publichols):
        self.__publichols = publichols
