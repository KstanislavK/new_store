from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from filmsapp.models import Films, FilmsCategory
from johnson_store.views import get_same_cat_film

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request, pk=None, page=1):
    title = "пленки"
    films = Films.objects.filter(is_active=True).order_by('name')
    links_menu = FilmsCategory.objects.all()

    if pk is not None:
        if pk == 0:
            films = Films.objects.filter(is_active=True).order_by('name')
            category = {'name': 'все', 'pk': 0}
        else:
            category = get_object_or_404(FilmsCategory, pk=pk)
            films = Films.objects.filter(category__pk=pk).filter(is_active=True).order_by('name')

        paginator = Paginator(films, 10)
        try:
            films_paginator = paginator.page(page)
        except PageNotAnInteger:
            films_paginator = paginator.page(1)
        except EmptyPage:
            films_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'films': films_paginator,
        }

        return render(request, 'filmsapp/index.html', context)

    context = {
        'title': title,
        'films': films,
        'links_menu': links_menu,
    }
    return render(request, 'filmsapp/index.html', context)


def film_card(request, pk):
    title = ""
    film = get_object_or_404(Films, pk=pk)
    links_menu = FilmsCategory.objects.all()

    same_films = get_same_cat_film(film)

    context = {
        'title': title,
        'film': film,
        'same_films': same_films,
        'links_menu': links_menu,
    }
    return render(request, 'filmsapp/film_card.html', context)
