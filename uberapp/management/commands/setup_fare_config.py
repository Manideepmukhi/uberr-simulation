from django.core.management.base import BaseCommand
from uberapp.models import FareConfig

class Command(BaseCommand):
    help = 'Insert or update fare configuration values'

    def handle(self, *args, **kwargs):
        configs = {
            'base_fare': 50.0,
            'per_km': 10.0,
            'per_minute': 2.0,
            'waiting_charge_per_min': 1.0,
        }

        for key, value in configs.items():
            FareConfig.objects.update_or_create(key=key, defaults={'value': value})
            self.stdout.write(self.style.SUCCESS(f"✅ {key} set to {value}"))

        self.stdout.write(self.style.SUCCESS("🎉 Fare configuration setup complete!"))

