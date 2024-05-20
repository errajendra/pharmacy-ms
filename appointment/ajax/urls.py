from django.urls import path
from .views import *


urlpatterns = [
    path("doctor-fees-on-book-appontment/", load_doctor_fees, name="load_doctor_fees"),
]