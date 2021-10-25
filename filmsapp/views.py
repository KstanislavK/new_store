from django.shortcuts import render

from filmsapp.models import Films, FilmsCategory


def index(request):
    title = "пленки"

    films = Films.objects.all()
    series = FilmsCategory.objects.all()

    context = {
        'title': title,
        'films': films,
        'series': series,
    }
    return render(request, 'filmsapp/index.html', context)
