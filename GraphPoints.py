from datetime import date, timedelta
import datetime
class GraphPoints:
    def __init__(self,name,xaxis,yaxis):
        self.__name = name
        self.__xaxis = xaxis
        self.__yaxis = yaxis
        self.__xpoints = [date.today()]
        self.__ypoints = [0]

    def get_name(self):
        return self.__name

    def get_xaxis(self):
        return self.__xaxis

    def get_yaxis(self):
        return self.__yaxis

    def get_xpoints(self):
        return self.__xpoints

    def get_ypoints(self):
        return self.__ypoints

    def set_xaxis(self,xaxis):
        self.__xaxis = xaxis

    def set_yaxis(self,yaxis):
        self.__yaxis = yaxis

    def set_xpoints(self,xpoints):
        self.__xpoints = xpoints

    def set_ypoints(self,ypoints):
        self.__ypoints = ypoints

    def increment_point(self,value=1):
        today = date.today()
        olddate = self.__xpoints[-1]
        if today == olddate:
            self.__ypoints[-1] += value
        else:
            delta = today - olddate
            for i in range(delta.days + 1):
                day = olddate + timedelta(days=i)
                self.__xpoints.append(day)
                self.__ypoints.append(0)
            self.__xpoints.append(today)
            self.__ypoints.append(value)



