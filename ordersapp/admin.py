from django.contrib import admin

from ordersapp.models import Orders


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'updated', 'status')
    list_filter = ('created', 'user')
