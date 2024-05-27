from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pharmacy.models import Patients, Doctor, Addmission, ClinicalNote
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required


def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-date')
    
    priority = request.GET.get('priority', None)
    payment_mode = request.GET.get('payment_mode', None)
    status = request.GET.get('status', None)
    doctor = request.GET.get('doctor', None)
    date = request.GET.get('date', None)
    
    if priority:
        appointments = appointments.filter(priority=priority)
    
    if payment_mode:
        appointments = appointments.filter(payment_mode=payment_mode)

    if doctor:
        appointments = appointments.filter(doctor__id=doctor)
        
    if status:
        appointments = appointments.filter(status=status)
    
    if date:
        appointments = appointments.filter(date__date=date)
    
    context = {
        "title": "Appointments",
        "appointments": appointments,
        "doctors": Doctor.objects.all()
    }
    return render(request, "appointment/list.html", context)


def new_appointment(request):
    form = AppointmentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("appointment_list_admin")
        else:
            messages.warning(request, str(form.errors))
    context = {
        "title": "Book New Appointment",
        # "form": form,
        "patients": Patients.objects.all(),
        "doctors": Doctor.objects.all()
    }
    return render(request, "appointment/new_booking.html", context)


def edit_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    if request.method == "POST":
        form = AppointmentForm(request.POST or None, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("appointment_list_admin")
        else:
            messages.warning(request, str(form.errors))
    context = {
        "title": "Update Appointment",
        "instance": appointment,
        "patients": Patients.objects.all(),
        "doctors": Doctor.objects.all()
    }
    return render(request, "appointment/new_booking.html", context)


def delete_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return redirect("appointment_list_admin")


