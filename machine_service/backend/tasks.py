from celery import shared_task
import random
from backend.models import Location,Car


@shared_task
def upload_location_car():
    cars = Car.objects.all()
    locations = Location.objects.all()
    for car in cars:
        car.location = random.choice(locations)
        car.save()
    return 'Done'
