from django.urls import path
from . import views

urlpatterns = [
    path('choose-region/', views.choose_region, name='choose_region'),
    path('choose-places/', views.choose_places, name='choose_places'),
    path('final/', views.generate_itinerary_view, name='generate_itinerary'),
    path('create/', views.save_itinerary_entries, name='create_itinerary'),
    path('foods/<int:itinerary_id>', views.create_food_list, name='foods'),
    path('detail/<int:itinerary_id>/', views.itinerary_detail, name='itinerary_detail'),
    path('update/<int:itinerary_id>/', views.update_itinerary, name='update_itinerary')
]
