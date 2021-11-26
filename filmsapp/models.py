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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Серия"
        verbose_name_plural = "Серии"


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
        default="films_img/johnson_default.png"
    )
    price_roll = models.IntegerField(
        verbose_name="цена за рулон",
        default=0,
    )
    price_meter = models.IntegerField(
        verbose_name="цена за метр",
        default=0,
    )
    quantity = models.IntegerField(
        verbose_name='количество',
        default=1,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пленка"
        verbose_name_plural = "Пленки"

    @staticmethod
    def get_items():
        return Films.objects.filter(is_active=True).order_by('category', 'name')
