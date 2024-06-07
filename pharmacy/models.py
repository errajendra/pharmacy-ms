from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Department(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)



class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)



class CustomUser(AbstractUser):
    
    first_name = models.CharField(_("first name"), max_length=150, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, default="")
    user_type_data = (
        ("AdminHOD", "AdminHOD"), #1
        ("Pharmacist", "Pharmacist"),
        ("Doctor", "Doctor"),
        ("Supplier", "Supplier"),
        ("Vender", "Vender"),
        ("Pathologist", "Pathologist"), # Pharmacy Clerk (old)
        ("Patients", "Patients"), # Customer
        ("Nurse", "Nurse"), # Pharmacy Clerk (old)
        ("Reception", "Reception"),
    )
    user_type = models.CharField(default="AdminHOD", choices=user_type_data, max_length=20)
    
    def __str__(self) -> str:
        return "{} {} - {}".format(self.first_name if self.first_name else '', self.last_name if self.last_name else '', self.username if self.username else '')


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
    
    class Meta:
        verbose_name = "Pharmasist"
    


class Doctor(BaseModel):
    gender_category = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    fees = models.PositiveIntegerField(verbose_name="Doctor Fees", default=0)
    emp_no = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(default="0", blank=True, null=True)
    gender = models.CharField(max_length=100, null=True, choices=gender_category)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    profile_pic = models.ImageField(default="doctor.png", null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.admin)



class Nurse(BaseModel):
    gender_category = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    emp_no = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, default="Female", choices=gender_category)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    profile_pic = models.ImageField(default="doctor.png", null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.admin)



class Reception(BaseModel):
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


# Pathologist
class Pathologist(BaseModel):
    gender_category = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
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
        ("Other", "Other"),
    )
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(
        max_length=7, null=True, blank=True, choices=gender_category
    )
    first_name = models.CharField(max_length=36, null=True, blank=True)
    last_name = models.CharField(max_length=36, null=True, blank=True)
    age = models.CharField(
        max_length=3, null=True, blank=True
    )
    phone_number = models.CharField(verbose_name="Mobile Number",max_length=15, null=True, blank=True)
    phone_number2 = models.CharField(verbose_name="Alternate Mobile Number",  max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(default="patient.jpg", upload_to="patient-profile", null=True, blank=True)
    dob = models.DateField(verbose_name="Age(DOB)", blank=True, null=True)
    bg = models.CharField(
        verbose_name="Blood Group",
        max_length=10,
        default="Not Known",
        choices=[
            ("Not Known", "Not Known"),
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("O+", "O+"),
            ("O-", "O-"),
            ("AB+", "AB+"),
            ("AB-", "AB-")
        ]
    )
    marital_status = models.CharField(
        verbose_name="Marital Status",
        max_length=15,
        choices=[
            ("Single", "Single"),
            ("Married ", "Married "),
            ("Separated", "Separated"),
            ("Widow", "Widow"),
        ],
        default="Single"
    )
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE,
        verbose_name="Language Preference",
        null=True, blank=True
    )
    
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=36, null=True, blank=True)
    pin_code = models.PositiveIntegerField(null=True, blank=True)
    
    # Life Style
    
    abha_no = models.CharField(verbose_name="Abha Number", max_length=100, null=True, blank=True)
    pm_jay = models.CharField(verbose_name="PM Jay", max_length=100, null=True, blank=True)
    adhar = models.CharField(verbose_name="Adhar Number",max_length=15, null=True, blank=True)
    passport = models.CharField(verbose_name="Passport Number",max_length=100, null=True, blank=True)
    pan = models.CharField(verbose_name="PAN Number", max_length=100, null=True, blank=True)
    dl = models.CharField(verbose_name="Driving Licence Number", max_length=100, null=True, blank=True)
    cat = models.CharField(verbose_name="Govt. Reservation Category", max_length=100, null=True, blank=True)
    cast = models.CharField(verbose_name="Cast", max_length=100, null=True, blank=True)
    religion = models.CharField(verbose_name="Religion", max_length=100, null=True, blank=True)
    nationality = models.CharField(verbose_name="Nationality", max_length=100, null=True, blank=True)
    education = models.CharField(verbose_name="Education", max_length=100, null=True, blank=True)
    occupation = models.CharField(verbose_name="Occupation", max_length=100, null=True, blank=True)
    
    activity = models.CharField(
        verbose_name="Activity Level",
        choices=(
            ("High", "High"),
            ("Low", "Low"),
            ("Medium", "Medium"),
        ), null=True, blank=True
    )
    food_preference = models.CharField(
        verbose_name="Food Preference",
        choices=(
            ("Veg", "Veg"),
            ("Non Veg", "Non Veg"),
        ), null=True, blank=True
    )
    smooking = models.CharField(
        verbose_name="Smoking Habits",
        choices=(
            ("Frequent", "Frequent"),
            ("Daily", "Daily"),
            ("Sometime", "Sometime"),
            ("Never", "Never"),
        ), null=True, blank=True
    )
    alcohol = models.CharField(
        verbose_name="Alcohol Consumption",
        choices=(
            ("Frequent", "Frequent"),
            ("Daily", "Daily"),
            ("Sometime", "Sometime"),
            ("Never", "Never"),
        ), null=True, blank=True
    )

    def __str__(self):
        return "{} {} ({})".format(self.first_name if self.first_name else '', self.last_name if self.last_name else '', self.admin.username )



class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class HospitalItem(BaseModel):
    name = models.CharField(max_length=50)
    unit = models.PositiveIntegerField()
    actual_price = models.FloatField(default=0, verbose_name="Actual Price")
    price = models.FloatField(default=0, verbose_name="M.R.P")
    discount = models.FloatField(default=0, verbose_name="Discount (%)")
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class DrugType(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class DrugUnit(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Manufacturer(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Vender(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, null=True, blank=True)
    dl = models.CharField(max_length=50, verbose_name="DL No.", null=True, blank=True)
    gst = models.CharField(max_length=50, verbose_name="GST", null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name="Address", null=True, blank=True)

    def __str__(self):
        return str(self.name)



class Prescription(BaseModel):
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
    drug_name = models.CharField(verbose_name="Medicine Name", max_length=50, null=True, blank=True)
    route = models.CharField(verbose_name="Route", max_length=50, null=True, blank=True)
    dose = models.CharField(verbose_name="Dosage & Frequency", max_length=50, null=True, blank=True)
    intake = models.CharField(
        verbose_name="Intake", max_length=15, 
        choices=(
            ("Before Eat", "Before Eat"),
            ("After Eat", "After Eat")
        ),
        null=True, blank=True)
    duration = models.PositiveIntegerField(verbose_name="Duration (in Days)", null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity", null=True, blank=True)
    instruction = models.CharField(verbose_name="Additional Instruction", max_length=50, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.pk}"



class ClinicalNote(BaseModel):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    note_type = models.CharField(
        verbose_name="Note Type",
        max_length=15,
        choices=(
            ("Complaints", "Complaints"),
            ("Observation", "Observation"),
            ("Diagnosis", "Diagnosis"),
            ("Notes", "Notes"),
        )
    )
    note = models.TextField()
    image = models.ImageField(verbose_name="Photo", upload_to="clinical-notes/", null=True, blank=True)
    
    def __str__(self) -> str:
        return str(self.pk) + " - " + self.note_type


class BedType(BaseModel):
    bed_type = models.CharField(verbose_name="Bed Type", max_length=100)
    
    
class Floor(BaseModel):
    name = models.CharField(verbose_name="Bed Group", max_length=100)
    floor = models.CharField(verbose_name="Floor", max_length=100)
    desc = models.CharField(verbose_name="Description", max_length=400, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name + " - " + self.floor
    
class Bed(BaseModel):
    bed_no = models.IntegerField()
    bed_type = models.ForeignKey(BedType, on_delete=models.CASCADE, related_name="Bed_Type")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="Floor")
    status = models.BooleanField(default=False)


class Addmission(BaseModel):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100, null=True, blank=True)
    
    # OPD
    weight = models.FloatField(verbose_name="Patient Weight", blank=True, null=True, help_text="Enter Weight Reading")
    bp_systolic = models.CharField(verbose_name="Blood Pressure (mmHg) - Systolic", max_length=50, blank=True, null=True, help_text="Enter Systolic Reading")
    bp_diastolic = models.CharField(verbose_name="Blood Pressure (mmHg) - Diastolic", max_length=50, blank=True, null=True, help_text="Enter Diastolic Reading")
    pulse = models.FloatField(verbose_name="Pulse (Heartbeats/min)", blank=True, null=True, help_text="Enter Reading (Sitting/Standing)")
    respiration_rates = models.FloatField(verbose_name="Respiration Rates (Heartbeats/min)", blank=True, null=True, help_text="Enter Reading")
    temp = models.FloatField(verbose_name="Temperature (°F)", blank=True, null=True, help_text="Enter Reading of Temperature (in °F)")
    spo2 = models.FloatField(verbose_name="SPO2 (%)", blank=True, null=True, help_text="Enter SPO2 (%) Reading")
    
    purpose = models.CharField(
        choices=(
            ("OPD", "OPD"),
            ("IPD/Bed Addmission", "IPD/Bed Addmission"),
            # ("OT", "OT"),
            # ("ICU", "ICU"),
        ),
        max_length=20, default="OPD"
    )
    
    fees = models.FloatField(verbose_name="Fees", default=0)
    
    # open these bellow fields on  form when choose purpose of IPD or Bed Addmission option
    advanced_fees = models.FloatField(verbose_name="Advanced Fees", default=0)
    bht_no = models.CharField(verbose_name="BHT No", max_length=48, null=True, blank=True)
    # uid = models.CharField(max_length=15, verbose_name="Adhar Number", null=True, blank=True)
    guardian = models.CharField(max_length=36, verbose_name="Guardian Name", null=True, blank=True)
    addmission_time = models.DateTimeField(verbose_name="Date & Time of Addmission", null=True, blank=True)
    discharge_time = models.DateTimeField(verbose_name="Date & Time of Discharge", null=True, blank=True)
    ward_bed = models.CharField(verbose_name="Ward Type.", max_length=48, null=True, blank=True)
    no_of_beds = models.PositiveIntegerField(verbose_name="Bed No.", null=True, blank=True)
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True)
    operation_date = models.DateTimeField(verbose_name="Date & Time of Operation", null=True, blank=True)
    addmission_type = models.CharField(
        choices=(
            ("Routine", "Routine"),
            ("Emergency", "Emergency"),
            ("MLC", "MLC"),
            ("Accident", "Accident"),
        ),
        max_length=20, default="Routine"
    )
    mlc_no = models.CharField(verbose_name="MLC No", max_length=48, null=True, blank=True)
    icd = models.CharField(verbose_name="ICD", max_length=48, null=True, blank=True)
    provisonal_diagnosis = models.CharField(verbose_name="Provisional Diagnosis", max_length=200, null=True, blank=True)
    final_diagnosis = models.CharField(verbose_name="Final Diagnosis", max_length=200, null=True, blank=True)
    summary_of_case = models.TextField(verbose_name="Summary of Case", null=True, blank=True)
    staff = models.ForeignKey(Nurse, on_delete=models.SET_NULL, verbose_name="Staff Nurse (Asigned)", null=True, blank=True)
    facilities = models.CharField(max_length=200, null=True, blank=True)
    days = models.PositiveIntegerField(null=True, blank=True)
    any_known_allergy = models.CharField(verbose_name="Any Known Allergy", max_length=200, null=True, blank=True)
    condition = models.CharField(verbose_name="Condition", max_length=200, null=True, blank=True)
    usages = models.CharField(verbose_name="Usages", max_length=200, null=True, blank=True)
    result = models.CharField(
        choices=(
            ("Recovered", "Recovered"),
            ("Dorp", "Dorp"),
            ("Unchanged", "Unchanged"),
            ("LAMA", "LAMA"),
            ("Abscond", "Abscond"),
            ("Died", "Died"),
        ),
        max_length=20, default="Recovered"
    )
    couse_of_death = models.CharField(verbose_name="Cause of Death", max_length=200, null=True, blank=True)
    remark = models.CharField(verbose_name="Remark", max_length=200, null=True, blank=True)
    
    
    
    def __str__(self) -> str:
        return f"{self.patient}"



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
        DrugType, null=True, on_delete=models.SET_NULL, blank=True, verbose_name="Product Type"
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
    generic_drug_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Medicine Generic Name")
    # strengh = models.CharField(max_length=50, blank=True, null=True, verbose_name="Strength")
    # shelf = models.CharField(max_length=50, blank=True, null=True, verbose_name="Shelf")
    drug_description = models.TextField(blank=True, max_length=1000, null=True)
    
    unit = models.PositiveIntegerField(
        default=1, null=True, blank=True,
    )
    unit_quantity = models.PositiveIntegerField(verbose_name="Quantity in Strip", default=10)
    quantity = models.IntegerField(verbose_name="Total Quantity", default=0, blank=True, null=True)
    batch = models.CharField(max_length=50, blank=True, null=True)
    actual_price = models.FloatField(default=0, blank=True, null=True, verbose_name="Actual Price")
    price = models.FloatField(default=0, verbose_name="M.R.P/Unit")
    
    # drug_color = models.CharField(max_length=50, blank=True, null=True)
    hsn = models.CharField(max_length=50, verbose_name="HSN Code", blank=True, null=True)
    discount = models.FloatField(default=0, blank=True, null=True,)
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
    
    valid_from = models.DateField(blank=True, null=True, default=timezone.now)
    valid_to = models.DateField(blank=True, null=True)
    drug_pic = models.ImageField(default="images2.png", null=True, blank=True)
    
    status = models.BooleanField(default=True, help_text="Active Status, Uncheck If You Want To Delete This Drug Information.")
    objects = ExpiredManager()

    def __str__(self):
        return str(self.drug_name)
    
    @property
    def sell(self):
        data = BillingPOS.objects.filter(details__item_details__contains=[{"medicine_id":self.id}])
        if not data:
            return False
        
        sell_quantity = 0
        sell_total = 0
        for x in range(len(data)):
            sell_quantity += sum([i['quantity'] for i in data[x].details["item_details"] if i["medicine_id"] == self.id])
            sell_total += sum([i['total'] for i in data[x].details["item_details"] if i["medicine_id"] == self.id])
        detail = {
            'sell_quantity': sell_quantity,
            'sell_amount': sell_total,
        }
        return detail
    
    @property
    def purchese(self):
        data = self.newpurchasedata_set.all()
        total = data.aggregate(total=models.Sum('total'))['total']
        quantity = data.aggregate(total=models.Sum('quantity'))['total']
        data = {
            'quantity' : quantity or "",
            'amount' : total or "",
        }
        return data
    
    @property
    def quantity_price(self):
        if self.price:
            try:
                return self.price/self.unit_quantity
            except:
                pass
        return 0
        
    

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
        if instance.user_type == "Pathologist":  # Pharmacy Clerk (old)
            Pathologist.objects.create(admin=instance, address="")
        if instance.user_type == "Patients":
            Patients.objects.create(admin=instance, address="")
        if instance.user_type == "Nurse":
            Nurse.objects.create(admin=instance, address="")
        if instance.user_type == "Reception":
            Reception.objects.create(admin=instance, address="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "AdminHOD":
        instance.adminhod.save()
    if instance.user_type == "Pharmacist":
        instance.pharmacist.save()
    if instance.user_type == "Doctor":
        instance.doctor.save()
    if instance.user_type == "Pathologist": # Pharmacy Clerk (old)
        instance.pathologist.save()
    if instance.user_type == "Patients":
        instance.patients.save()
    if instance.user_type == "Nurse":
        instance.nurse.save()
    if instance.user_type == "Reception":
        instance.reception.save()


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
    quantity = models.IntegerField(default=1) # Number of Unit 
    sub_total = models.FloatField()
    discount = models.FloatField()
    total = models.FloatField()
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        
    @property
    def get_total_quanity(self):
        return self.quantity * self.drug_name.unit_quantity


class PurchasedInvoice(BaseModel):
    medicine_data = models.ManyToManyField(NewPurchaseData)
    invoice_no = models.CharField(30)
    manufacture = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
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
    medicine = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True, related_name="carts")
    hospital_item = models.ForeignKey(HospitalItem, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
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
            if self.medicine:
                return round((self.medicine.quantity_price * self.quantity) - (self.medicine.quantity_price * self.quantity * self.discount / 100), 2)
            elif self.hospital_item:
                return round((self.hospital_item.price * self.quantity) - (self.hospital_item.price * self.quantity * self.discount / 100), 2)
            return None
        except:
            return None



class BillingPOS(BaseModel):
    custumer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    details = models.JSONField()
    
    def __str__(self) -> str:
        return str(self.pk)
    
  

"""
Inventory Management Models
"""  

class InventoryCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)



class InventoryStore(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)



class InventorySupplier(BaseModel):
    name = models.CharField(verbose_name="Name", max_length=50, unique=True)
    phone = models.CharField(verbose_name="Phone", max_length=15, unique=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    contact_person = models.CharField(verbose_name="Contact Person Name", max_length=50, blank=True, null=True)
    address = models.CharField(verbose_name="Address", max_length=150, blank=True)
    contact_person_phone = models.CharField(verbose_name="Contact Person Phone", max_length=15, blank=True, null=True)
    contact_person_email = models.EmailField(verbose_name="Contact Person Email", max_length=50, blank=True, null=True)
    description = models.CharField(verbose_name="Description", max_length=250, blank=True, null=True)
    objects = models.Manager()
    
    class Meta:
        verbose_name = "Inventory Supplier"
        verbose_name_plural = "Inventory Suppliers"
        ordering = ('-id',)

    def __str__(self):
        return self.name

        


class InventoryItem(BaseModel):
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE, related_name="inventories")
    name = models.CharField(verbose_name="Item Name", max_length=50, unique=True)
    unit = models.CharField(verbose_name="Unit", max_length=50, blank=True)
    description = models.CharField(verbose_name="Description", max_length=400, blank=True)
        
    class Meta:
        verbose_name = "Inventory Item"
        ordering = ('-created_at',) 

    def __str__(self):
        return self.name     



class InventoryStock(BaseModel):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="stocks")
    store = models.ForeignKey(InventoryStore, on_delete=models.CASCADE, related_name="stocks")
    supplier = models.ForeignKey(InventorySupplier, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.IntegerField()
    purchase_price = models.FloatField()
    date = models.DateField(default=timezone.now)
    description = models.CharField(verbose_name="Description", max_length=400, null=True, blank=True)
    file = models.FileField(upload_to="inventory-stock-files/", null=True, blank=True)
    
    def __str__(self):
        return str(self.item.name) + " - " + str(self.store.name)


