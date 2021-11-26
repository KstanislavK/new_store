from django.conf import settings
from django.db import models

from filmsapp.models import Films
from ordersapp.models import OrderItem


class BasketQuerySet(models.QuerySet):
    def data(self, *args, **kwargs):
        for object in self:
            object.film.quantity += object.quantity
            object.film.quantity.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket'
    )
    film = models.ForeignKey(
        Films,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name="количество",
        default=0
    )
    add_datetime = models.DateTimeField(
        verbose_name="время",
        auto_now_add=True
    )

    @staticmethod
    def get_items(pk):
        return Basket.objects.filter(pk=pk).first()

    @property
    def film_cost(self):
        return self.film.price_roll * self.quantity

    @property
    def total_quantity(self):
        items = Basket.objects.filter(user=self.user)
        total_quantity = sum(list(map(lambda x: x.quantity, items)))
        return total_quantity

    @property
    def total_cost(self):
        items = Basket.objects.filter(user=self.user)
        total_cost = sum(list(map(lambda x: x.film_cost, items)))
        return total_cost

    def save(self, *args, **kwargs):
        if self.pk:
            self.film.quantity -= self.quantity - self.__class__.get_items(self.pk).quantity
        else:
            self.film.quantity -= self.quantity
        self.film.save()
        super(self.__class__, self).save(*args, **kwargs)
