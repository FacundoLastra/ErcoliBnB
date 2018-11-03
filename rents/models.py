from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Prop(models.Model):
    description = models.CharField(max_length=500)
    dailyPrice = models.IntegerField()
    image = models.ImageField(upload_to='image', max_length=100)
    title = models.CharField(max_length=50)
    maxGuests = models.IntegerField()
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.title


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
    date = models.DateField()
    prop = models.ForeignKey(Prop, null=True, blank=True, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name_plural = "reservationDates"
