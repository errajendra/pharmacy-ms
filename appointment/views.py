from django.shortcuts import render, redirect
from pharmacy.models import Patients, Doctor
from .models import Appointment
from .forms import AppointmentForm


def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-date')
    context = {
        "title": "Appointments",
        "appointments": appointments
    }
    return render(request, "appointment/list.html", context)


def new_appointment(request):
    form = AppointmentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("appointment_list_admin")
    context = {
        "title": "Book New Appointment",
        "form": form,
        "patients": Patients.objects.all(),
        "doctors": Doctor.objects.all()
    }
    return render(request, "appointment/new_booking.html", context)
