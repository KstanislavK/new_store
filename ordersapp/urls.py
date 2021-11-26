from django.urls import path

from ordersapp.views import OrdersList, OrderItemCreate, OrderRead, OrderUpdate, OrderDelete, order_forming_complete, get_product_price

app_name = 'ordersapp'


urlpatterns = [
    path('', OrdersList.as_view(), name='orders_list'),
    path('create/', OrderItemCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', OrderRead.as_view(), name='order_read'),
    path('update/<int:pk>/', OrderUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='order_delete'),
    path('forming/complete/<int:pk>/', order_forming_complete, name='order_forming_complete'),
    path('product/<int:pk>/price/', get_product_price, name='get_price'),
]
