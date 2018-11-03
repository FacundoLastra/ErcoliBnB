from django.contrib import admin
from .models import City, Prop, ReservationDate, Reservation

# Register your models here.

admin.site.register(City)
admin.site.register(Prop)
admin.site.register(ReservationDate)
admin.site.register(Reservation)