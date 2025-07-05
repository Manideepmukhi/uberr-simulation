from django.db import models
from django.utils import timezone


class Driver(models.Model):
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    cancelled_rides_count = models.IntegerField(default=0)
    last_completed_ride_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Rider(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        CREATED = 'create_ride', 'Create Ride'
        ASSIGNED = 'driver_assigned', 'Driver Assigned'
        AT_LOCATION = 'driver_at_location', 'Driver at Location'
        STARTED = 'start_ride', 'Ride Started'
        ENDED = 'end_ride', 'Ride Ended'

    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    drop_lat = models.FloatField()
    drop_lng = models.FloatField()
    status = models.CharField(max_length=20, choices=RideStatus.choices, default=RideStatus.CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    driver_assigned_at = models.DateTimeField(null=True, blank=True)
    driver_arrived_at = models.DateTimeField(null=True, blank=True)
    ride_started_at = models.DateTimeField(null=True, blank=True)
    ride_ended_at = models.DateTimeField(null=True, blank=True)
    fare = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status}"


class FareConfig(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.key} = {self.value}"
