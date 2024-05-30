from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import Form
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column



import json


class PatientPicForm1(forms.ModelForm):
    class Meta:
        model = Patients
        fields = "__all__"
        exclude = ["admin", "gender", "mobile", "address", "dob"]


class DateInput(forms.DateInput):
    input_type = "date"



class ClientForm(forms.Form):
    mobile = PhoneNumberField()



class PatientModelForm(ModelForm):
    email = forms.EmailField(
        label="Email",
        max_length=50,
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    
    class Meta:
        model = Patients
        fields = (
            "first_name", "last_name", "gender", "dob", "age", "marital_status", "bg",
            "phone_number", "phone_number2", "address", "city", "pin_code",
            "abha_no", "pm_jay", "adhar", "passport", "pan", "dl", "cat", "cast", "religion",
            "nationality", "education", "occupation", "activity", "food_preference", "smooking", "alcohol"
        )
        widgets = {
            "marital_status": forms.Select(attrs={"class":"form-control"}),
            "bg": forms.Select(attrs={"class":"form-control"}),
            "language": forms.Select(attrs={"class":"form-control"}),
            "activity": forms.Select(attrs={"class":"form-control"}),
            "gender": forms.Select(attrs={"class":"form-control"}),
            "food_preference": forms.Select(attrs={"class":"form-control"}),
            "smooking": forms.Select(attrs={"class":"form-control"}),
            "alcohol": forms.Select(attrs={"class":"form-control"}),
        }
        
        


class PatientForm(forms.Form):
    # doctor = forms.ModelChoiceField(
    #     label="Doctor",
    #     queryset=Doctor.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-control"}),
    # )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    phone_number = forms.CharField(label="Mobile", required=False, max_length=50)
    email = forms.EmailField(
        label="Email",
        max_length=50,
        required=False, 
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    gender_list = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))
    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    # dob = forms.DateField(
    #     label="dob", widget=DateInput(attrs={"class": "form-control"})
    # )
    # age = forms.ChoiceField(
    #     choices=[(i, i) for i in range(100)],
    #     label="Age",
    #     required=False,
    #     widget=forms.Select(attrs={"class": "form-control"})
    # )
    # username = forms.CharField(
    #     label="Username",
    #     max_length=50,
    #     widget=forms.TextInput(attrs={"class": "form-control"}),
    # )
    # password = forms.CharField(
    #     label="Password",
    #     max_length=50,
    #     widget=forms.PasswordInput(attrs={"class": "form-control"}),
    # )

    # Validations for patient
    def clean_reg_no(self):
        reg_no = self.cleaned_data["reg_no"]
        if not reg_no:
            raise ValidationError("This field is required")
        for instance in Patients.objects.all():
            if instance.reg_no == reg_no:
                raise ValidationError("Registration number already exist")

        return reg_no

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number:
            pass
        elif len(phone_number) < 10:
            raise forms.ValidationError("Invalid Number")
        return phone_number
    

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # if not email:
        #     raise ValidationError("Email field is required")
        # if CustomUser.objects.filter(email=email).exists():
        #     raise ValidationError("Email already exist")
        return email

    def clean_firstName(self):
        first_name = self.cleaned_data["first_name"]
        if not first_name:
            raise ValidationError("This field is required")
        return first_name

    def clean_secondName(self):
        last_name = self.cleaned_data["last_name"]
        if not last_name:
            raise ValidationError("This field is required")
        return last_name


class EditPatientForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    phone_number = forms.CharField(
        label="Mobile",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    gender_list = (("Male", "Male"), ("Female", "Female"))
    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    # dob = forms.DateField(
    #     label="dob", widget=DateInput(attrs={"class": "form-control"})
    # )
    age = forms.ChoiceField(
        choices=[(i, i) for i in range(100)],
        label="Age",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )



class StockForm(forms.ModelForm):
    total_price = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'readonly': 'true', "class":"form-control w-auto"}),
    )
    
    class Meta:
        model = Stock
        fields = (
            "category", "type", "manufacture", "vender",
            "drug_name", "generic_drug_name", "drug_description",
            "batch", "actual_price", "price", "unit", "unit_quantity", "quantity", "total_price",
            "discount", "gst", "hsn", "valid_to", "drug_pic")
            
        widgets = {
            "category": forms.Select(attrs={"class":"form-control w-auto"}),
            "type": forms.Select(attrs={"class":"form-control w-auto"}),
            "manufacture": forms.Select(attrs={"class":"form-control w-auto"}),
            "supplier": forms.Select(attrs={"class":"form-control w-auto"}),
            "vender": forms.Select(attrs={"class":"form-control w-auto"}),
            "gst": forms.Select(attrs={"class":"form-control w-auto"}),
            "unit": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            "unit_quantity": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            "actual_price": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            "price": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            "quantity": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            "hsn": forms.TextInput(attrs={"class":"form-control"}),
            "discount": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            "valid_to": forms.DateInput(attrs={"class":"form-control w-auto", "type": "date"}), 
        }



class StockFormPharmacist(forms.ModelForm):

    class Meta:
        model = Stock
        fields = "__all__"
        exclude = [
            "status",
            "valid_from"
        ]
        widgets = {
            "category": forms.Select(attrs={"class":"form-control w-auto"}),
            "type": forms.Select(attrs={"class":"form-control w-auto"}),
            "manufacture": forms.Select(attrs={"class":"form-control w-auto"}),
            "vender": forms.Select(attrs={"class":"form-control w-auto"}),
            "gst": forms.Select(attrs={"class":"form-control w-auto"}),
            "drug_name": forms.TextInput(attrs={"class":"form-control"}),
            "generic_drug_name": forms.TextInput(attrs={"class":"form-control"}),
            "drug_description": forms.Textarea(attrs={"class":"form-control"}),
            "unit": forms.NumberInput(attrs={"class":"form-control"}),
            "vat": forms.NumberInput(attrs={"class":"form-control"}),
            "quantity": forms.NumberInput(attrs={"class":"form-control"}),
            "batch": forms.TextInput(attrs={"class":"form-control"}),
            "hsn": forms.TextInput(attrs={"class":"form-control"}),
            "price": forms.NumberInput(attrs={"class":"form-control"}),
            "actual_price": forms.NumberInput(attrs={"class":"form-control"}),
            "discount": forms.NumberInput(attrs={"class":"form-control"}),
            "valid_to": DateInput(attrs={"class": "form-control"}),
        }



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"



class VenderForm(forms.ModelForm):
    class Meta:
        model = Vender
        fields = "__all__"


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class DrugTypeForm(forms.ModelForm):
    class Meta:
        model = DrugType
        fields = "__all__"


class DrugUnitForm(forms.ModelForm):
    class Meta:
        model = DrugUnit
        fields = "__all__"


# class PrescriptionForm(forms.ModelForm):
#     class Meta:
#         model = Prescription
#         fields = "__all__"
class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
        fields = [
           'drug_name', 'route', 
            'dose', 'intake', 'duration', 'quantity', 'instruction'
        ]
        widgets = {
            'drug_name': forms.TextInput(attrs={'class': 'form-control'}),
            'route': forms.TextInput(attrs={'class': 'form-control'}),
            'dose': forms.TextInput(attrs={'class': 'form-control'}),
            'intake': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'instruction': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Pharmacist
        fields = "__all__"
        exclude = ["admin", "gender", "mobile", "address"]


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"
        exclude = ["admin", "gender", "mobile", "address"]

        def clean_firstName(self):
            first_name = self.cleaned_data["first_name"]
            if not first_name:
                raise ValidationError("This field is required")
            return first_name

        def clean_mobile(self):
            mobile = self.cleaned_data.get("mobile")
            if not mobile:
                raise forms.ValidationError("This field is requied")
            return mobile

        def clean_username(self):
            username = self.cleaned_data["username"]
            if not username:
                raise ValidationError("This field is required")
            for instance in CustomUser.objects.all():
                if instance.username == username:
                    raise ValidationError("Username aready exist")


class ClerkForm(ModelForm):
    class Meta:
        model = Pathologist
        fields = "__all__"
        exclude = ["admin", "gender", "mobile", "address"]


class HodForm(ModelForm):
    class Meta:
        model = AdminHOD
        fields = "__all__"
        exclude = ["admin", "gender", "mobile", "address"]


class PatientSearchForm1(ModelForm):
    class Meta:
        model = Patients
        fields = "__all__"
        exclude = ["profile_pic", "gender", "mobile", "address", "dob"]


class PatientForm7(ModelForm):
    class Meta:
        model = Patients
        fields = "__all__"


class DispenseForm(ModelForm):
    class Meta:
        model = Dispense
        fields = ["drug_id", "dispense_quantity", "instructions"]
        exclude = ["stock_ref_no", "order_status", "discount", "gst", "total_amount"]


class ReceiveStockForm(ModelForm):
    valid_to = forms.DateField(
        label="Expiry Date", widget=DateInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Stock
        fields = "__all__"
        exclude = [
            "category",
            "drug_name",
            "valid_from",
            "dispense_quantity",
            "reorder_level",
            "date_from",
            "date_to",
            "quantity",
            "manufacture",
        ]


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["discount"]


class AddUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "username", 
            "first_name", 
            "last_name",
            "email",
            "password",
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class AddmissionForm(ModelForm):
    class Meta:
        model = Addmission
        fields = "__all__"
        
        widgets = {
            "patient": forms.Select(attrs={"class":"form-control w-auto"}),
            "doctor": forms.Select(attrs={"class":"form-control w-auto"}),
            "department": forms.Select(attrs={"class":"form-control w-auto"}),
            "purpose": forms.Select(attrs={"class":"form-control w-auto"}),
            
            # OPD
            "weight": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            "bp_systolic": forms.TextInput(attrs={"class":"form-control w-auto"}),
            "bp_diastolic": forms.TextInput(attrs={"class":"form-control w-auto"}),
            "pulse": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            "respiration_rates": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            "temp": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            "spo2": forms.NumberInput(attrs={"class":"form-control w-auto"}),

            # open these fields when purpose is OPD
            # "fees": forms.NumberInput(attrs={"class":"form-control w-auto", "data-purpose":"FieldsOPD"}),
            "fees": forms.NumberInput(attrs={"class":"form-control w-auto"}),
            
            # open these fields when purpose is IPD or Bed Addmission
            "advanced_fees": forms.NumberInput(attrs={"class":"form-control w-auto", "data-purpose":"BedIPD"}),
            "bht_no": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "uid": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "guardian": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "addmission_time": forms.TextInput(attrs={"class":"form-control w-auto", 'type':'datetime-local', "data-purpose":"BedIPD"}),
            "discharge_time": forms.TextInput(attrs={"class":"form-control w-auto", 'type':'datetime-local', "data-purpose":"BedIPD"}),
            "ward_bed": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "no_of_beds": forms.NumberInput(attrs={"class":"form-control w-auto", "data-purpose":"BedIPD"}),
            "operation_date": forms.DateTimeInput(attrs={"class":"form-control w-auto", 'type':'datetime-local', "data-purpose":"BedIPD"}),
            "addmission_type": forms.Select(attrs={"class":"form-control w-auto", "data-purpose":"BedIPD"}),
            "mlc_no": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "icd": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "provisonal_diagnosis": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "final_diagnosis": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "summary_of_case": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "staff": forms.Select(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "facilities": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "result": forms.Select(attrs={"class":"form-control w-auto", "data-purpose":"BedIPD"}),
            "couse_of_death": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "days": forms.NumberInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
            "condition": forms.TextInput(attrs={"class":"form-control w-auto", "data-purpose":"BedIPD"}),
            "usages": forms.TextInput(attrs={"class":"form-control", "data-purpose":"BedIPD"}),
        }



class HospitalItemForm(ModelForm):
    class Meta:
        model = HospitalItem
        fields = "__all__"
        
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "unit": forms.NumberInput(attrs={"class":"form-control"}),
            "actual_price": forms.NumberInput(attrs={"class":"form-control"}),
            "price": forms.NumberInput(attrs={"class":"form-control"}),
            "discount": forms.NumberInput(attrs={"class":"form-control"}),
        }



class NurseForm(ModelForm):
    email = forms.EmailField(
        label="Email",
        max_length=50,
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    
    class Meta:
        model = Nurse
        fields = ("gender", "department", "mobile", "address", )
        # widgets = {
        #     "marital_status": forms.Select(attrs={"class":"form-control"}),
        #     "gender": forms.Select(attrs={"class":"form-control"}),
        #     # "bg": forms.Select(attrs={"class":"form-control"}),
        #     "age": forms.DateInput(attrs={"class":"form-control", "type": "date"}),
        #     "department": forms.Select(attrs={"class":"form-control"}),
        # }


class ReceptionistForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        max_length=50,
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    age = forms.IntegerField(
        label="Age",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=[('Female', 'Female'), ('Male', 'Male')],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    emp_no = forms.CharField(
        label="Employee No.",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    profile_pic = forms.ImageField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )
    mobile = forms.CharField(
        label="Mobile",
        max_length=15,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    
    class Meta:
        model = Reception
        fields = "__all__"
        exclude = [ "admin"]


from django.forms import modelformset_factory
class ClinicalNoteForm(forms.ModelForm):
    class Meta:
        model = ClinicalNote
        fields = ['note_type', 'note', 'image']
        widgets = {
            'note_type': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ClinicalNoteForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
ClinicalNoteFormSet = modelformset_factory(ClinicalNote, form=ClinicalNoteForm, extra=1, can_delete=True)


class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = Addmission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PatientRecordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Check if the instance is being edited
        if self.instance and self.instance.pk:
            self.fields['patient'].disabled = True
            self.fields['doctor'].disabled = True
        
        self.helper.layout = Layout(
            Fieldset(
                'General Information',
                'patient',
                'department',
                'doctor',
                'reason',
                'purpose',
                'fees',
            ),
            Fieldset(
                'OPD Details',
                'weight',
                'bp_systolic',
                'bp_diastolic',
                'pulse',
                'respiration_rates',
                'temp',
                'spo2',
                css_class='opd-details'
            ),
            Fieldset(
                'IPD/Bed Addmission Details',
                'bht_no',
                'uid',
                'guardian',
                'addmission_time',
                'discharge_time',
                'ward_bed',
                'no_of_beds',
                'operation_date',
                'addmission_type',
                'mlc_no',
                'icd',
                'provisonal_diagnosis',
                'final_diagnosis',
                'summary_of_case',
                'staff',
                'facilities',
                'result',
                'couse_of_death',
                'remark',
                css_class='ipd-details'
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-info')
            )
        )
