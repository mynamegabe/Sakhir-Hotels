from datetime import date
import datetime
class Review:
    count_id = 0
    def __init__(self,username,email,rating,title,review):
        Review.count_id += 1
        self.__review_id = Review.count_id
        self.__name = username
        self.__email = email
        self.__rating = rating
        self.__title = title
        self.__review = review
        self.__date = datetime.datetime.strptime(date.today().strftime("%d %B %Y"),"%d %B %Y")

    def get_review_id(self):
        return self.__review_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_rating(self):
        return self.__rating

    def get_title(self):
        return self.__title

    def get_review(self):
        return self.__review

    def get_date(self):
        return self.__date

    def set_review_id(self,review_id):
        self.__review_id = review_id

    def set_name(self,name):
        self.__name = name

    def set_email(self,email):
        self.__email = email

    def set_rating(self,rating):
        self.__rating = rating

    def set_title(self,title):
        self.__title = title

    def set_review(self,review):
        self.__review = review

    def set_date(self,date):
        self.__date = date
