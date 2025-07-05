from django.core.management.base import BaseCommand
from django.utils import timezone
from uberapp.models import Ride, FareConfig
import time
import random

class Command(BaseCommand):
    help = 'Simulate ride flow for rides in create_ride state'

    def handle(self, *args, **kwargs):
        rides = Ride.objects.filter(status='create_ride')
        if not rides.exists():
            self.stdout.write(self.style.WARNING("❗ No rides in 'create_ride' state to simulate."))
            return

        for ride in rides:
            self.stdout.write(f"\n🚗 Simulating Ride {ride.id}...")

            # Step 1: Driver reaches pickup
            ride.status = 'driver_at_location'
            ride.driver_arrived_at = timezone.now()
            ride.save()
            self.stdout.write("✅ Driver reached pickup location")

            # Step 2: Start ride
            time.sleep(1)
            ride.status = 'start_ride'
            ride.ride_started_at = timezone.now()
            ride.save()
            self.stdout.write("✅ Ride started")

            # Step 3: End ride
            time.sleep(1)
            ride.status = 'end_ride'
            ride.ride_ended_at = timezone.now()
            ride.save()
            self.stdout.write("✅ Ride ended")

            # Step 4: Compute fare
            self.compute_fare(ride)

    def compute_fare(self, ride):
        base_fare = self.get_config('base_fare')
        per_km = self.get_config('per_km')
        per_minute = self.get_config('per_minute')
        waiting_charge_per_min = self.get_config('waiting_charge_per_min')

        # Simulate values
        distance_km = random.uniform(2, 10)  # e.g., 5.3 km
        duration_min = (ride.ride_ended_at - ride.ride_started_at).seconds / 60
        waiting_min = (ride.ride_started_at - ride.driver_arrived_at).seconds / 60

        fare = (
            base_fare +
            (distance_km * per_km) +
            (duration_min * per_minute) +
            (waiting_min * waiting_charge_per_min)
        )

        ride.fare = round(fare, 2)
        ride.save()

        self.stdout.write(self.style.SUCCESS(
            f"💰 Ride {ride.id} Fare: ₹{ride.fare:.2f} (Distance: {distance_km:.2f} km, Duration: {duration_min:.2f} mins, Wait: {waiting_min:.2f} mins)"
        ))

    def get_config(self, key):
        return FareConfig.objects.get(key=key).value
