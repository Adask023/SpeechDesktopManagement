import pyowm
from pyowm.utils.config import get_default_config


class WeatherItem:
    APIkey = 'Your weather API key'

    def __init__(self, city):
        self.city = city
        config_dict = get_default_config()
        config_dict['language'] = 'pl'

        owm = pyowm.OWM(self.APIkey, config_dict)
        loc = owm.weather_manager().weather_at_place(self.city)
        self.weather = loc.weather

    def getCityName(self):
        return self.city

    def getHumidity(self):
        return self.weather.humidity

    def getStatus(self):
        status = self.weather.detailed_status
        return status

    def getTemperature(self):
        temp = self.weather.temperature(unit='celsius')
        actual_temp = float(temp['temp'])
        return actual_temp

# testy
# london = WeatherItem('tokio')
# print(london.getStatus())
# print(london.getHumidity())
# print(london.getTemperature())
