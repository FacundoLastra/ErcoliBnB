from datetime import datetime
from django.shortcuts import render, redirect
from django.http import Http404
from rents.models import *

# Create your views here.
def index(request):
    cities = City.objects.all()
    if 'cityId' in request.GET:
        filtered = Prop.objects.all().filter(city = request.GET['cityId'])
        city = City.objects.all().filter(id = request.GET['cityId'])
        if city:
            city = city[0]
        cities = City.objects.exclude(id = request.GET['cityId'] )
        context = {
            'props': filtered,
            'cities': cities,
            'selectedCity':city
        }
        return render(request, 'rents/index.html', context)
    else:
        props = Prop.objects.all()
        context = {
            'props': props,
            'cities': cities
        }
        return render(request, 'rents/index.html', context)


def detail(request, propid):
    try:
        propInfo = Prop.objects.get(id=propid)
    except Prop.DoesNotExist:
        raise Http404("No existe la propiedad")
    return render(request, 'rents/propInfo.html', {'propInfo': propInfo})


def reserveProp(request):
    if request.method == 'POST':
        beginDate = datetime.strptime(request.POST['dateFrom'], '%Y-%m-%d').date()
        endDate = datetime.strptime(request.POST['dateTo'], '%Y-%m-%d').date()
        prop = Prop.objects.get(id=request.POST['propId'])
        reservationDates = ReservationDate.objects.filter(prop=prop.id)
        for reservationDate in reservationDates:
            if reservationDate  is not None:
                if reservationDate.checkIn <= beginDate <= endDate:
                    return render(request, 'rents/notAvailable.html')
                if reservationDate.checkIn <= endDate <= reservationDate.checkOut:
                    return render(request, 'rents/notAvailable.html')
        rd = ReservationDate(
            date=datetime.now().date(),
            checkIn=beginDate,
            checkOut=endDate,
            prop=prop)
        r = Reservation(
            reservationDate=rd,
            prop=prop,
            firstName=request.POST['firstName'],
            lastName=request.POST['lastName'],
            email=request.POST['email'])
        rd.reservation=r
        rd.save()
        r.total = r.prop.dailyPrice * r.prop.reservationdate_set.filter(reservation=r).count()
        r.save()
        return redirect('rents:okReservation', r.id)


def okReservation(request, idReservation):
    try:
        reservation = Reservation.objects.get(id=idReservation)
    except Prop.DoesNotExist:
        raise Http404("Propiedad no encontrada")
    return render(request, 'rents/okReservation.html', {'prop': reservation})