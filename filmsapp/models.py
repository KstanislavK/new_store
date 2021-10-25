from django.db import models


class FilmsCategory(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="имя",
    )

    description = models.TextField(
        verbose_name="описание",
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Films(models.Model):
    category = models.ForeignKey(
        FilmsCategory,
        on_delete=models.PROTECT,
        verbose_name="категория",
    )
    name = models.CharField(
        verbose_name="название",
        max_length=128,
    )
    short_desc = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="краткое описание"
    )
    image = models.ImageField(
        upload_to="films_img",
        blank=True,
    )
    price_roll = models.IntegerField(
        verbose_name="цена",
        default=0,
    )
    price_meter = models.IntegerField(
        verbose_name="цена",
        default=0,
    )
