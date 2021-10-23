from django.shortcuts import render


def index(request):
    return render(request, 'johnson_store/index.html')


def contacts(request):
    return render(request, 'johnson_store/contacts.html')
