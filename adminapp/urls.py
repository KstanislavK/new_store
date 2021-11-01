from django.urls import path

from .views import *

app_name = 'adminapp'


urlpatterns = [
    path('users/create/', user_create, name='user_create'),
    path('users/read/', users, name='users'),
    # path('users/update/<int:pk>/', user_update, name='user_update'),
    # path('users/delete/<int:pk>/', user_delete, name='user_delete'),
    #
    # path('categories/create/', category_create, name='category_create'),
    path('categories/read/', categories, name='categories'),
    # path('categories/update/<int:pk>/', category_update, name='category_update'),
    # path('categories/delete/<int:pk>/', category_delete, name='category_delete'),
    #
    # path('films/create/category/<int:pk>/', films_create, name='films_create'),
    path('films/read/category/<int:pk>/', films, name='films'),
    # path('films/read/<int:pk>/', films_read, name='films_read'),
    # path('films/update/<int:pk>/', films_update, name='films_update'),
    # path('films/delete/<int:pk>/', films_delete, name='films_delete'),
]
