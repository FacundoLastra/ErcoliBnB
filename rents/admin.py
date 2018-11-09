from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Prop, ReservationDate, City

admin.site.site_header = "Ercolibnb: admin page"

class ReservationDateInLine(admin.TabularInline):
    model=ReservationDate
    fk_name='prop'
    extra=0

class AdminPropertyInLine(admin.ModelAdmin):
    inlines=[ReservationDateInLine]

admin.site.register(City)
admin.site.register(Prop, AdminPropertyInLine)

admin.site.unregister(Group)
