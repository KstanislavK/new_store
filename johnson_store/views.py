import random

from django.shortcuts import render
from filmsapp.models import Films


def get_hot_offer():
    films = Films.objects.all()
    return random.sample(list(films), 3)[0]


def get_same_cat_film(hot_offer):
    same_cat_film = Films.objects.filter(category=hot_offer.category).exclude(pk=hot_offer.pk)
    return same_cat_film


def index(request):
    title = "Главная"

    films = Films.objects.all()
    hot_offer = get_hot_offer()
    same_cat_film = get_same_cat_film(hot_offer)

    context = {
        'title': title,
        'films': films,
        'hot_offer': hot_offer,
        'same_cat_film': same_cat_film,
    }
    return render(request, 'johnson_store/index.html', context)


def contacts(request):
    title = "Контакты"

    films = Films.objects.all()

    context = {
        'title': title,
        'films': films,
    }
    return render(request, 'johnson_store/contacts.html', context)
