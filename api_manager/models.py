from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User


class Itinerary(models.Model):
    """
    A model representing an itinerary with the following fields:
    - name: a unique string representing the name of the itinerary
    - user: a foreign key to the User model representing the user who created the itinerary
    - destination: a string representing the destination of the itinerary (optional)
    - created_at: a datetime field representing the date and time the itinerary was created
    """
    name = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_unique_name(self, base_name, user):
        """
        Generate a unique name for an itinerary by appending a suffix to the base name.
        @param base_name - the base name for the itinerary
        @param user - the user associated with the itinerary
        @return A unique name for the itinerary
        """
        suffix = 1
        new_name = base_name
        while Itinerary.objects.filter(name=new_name, user=user).exists():
            suffix += 1
            new_name = f"{base_name} {suffix}"
        return new_name

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.name = self.generate_unique_name(self.name, self.user)
        super(Itinerary, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ['-created_at']


class ItineraryEntry(models.Model):
    """
    A model representing an entry in an itinerary.
    """
    date = models.DateField(null=True, blank=True)
    avgtemp = models.FloatField(null=True, blank=True)
    avg_humidity = models.FloatField(null=True, blank=True)
    rain_probability = models.FloatField(null=True, blank=True)
    snow_probability = models.FloatField(null=True, blank=True)
    activity = models.TextField()
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='itinerary_entries')

    def __str__(self):
        return f"{self.date}"
    
    class Meta:
        ordering = ['date']
    

class FoodList(models.Model):
    """
    A model representing a list of food items.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='food_list')

    def __str__(self):
        return f"{self.name}"