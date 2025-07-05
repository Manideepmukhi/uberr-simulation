from django.db import models


class Rider(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    is_available = models.BooleanField(default=True)
    last_completed_ride_at = models.DateTimeField(null=True, blank=True)
    cancelled_rides = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        CREATE_RIDE = 'create_ride'
        DRIVER_ASSIGNED = 'driver_assigned'
        DRIVER_AT_LOCATION = 'driver_at_location'
        START_RIDE = 'start_ride'
        END_RIDE = 'end_ride'

    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)

    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    drop_lat = models.FloatField()
    drop_lng = models.FloatField()

    status = models.CharField(
        max_length=30,
        choices=RideStatus.choices,
        default=RideStatus.CREATE_RIDE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    driver_assigned_at = models.DateTimeField(null=True, blank=True)
    driver_at_location_at = models.DateTimeField(null=True, blank=True)
    ride_start_at = models.DateTimeField(null=True, blank=True)
    ride_end_at = models.DateTimeField(null=True, blank=True)

    fare = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status}"

