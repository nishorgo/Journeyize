from django.contrib import admin
from .models import Itinerary, ItineraryEntry, FoodList

# Register your models here.
admin.site.register(Itinerary)
admin.site.register(ItineraryEntry)
admin.site.register(FoodList)