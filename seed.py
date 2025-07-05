import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UBERR.settings')
django.setup()

from uberapp.models import Rider, Driver

def generate_coordinates(base_lat=12.9716, base_lng=77.5946, delta=0.05):
    return (
        round(base_lat + random.uniform(-delta, delta), 6),
        round(base_lng + random.uniform(-delta, delta), 6)
    )

def seed_riders(n=10):
    for i in range(n):
        lat, lng = generate_coordinates()
        Rider.objects.create(
            name=f"Rider {i+1}",
            latitude=lat,
            longitude=lng
        )
    print(f"✅ Seeded {n} riders.")

def seed_drivers(n=15):
    for i in range(n):
        lat, lng = generate_coordinates()
        Driver.objects.create(
            name=f"Driver {i+1}",
            is_available=True,
            latitude=lat,
            longitude=lng
        )
    print(f"✅ Seeded {n} drivers.")

if __name__ == '__main__':
    seed_riders()
    seed_drivers()
