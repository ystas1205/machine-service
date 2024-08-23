from django.urls import path

from backend.views import CargoView, CarView, FilteredCargoView

app_name = 'backend'
urlpatterns = [
    path('cargo', CargoView.as_view(), name='shipments'),
    path('car', CarView.as_view(), name='car'),
    path('cargo/<int:pk>/', CargoView.as_view()),
    path('cargo/filter/',
         FilteredCargoView.as_view({'get': 'get_filtered_cargos'}),
         name='filtered_shipments')

]
