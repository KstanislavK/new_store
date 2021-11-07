from django.contrib import admin
from django.urls import path

from filmsapp.views import index, film_card

app_name = 'films'


urlpatterns = [
    path('', index, name="index"),
    path('category/<int:pk>', index, name="category"),
    path('film/<int:pk>', film_card, name="film_card"),
    path('category/<int:pk>/page/<int:page>', index, name="page"),
]
