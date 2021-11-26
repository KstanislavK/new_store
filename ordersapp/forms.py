from django import forms

from filmsapp.models import Films
from ordersapp.models import Orders, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='Цена', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields['film'].queryset = Films.get_items()
            field.widget.attrs['class'] = 'form-control'
