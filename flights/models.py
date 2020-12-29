from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    # origin = models.CharField(max_length=64)
    # destination = models.CharField(max_length=64)
    origin = models.ForeignKey(
        Airport, on_delete=CASCADE, related_name="departures")
    destination = models.ForeignKey(
        Airport, on_delete=CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

    def is_valid_flight(self):
        return self.origin != self.destination and self.duration > 0


class Passenger(models.Model):
    name = models.CharField(max_length=120)
    flights = models.ManyToManyField(
        Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.name}"
