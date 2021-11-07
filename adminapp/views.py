from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from adminapp.forms import FilmEditForm, CatEditForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from basketapp.models import Basket
from filmsapp.models import FilmsCategory, Films

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, CreateView, UpdateView


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    title = 'админка/главная'
    users_count = ShopUser.objects.all().count()
    users_count_active = ShopUser.objects.all().filter(is_active=True).count()

    categories_count = FilmsCategory.objects.all().count()
    films_count = Films.objects.all().count()
    goods_in_basket_added = Basket.objects.all().count()

    context = {
        'title': title,
        'users_count': users_count,
        'users_count_active': users_count_active,
        'categories_count': categories_count,
        'films_count': films_count,
        'goods_in_basket_added': goods_in_basket_added
    }

    return render(request, 'adminapp/dashboard.html', context)


class UserListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    def get_context_data(self):
        context = super(UserListView, self).get_context_data()
        title = 'Пользователи'
        context.update({'title': title})
        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self):
        context = super(UserCreateView, self).get_context_data()
        title = 'Создание пользователя'
        context.update({'title': title})
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context.update({'title': 'Редактирование пользователя'})
        return context


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'GET':
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()

        return HttpResponseRedirect(reverse('adminapp:user_update', args=[user.pk]))


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'
    categories_list = FilmsCategory.objects.annotate(cnt=Count('films')).order_by('name')

    content = {
        'title': title,
        'objects': categories_list,
    }

    return render(request, 'adminapp/categories.html', content)


class CategoryCreateView(CreateView):
    model = FilmsCategory
    template_name = 'adminapp/category_update.html'
    success_url = 'adminapp/categories.html'
    fields = '__all__'

    def get_context_data(self):
        context = super(CategoryCreateView, self).get_context_data()
        context.update({'title': 'Создание категории'})
        return context


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    edit_cat = get_object_or_404(FilmsCategory, pk=pk)
    title = f'{edit_cat.name}/редактирование'

    if request.method == 'POST':
        edit_form = CatEditForm(request.POST, instance=edit_cat)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_update', args=[edit_cat.pk]))

    else:
        edit_form = CatEditForm(instance=edit_cat)

    context = {
        'title': title,
        'update_form': edit_form,
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category = get_object_or_404(Films, pk=pk)

    if request.method == 'GET':
        if category.is_active:
            category.is_active = False
        else:
            category.is_active = True
        category.save()

        return HttpResponseRedirect(reverse('adminapp:categories', args=[category.pk]))


@user_passes_test(lambda u: u.is_superuser)
def films(request, pk):
    title = 'Пленки'

    category = get_object_or_404(FilmsCategory, pk=pk)
    films_list = Films.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': films_list
    }

    return render(request, 'adminapp/films.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def films_create(request, pk):
#     title = 'пленки/создание'
#     category = get_object_or_404(FilmsCategory, pk=pk)
#     if request.method == 'POST':
#         film_form = FilmEditForm(request.POST, request.FILES)
#         if film_form.is_valid():
#             film_form.save()
#             return HttpResponseRedirect(reverse('adminapp:films', args=[pk]))
#
#     else:
#         film_form = FilmEditForm(initial={'category': category})
#
#     context = {
#         'title': title,
#         'update_form': film_form,
#         'category': category
#     }
#     return render(request, 'adminapp/film_update.html', context)


class FilmCreateView(LoginRequiredMixin, CreateView):
    model = Films
    template_name = 'adminapp/film_update.html'
    success_url = reverse_lazy('adminapp:films')
    fields = '__all__'

    def get_context_data(self):
        context = super(FilmCreateView, self).get_context_data()
        title = 'Добавить пленку'
        context.update({'title': title})
        return context


@user_passes_test(lambda u: u.is_superuser)
def films_update(request, pk):
    edit_film = get_object_or_404(Films, pk=pk)
    title = f'Редактирование {edit_film.name}'

    if request.method == 'POST':
        edit_form = FilmEditForm(request.POST, request.FILES, instance=edit_film)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:films_update', args=[edit_film.pk]))

    else:
        edit_form = FilmEditForm(instance=edit_film)

    context = {
        'title': title,
        'update_form': edit_form,
        'category': edit_film.category,
        'edit_film_pk': edit_film.pk
    }
    return render(request, 'adminapp/film_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def films_delete(request, pk):
    film = get_object_or_404(Films, pk=pk)

    if request.method == 'GET':
        if film.is_active:
            film.is_active = False
        else:
            film.is_active = True
        film.save()

        return HttpResponseRedirect(reverse('adminapp:films', args=[film.category.pk]))


class FilmsAllListView(LoginRequiredMixin, ListView):
    model = Films
    template_name = 'adminapp/films_all.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Films.objects.all().order_by('category', '-is_active', 'name')

    def get_context_data(self, **kwargs):
        context = super(FilmsAllListView, self).get_context_data(**kwargs)
        title = 'Все пленки'
        context.update({'title': title})
        return context
