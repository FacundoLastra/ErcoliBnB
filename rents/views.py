from datetime import datetime
from django.shortcuts import render, redirect
from django.http import Http404
from rents.models import *
from datetime import timedelta

# Create your views here.
def index(request):
    cities = City.objects.all()
    if 'cityId' and 'dateFrom' and 'dateTo' and 'guestCount' in request.GET:
        filtered = filterProps(request.GET['cityId'],request.GET['dateFrom'],request.GET['dateTo'],request.GET['guestCount'])
        
        selectedCity = City.objects.get(id = request.GET['cityId'])
        
        request.session['dateFrom'] = request.GET['dateFrom']
        request.session['dateTo'] = request.GET['dateTo']
        request.session['guestCount'] = request.GET['guestCount']

        cities = City.objects.exclude(id = request.GET['cityId'] )

        context = {
            'userSearch': True,
            'props': filtered,
            'cities': cities,
            'selectedCity':selectedCity
        }
        return render(request, 'rents/index.html', context)
    else:
        request.session.flush()
        context = {
            'userSearch': False,
            'cities': cities
        }
        return render(request, 'rents/index.html', context)


def detail(request, propid):
    try:
        propInfo = Prop.objects.get(id=propid)
        propDays = ReservationDate.objects.filter(prop=propInfo, reservation=None)
    except Prop.DoesNotExist:
        raise Http404("No existe la propiedad")
    return render(request, 'rents/propInfo.html', {'propInfo': propInfo,'propDays': propDays})


def reserveProp(request):
    if request.method == 'POST':
        
        dateFrom = datetime.strptime(request.POST['dateFrom'], '%Y-%m-%d').date()
        dateTo = datetime.strptime(request.POST['dateTo'], '%Y-%m-%d').date()
        
        prop = Prop.objects.get(id=request.POST['propId'])

        if not isAvailableProp(prop, dateFrom, dateTo) or int(request.POST['guestCount'],10) > prop.maxGuests:
            return render(request, 'rents/notAvailable.html')
        
        reservation = Reservation(
            reservationDate = datetime.now().date(),
            prop = prop,
            firstName = request.POST['firstName'],
            lastName = request.POST['lastName'],
            email = request.POST['email'])  
        reservation.save()

        associateReservationToReservationDates(reservation, dateFrom, dateTo)

        reservation.total = reservation.prop.dailyPrice * reservation.prop.reservationdate_set.filter(reservation=reservation).count()
        
        reservation.save()
        return redirect('rents:okReservation', reservation.id)


def okReservation(request, idReservation):
    try:
        reservation = Reservation.objects.get(id = idReservation)
    except Prop.DoesNotExist:
        raise Http404("Propiedad no encontrada")
    return render(request, 'rents/okReservation.html', {'prop': reservation})

def filterProps(cityId, dateFrom, dateTo, guestCount):
    propList = Prop.objects.all().filter(city = cityId)

    if guestCount:
        propList = propList.filter(maxGuests__gte = guestCount)
    
    propList = checkPropListAvailability(propList, dateFrom, dateTo)
        
    return propList

def checkPropListAvailability(propList, dateFrom, dateTo):
    if dateFrom and dateTo:
        dateFrom = datetime.strptime(dateFrom, '%Y-%m-%d').date()
        dateTo = datetime.strptime(dateTo, '%Y-%m-%d').date()

        for prop in propList:
            if not isAvailableProp(prop, dateFrom, dateTo):
                propList = propList.exclude(id= prop.id)

    return propList

def isAvailableProp(prop, dateFrom, dateTo):

    availableProp = True

    reservationDates = getReservationDatesBy(prop.id, dateFrom, dateTo)

    if (dateTo - dateFrom) > timedelta(days=reservationDates.count()):
        availableProp = False

    for reservationDate in reservationDates:
        if reservationDate.reservation is not None:
            availableProp = False

    if not reservationDates:
        availableProp = False

    return availableProp

def associateReservationToReservationDates(reservation, dateFrom, dateTo):
    for reservationDate in getReservationDatesBy(reservation.prop.id, dateFrom, dateTo):
        reservationDate.reservation = reservation
        reservationDate.save()

def getReservationDatesBy(propId ,dateFrom, dateTo):
    return ReservationDate.objects.filter(prop = propId).filter(date__gte = dateFrom).filter(date__lte = dateTo)
