from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.index),
    path('<city_name>', views.details),

]