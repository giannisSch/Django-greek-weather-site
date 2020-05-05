from bs4 import BeautifulSoup
import requests
import csv
import re
import datetime

def get_date(counter_days):
	today = datetime.date.today()
	tdelta = datetime.timedelta(days=counter_days)
	return today + tdelta

def get_time(td, counter_days):
	time_text = td.find('td').text.split(':')
	time = datetime.time(int(time_text[0]), int(time_text[1]))
	date_and_time = datetime.datetime.combine(get_date(counter_days-1), time) 
	return date_and_time

def get_temperature(td):
	if (td.find('div', class_='normal tempcolorcell')):
		temp_humidity = td.find('div', class_='normal tempcolorcell').text
	if (td.find('div', class_='normal maxtemp tempcolorcell')):
		temp_humidity = td.find('div', class_='normal maxtemp tempcolorcell').text
	split = temp_humidity.strip().split('\n')
	if len(split) == 2:
		temperature = split[0].split("°")[0]
		humidity = split[1].split("%")[0]
		return temperature, "", humidity
	if len(split) == 3: 						#face temperature
		temperature = split[0].split("°")[0]
		temperature_face = split[1].split("°")[0]
		humidity = split[2].split("%")[0]
		return temperature, temperature_face, humidity


def get_wind(td):
	td_wind = td.text
	beaufort_direction_speed = td_wind.strip()
	if beaufort_direction_speed  == "ΑΠΝΟΙΑ":
		return "AΠΝΟΙΑ", "", 0
	beaufort_direction_speed = beaufort_direction_speed.split('\n')
	beaufort_direction = beaufort_direction_speed[0].replace("Μπφ","").split(" ")
	beaufort = beaufort_direction[0]
	direction = beaufort_direction[2]
	speed = beaufort_direction_speed[1].split('Km/h')[0]
	return beaufort, direction, speed

def get_description(td):
	return td.text.strip().replace('\n','',1).split('\n')[0]

def get_icon_URL(td):
	src = td.find('img', class_= 'CFicon')
	url = 'https://meteo.gr/' + src['src']
	return url

def per_hour_row_margin(tr, meteo_dict, counter_days):
	"""
	print(get_time(tr.find('td', class_= 'innerTableCell fulltime')))
	print(get_temperature(tr.find('td', class_= 'innerTableCell temperature tempwidth')))
	print(get_wind(tr.find('td', class_= 'innerTableCell anemosfull')))
	print(get_description(tr.find('td', class_= 'innerTableCell PhenomenaSpecialTableCell phenomenafull')))
	"""
	date_and_time = get_time(tr.find('td', class_= 'innerTableCell fulltime'), counter_days)
	temperature, temperature_face, humidity = get_temperature(tr.find('td', class_= 'innerTableCell temperature tempwidth'))
	beaufort, direction, speed = get_wind(tr.find('td', class_= 'innerTableCell anemosfull'))
	description = get_description(tr.find('td', class_= 'innerTableCell PhenomenaSpecialTableCell phenomenafull'))
	icon = get_icon_URL(tr.find('td', class_= 'innerTableCell PhenomenaSpecialTableCell phenomenafull'))

	meteo_dict[get_time(tr.find('td', class_= 'innerTableCell fulltime'), counter_days)] = {
												'temperature' : temperature, 
												'temperature_face' : temperature_face,
												'humidity' : humidity,
												'beaufort' : beaufort,
												'direction' : direction,
												'speed' : speed,
												'description' : description,
												'icon': icon}

def main(city_id):
	counter_days = 0
	source = requests.get(f'https://meteo.gr/cf.cfm?city_id={city_id}').text
	soup = BeautifulSoup(source, 'lxml')
	meteo_dict = {}
	content = soup.find('div', class_='content')
	table = content.find('table')
	children = table.findChildren("tr" , recursive=False)
	for tr in children:
		if (tr.find('td', class_= 'innerTableCell fulltime')):
			per_hour_row_margin(tr, meteo_dict, counter_days)
		else:
			counter_days += 1
	return meteo_dict

if __name__ == "__main__":
	main()
