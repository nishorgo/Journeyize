from django.urls import path
from .views import choose_region, choose_places, choose_foods, itinerary_view

urlpatterns = [
    path('choose-region/', choose_region, name='choose_region'),
    path('choose-places/', choose_places, name='choose_places'),
    path('choose-foods/', choose_foods, name='choose_foods'),
    path('final/', itinerary_view, name='itinerary_view'),
]
