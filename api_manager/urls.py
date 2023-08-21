from django.urls import path
from .views import choose_region, choose_places, create_food_list, generate_itinerary_view, save_itinerary_entries, itinerary_detail

urlpatterns = [
    path('choose-region/', choose_region, name='choose_region'),
    path('choose-places/', choose_places, name='choose_places'),
    path('final/', generate_itinerary_view, name='generate_itinerary'),
    path('create/', save_itinerary_entries, name='create_itinerary'),
    path('foods/<int:itinerary_id>', create_food_list, name='foods'),
    path('detail/<int:itinerary_id>/', itinerary_detail, name='itinerary_detail'),
]
