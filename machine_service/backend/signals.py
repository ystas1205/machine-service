import random
import string
import json
from django.db import IntegrityError
from django.db.models.signals import pre_save, post_migrate
from django.dispatch import receiver
from backend.models import Car, Location


@receiver(pre_save, sender=Car)
def add_random_letter(sender, instance, **kwargs):
    """ Генерация случайной заглавной буквы английского алфавита"""
    if len(instance.unique_number) == 5:
        # random_letter = random.choice(string.ascii_uppercase)
        instance.unique_number = f"{instance.unique_number}"
    else:
        random_letter = random.choice(string.ascii_uppercase)
        instance.unique_number = f"{instance.unique_number}{random_letter}"


@receiver(post_migrate)
def load_data_from_json_location(sender, **kwargs):
    """Выгрузку списка в базу данных Postgres при запуске приложения."""
    with open('location.json') as f:
        data = json.load(f)
    for item in data:
        try:
            Location.objects.create(**item)
        except IntegrityError:
            pass


@receiver(post_migrate)
def load_data_from_json_car(sender, **kwargs):
    """ Заполнение БД 20 машинами при запуске приложениня."""
    with open('car.json') as f:
        data = json.load(f)
    for item in data:
        try:
            Car.objects.create(**item)
        except IntegrityError:
            pass
