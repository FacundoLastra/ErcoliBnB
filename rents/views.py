from datetime import datetime
from django.shortcuts import render, redirect
from django.http import Http404
from rents.models import *


# Create your views here.
def index(request):
    cities = City.objects.all()
    if 'filter' in request.GET:
        filtered = Prop.objects.all().filter(city=request.GET['idCity'])
        context = {
            'props': filtered,
            'cities': cities
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
        propInfo = Propiedad.objects.get(id=propiedadid)
    except Prop.DoesNotExist:
        raise Http404("No existe la propiedad")
    return render(request, 'rents/propInfo.html', {'propInfo': propInfo})


def reserve(request):
    if request.method == 'POST':
        beginDate = datetime.strptime(request.POST['dateFrom'], '%Y-%m-%d').date()
        endDate = datetime.strptime(request.POST['dateTo'], '%Y-%m-%d').date()
        prop = Prop.objects.get(id=request.POST['propId'])
        reservationDates = Reserva.objects.filter(propiedad=prop.id)
        for reservationDate in reservationDates:
            if reservationDate.reservationDate is not None:
                if beginDate <= reservationDate.reservationDate <= endDate:
                    return render(request, 'rents/notAvailable.html')
        r = Reservation(
            resevationDate=datetime.now().date(),
            prop=prop,
            firstName=request.POST['firstName'],
            lastName=request.POST['lastName'],
            email=request.POST['email'])
        r.save()
        for reservationDate in reservationDates:
            if beginDate <= reservationDate.reservationDate <= endDate:
                reservationDate.reservationDate = r
                reservationDate.save()
        r.total = 100#harcode value => r.propiedad.precioDiario * r.propiedad.fechaAlquiler_set.filter(reserva=r).count()
        r.save()
        return redirect('rents:okReservation', r.id)


def okReservation(request, idReservation):
    try:
        reservation = Reserva.objects.get(id=idReserva)
    except Prop.DoesNotExist:
        raise Http404("Propiedad no encontrada")
    return render(request, 'rents/okReservation.html', {'prop': reservation})