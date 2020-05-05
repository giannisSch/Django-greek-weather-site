from django.db import models

# Create your models here.
class MeteoData(models.Model):
    date = models.DateTimeField()  
    temperature = models.CharField(max_length=200)
    temperature_face = models.CharField(max_length=200)
    humidity = models.CharField(max_length=200)
    beaufort = models.CharField(max_length=200)
    direction = models.CharField(max_length=200)
    speed = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    @staticmethod
    def create_objects_from_dictionary(dictionary):
        for key, value in dictionary.items():
            if value['temperature_face'] == '':
                value['temperature_face'] = value['temperature'] # in order not to be empty
            meteo_object = MeteoData(date = key, temperature = value['temperature'], temperature_face = value['temperature_face'], humidity = value['humidity'],
            beaufort=value['beaufort'], direction = value['direction'], speed=value['speed'], icon = value['icon'], description = value['description'])
            meteo_object.save()


class OpenWeatherData(models.Model):
    date = models.DateTimeField()
    temperature = models.CharField(max_length=200)  
    temperature_face = models.CharField(max_length=200)
    humidity = models.CharField(max_length=200)
    speed = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    @staticmethod
    def create_objects_from_dictionary(dictionary):
        for key, value in dictionary.items():
            open_weather_object = OpenWeatherData(date = key, temperature = value['temperature'], temperature_face = value['temperature_face'], humidity = value['humidity'],
            speed=value['speed'], icon = value['icon'], description = value['description'])
            open_weather_object.save()

class WeatherData(models.Model):
    date = models.DateTimeField()
    meteo = models.OneToOneField( MeteoData, on_delete=models.CASCADE)
    open_weather = models.OneToOneField( OpenWeatherData, on_delete=models.CASCADE)

    @staticmethod
    def create_weather_data_object():
        meteo_all =  MeteoData.objects.all()
        open_weather_all = OpenWeatherData.objects.all()
        for meteo, open_weather in zip(meteo_all, open_weather_all): #prosoxi edw sumfwna me to json prepei na shiftarw parw to prwto stoixeio tou open_weather omws to site isxurizetai oti den xreiazetai ama sugkrizeis ta dedomena
            weather_data = WeatherData(date = meteo.date, meteo = meteo, open_weather = open_weather)
            weather_data.save()

class State(models.Model):
    name = models.CharField(max_length=200)

    @staticmethod
    def create_states_informations(dictionary):
        for state, cities in dictionary.items():
            if state != 'ΑΚΤΕΣ ΑΤΤΙΚΗΣ' and state != 'ΑΡΧΑΙΟΛΟΓΙΚΟΙ ΧΩΡΟΙ' and state != 'ΧΙΟΝΟΔΡΟΜΙΚΑ ΚΕΝΤΡΑ' and state != 'ΧΕΙΜΕΡΙΝΟΙ ΠΡΟΟΡΙΣΜΟΙ' and state != 'ΟΔΙΚΟ ΔΙΚΤΥΟ':
                state_object = State(name = state)
                state_object.save()
                for name, informations in cities.items():
                    city_object = City(state = state_object, name = name, identifier = informations['id'],longitude = informations['longitude'], latitude = informations['latitude'])
                    city_object.save()
    

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)


