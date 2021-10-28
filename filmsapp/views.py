from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from filmsapp.models import Films, FilmsCategory
from johnson_store.views import get_same_cat_film


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def index(request, pk=None):
    title = "пленки"
    films = Films.objects.all().order_by('name')
    links_menu = FilmsCategory.objects.all()
    basket = get_basket(request.user)

    if pk is not None:
        if pk == 0:
            films = Films.objects.all().order_by('name')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(FilmsCategory, pk=pk)
            films = Films.objects.filter(category__pk=pk).order_by('name')

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'films': films,
            'basket': basket,
        }

        return render(request, 'filmsapp/index.html', context)

    context = {
        'title': title,
        'films': films,
        'links_menu': links_menu,
        'basket': basket,
    }
    return render(request, 'filmsapp/index.html', context)


def film_card(request, pk):
    title = ""
    basket = get_basket(request.user)
    film = get_object_or_404(Films, pk=pk)
    links_menu = FilmsCategory.objects.all()

    same_films = get_same_cat_film(film)

    context = {
        'title': title,
        'basket': basket,
        'film': film,
        'same_films': same_films,
        'links_menu': links_menu,
    }
    return render(request, 'filmsapp/film_card.html', context)
