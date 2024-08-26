import random
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from backend.validators import validate_unique_number


class Location(models.Model):
    city = models.CharField(max_length=255, verbose_name='Город')
    state = models.CharField(max_length=255, verbose_name='Штат')
    zip_code = models.CharField(max_length=10, unique=True,
                                verbose_name='Почтовый индекс (zip),')
    latitude = models.DecimalField(max_digits=10, decimal_places=7,
                                   verbose_name='Широта')
    longitude = models.DecimalField(max_digits=10, decimal_places=7,
                                    verbose_name='Долгота')

    def __str__(self):
        return f"{self.city}, {self.state} {self.zip_code}"

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = "Список локаций"


class Car(models.Model):
    id = models.BigIntegerField(primary_key=True)
    unique_number = models.CharField(max_length=5,
                                     verbose_name="Уникальный номер",
                                     unique=True,
                                     validators=[validate_unique_number])
    location = models.ForeignKey(Location, verbose_name='Текущая локация',
                                 related_name='car',
                                 on_delete=models.CASCADE, null=True,
                                 blank=True)
    load_capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        verbose_name="Грузоподъёмность")

    def __str__(self):
        return f"{self.unique_number}, {self.load_capacity}"

    class Meta:
        verbose_name = 'Машины'
        verbose_name_plural = "Список машин"

    def save(self, *args, **kwargs):
        """ При создании машин по умолчанию локация
         каждой машины заполняется случайным образом"""
        if not self.location:
            if Location.objects.exists():
                location_id = random.choice(
                    Location.objects.values_list('id', flat=True))
                self.location = Location.objects.get(id=location_id)
        super().save(*args, **kwargs)
        # locations = Location.objects.all()
        # if locations.exists():
        #     self.location = random.choice(locations)
        # super().save(*args, **kwargs)


class Cargo(models.Model):
    location_pick_up = models.ForeignKey(Location,
                                         verbose_name='Локация самовывоза',
                                         related_name='location_pick_up_cargo',
                                         on_delete=models.CASCADE)

    delivery_pick_up = models.ForeignKey(Location,
                                         verbose_name='Локация доставка груза',
                                         related_name='delivery_pick_up_cargo',
                                         on_delete=models.CASCADE)

    weight = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        verbose_name="Вес груза")

    description = models.CharField(max_length=500, verbose_name='Описание')

    def __str__(self):
        return f"{self.weight}, {self.description}"

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = "Список грузов"
