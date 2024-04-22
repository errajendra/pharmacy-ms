from pharmacy.clerkViews import receptionistProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
import inflect, io, csv

from .forms import *
from .models import *

from django.views.decorators.csrf import csrf_exempt


def adminDashboard(request):
    patients_total = Patients.objects.all().count()

    doctors = Doctor.objects.all().count()
    pharmacist = Pharmacist.objects.all().count()
    receptionist = PharmacyClerk.objects.all().count()
    out_of_stock = Stock.objects.filter(quantity__lte=0).count()
    total_stock = Stock.objects.all().count()

    today = datetime.today()
    for_today = Patients.objects.filter(
        created_at__year=today.year,
        created_at__month=today.month,
        created_at__day=today.day,
    ).count()
    print(for_today)
    exipred = (
        Stock.objects.annotate(
            expired=ExpressionWrapper(
                Q(valid_to__lt=Now()), output_field=BooleanField()
            )
        )
        .filter(expired=True)
        .count()
    )

    context = {
        "patients_total": patients_total,
        "expired_total": exipred,
        "out_of_stock": out_of_stock,
        "total_drugs": total_stock,
        "all_doctors": doctors,
        "all_pharmacists": pharmacist,
        "all_clerks": receptionist,
        "for_today": for_today,
    }
    return render(request, "hod_templates/admin_dashboard.html", context)


def createPatient(request):
    form = PatientForm()

    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            phone_number = form.cleaned_data["phone_number"]
            # dob = form.cleaned_data["dob"]
            gender = form.cleaned_data["gender"]
            # doctor = form.cleaned_data["doctor"]
            # print(type(doctor), doctor, doctor.id)
            # if doctor:
            #     try:
            #         doctor = Doctor.objects.get(username=doctor)
            #     except:
            #         doctor = None
            # print(doctor)

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                last_name=last_name,
                user_type="Patients",
            )
            user.patients.address = address
            user.patients.phone_number = phone_number
            # user.patients.dob = dob
            # user.patients.doctor = doctor
            user.patients.first_name = first_name
            user.patients.last_name = last_name
            user.patients.gender = gender

            user.save()
            messages.success(request, username + " was Successfully Added")

            return redirect("patient_form")

    context = {"form": form, "title": "Add Patient"}

    return render(request, "hod_templates/patient_form.html", context)


def allPatients(request):
    form = PatientSearchForm1(request.POST or None)
    patients = Patients.objects.all()
    context = {"patients": patients, "form": form, "title": "Admitted Patients"}
    if request.method == "POST":
        # admin=form['first_name'].value()
        name = request.POST.get("search")
        patients = Patients.objects.filter(first_name__icontains=name)

        context = {"patients": patients, form: form}
    return render(request, "hod_templates/admited_patients.html", context) 


def confirmDelete(request, pk):
    try:
        patient = Patients.objects.get(id=pk)
        if request.method == "POST":
            patient.delete()
            return redirect("all_patients")
    except:
        messages.error(
            request,
            "Patient Cannot be deleted  deleted , Patient is still on medication or an error occured",
        )
        return redirect("all_patients")

    context = {
        "patient": patient,
    }

    return render(request, "hod_templates/sure_delete.html", context)


@login_required
def createPharmacist(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type="Pharmacist",
        )
        user.first_name = first_name
        user.last_name = last_name
        user.pharmacist.address = address
        user.pharmacist.mobile = mobile

        user.save()
        messages.success(request, "Staff Added Successfully!")
        return redirect("add_pharmacist")

    context = {"title": "Add Pharmacist"}

    return render(request, "hod_templates/pharmacist_form.html", context)


def managePharmacist(request):
    staffs = Pharmacist.objects.all()
    context = {"staffs": staffs, "title": "Manage Pharmacist"}

    return render(request, "hod_templates/all_pharmacist.html", context)


def createDoctor(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        department = request.POST.get("department")

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type="Doctor",
            )
            user.doctor.address = address
            user.doctor.mobile = mobile
            if department:
                department = Department.objects.get(id=department)
            user.doctor.department = department

            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect("add_doctor")
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect("add_doctor")

    context = {
        "title": "Add Doctor",
        "departments": Department.objects.all()
    }

    return render(request, "hod_templates/add_doctor.html", context)


def manageDoctor(request):
    staffs = Doctor.objects.all()

    context = {"staffs": staffs, "title": "Dotors Details"}

    return render(request, "hod_templates/manage_doctor.html", context)


def createPharmacyClerk(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=4,
            )
            user.pharmacyclerk.address = address
            user.pharmacyclerk.mobile = mobile

            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect("add_pharmacyClerk")
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect("add_pharmacyClerk")

    context = {"title": "Add Pharmacy Clerk"}

    return render(request, "hod_templates/add_pharmacyClerk.html", context)


def managePharmacyClerk(request):
    staffs = PharmacyClerk.objects.all()
    context = {"staffs": staffs, "title": "Manage PharmacyClerk"}

    return render(request, "hod_templates/manage_pharmacyClerk.html", context)


""" Upload medicine in bulk through csv. """
def upload_medicine_bulk_by_csv(request):
    if request.method == "POST":
        
        csv_file = request.FILES['file']
        
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
            
        data_set = csv_file.read().decode('UTF-8')
        
        # setup a stream which is when we loop through each line we are able to handle a data in a stream    
        io_string = io.StringIO(data_set)
        next(io_string)
        medicines_to_create = []
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            try:
                cat, _md_type_created = Category.objects.get_or_create(name=column[0].strip())
                vender, _md_vender_created = Vender.objects.get_or_create(name=column[11].strip())
                # manufacturer, _md_manufacturer_created = Manufacturer.objects.get_or_create(name=column[12].strip())
                med = Stock(
                    category=cat,
                    drug_name=column[1],
                    generic_drug_name=column[2],
                    drug_description=column[3],
                    unit = column[4],
                    quantity = column[5],
                    price = column[6],
                    actual_price = column[7],
                    batch = column[8],
                    valid_to = datetime.strptime(f"01/{column[9]}", "%d/%m/%y"),
                    vender = vender,
                    # manufacturer = manufacturer,
                )
                medicines_to_create.append(med)
            except Exception as e:
                break
        Stock.objects.bulk_create(objs=medicines_to_create, batch_size=50, ignore_conflicts=True)
        messages.success(request, f"{len(medicines_to_create)} medicines added successfuly.")
    context = {
        "title": "Upload Medicines by CSV"
    }
    return render(request, "hod_templates/upload_medicines_by_csv.html", context)


def addStock(request):
    form = StockForm(request.POST, request.FILES)
    if form.is_valid():
        # form = StockForm(request.POST, request.FILES)
        # context = {
        #     "medicine_name": request.POST["drug_name"],
        #     "drug_description": request.POST["drug_description"],
        #     "quantity": request.POST["quantity"],
        #     "discount": request.POST["discount"],
        #     "mrp": request.POST["price"],
        #     "rate": request.POST["igst"],
        #     "tax": request.POST["tax"],
        #     "batch": request.POST["batch_number"],
        #     "packing": request.POST["packing"],
        # }
        # PurchasedInvoice.objects.create(invoice_data=context)
        form.save()
        return redirect("manage_stock")

    context = {"form": form, "title": "Add New Drug"}
    return render(request, "hod_templates/add_stock.html", context)


def manageStock(request):
    # stocks = Stock.objects.all().order_by("-id")
    # ex = Stock.objects.annotate(
    #     expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    # ).filter(expired=True)
    eo = Stock.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=False)

    context = {
        "stocks": eo,
        # "expired": ex,
        "expa": eo,
        "title": "Manage Stocked Medicines",
    }

    return render(request, "hod_templates/manage_stock.html", context)


def manageStockExpirerd(request):
    # stocks = Stock.objects.all().order_by("-id")
    ex = Stock.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
    # eo = Stock.objects.annotate(
    #     expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    # ).filter(expired=False)
    context = {
        "title": "Manage Expired Medicines",
        "stocks": ex,
        "expired": ex,
    }
    return render(request, "hod_templates/manage_stock.html", context)



# Category View
def manageCategory(request):
    categories = Category.objects.all().order_by("-id")
    context = {
        "categories": categories,
        "title": "Manage Drugs Categories",
    }
    return render(request, "hod_templates/manage_categories.html", context)


def addCategory(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Category added Successfully!")

            return redirect("manage_category")
    context = {"form": form, "title": "Add a New Drug Category"}
    return render(request, "hod_templates/add_category.html", context)


def editCategory(request, id):
    cat = get_object_or_404(Category, id=id)
    form = CategoryForm(instance=cat, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully!")

            return redirect("manage_category")
    context = {"form": form, "title": "Update Drug Category"}
    return render(request, "hod_templates/add_category.html", context)


def deleteCategory(request, id):
    cat = get_object_or_404(Category, id=id)
    cat.delete()
    return redirect("manage_category")


# Department View
def manageDepartment(request):
    departments = Department.objects.all().order_by("-id")
    context = {
        "departments": departments,
        "title": "Manage Department",
    }
    return render(request, "hod_templates/manage_department.html", context)


def addDepartment(request):
    form = DepartmentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Department added Successfully!")

            return redirect("manage_department")
    context = {"form": form, "title": "Add a New Department"}
    return render(request, "hod_templates/add_category.html", context)


def editDepartment(request, id):
    cat = get_object_or_404(Department, id=id)
    form = DepartmentForm(instance=cat, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Department Updated Successfully!")

            return redirect("manage_department")
    context = {"form": form, "title": "Update Department"}
    return render(request, "hod_templates/add_category.html", context)


def deleteDepartment(request, id):
    cat = get_object_or_404(Department, id=id)
    cat.delete()
    return redirect("manage_department")



# Manufacturer
def manageManufacturer(request):
    manufacturers = Manufacturer.objects.all().order_by("-id")
    context = {
        "manufacturers": manufacturers,
        "title": "Manage Drugs Leaf",
    }
    return render(request, "hod_templates/manage_manufacturer.html", context)


def addManufacturer(request):
    form = ManufacturerForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Manufacturer added Successfully!")

            return redirect("manage_manufacturer")
    context = {"form": form, "title": "Add a New Drug Manufacturer"}
    return render(request, "hod_templates/add_category.html", context)


def editManufacturer(request, id):
    cat = get_object_or_404(Manufacturer, id=id)
    form = ManufacturerForm(instance=cat, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Manufacturer Updated Successfully!")

            return redirect("manage_manufacturer")
    context = {"form": form, "title": "Update Drug Manufacturer"}
    return render(request, "hod_templates/add_category.html", context)


def deleteManufacturer(request, id):
    cat = get_object_or_404(Manufacturer, id=id)
    cat.delete()
    return redirect("manage_manufacturer")


# Drug Type
def manageDrugType(request):
    drug_Types = DrugType.objects.all().order_by("-id")
    context = {
        "drug_types": drug_Types,
        "title": "Manage Drugs Type",
    }
    return render(request, "hod_templates/manage_drug_type.html", context)


def addDrugType(request):
    form = DrugTypeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Drug Type added Successfully!")

            return redirect("manage_drug_type")
    context = {"form": form, "title": "Add a New Drug DrugType"}
    return render(request, "hod_templates/add_category.html", context)


def editDrugType(request, id):
    cat = get_object_or_404(DrugType, id=id)
    form = DrugTypeForm(instance=cat, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Drug Type Updated Successfully!")

            return redirect("manage_drug_type")
    context = {"form": form, "title": "Update DrugType"}
    return render(request, "hod_templates/add_category.html", context)


def deleteDrugType(request, id):
    cat = get_object_or_404(DrugType, id=id)
    cat.delete()
    return redirect("manage_drug_type")


# Drug Unit
def manageDrugUnit(request):
    drug_units = DrugUnit.objects.all().order_by("-id")
    context = {
        "drug_units": drug_units,
        "title": "Manage Drugs Unit",
    }
    return render(request, "hod_templates/manage_drug_unit.html", context)


def addDrugUnit(request):
    form = DrugUnitForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Drug Unit added Successfully!")

            return redirect("manage_drug_unit")
    context = {"form": form, "title": "Add a New Drug Unit"}
    return render(request, "hod_templates/add_category.html", context)


def editDrugUnit(request, id):
    cat = get_object_or_404(DrugUnit, id=id)
    form = DrugUnitForm(instance=cat, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Drug Unit Updated Successfully!")

            return redirect("manage_drug_unit")
    context = {"form": form, "title": "Update Drug Unit"}
    return render(request, "hod_templates/add_category.html", context)


def deleteDrugUnit(request, id):
    cat = get_object_or_404(DrugUnit, id=id)
    cat.delete()
    return redirect("manage_drug_unit")


# Prescription
def addPrescription(request):
    form = PrescriptionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("prescribe")

    context = {"form": form, "title": "Prescribe Drug"}
    return render(request, "hod_templates/prescribe.html", context)


def editPatient(request, patient_id):
    # adds patient id into session variable
    request.session["patient_id"] = patient_id

    patient = Patients.objects.get(admin=patient_id)

    form = EditPatientForm()

    # filling the form with data from the database
    form.fields["email"].initial = patient.admin.email
    form.fields["username"].initial = patient.admin.username
    form.fields["first_name"].initial = patient.first_name
    form.fields["last_name"].initial = patient.last_name
    form.fields["address"].initial = patient.address
    form.fields["gender"].initial = patient.gender
    form.fields["phone_number"].initial = patient.phone_number
    form.fields["age"].initial = patient.age
    if request.method == "POST":
        if patient_id == None:
            return redirect("all_patients")
        form = EditPatientForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            address = form.cleaned_data["address"]
            gender = form.cleaned_data["gender"]
            age = form.cleaned_data["age"]
            phone_number = form.cleaned_data["phone_number"]

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=patient_id)
                user.username = username

                user.email = email
                user.save()

                # Then Update Students Table
                patients_edit = Patients.objects.get(admin=patient_id)
                patients_edit.address = address
                patients_edit.gender = gender
                patients_edit.age = age
                patients_edit.phone_number = phone_number
                patients_edit.first_name = first_name
                patients_edit.last_name = last_name

                patients_edit.save()
                messages.success(request, "Patient Updated Successfully!")
                return redirect("all_patients")
            except:
                messages.success(request, "Failed to Update Patient.")
                return redirect("all_patients")

    context = {
        "id": patient_id,
        # "username": patient.admin.username,
        "form": form,
        "title": "Edit Patient",
    }
    return render(request, "hod_templates/edit_patient.html", context)


def patient_personalRecords(request, pk):
    patient = Patients.objects.get(id=pk)
    prescrip = patient.prescription_set.all()
    stocks = patient.dispense_set.all()

    context = {"patient": patient, "prescription": prescrip, "stocks": stocks}
    return render(request, "hod_templates/patient_personalRecords.html", context)


def deletePrescription(request, pk):
    prescribe = Prescription.objects.get(id=pk)
    if request.method == "POST":
        prescribe.delete()
        return redirect("all_patients")

    context = {"patient": prescribe}

    return render(request, "hod_templates/sure_delete.html", context)


def hodProfile(request):
    customuser = CustomUser.objects.get(id=request.user.id)
    staff = AdminHOD.objects.get(admin=customuser.id)

    form = HodForm()
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.save()

        staff = AdminHOD.objects.get(admin=customuser.id)
        form = HodForm(request.POST, request.FILES, instance=staff)
        staff.address = address

        staff.mobile = mobile
        staff.save()

        if form.is_valid():
            form.save()

    context = {"form": form, "staff": staff, "user": customuser}

    return render(request, "hod_templates/hod_profile.html", context)


def deleteDoctor(request, pk):
    try:
        doctor = Doctor.objects.get(id=pk)
        if request.method == "POST":
            doctor.delete()
            messages.success(request, "Doctor  deleted successfully")

            return redirect("manage_doctor")

    except:
        messages.error(request, "Doctor aready deleted")
        return redirect("manage_doctor")

    return render(request, "hod_templates/sure_delete.html")


def deletePharmacist(request, pk):
    try:
        pharmacist = Pharmacist.objects.get(id=pk)
        if request.method == "POST":
            pharmacist.delete()
            messages.success(request, "Pharmacist  deleted successfully")

            return redirect("manage_pharmacist")

    except:
        messages.error(request, "Pharmacist aready deleted")
        return redirect("manage_pharmacist")

    return render(request, "hod_templates/sure_delete.html")


def deletePharmacyClerk(request, pk):
    try:
        clerk = PharmacyClerk.objects.get(id=pk)
        if request.method == "POST":
            clerk.delete()
            messages.success(request, "Pharmacy Clerk  deleted   successfully")

            return redirect("manage_pharmacyClerk")

    except:
        messages.error(request, "Pharmacy  Clerk Not deleted")
        return redirect("manage_pharmacyClerk")

    return render(request, "hod_templates/sure_delete.html")


def editPharmacist(request, staff_id):
    staff = Pharmacist.objects.get(admin=staff_id)
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")

        # INSERTING into Customuser Model
        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        # INSERTING into Staff Model
        staff = Pharmacist.objects.get(admin=staff_id)
        staff.address = address
        staff.save()

        messages.success(request, "Staff Updated Successfully.")
        return redirect("manage_pharmacist")
    context = {"staff": staff, "id": staff_id, "title": "Edit Pharmacist "}
    return render(request, "hod_templates/edit_pharmacist.html", context)


def editDoctor(request, doctor_id):
    staff = Doctor.objects.get(admin=doctor_id)
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        department = request.POST.get("department", None)

        # INSERTING into Customuser Model
        user = CustomUser.objects.get(id=doctor_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        # INSERTING into Staff Model
        staff = Doctor.objects.get(admin=doctor_id)
        staff.address = address
        if department:
            department = Department.objects.get(id=department)
            staff.department = department
        staff.save()

        messages.success(request, "Staff Updated Successfully.")

    context = {
        "staff": staff, 
        "title": "Edit Doctor",
        "departments": Department.objects.all()
    }
    return render(request, "hod_templates/edit_doctor.html", context)


def editPharmacyClerk(request, clerk_id):
    clerk = PharmacyClerk.objects.get(admin=clerk_id)
    if request.method == "POST":
        username = request.POST.get("username")
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        email = request.POST.get("email")

        try:
            user = CustomUser.objects.get(id=clerk_id)
            user.email = email
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            clerk = PharmacyClerk.objects.get(admin=clerk_id)
            clerk.address = address
            clerk.mobile = mobile
            clerk.gender = gender
            clerk.save()

            messages.success(request, "Receptionist Updated Succefully")
        except:
            messages.success(
                request, "An Error Was Encounterd Receptionist Not Updated"
            )

    context = {"staff": clerk, "title": "Edit PharmacyClerk"}
    return render(request, "hod_templates/edit_clerk.html", context)


def editAdmin(request):
    customuser = CustomUser.objects.get(id=request.user.id)
    staff = AdminHOD.objects.get(admin=customuser.id)

    form = HodForm()
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.save()

        staff = AdminHOD.objects.get(admin=customuser.id)
        form = HodForm(request.POST, request.FILES, instance=staff)
        staff.address = address

        staff.mobile = mobile
        staff.save()

        if form.is_valid():
            form.save()

    context = {"form": form, "staff": staff, "user": customuser}

    return render(request, "hod_templates/edit-profile.html", context)


def editStock(request, pk):
    drugs = Stock.objects.get(id=pk)
    form = StockForm(data=request.POST or None, files=request.FILES or None, instance=drugs)

    if request.method == "POST":
        if form.is_valid():
            # form = StockForm(request.POST or None, instance=drugs)

            category = request.POST.get("category")
            drug_name = request.POST.get("drug_name")
            quantity = request.POST.get("quantity")
            # email=request.POST.get('email')

            try:
                drugs = Stock.objects.get(id=pk)
                drugs.drug_name = drug_name
                drugs.quantity = quantity
                drugs.save()
                form.save()
                messages.success(request, "Receptionist Updated Succefully")
                return redirect("manage_stock")
            except  Exception as e:
                print(e)
                messages.error(
                    request, f"{e}"
                )

    context = {"drugs": drugs, "form": form, "title": "Edit Stock"}
    return render(request, "hod_templates/edit_drug.html", context)


def deleteDrug(request, pk):
    try:
        drugs = Stock.objects.get(id=pk)
        if request.method == "POST":
            drugs.delete()
            messages.success(request, "Pharmacist  deleted successfully")

            return redirect("manage_stock")

    except:
        messages.error(request, "Pharmacist aready deleted")
        return redirect("manage_stock")

    return render(request, "hod_templates/sure_delete.html")


def receiveDrug(request, pk):
    receive = Stock.objects.get(id=pk)
    form = ReceiveStockForm()
    try:
        form = ReceiveStockForm(request.POST or None)

        if form.is_valid():
            form = ReceiveStockForm(request.POST or None, instance=receive)

            instance = form.save(commit=False)
            instance.quantity += instance.receive_quantity
            instance.save()
            form = ReceiveStockForm()

            messages.success(
                request,
                str(instance.receive_quantity)
                + " "
                + instance.drug_name
                + " "
                + "drugs added successfully",
            )

            return redirect("manage_stock")

    except:
        messages.error(request, "An Error occured, Drug quantity Not added")

        return redirect("manage_stock")
    context = {"form": form, "title": "Add Drug"}
    return render(request, "hod_templates/modal_form.html", context)


def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(
            request,
            "Reorder level for "
            + str(instance.drug_name)
            + " is updated to "
            + str(instance.price),
        )

        return redirect("manage_stock")
    context = {"instance": queryset, "form": form, "title": "Reorder Level"}

    return render(request, "hod_templates/reorder_level.html", context)


def drugDetails(request, pk):
    stocks = Stock.objects.get(id=pk)
    # prescrip=stocks.prescription_set.all()
    # stocks=stocks.dispense_set.all()

    context = {
        "stocks": stocks,
        # "prescription":prescrip,
        # "stocks":stocks
    }
    return render(request, "hod_templates/view_drug.html", context)


def purchased_invoice_list(request):
    all_invoice = PurchasedInvoice.objects.all()
    context = {
        "all_invoice": all_invoice
    }
    return render(request, "hod_templates/purchased_invoice.html", context)


def purchased_invoice_detail(request, pk):
    get_invoice = PurchasedInvoice.objects.get(id=int(pk))
    # total_amount = float(get_invoice.invoice_data['price']) - float(get_invoice.invoice_data['discount']) + float(
    #     get_invoice.invoice_data['tax'])
    # p = inflect.engine()
    # grand_total_str = p.number_to_words(total_amount)
    medicine_list = NewPurchaseData.objects.filter(id__in=get_invoice.medicine_data.all())
    p = inflect.engine()
    grand_total_str = p.number_to_words(get_invoice.total)
    print(medicine_list, "medicine_list")
    context = {
        "medicine_list": medicine_list,
        "get_invoice": get_invoice,
        "total_amount": "total_amount",
        "grand_total_str": grand_total_str
    }
    return render(request, "hod_templates/purchase/invoice_view.html", context)


# def delete_invoice(request)


# Billing POS
def billingPOS(request):
    drugs = Stock.objects.prefetch_related().all()
    # categories = drugs.values_list('category', flat=True)
    categories = Category.objects.all()
    venders = Vender.objects.all()
    custumers = CustomUser.objects.filter(user_type="Patients")
    context = {
        "drugs": drugs,
        'categories': categories,
        "venders": venders,
        "custumers": custumers
    }
    return render(request, "pos/pos.html", context)


#  Billing Print POS
def billingPrintPOS(request, id, action=None):
    bill = get_object_or_404(BillingPOS, id=id)
    context = {
        "bill": bill
    }
    return render(request, "pos/bill-print.html", context)



# Manage Vender
def manageVender(request):
    venders = Vender.objects.all()
    context = {
        "venders": venders,
        "title": "Manage Vensers",
    }
    return render(request, "hod_templates/manage_venders.html", context)


def addVender(request):
    form = VenderForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user_type = "Vender"
            form.save()
            messages.success(request, "Vender added Successfully!")

            return redirect("manage_vender")
    context = {"form": form, "title": "Add a New Vender"}
    return render(request, "hod_templates/add_category.html", context)


def editVender(request, id):
    cat = get_object_or_404(Vender, id=id)
    form = VenderForm(instance=cat, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Vender Updated Successfully!")

            return redirect("manage_vender")
    context = {"form": form, "title": "Update Vender"}
    return render(request, "hod_templates/add_category.html", context)


def deleteVender(request, id):
    cat = get_object_or_404(Vender, id=id)
    cat.delete()
    return redirect("manage_vender")


# Manage Supplier
def manageSupplier(request):
    suppliers = CustomUser.objects.filter(user_type="Supplier").order_by("-id")
    context = {
        "suppliers": suppliers,
        "title": "Manage Vensers",
    }
    return render(request, "hod_templates/manage_suppliers.html", context)


def addSupplier(request):
    form = AddUserForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user_type = "Supplier"
            form.save()
            messages.success(request, "Supplier added Successfully!")

            return redirect("manage_supplier")
    context = {"form": form, "title": "Add a New Supplier"}
    return render(request, "hod_templates/add_category.html", context)


def editSupplier(request, id):
    supplier = get_object_or_404(CustomUser, id=id)
    form = AddUserForm(instance=supplier, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier Updated Successfully!")

            return redirect("manage_supplier")
    context = {"form": form, "title": "Update Supplier"}
    return render(request, "hod_templates/add_category.html", context)


def deleteSupplier(request, id):
    supplier = get_object_or_404(CustomUser, id=id)
    supplier.delete()
    return redirect("manage_supplier")


def new_purchase_fun(request):
    manufacture_list = Stock.objects.all()
    purchased_list = NewPurchaseData.objects.filter(status=False)

    sub_total = sum(purchase.sub_total for purchase in purchased_list)
    discount = sum(purchase.discount for purchase in purchased_list)
    total = sum(purchase.total for purchase in purchased_list)

    context = {
        "manufacture_list": manufacture_list,
        "purchased_list": purchased_list,
        "sub_total": sub_total,
        "discount": discount,
        "total": total,
    }

    if request.method == "POST":
        date_get = request.POST.get("purchase_date")
        invoice_num = request.POST.get("voice_num")
        manufacture_name = request.POST.get("manufacture_name")
        purchase_ids = request.POST.getlist('purchase_id[]')
        payment_type = request.POST.get("payment_type")
        paid_amount = request.POST.get("paid_amount")
        due_amount = request.POST.get("due_amount")

        sub_total_pur = sum(
            get_object_or_404(NewPurchaseData, id=int(purchase_id)).sub_total for purchase_id in purchase_ids)
        discount_pur = sum(
            get_object_or_404(NewPurchaseData, id=int(purchase_id)).discount for purchase_id in purchase_ids)
        total_pur = sum(get_object_or_404(NewPurchaseData, id=int(purchase_id)).total for purchase_id in purchase_ids)

        purchased_invoice = PurchasedInvoice.objects.create(
            invoice_no=invoice_num,
            manufacture=manufacture_name,
            date=date_get,
            quantity=discount_pur,
            sub_total=sub_total_pur,
            discount=discount_pur,
            total=total_pur,
            paid=paid_amount,
            due=due_amount,
            payment_type=payment_type
        )

        for purchase_id in purchase_ids:
            instance = get_object_or_404(NewPurchaseData, id=int(purchase_id))
            purchased_invoice.medicine_data.add(instance)
            instance.status = True
            instance.save()
        messages.success(request, "Purchase created successfully")
        return redirect("new_purchase")

    return render(request, "hod_templates/purchase/new_purchase.html", context)


@csrf_exempt
def search_stock(request):
    query = request.GET.get('query', '')
    results = Stock.objects.filter(drug_name__icontains=query) | Stock.objects.filter(
        generic_drug_name__icontains=query)
    data = [
        {'drug_name': stock.drug_name,
         'generic_name': stock.generic_drug_name,
         'price': stock.price,
         'image': stock.drug_pic.url,
         'id': stock.id,
         } for stock in results]
    return JsonResponse(data, safe=False)


def add_searched_stock(request):
    stock_id = request.GET.get("selected_option")
    ins_stock = Stock.objects.get(id=int(stock_id))
    if NewPurchaseData.objects.filter(drug_name=ins_stock, status=False).exists():
        pass
    else:
        instance = NewPurchaseData.objects.create(drug_name=ins_stock, mrp_per_unit=0, buy_price_per_unit=0, quantity=0,
                                                  sub_total=0, discount=0, total=0)
        messages.success(request, "Item has been added")
    return redirect("new_purchase")


def delete_searched_stock(request, id):
    ins = get_object_or_404(NewPurchaseData, id=int(id))
    ins.delete()
    messages.success(request, "Item has been removed")
    return redirect("new_purchase")


@csrf_exempt
def update_added_stock_detail(request):
    stock_id = request.POST.get("purchase_id")
    new_value = request.POST.get("new_value")
    data_type = request.POST.get("data_type")
    get_instance = get_object_or_404(NewPurchaseData, id=int(stock_id))
    if data_type == "buy_price_per_unit":
        get_instance.buy_price_per_unit = int(new_value)
        get_instance.sub_total = int(get_instance.quantity) * int(new_value)
        get_instance.total = int(get_instance.quantity) * int(new_value)
        messages.success(request, "MRP Item updated")
    elif data_type == "quantity":
        get_instance.quantity = int(new_value)
        get_instance.sub_total = int(get_instance.buy_price_per_unit) * int(new_value)
        get_instance.total = int(get_instance.buy_price_per_unit) * int(new_value)
        messages.success(request, "Item updated")
    elif data_type == "discount":
        get_instance.discount = int(new_value)
        discount_price = ((int(new_value) / get_instance.sub_total) * 100)
        get_instance.total = int(get_instance.sub_total - discount_price)
        print((get_instance.sub_total - discount_price), discount_price)
        messages.success(request, "Item updated")
    get_instance.save()
    return redirect("new_purchase")


def purchase_history(request):
    all_history = PurchasedInvoice.objects.all()
    context = {
        "all_history": all_history
    }
    return render(request, "hod_templates/purchase/purchase_history.html", context)




# Patient Addmission
def manageAddmission(request):
    addmissions = Addmission.objects.all().order_by("-id")
    context = {
        "addmissions": addmissions,
        "title": "Manage Patient Addmission",
    }
    return render(request, "hod_templates/manage_addmission.html", context)


def addAddmission(request):
    form = AddmissionForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Patient Addmission added Successfully!")

            return redirect("manage_addmission")
    context = {"form": form, "title": "New Patient Addmission"}
    return render(request, "hod_templates/add_category.html", context)


def editAddmission(request, id):
    cat = get_object_or_404(Addmission, id=id)
    form = AddmissionForm(instance=cat, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Patient Addmission Updated Successfully!")

            return redirect("manage_addmission")
    context = {"form": form, "title": "Update Addmission"}
    return render(request, "hod_templates/add_category.html", context)


def deleteAddmission(request, id):
    cat = get_object_or_404(Addmission, id=id)
    cat.delete()
    return redirect("manage_addmission")

