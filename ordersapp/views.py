from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basketapp.models import Basket
from filmsapp.models import Films
from ordersapp.forms import OrderItemForm
from ordersapp.models import Orders, OrderItem


class OrdersList(ListView):
    model = Orders

    def get_queryset(self):
        return Orders.objects.all()


class OrderItemCreate(CreateView, LoginRequiredMixin):
    model = Orders
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Orders, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Orders, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['film'] = basket_items[num].film
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].film.price_roll
                # basket_items.delete()
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemCreate, self).form_valid(form)


class OrderUpdate(UpdateView, LoginRequiredMixin):
    model = Orders
    fields = []
    context_object_name = 'objects'
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Orders, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST)
            # formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.film.price_roll

            data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView, LoginRequiredMixin):
    model = Orders
    success_url = reverse_lazy('orders:orders_list')


class OrderRead(DetailView, LoginRequiredMixin):
    model = Orders
    template_name = 'ordersapp/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data()
        context['title'] = 'Просмотр заказа'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    order.status = Orders.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orders:orders_list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def film_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'film':
        if instance.pk:
            instance.film.quantity -= instance.quantity - sender.get_items(instance.pk).quantity
        else:
            instance.film.quantity -= instance.quantity
        instance.film.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def film_quantity_update_delete(sender, instance, **kwargs):
        instance.film.quantity += instance.quantity
        instance.film.save()


def get_product_price(request, pk):
    if request.is_ajax():
        product = Films.objects.filter(pk=int(pk)).first()
        if product:
            return JsonResponse({'price': product.price_roll})
        else:
            return JsonResponse({'price': 0})
