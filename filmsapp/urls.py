from django.contrib import admin
from django.urls import path

from filmsapp.views import index

urlpatterns = [
    path('', index),
]
