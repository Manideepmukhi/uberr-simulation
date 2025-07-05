from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from uberapp.models import Ride, Driver
import math
import random

class Command(BaseCommand):
    help = 'Assign drivers to pending rides (create_ride state) based on proximity and rules'

    def handle(self, *args, **kwargs):
        unassigned_rides = Ride.objects.filter(status='create_ride')
        available_drivers = Driver.objects.filter(is_available=True)

        for ride in unassigned_rides:
            print(f"\n🔍 Checking ride {ride.id}...")

            assigned = False
            search_radius_km = 2

            while not assigned and search_radius_km <= 10:  # Max 10 km search
                print(f"📡 Searching drivers within {search_radius_km} km...")

                for driver in available_drivers:
                    if self.is_within_radius(ride.pickup_lat, ride.pickup_lng,
                                             driver.latitude, driver.longitude, search_radius_km):
                        if not self.is_driver_disqualified(driver, ride.rider_id):
                            # Assign driver
                            ride.driver = driver
                            ride.status = 'driver_assigned'
                            ride.driver_assigned_at = timezone.now()
                            ride.save()

                            driver.is_available = False
                            driver.save()

                            print(f"✅ Assigned driver {driver.name} to ride {ride.id}")
                            assigned = True
                            break

                search_radius_km += 2  # Expand search

            if not assigned:
                print(f"❌ No driver found for ride {ride.id}")

    def is_within_radius(self, lat1, lon1, lat2, lon2, radius_km):
        # Use Haversine formula
        R = 6371  # Earth radius in km
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance <= radius_km

    def is_driver_disqualified(self, driver, rider_id):
        # Add abuse prevention logic here
        from datetime import timedelta
        from uberapp.models import Ride

        # Rule 1: Already assigned → skip
        if Ride.objects.filter(driver=driver, status__in=[
            'driver_assigned', 'driver_at_location', 'start_ride']).exists():
            return True

        # Rule 2: Recently completed ride with same rider
        thirty_minutes_ago = timezone.now() - timedelta(minutes=30)
        if Ride.objects.filter(driver=driver, rider_id=rider_id,
                               ride_ended_at__gte=thirty_minutes_ago).exists():
            return True

        # Rule 3: Cancelled last 2 rides
        if driver.cancelled_rides_count >= 2:
            return True

        return False
