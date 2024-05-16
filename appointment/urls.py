from django.urls import path
from .views import *


urlpatterns = [
    path("admin-appointment-list/", appointment_list, name="appointment_list_admin"),
    path("admin-appointment-book/", new_appointment, name="new_appointment_admin"),
    path("admin-appointment-update/<int:id>/", edit_appointment, name="edit_appointment_admin"),
    path("admin-appointment-delte/<int:id>/", delete_appointment, name="delete_appointment_admin"),
]