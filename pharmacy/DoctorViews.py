from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import  UserCreationForm
from .decorators import *
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from appointment.models import Appointment
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.urls import reverse
from django.forms import inlineformset_factory

def doctorHome(request): 
    prescip = Prescription.objects.all().count()

    context={
        "Prescription_total":prescip

    }
    return render(request,'doctor_templates/doctor_home.html',context)

def doctorProfile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=Doctor.objects.get(admin=customuser.id)

    form=DoctorForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')


        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.save()

        staff=Doctor.objects.get(admin=customuser.id)
        form =DoctorForm(request.POST,request.FILES,instance=staff)

        staff.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "staff":staff,
        "user":customuser
    }

    return render(request,'doctor_templates/doctor_profile.html',context)

def managePatients(request):
    patients=Patients.objects.all()

    context={
        "patients":patients,

    }
    return render(request,'doctor_templates/manage_patients.html',context)

def addPrescription(request,pk):        
    patient=Patients.objects.get(id=pk)
    form=PrescriptionForm(initial={'patient_id':patient})
    if request.method == 'POST':
        try:
            form=PrescriptionForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request,'Prescription added successfully')
                return redirect('manage_precrip_doctor')
        except:
            messages.error(request,'Prescription Not Added')
            return redirect('manage_patient-doctor')


 
    
    context={
        "form":form
    }
    return render(request,'doctor_templates/prescribe_form.html',context)

def patient_personalDetails(request,pk):
    patient=Addmission.objects.get(id=pk)
    # patient=Patients.objects.get(id=pk)
    # prescrip=addmission.prescription_set.all()

    context={
        "patient":patient,
        # "prescription":prescrip

    }
    return render(request,'doctor_templates/patient_personalRecords.html',context)

def deletePrescription(request,pk):
    prescribe=Prescription.objects.get(id=pk)

    if request.method == 'POST':
        try:
            prescribe.delete()
            messages.success(request,'Prescription Deleted successfully')
            return redirect('manage_precrip_doctor')
        except:
            messages.error(request,'Prescription Not Deleted successfully')
            return redirect('manage_precrip_doctor')




    context={
        "patient":prescribe
    }

    return render(request,'doctor_templates/sure_delete.html',context)
    
def managePrescription(request):
    precrip=Prescription.objects.all()

    patient = Patients.objects.all()
    
       
    context={
        "prescrips":precrip,
        "patient":patient
    }
    return render(request,'doctor_templates/manage_prescription.html' ,context)


@login_required
def editPrescription(request,pk):
    prescribe=Prescription.objects.get(id=pk)
    form=PrescriptionForm(instance=prescribe)

    
    if request.method == 'POST':
        form=PrescriptionForm(request.POST ,instance=prescribe)

        try:
            if form.is_valid():
                form.save()

                messages.success(request,'Prescription Updated successfully')
                return redirect('manage_precrip_doctor')
        except:
            messages.error(request,' Error!! Prescription Not Updated')
            return redirect('manage_precrip_doctor')




    context={
        "patient":prescribe,
        "form":form
    }

    return render(request,'doctor_templates/edit_prescription.html',context)
    
    
@login_required
def appointment_list_doctor(request):
    doctor = get_object_or_404(Doctor, admin=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date')
    
    context = {
        "title": "Appointments",
        "appointments": appointments,
    }
    return render(request, "doctor_templates/appointment/appointment_list_doctor.html", context)


@login_required
def update_appointment_status(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == "POST":
        status = request.POST.get('status')
        appointment.status = status
        appointment.save()
        messages.success(request, 'Appointment status updated successfully.')
    if request.user.user_type == 'Reception':
        return redirect("appointment_list_receptionist")
    else:
        return redirect('appointment_list_doctor')


@login_required
def patient_record_doctor(request):
    doctor = get_object_or_404(Doctor, admin=request.user)
    addmissions = Addmission.objects.filter(doctor=doctor).order_by("-id")
    context = {
        "addmissions": addmissions,
        "title": "Manage Patient Record",
    }
    return render(request, "doctor_templates/patient-record/patient_list_doctor.html", context)


@login_required
def update_patient_record_doctor(request, id):
    cat = get_object_or_404(Addmission, id=id)
    form = PatientRecordForm(instance=cat, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Patient Record Updated Successfully!")

            return redirect("patient_record_doctor")
    context = {"form": form, "title": "Update Patient Record"}
    return render(request, "doctor_templates/patient-record/update_patient_record.html", context)


@csrf_exempt
def view_patient_details(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            patient_id = request.POST.get('patient_id')
            admission = Addmission.objects.get(id=patient_id)
            context = {'data': admission}
            html = render_to_string("doctor_templates/patient-record/view_patient_detail.html", context, request=request)
            return JsonResponse({'html': html})
        except Addmission.DoesNotExist:
            return JsonResponse({'html': '<p>Admission not found.</p>'}, status=404)
        except Exception as ex:
            return JsonResponse({'html': f'<p>Error: {str(ex)}</p>'}, status=500)
    return JsonResponse({'html': '<p>Invalid request.</p>'}, status=400)


@login_required
def all_patient_record_doctor(request):
    doctor = get_object_or_404(Doctor, admin=request.user)
    patients = Addmission.objects.filter(doctor=doctor).order_by("-id")
    context = {
        "patients": patients,
        "title": "Patient Record",
    }
    return render(request, "doctor_templates/prescription/all_patient_list.html", context)

  
@login_required  
def view_patient_profile(request, id):
    addmission = Addmission.objects.get(id=id)
    doctor = Doctor.objects.get(id=addmission.doctor.id)
    patient = Patients.objects.get(id=addmission.patient_id)
    prescriptions = Prescription.objects.filter(patient_id=patient, doctor=doctor).prefetch_related('clinicalnote_set')
    context = {
        "data":addmission,
        "prescriptions":prescriptions
    }
    return render(request, "doctor_templates/prescription/patient_profile.html", context)
 

@login_required 
def add_prescription_patient(request, id):
    addmission = get_object_or_404(Addmission, id=id)
    patient = get_object_or_404(Patients, id=addmission.patient_id)
    doctor = get_object_or_404(Doctor, id=addmission.doctor.id)

    ClinicalNoteFormSet = inlineformset_factory(
        Prescription, ClinicalNote, fields=('note_type', 'note', 'image'), extra=1
    )

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        clinical_note_formset = ClinicalNoteFormSet(request.POST, request.FILES)
        if form.is_valid() and clinical_note_formset.is_valid():
            prescription = form.save(commit=False)
            prescription.patient_id = patient
            prescription.doctor = doctor
            prescription.save()
            for clinical_note_form in clinical_note_formset:
                if clinical_note_form.cleaned_data.get('note'):
                    clinical_note = clinical_note_form.save(commit=False)
                    clinical_note.prescription = prescription
                    clinical_note.added_by = request.user
                    clinical_note.save()
            messages.success(request, 'Prescription and clinical notes added successfully.')
            return redirect(reverse('view_patient_profile', kwargs={'id': id}))
        else:
            messages.error(request, 'Failed to add prescription or clinical notes. Please check the form data.')
    else:
        form = PrescriptionForm(initial={'patient': patient})
        clinical_note_formset = ClinicalNoteFormSet(queryset=ClinicalNote.objects.none())

    context = {
        "form": form,
        "clinical_note_formset": clinical_note_formset,
        "patient": patient
    }
    return render(request, 'doctor_templates/prescription/add_prescription.html', context)
        
@login_required
def clinical_notes_doctor(request):
    user = request.user
    if user.user_type == 'Doctor':
        notes = ClinicalNote.objects.filter(added_by=user).order_by("-id")
        context = {
            "notes": notes,
            "title": "Clinical Notes",
        }
        return render(request, "doctor_templates/clinical-notes/clinical_notes_doctor.html", context)
    else:
        return render(request, "appointment/clinical_notes_doctor.html")


@login_required
def add_clinical_note_doctor(request):
    if request.method == 'POST':
        note_type = request.POST.get('note_type')
        note = request.POST.get('note')
        image = request.FILES.get('image')

        if not note_type or not note:
            messages.error(request, 'Note type and note are required.')
        else:
            if request.user.user_type == 'Doctor':
                clinical_note = ClinicalNote(
                    added_by=request.user,
                    note_type=note_type,
                    note=note,
                    image=image
                )
                clinical_note.save()
                messages.success(request, 'Clinical note added successfully.')
                return redirect('clinical_notes_doctor')
            else:
                messages.warning(request, "User is not Doctor!!")

    context = {
        'title': 'Add Clinical Note'
    }
    
    return render(request, 'doctor_templates/clinical-notes/add_clinical_note.html', context)


@login_required
def edit_clinical_note_doctor(request, id):
    clinical_note = get_object_or_404(ClinicalNote, id=id)
    if request.method == "POST":
        note_type = request.POST.get('note_type')
        note = request.POST.get('note')
        image = request.FILES.get('image')

        if not note_type or not note:
            messages.error(request, 'Note type and note are required.')
        else:
            if request.user.user_type == 'Doctor':
                clinical_note.note_type = note_type
                clinical_note.note = note
                if image:
                    clinical_note.image = image
                clinical_note.save()
                messages.success(request, "Clinical note updated successfully!")
                return redirect("clinical_notes_doctor")
            else:
                messages.warning(request, "User is not Doctor!!")

    context = {
        "clinical_note": clinical_note,
        "title": "Update Clinical Note"
    }
    return render(request, "doctor_templates/clinical-notes/edit_clinical_notes.html", context)
    
    
@login_required
def delete_clinical_note_doctor(request, id):
    instance = get_object_or_404(ClinicalNote, id=id)
    instance.delete()
    return redirect("clinical_notes_doctor")
