from django.conf.urls import url
from rents.views import *
from . import views

urlpatterns = [
    url(r'^$', index),
    url(r'^prop/(?P<propid>\d+)$', detail, name="prop"),
    url(r'^rents/reserveProp/', reserveProp, name='reserveProp'),
    url(r'^reserveProp/([0-9]+)/$', okReservation, name='okReservation'),

]
