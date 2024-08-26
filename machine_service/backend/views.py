from django.http import JsonResponse
from geopy.distance import geodesic, distance
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from geopy.geocoders import Nominatim
from backend.models import Location, Cargo, Car
from backend.serializers import CargoSerializer, CarSerializer, \
    CargoDetailSerializer, FilteredCargoSerializer, CargoCreatingSerializer
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet


class CargoView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        """Создание нового груза (характеристики локаций pick-up,
         delivery определяются по введенному zip-коду);
        """
        if {'pick_up_zip_code', 'delivery_zip_code', 'weight',
            'description'}.issubset(request.data):

            pick_up_zip_code = request.data.get('pick_up_zip_code')
            delivery_zip_code = request.data.get('delivery_zip_code')

            try:
                pick_up_zip_code = Location.objects.get(
                    zip_code=pick_up_zip_code)
                delivery_zip_code = Location.objects.get(
                    zip_code=delivery_zip_code)
                request.data._mutable = True
                request.data.update(
                    {'location_pick_up': pick_up_zip_code.id,
                     "delivery_pick_up": delivery_zip_code.id})
                serializer = CargoCreatingSerializer(data=request.data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    return JsonResponse({'status': 'Груз добавлен'},
                                        status=status.HTTP_201_CREATED)

            except Location.DoesNotExist:
                return JsonResponse(
                    {'error': 'Данной локации в базе нет'},
                    status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(
            {'Status': 'Не указаны все необходимые аргументы'},
            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        """Получение списка грузов (локации pick-up, delivery,
         количество ближайших машин до груза ( =< 450 миль))"""
        if pk is None:
            cargos = Cargo.objects.all()

            serializer = CargoSerializer(cargos, many=True)
            return Response(serializer.data)
        else:
            try:
                cargos = Cargo.objects.get(id=pk)
            except Cargo.DoesNotExist:
                return Response({'error': 'Данного груза в базе нет'},
                                status=404)
            serializer = CargoDetailSerializer(cargos)
            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """ Удаление груза по ID """
        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            query = Q()
            objects_deleted = False
            for contact_id in items_list:
                if contact_id.isdigit():
                    query = query | Q(id=contact_id)
                    objects_deleted = True
                else:
                    return JsonResponse(
                        {'message': 'Введены некорректные данные'},
                        status=status.HTTP_403_FORBIDDEN)
            if objects_deleted:
                deleted_count = Cargo.objects.filter(query).delete()[
                    0]
                return JsonResponse(
                    {'message': f'Удалено {deleted_count}'},
                    status=status.HTTP_204_NO_CONTENT)
        return JsonResponse(
            {'Status': 'Не указаны все необходимые аргументы'},
            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """ Редактирование груза по ID (вес, описание) """

        if 'id' in request.data:
            if request.data['id'].isdigit():
                try:
                    cargo = Cargo.objects.get(id=request.data['id'])
                except Cargo.DoesNotExist:
                    return Response({'error': 'Данного груза в базе нет'})
                if cargo:
                    serializer = CargoSerializer(cargo,
                                                 data=request.data,
                                                 partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response(
                            {'status': 'Груз обновлен'},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'Status': 'Не указаны все необходимые аргументы'},
            status=status.HTTP_400_BAD_REQUEST)


class CarView(APIView):
    parser_classes = [MultiPartParser]

    def patch(self, request, *args, **kwargs):
        """ Редактирование машины по ID
        (локация (определяется по введенному zip-коду))) """

        if 'id' in request.data and 'location_zip_code' in request.data:
            if request.data['id'].isdigit():
                try:
                    car = Car.objects.get(id=request.data['id'])
                    location = Location.objects.get(
                        zip_code=request.data['location_zip_code'])
                except Location.DoesNotExist:
                    return JsonResponse(
                        {'error': 'Данной локации в базе нет'},
                        status=status.HTTP_404_NOT_FOUND)
                except Car.DoesNotExist:
                    return JsonResponse(
                        {'error': 'Данной машины в базе нет'},
                        status=status.HTTP_404_NOT_FOUND)

                if car and location:
                    request.data._mutable = True
                    request.data.update(
                        {'location': location.id})

                serializer = CarSerializer(car,
                                           data=request.data,
                                           partial=True,
                                           )

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return JsonResponse(
                        {'status': 'Машина обновлена'},
                        status=status.HTTP_201_CREATED)
        return JsonResponse(
            {'Status': 'Не указаны все необходимые аргументы'},
            status=status.HTTP_400_BAD_REQUEST)


class FilteredCargoView(ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    @action(detail=False, methods=['get'], url_path='filter',
            url_name='filter')
    def get_filtered_cargos(self, request, *args, **kwargs):
        """ Фильтр списка грузов (вес, мили ближайших машин до грузов)"""
        global distance
        weight_min = request.query_params.get('weight_min', '1')
        weight_max = request.query_params.get('weight_max', '1000')
        distance_max = request.query_params.get('distance_max', '100000')
        if weight_min.isdigit() and weight_max.isdigit() and distance_max.isdigit():
            cargos = Cargo.objects.filter(weight__gte=weight_min,
                                          weight__lte=weight_max)
            list_cargos = []
            for cargo in cargos:
                distance = self.get_car(distance_max,
                                        cargo.location_pick_up)
                list_cargos.append(cargo)

            serializer = FilteredCargoSerializer(list_cargos, many=True,
                                                 context={'cars': distance})
            return Response(serializer.data)
        return JsonResponse(
            {'Status': 'Введены некорректные данные'},
            status=status.HTTP_400_BAD_REQUEST)

    def get_car(self, distance_max, location):
        """ Получение машин с дистанцией до грузов"""
        geolocator = Nominatim(user_agent="my_app")
        location_point = (location.latitude, location.longitude)
        cars = Car.objects.all()
        car_list = []
        for car in cars:
            car_location = car.location
            car_point = (car_location.latitude, car_location.longitude)
            distance = geodesic(location_point, car_point).miles
            if distance <= int(distance_max):
                car_list.append({'number_car': car.unique_number,
                                 'distance': f"{distance:.2f}"})
        return car_list
