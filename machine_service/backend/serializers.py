from geopy import Nominatim
from geopy.distance import geodesic
from rest_framework import serializers
from backend.models import Cargo, Car


class CargoCreatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['location_pick_up', 'delivery_pick_up', 'weight',
                  'description']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'id', 'unique_number', 'location', 'load_capacity',)



class CargoSerializer(serializers.ModelSerializer):
    pick_up_location = serializers.SerializerMethodField()
    delivery_location = serializers.SerializerMethodField()
    nearest_cars = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ['pick_up_location', 'delivery_location', 'weight',
                  'description', 'nearest_cars']

    def get_pick_up_location(self, obj):
        return f"{obj.location_pick_up.city}, {obj.location_pick_up.state} {obj.location_pick_up.zip_code}"

    def get_delivery_location(self, obj):
        return f"{obj.delivery_pick_up.city}, {obj.delivery_pick_up.state} {obj.delivery_pick_up.zip_code}"

    def get_nearest_cars(self, obj):

        location = obj.location_pick_up
        geolocator = Nominatim(user_agent="my_app")
        location_point = (location.latitude, location.longitude)
        cars = Car.objects.all()
        nearest_cars = []
        for car in cars:
            car_location = car.location
            car_point = (car_location.latitude, car_location.longitude)
            distance = geodesic(location_point, car_point).miles
            if distance <= 450:
                nearest_cars.append(car)
        return len(nearest_cars)


class CargoDetailSerializer(serializers.ModelSerializer):
    pick_up_location = serializers.SerializerMethodField()
    delivery_location = serializers.SerializerMethodField()
    cars = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ['pick_up_location', 'delivery_location', 'weight',
                  'description', 'cars']

    def get_pick_up_location(self, obj):
        return f"{obj.location_pick_up.city}, {obj.location_pick_up.state} {obj.location_pick_up.zip_code}"

    def get_delivery_location(self, obj):
        return f"{obj.delivery_pick_up.city}, {obj.delivery_pick_up.state} {obj.delivery_pick_up.zip_code}"

    def get_cars(self, location):
        location = location.location_pick_up
        geolocator = Nominatim(user_agent="my_app")
        location_point = (location.latitude, location.longitude)
        cars = Car.objects.all()
        car_list = []
        for car in cars:
            car_location = car.location
            car_point = (car_location.latitude, car_location.longitude)
            distance = geodesic(location_point, car_point).miles
            car_list.append(
                f"unique_number_car:{car.unique_number}, "
                f"distance:{distance:.2f} miles")
        return car_list


class FilteredCargoSerializer(serializers.ModelSerializer):
    pick_up_location = serializers.SerializerMethodField()
    delivery_location = serializers.SerializerMethodField()
    cars = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ['pick_up_location', 'delivery_location', 'weight',
                  'description', 'cars']

    def get_pick_up_location(self, obj):
        return f"{obj.location_pick_up.city}, {obj.location_pick_up.state} {obj.location_pick_up.zip_code}"

    def get_delivery_location(self, obj):
        return f"{obj.delivery_pick_up.city}, {obj.delivery_pick_up.state} {obj.delivery_pick_up.zip_code}"

    def get_cars(self, obj):
        return self.context.get('cars')
