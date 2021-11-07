from django.urls import path

from .views import *

app_name = 'adminapp'


urlpatterns = [
    path('', index, name='index'),

    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/read/', UserListView.as_view(), name='users'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', user_delete, name='user_delete'),
    #
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', categories, name='categories'),
    path('categories/update/<int:pk>/', category_update, name='category_update'),
    path('categories/delete/<int:pk>/', category_delete, name='category_delete'),
    #
    path('films/create/category/<int:pk>/', FilmCreateView.as_view(), name='films_create'),
    path('films/read/category/<int:pk>/', films, name='films'),
    path('films/update/<int:pk>/', films_update, name='films_update'),
    path('films/delete/<int:pk>/', films_delete, name='films_delete'),
    path('films/all/', FilmsAllListView.as_view(), name='films_all'),
]
