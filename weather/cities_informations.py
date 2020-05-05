"""
On this file we are extracting cities informations from meteo.gr
We exctract the {state of city: {city name : {id ,longtitude, latitude}}
"""

from bs4 import BeautifulSoup
import requests
import re
import csv
import time
import json
def get_cities(url):
	source = requests.get(url).text
	soup = BeautifulSoup(source, 'lxml')
	areas = soup.find_all('h2', class_='m')
	towns = soup.find_all('div', class_='divided')
	menu_dict = {}
	for area, towm in zip(areas, towns):
		m = re.findall(r'href="\/cf\.cfm\?city_id=(\d+)">( *\w+.*)<\/a>', str(towm))
		if len(m) > 0:
			menu_dict[area.text.strip()] = {city.strip():ids for ids,city in m}
	return menu_dict

def get_coordinates(identifier):
	source = requests.get(f'https://meteo.gr/cf.cfm?city_id={identifier}').text
	soup = BeautifulSoup(source, 'lxml')
	json_coordinates_script  = json.loads(((soup.find_all('script', type = 'application/ld+json'))[1]).text)
	latitude = json_coordinates_script['geo']['latitude']
	longitude = json_coordinates_script['geo']['longitude']
	return(latitude, longitude)
	
def get_informations(cities_dict):
	for state, cities in cities_dict.items():
		for name, identifier in cities.items():
			time.sleep(8)
			try:
				latitude, longitude = get_coordinates(identifier)
				cities_dict[state][name] = {'id' : identifier, 'latitude' : latitude, 'longitude' : longitude}
			except:
				cities_dict[state][name] = {'id' : identifier, 'latitude' : 0, 'longitude' : 0}
				print(f"ERROR {identifier} + {name}")
	return(cities_dict)

def main():
	url = 'https://meteo.gr/cf.cfm?city_id=171' # URL of nauplion, a random city in order to get the available menu
	cities_dict = get_cities(url)
	cities_info_dict = get_informations(cities_dict)
	return(cities_info_dict)

if __name__ == "__main__":
	main()

