from django.core.management.base import BaseCommand
import json
import os

from authapp.models import ShopUser
from filmsapp.models import FilmsCategory, Films

JSON_PATH = 'filmsapp/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('series')

        FilmsCategory.objects.all().delete()
        for category in categories:
            new_category = FilmsCategory(**category)
            new_category.save()

        films = load_from_json('films')

        Films.objects.all().delete()
        for film in films:
            category_name = film['category']

            _category = FilmsCategory.objects.get(name=category_name)
            film['category'] = _category
            new_film = Films(**film)
            new_film.save()

        ShopUser.objects.create_superuser('admin', 'admin@local', 'admin')
