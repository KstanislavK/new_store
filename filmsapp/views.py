from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from filmsapp.models import Films, FilmsCategory


def index(request, pk=None):
    title = "пленки"
    films = Films.objects.all().order_by('name')
    links_menu = FilmsCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

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
