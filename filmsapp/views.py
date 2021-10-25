from django.shortcuts import render


def index(request):
    title = "пленки"
    category_links = []

    context = {
        'title': title,
        'category_links': category_links,
    }
    return render(request, 'filmsapp/index.html')
