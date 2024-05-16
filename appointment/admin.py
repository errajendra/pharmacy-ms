from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'patient', 'doctor', 'date', 'status', 'shift', 'booking_mode', 'fee',
        'payment_mode', 'priority', 'message', 'address', 'token')
    list_filter = ('status', 'booking_mode', 'doctor', 'date', 'payment_mode', 'priority', 'created_at')
    search_fields = ('payment_mode', 'priority', 'message', 'address', 'doctor__admin__first_name')
