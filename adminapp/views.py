from django.db.models import Count
from django.shortcuts import render

from authapp.models import ShopUser
from filmsapp.models import FilmsCategory


def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    content = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', content)


def categories(request):
    title = 'админка/категории'
    # categories_list = FilmsCategory.objects.all().order_by('name')
    categories_list = FilmsCategory.objects.annotate(cnt=Count('films')).order_by('name')

    content = {
        'title': title,
        'objects': categories_list,
    }

    return render(request, 'adminapp/categories.html', content)
