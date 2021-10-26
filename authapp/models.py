from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    company_name = models.CharField(max_length=64, verbose_name="название компании", blank=True)
