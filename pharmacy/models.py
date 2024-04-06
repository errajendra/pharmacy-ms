from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    user_type_data = (
        (1, "AdminHOD"),
        (2, "Pharmacist"),
        (3, "Doctor"),
        (4, "PharmacyClerk"),
        (5, "Patients"),
    )
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Patients(BaseModel):
    gender_category = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=30, null=True, blank=True, unique=True)
    gender = models.CharField(
        max_length=7, null=True, blank=True, choices=gender_category
    )
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    profile_pic = models.ImageField(default="patient.jpg", null=True, blank=True)
    age = models.IntegerField(default="0", blank=True, null=True)
    address = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.admin)


class AdminHOD(BaseModel):
    gender_category = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    emp_no = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, choices=gender_category)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    profile_pic = models.ImageField(default="admin.png", null=True, blank=True)
    date_employed = models.DateTimeField(auto_now_add=True, auto_now=False)
    objects = models.Manager()

    def __str__(self):
        return str(self.admin)


class Pharmacist(BaseModel):
    gender_category = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    emp_no = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(default="0", blank=True, null=True)
    gender = models.CharField(max_length=100, null=True, choices=gender_category)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    profile_pic = models.ImageField(default="images2.png", null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.admin)


class Doctor(BaseModel):
    gender_category = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    emp_no = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(default="0", blank=True, null=True)
    gender = models.CharField(max_length=100, null=True, choices=gender_category)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    profile_pic = models.ImageField(default="doctor.png", null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.admin)


class PharmacyClerk(BaseModel):
    gender_category = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    emp_no = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, choices=gender_category)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    profile_pic = models.ImageField(default="images2.png", null=True, blank=True)
    age = models.IntegerField(default="0", blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.admin)


class Category(BaseModel):
    name = models.CharField(max_length=50, blank=False, null=True)

    def __str__(self):
        return str(self.name)


class Prescription(BaseModel):
    patient_id = models.ForeignKey(Patients, null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True)
    prescribe = models.CharField(max_length=100, null=True)


class ExpiredManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                expired=ExpressionWrapper(
                    Q(valid_to__lt=Now()), output_field=BooleanField()
                )
            )
        )


class Stock(BaseModel):
    category = models.ForeignKey(
        Category, null=True, on_delete=models.CASCADE, blank=True
    )
    drug_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Medicine Name")
    drug_color = models.CharField(max_length=50, blank=True, null=True)
    batch_number = models.CharField(max_length=50, blank=True, null=True)
    packing = models.PositiveIntegerField(verbose_name="No Of Tablet")
    quantity = models.IntegerField(default="0", blank=True, null=True)
    mrp = models.IntegerField(default="0", blank=True, null=True, verbose_name="M.R.P")
    rate = models.IntegerField(default="0", blank=True, null=True)
    discount = models.IntegerField(default="0", blank=True, null=True)
    tax = models.FloatField(default="0.0", blank=True, null=True)
    manufacture = models.CharField(max_length=50, blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True, default=timezone.now)
    valid_to = models.DateTimeField(blank=False, null=True)
    drug_description = models.TextField(blank=True, max_length=1000, null=True)
    drug_pic = models.ImageField(default="images2.png", null=True, blank=True)
    objects = ExpiredManager()

    def __str__(self):
        return str(self.drug_name)


class Dispense(BaseModel):
    patient_id = models.ForeignKey(Patients, on_delete=models.DO_NOTHING, null=True)
    drug_id = models.ForeignKey(
        Stock, on_delete=models.SET_NULL, null=True, blank=False
    )
    instructions = models.CharField(max_length=200, null=True, blank=True)
    dispense_quantity = models.PositiveIntegerField(default="1", blank=False, null=True)
    discount = models.FloatField(max_length=300, null=True, blank=True)
    gst = models.FloatField(max_length=300, null=True, blank=True)
    total_amount = models.FloatField(max_length=300, null=True, blank=False)
    order_status = models.BooleanField(default=False)


class PatientFeedback(BaseModel):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    admin_id = models.ForeignKey(AdminHOD, null=True, on_delete=models.CASCADE)
    pharmacist_id = models.ForeignKey(Pharmacist, null=True, on_delete=models.CASCADE)
    feedback = models.TextField(null=True)
    feedback_reply = models.TextField(null=True)
    admin_created_at = models.DateTimeField(null=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Pharmacist.objects.create(admin=instance, address="")
        if instance.user_type == 3:
            Doctor.objects.create(admin=instance, address="")
        if instance.user_type == 4:
            PharmacyClerk.objects.create(admin=instance, address="")
        if instance.user_type == 5:
            Patients.objects.create(admin=instance, address="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.pharmacist.save()
    if instance.user_type == 3:
        instance.doctor.save()
    if instance.user_type == 4:
        instance.pharmacyclerk.save()
    if instance.user_type == 5:
        instance.patients.save()


""" patient invoice save model """


class SellInvoice(BaseModel):
    patient_id = models.ForeignKey(Patients, on_delete=models.DO_NOTHING)
    invoice_detail = models.JSONField()

    class Meta:
        ordering = ("-created_at",)


class PurchasedInvoice(BaseModel):
    invoice_data = models.JSONField()

    class Meta:
        ordering = ("-created_at",)


