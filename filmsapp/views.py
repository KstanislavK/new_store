from django.shortcuts import render


def index(request):
    return render(request, 'filmsapp/index.html')
