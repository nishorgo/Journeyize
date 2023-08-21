from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User


class Itinerary(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_unique_name(self, base_name, user):
        suffix = 1
        new_name = base_name
        while Itinerary.objects.filter(name=new_name, user=user).exists():
            suffix += 1
            new_name = f"{base_name} {suffix}"
        return new_name

    def save(self, *args, **kwargs):
        if Itinerary.objects.filter(name=self.name, user=self.user).exists():
            self.name = self.generate_unique_name(self.name, self.user)
        super(Itinerary, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"


class ItineraryEntry(models.Model):
    date = models.DateField(null=True, blank=True)
    avgtemp = models.FloatField(null=True, blank=True)
    avg_humidity = models.FloatField(null=True, blank=True)
    rain_probability = models.FloatField(null=True, blank=True)
    snow_probability = models.FloatField(null=True, blank=True)
    activity = models.TextField()
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='itinerary_entries')

    def __str__(self):
        return f"{self.date}"
    

class FoodList(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='food_list')

    def __str__(self):
        return f"{self.name}"




