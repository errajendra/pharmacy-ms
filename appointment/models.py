from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from pharmacy.models import BaseModel, Doctor, Patients, Addmission
from django.utils.timezone import datetime


class Appointment(BaseModel):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    booking_mode = models.CharField(
        verbose_name="Booking Mode",
        max_length=15,
        choices=[
            ("Offline", "Offline"),
            ("Online", "Online")
        ],
        default="Offline"
    )
    status = models.CharField(
        verbose_name="Booking Status",
        max_length=15,
        choices=[
            ("Pending", "Pending"),
            ("Scheduled", "Scheduled"),
            ("Confirmed", "Confirmed"),
            ("Rescheduled", "Rescheduled"),
            ("Cancel", "Cancel")
        ],
        default="Pending"
    )
    shift = models.CharField(
        max_length=15,
        choices=[
            ("Morning", "Morning"),
            ("Evening", "Evening")
        ],
        default="Morning"
    )
    fee = models.FloatField(verbose_name="Doctor Fees", default=0)
    payment_mode = models.CharField(
        verbose_name="Payment Mode",
        choices=[
            ("Cash", "Cash"),
            ("Upi", "Upi"),
            ("Bank Transfer", "Bank Transfer"),
            ("Other", "Other"),
        ],
        max_length=15,
        default="Cash"
    )
    priority = models.CharField(
        verbose_name="Appointment Priority",
        choices=[
            ("Normal", "Normal"),
            ("Urgent", "Urgent"),
            ("Very Urgent", "Very Urgent"),
            ("Low", "Low"),
        ],
        max_length=15,
        default="Normal"
    )
    message = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    token = models.PositiveIntegerField(
        verbose_name="Token Number", null=True, blank=True
    )
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.__class__.objects.filter(doctor=self.doctor).count() + 1
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ("-created_at",)
        unique_together = ("doctor", "date", "token")
        verbose_name = "Appointment"


@receiver(post_save, sender=Appointment)
def save_user_profile(sender, instance, **kwargs):
    if instance.status == "Confirmed":
        Addmission.objects.create(
            patient=instance.patient,
            doctor=instance.doctor,
            department=instance.doctor.department,
            addmission_time = datetime.now()
        )
