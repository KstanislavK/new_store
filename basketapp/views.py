from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from filmsapp.models import Films


def basket(request):
    context = {}
    return render(request, 'basketapp/basket.html', context)


def basket_add(request, pk):
    film = get_object_or_404(Films, pk=pk)

    basket = Basket.objects.filter(user=request.user, film=film).first()

    if not basket:
        basket = Basket(user=request.user, film=film)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request):
    context = {}
    return render(request, 'basketapp/basket.html', context)
