from django.conf.urls import url
from alquileres.views import *
from . import views

urlpatterns = [
    url(r'^$', index),
    url(r'^prop/(?P<propid>\d+)$', detail, name="dpto"),
    url(r'^reservations/reserveProp/', views.reserveProp, name='reserveProp'),
    url(r'^reserveProp/([0-9]+)/$', views.okReservation, name='okReservation'),

]
