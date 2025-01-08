from django.contrib import admin # type: ignore
from .models import Resources, Bookings

# Register your models here.
admin.site.register(Resources)
admin.site.register(Bookings)