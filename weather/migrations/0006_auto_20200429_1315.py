# Generated by Django 3.0.4 on 2020-04-29 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_auto_20200429_0939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='name',
            new_name='city_name',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='state',
            new_name='city_state',
        ),
    ]
