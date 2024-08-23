from django.contrib import admin

from backend.models import Location, Car, Cargo


# Register your models here.


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'city', 'state', 'zip_code', 'latitude', 'longitude']
    list_display_links = ['id', ]


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'unique_number', 'location', 'load_capacity']
    list_display_links = ['id', ]


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'weight', 'delivery_pick_up',
                    'location_pick_up']
    list_display_links = ['id', ]
