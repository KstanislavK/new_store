from django.contrib import admin
from django.urls import path

from filmsapp.views import index


app_name = 'films'


urlpatterns = [
    path('', index, name="index"),
    path('category/<int:pk>', index, name="category"),
]
