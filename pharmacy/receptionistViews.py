from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from appointment.models import Appointment
from .forms import *
from .models import *
from appointment.forms import AppointmentForm

@login_required
def receptionistHome(request):
    return render(request,'receptionist_templates/receptionist_home.html')


@login_required
def appointment_list_receptionist(request):
    appointments = Appointment.objects.all().order_by('-date')
    
    context = {
        "title": "Appointments",
        "appointments": appointments,
    }
    return render(request, "receptionist_templates/appointment/appointment_list.html", context)


@login_required
def add_appointment_receptionist(request):
    form = AppointmentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("appointment_list_receptionist")
        else:
            messages.warning(request, str(form.errors))
    context = {
        "title": "Book New Appointment",
        # "form": form,
        "patients": Patients.objects.all(),
        "doctors": Doctor.objects.all()
    }
    return render(request, "receptionist_templates/appointment/add_appointment.html", context)
