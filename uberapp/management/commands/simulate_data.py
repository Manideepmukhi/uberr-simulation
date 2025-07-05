import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from uberapp.models import Rider, Driver, Ride

class Command(BaseCommand):
    help = "Simulates riders, drivers, and initial ride requests"

    def handle(self, *args, **options):
        Ride.objects.all().delete()
        Rider.objects.all().delete()
        Driver.objects.all().delete()

        print("Creating 10 riders...")
        for i in range(10):
            Rider.objects.create(
                name=f"Rider {i+1}",
                latitude=22.50 + random.uniform(0, 0.1),
                longitude=88.30 + random.uniform(0, 0.1)
            )
        print("✔ Riders created")

        print("Creating 15 drivers...")
        for i in range(15):
            Driver.objects.create(
                name=f"Driver {i+1}",
                is_available=True,
                latitude=22.50 + random.uniform(0, 0.1),
                longitude=88.30 + random.uniform(0, 0.1)
            )
        print("✔ Drivers created")

        riders = list(Rider.objects.all())
        print("Creating ride requests (1–2 per rider)...")
        for rider in riders:
            for _ in range(random.randint(1, 2)):
                Ride.objects.create(
                    rider=rider,
                    pickup_lat=rider.latitude,
                    pickup_lng=rider.longitude,
                    drop_lat=22.50 + random.uniform(0, 0.1),
                    drop_lng=88.30 + random.uniform(0, 0.1)
                )
        print("✔ Ride requests created successfully 🎉")
