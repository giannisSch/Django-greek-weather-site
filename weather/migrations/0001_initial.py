# Generated by Django 3.0.4 on 2020-04-15 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeteoData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('temperature_face', models.CharField(max_length=200)),
                ('humidity', models.CharField(max_length=200)),
                ('beaufort', models.CharField(max_length=200)),
                ('direction', models.CharField(max_length=200)),
                ('speed', models.CharField(max_length=200)),
                ('icon', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='OpenWeatherData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('temperature_face', models.CharField(max_length=200)),
                ('humidity', models.CharField(max_length=200)),
                ('beaufort', models.CharField(max_length=200)),
                ('direction', models.CharField(max_length=200)),
                ('speed', models.CharField(max_length=200)),
                ('icon', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('meteo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.MeteoData')),
                ('open_weather', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weather.OpenWeatherData')),
            ],
        ),
    ]
