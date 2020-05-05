from django.http import HttpResponse
from django.shortcuts import render
from .models import MeteoData, OpenWeatherData, WeatherData, City, State
from . import meteo
from . import open_weather
from . import cities_informations

import requests
import json
import datetime


def index(request, city_name = 'ΑΡΓΟΣ'):
        menu = State.objects.all()
        return render(request, 'weather/index.html', {'menu' : menu})

def details(request, city_name = 'ΑΡΓΟΣ'):
        
        try:  
                city_id = City.objects.get(name=city_name).identifier
        except:
                return render(request, 'weather/error.html')
        latitude  = City.objects.get(name=city_name).latitude
        longitude  = City.objects.get(name=city_name).longitude
        
        MeteoData.objects.all().delete()
        OpenWeatherData.objects.all().delete()
        WeatherData.objects.all().delete()
        try:
                MeteoData.create_objects_from_dictionary(meteo.main(city_id))
                OpenWeatherData.create_objects_from_dictionary(open_weather.get_dictionary(latitude, longitude))
                WeatherData.create_weather_data_object()
        except:
                return render(request, 'weather/error.html')
        
        
        all_weather_data = WeatherData.objects.all()
        
        java_list = []
        for data in OpenWeatherData.objects.all():
                # month have to be -1 because 00 is January
                java_list.append({'x': data.date.strftime("new Date(%Y, %m - 1, %d, %H, %M)"), 'y': data.temperature})
        
        
        dictionary = {
                'weather': all_weather_data, 'scart' : java_list, 'city_name' : city_name 
        }
        return render(request, 'weather/details.html', dictionary)