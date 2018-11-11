from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Prop(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50, default="Property Name")
    description = models.CharField(max_length=500, default="No description available")
    dailyPrice = models.IntegerField()
    image = models.ImageField(upload_to='image', max_length=100)
    maxGuests = models.IntegerField()
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.name

class Reservation(models.Model):
    total = models.IntegerField(blank=True, null=True)
    firstName = models.CharField(blank=True, null=True, max_length=50)
    lastName = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(blank=True, null=True, max_length=200)
    prop = models.ForeignKey(Prop, on_delete=models.PROTECT, blank=False, null=False)
    reservationDate = models.DateField(blank=False, null=False, auto_now=True)

    def __str__(self):
        return self.firstName + ' ' + self.lastName

class ReservationDate(models.Model):
    date = models.DateField(blank=False, null=False)
    prop = models.ForeignKey(Prop, on_delete=models.PROTECT, blank=False, null=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "reservationDates"