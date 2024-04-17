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
        ("AdminHOD", "AdminHOD"), #1
        ("Pharmacist", "Pharmacist"), #2 Custumer
        ("Doctor", "Doctor"),
        ("Supplier", "Supplier"),
        ("Vender", "Vender"),
        ("PharmacyClerk", "PharmacyClerk"),
        ("Patients", "Patients"),
    )
    user_type = models.CharField(default="AdminHOD", choices=user_type_data, max_length=20)


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


class Patients(BaseModel):
    gender_category = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
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



class Category(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


# class DrugLeaf(BaseModel):
#     leaf_type = models.CharField(max_length=50)
#     number_per_box = models.PositiveIntegerField()

#     def __str__(self):
#         return str(self.leaf_type)


class DrugType(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class DrugUnit(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Manufacturer(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Vender(BaseModel):
    name = models.CharField(max_length=50)

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
    """
    Drug Stock
    """
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, blank=True
    )
    # leaf = models.ForeignKey(
    #     DrugLeaf, null=True, on_delete=models.SET_NULL, blank=True
    # )
    type = models.ForeignKey(
        DrugType, null=True, on_delete=models.SET_NULL, blank=True
    )
    manufacture = models.ForeignKey(
        Manufacturer,
        null=True, on_delete=models.SET_NULL, blank=True
    )
    vender = models.ForeignKey(
        Vender,
        null=True, on_delete=models.SET_NULL, blank=True
    )
    
    drug_name = models.CharField(max_length=50, verbose_name="Medicine Name")
    generic_drug_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Medicine Generic Name")
    # strengh = models.CharField(max_length=50, blank=True, null=True, verbose_name="Strength")
    # shelf = models.CharField(max_length=50, blank=True, null=True, verbose_name="Shelf")
    drug_description = models.TextField(blank=True, max_length=1000, null=True)
    
    unit = models.PositiveIntegerField(
        default=1, null=True, blank=True,
    )
    vat = models.PositiveIntegerField(verbose_name="VAT", blank=True, null=True)
    quantity = models.IntegerField(default="0", blank=True, null=True)
    batch = models.CharField(max_length=50, blank=True, null=True)
    actual_price = models.FloatField(default="0", blank=True, null=True, verbose_name="Actual Price")
    price = models.FloatField(default="0", blank=True, null=True, verbose_name="M.R.P")
    
    # drug_color = models.CharField(max_length=50, blank=True, null=True)
    # batch_number = models.CharField(max_length=50, blank=True, null=True)
    discount = models.IntegerField(default=0)
    gst = models.IntegerField(
        # 0, 5, 12, 18, 28
        choices=(
            (0, "0 %"),
            (5, "5 %"),
            (12, "12 %"),
            (18, "18 %"),
            (28, "28 %"),
        ),
        verbose_name="GST",
        default="0", blank=True, null=True, 
        help_text='Invoice GST in percentage')
    # hot = models.IntegerField(default="0", blank=True, null=True)
    # globle = models.IntegerField(verbose_name="Globel", default="0", blank=True, null=True)
    # tax = models.FloatField(default="0.0", blank=True, null=True)
    
    valid_from = models.DateTimeField(blank=True, null=True, default=timezone.now)
    valid_to = models.DateTimeField(blank=False, null=True)
    drug_pic = models.ImageField(default="images2.png", null=True, blank=True)
    
    status = models.BooleanField(default=True, help_text="Active Status, Uncheck If You Want To Delete This Drug Information.")
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
        if instance.user_type == "AdminHOD":
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == "Pharmacist":
            Pharmacist.objects.create(admin=instance, address="")
        if instance.user_type == "Doctor":
            Doctor.objects.create(admin=instance, address="")
        if instance.user_type == "PharmacyClerk":
            PharmacyClerk.objects.create(admin=instance, address="")
        if instance.user_type == "Patients":
            Patients.objects.create(admin=instance, address="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "AdminHOD":
        instance.adminhod.save()
    if instance.user_type == "Pharmacist":
        instance.pharmacist.save()
    if instance.user_type == "Doctor":
        instance.doctor.save()
    if instance.user_type == "PharmacyClerk":
        instance.pharmacyclerk.save()
    if instance.user_type == "Patients":
        instance.patients.save()


""" patient invoice save model """


class SellInvoice(BaseModel):
    patient_id = models.ForeignKey(Patients, on_delete=models.DO_NOTHING)
    invoice_detail = models.JSONField()

    class Meta:
        ordering = ("-created_at",)


class NewPurchaseData(BaseModel):
    drug_name = models.ForeignKey(Stock, on_delete=models.CASCADE)
    batches = models.CharField(max_length=10, null=True, blank=True)
    mrp_per_unit = models.FloatField()
    buy_price_per_unit = models.FloatField()
    quantity = models.IntegerField()
    sub_total = models.FloatField()
    discount = models.FloatField()
    total = models.FloatField()
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)


class PurchasedInvoice(BaseModel):
    medicine_data = models.ManyToManyField(NewPurchaseData)
    invoice_no = models.CharField(30)
    manufacture = models.CharField(max_length=200)
    date = models.DateField()
    quantity = models.IntegerField()
    sub_total = models.FloatField()
    discount = models.FloatField()
    total = models.FloatField()
    paid = models.FloatField()
    due = models.FloatField()
    payment_type = models.CharField(max_length=20)

    class Meta:
        ordering = ("-created_at",)


class Cart(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart_items")
    medicine = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="carts")
    quantity = models.PositiveIntegerField(default=1)
    discount = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Cart"
        unique_together = ('user', 'medicine')  # Avoid duplicate entries for same product by a user
    
    def __str__(self) -> str:
        return f"{self.pk}"
    
    @property
    def total_price(self):
        try:
            return round((self.medicine.price * self.quantity) - (self.medicine.price * self.quantity * self.discount / 100), 2)
        except:
            return None



class BillingPOS(BaseModel):
    custumer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    details = models.JSONField()
    
    def __str__(self) -> str:
        return str(self.pk)
