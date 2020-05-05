import requests
import json
import datetime
import os.path

def get_dictionary(lat, lon):
	url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=0cb5cba93548cb2cdffa02368b549600&lang=el"
	response = requests.get(url)
	json_data = json.loads(response.text)

	#BASE = os.path.dirname(os.path.abspath(__file__))
	#with open(os.path.join(BASE, 'open_weather.json')) as myfile:
	#	data=myfile.read()
	#json_data = json.loads(data)

	# parse file
	dictionary = {}
	for element in (json_data['list']):
		date_time_str = element['dt_txt']
		date = datetime.datetime.strptime(date_time_str[:-3], '%Y-%m-%d %H:%M') #ignore seconds
		temperature = "{:.1f}".format(element['main']['temp'] - 273.15) 	#Celsious
		temperature_face = "{:.1f}".format(element['main']['feels_like'] - 273.15)
		humidity = element['main']['humidity']
		speed = element['wind']['speed']
		icon_name = element['weather'][0]['icon']
		icon = f'https://openweathermap.org/img/wn/{icon_name}.png'
		description = element['weather'][0]['description']
		dictionary[date] = {'temperature' : temperature,
							'temperature_face' : temperature_face,
							'humidity' : humidity,
							'speed' : speed,
							'icon' : icon,
							'description' : description}
	return dictionary
