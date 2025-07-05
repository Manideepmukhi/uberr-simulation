from django.contrib import admin
from .models import Driver, Rider, Ride, FareConfig

admin.site.register(Driver)
admin.site.register(Rider)
admin.site.register(Ride)
admin.site.register(FareConfig)
