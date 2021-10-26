from django.conf import settings
from django.db import models

from filmsapp.models import Films


class Basket(models.Model):
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

