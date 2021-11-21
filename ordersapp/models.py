from django.conf import settings
from django.db import models
from filmsapp.models import Films


class Orders(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'оптравлено в обработку'),
        (PROCEEDED, 'обрабатывается'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создан'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='обновлен'
    )
    status = models.CharField(
        verbose_name='статус',
        max_length=3,
        choices=ORDER_STATUS_CHOICES,
        default=FORMING
    )
    is_active = models.BooleanField(
        verbose_name='активен',
        default=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.film.price_roll, items)))

    # def delete(self):
    #     for item in self.orderitems.select_related():
    #         item.film.quantity += item.quantity
    #         item.film.save()
    #
    #     self.is_active = False
    #     self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Orders,
        related_name='orderitems',
        on_delete=models.CASCADE,
    )
    film = models.ForeignKey(
        Films,
        verbose_name='пленка',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )

    def get_product_cost(self):
        return self.film.price_roll * self.quantity
