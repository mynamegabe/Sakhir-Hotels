class Promo:
    count_id = 0

    def __init__(self, promo_name, promo_cn, desc, endDate, remarks):
        Promo.count_id += 1
        self.__promo_id = Promo.count_id
        self.__promo_name = promo_name
        self.__promo_cn = promo_cn
        self.__desc = desc
        self.__endDate = endDate
        self.__remarks = remarks

    def get_promo_id(self):
        return self.__promo_id

    def get_promo_name(self):
        return self.__promo_name

    def get_promo_cn(self):
        return self.__promo_cn

    def get_desc(self):
        return self.__desc

    def get_endDate(self):
        return self.__endDate

    def get_remarks(self):
        return self.__remarks

    def set_promo_id(self,promo_id):
        self.__promo_id = promo_id

    def set_promo_name(self,promo_name):
        self.__promo_name = promo_name

    def set_desc(self,desc):
        self.__desc = desc

    def set_endDate(self,endDate):
        self.__endDate = endDate

    def set_remarks(self,remarks):
        self.__remarks = remarks

