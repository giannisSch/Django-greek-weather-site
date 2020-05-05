from django.contrib import admin

from .models import MeteoData
from .models import OpenWeatherData
from .models import WeatherData
from .models import City
from .models import State

admin.site.register(MeteoData)
admin.site.register(OpenWeatherData)
admin.site.register(WeatherData)
admin.site.register(City)
admin.site.register(State)
