from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basketapp.models import Basket
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
                basket_items.delete()
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
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)

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

