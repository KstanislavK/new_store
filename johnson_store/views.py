from django.shortcuts import render
from filmsapp.models import Films, FilmsCategory


def index(request):
    title = "Главная"

    films = Films.objects.all()

    context = {
        'title': title,
        'films': films,
    }
    return render(request, 'johnson_store/index.html', context)


def contacts(request):
    return render(request, 'johnson_store/contacts.html')
