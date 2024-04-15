from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.db.models import Sum
import inflect


@login_required
def pharmacistHome(request):
    patients_total = Patients.objects.all().count()
    exipred = (
        Stock.objects.annotate(
            expired=ExpressionWrapper(
                Q(valid_to__lt=Now()), output_field=BooleanField()
            )
        )
        .filter(expired=True)
        .count()
    )

    out_of_stock = Stock.objects.filter(quantity__lte=0).count()
    total_stock = Stock.objects.all().count()

    context = {
        "patients_total": patients_total,
        "expired_total": exipred,
        "out_of_stock": out_of_stock,
        "total_drugs": total_stock,
    }
    return render(request, "pharmacist_templates/pharmacist_home.html", context)


@login_required
def userProfile(request):
    staff = Pharmacist.objects.all()
    form = CustomerForm()
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        address = request.POST.get("address")

        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.first_name = first_name
        customuser.last_name = last_name

        customuser.save()
        staff = Pharmacist.objects.get(admin=customuser.id)
        form = CustomerForm(request.POST, request.FILES, instance=staff)

        staff.address = address
        if form.is_valid():
            form.save()
        staff.save()

        messages.success(request, "Profile Updated Successfully")
        return redirect("pharmacist_profile")

    context = {"staff": staff, "form": form}

    return render(request, "pharmacist_templates/staff_profile.html", context)


def managePatientsPharmacist(request):
    patient = Patients.objects.all()
    context = {"patients": patient}
    return render(request, "pharmacist_templates/manage_patients.html", context)


def managePrescription(request):
    precrip = Dispense.objects.all()
    invoices = SellInvoice.objects.all()

    context = {
        "prescrips": precrip,
        "invoices": invoices
    }
    return render(request, "pharmacist_templates/patient_prescrip.html", context)


def manageStock(request):
    stocks = Stock.objects.all().order_by("-id")
    ex = Stock.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
    eo = Stock.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=False)
    context = {
        "title": "Manage Medicines",
        "stocks": stocks,
        "expired": ex,
    }
    return render(request, "pharmacist_templates/manage_stock.html", context)


def manageDispense(request, pk):
    queryset = Patients.objects.get(id=pk)
    prescrips = queryset.prescription_set.all()

    form = DispenseForm(request.POST or None, initial={"patient_id": queryset})
    drugs = Stock.objects.all()
    ex = Stock.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
    eo = Stock.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=False)
    # print(ex)

    try:
        if request.method == "POST":
            if form.is_valid():
                qu = form.cleaned_data["dispense_quantity"]
                ka = form.cleaned_data["drug_id"]
                find_stock = Stock.objects.get(drug_name=ka)
                form.instance.patient_id = queryset
                discount = (2 / find_stock.mrp) * 100
                form.instance.discount = '%.2f' % discount
                form.instance.gst = find_stock.tax
                total_amount = find_stock.mrp - (2 / find_stock.mrp) * 100 + find_stock.tax
                form.instance.total_amount = '%.2f' % total_amount
                form.save()
                find_stock.quantity -= qu
                find_stock.save()

                messages.success(request, "Drug Has been Successfully Dispensed")

                return redirect(f"/manage_disp/{pk}/")
            else:
                messages.error(request, "Validty Error")
                return redirect(f"/manage_disp/{pk}/")
    except Exception as ex:
        messages.error(
            request,
            f"Dispensing Not Allowed! The Drug is Expired ,please contact the admin for re-stock, Error in {ex} ",
        )
        return redirect(f"/manage_disp/{pk}/")

    added_dispense = Dispense.objects.filter(patient_id=queryset, order_status=False)
    # if added_dispense:
    sub_total = added_dispense.aggregate(Sum('drug_id__mrp'))
    p = inflect.engine()
    if added_dispense:
        dispense = True
        grand_total_str = p.number_to_words(added_dispense.aggregate(Sum("total_amount"))['total_amount__sum'])
    else:
        dispense = False
        grand_total_str = "Zero"
    context = {
        "patients": queryset,
        "form": form,
        # "stocks":stock,
        "drugs": drugs,
        "prescrips": prescrips,
        "expired": ex,
        "expa": eo,
        "added_dispense": added_dispense,
        "sub_total": sub_total,
        "all_discount": added_dispense.aggregate(Sum("discount")),
        "all_gst": added_dispense.aggregate(Sum("gst")),
        "grand_total": added_dispense.aggregate(Sum("total_amount")),
        "grand_total_str": grand_total_str,
        "patient_id": queryset.id,
        "dispense": dispense,
        "redirect_url": "pharmacist_manage_patients"
    }

    return render(request, "pharmacist_templates/manage_dispense.html", context)


def patient_feedback_message(request):
    feedbacks = PatientFeedback.objects.all()
    context = {"feedbacks": feedbacks}
    return render(request, "pharmacist_templates/patient_feedback.html", context)


@csrf_exempt
def patient_feedback_message_reply(request):
    feedback_id = request.POST.get("id")
    feedback_reply = request.POST.get("reply")
    try:
        feedback = PatientFeedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def deletefeedback(request, pk):
    try:
        fed = PatientFeedback.objects.get(id=pk)
        if request.method == "POST":
            fed.delete()
            messages.success(request, "Feedback  deleted successfully")
            return redirect("patient_feedback_message")

    except:
        messages.error(request, "Feedback Error, Please Check again")
        return redirect("patient_feedback_message")

    return render(request, "pharmacist_templates/sure_delete.html")


def drugDetails(request, pk):
    stocks = Stock.objects.get(id=pk)
    context = {
        "stocks": stocks,
    }
    return render(request, "pharmacist_templates/view_drug.html", context)


def deleteDispense4(request, pk):
    try:
        fed = Dispense.objects.get(id=pk)
        patient = Patients.objects.get(id=fed.patient_id.id)
        if request.method == "POST":
            fed.delete()
            """ stock quantity update """
            stock_update = Stock.objects.get(id=fed.drug_id.id)
            stock_update.quantity += fed.dispense_quantity
            stock_update.save()
            messages.success(request, "Dispense  deleted successfully")
            return redirect(f"/manage_disp/{patient.id}/")

    except:
        messages.error(request, "Delete Error, Please Check again")
        return redirect("pharmacist_prescription")

    return render(request, "pharmacist_templates/sure_delete.html")


# # def dispenseDrug(request,pk):
# #     queryset=Patients.objects.get(id=pk)
# #     form=DispenseForm(initial={'patient_id':queryset})
# #     if request.method == 'POST':
# #         form=DispenseForm(request.POST or None)
# #         if form.is_valid():
# #             form.save()


# #     context={


def sell_slip(request, pk):
    queryset = Patients.objects.get(id=pk)
    added_dispense = Dispense.objects.filter(patient_id=queryset, order_status=False)
    sub_total = float(added_dispense.aggregate(total_price=Sum('drug_id__mrp'))['total_price'])
    p = inflect.engine()
    grand_total_str = p.number_to_words(added_dispense.aggregate(Sum("total_amount"))['total_amount__sum'])
    context = {
        "patients": queryset,
        "added_dispense": added_dispense,
        "sub_total": sub_total,
        "all_discount": added_dispense.aggregate(Sum("discount")),
        "all_gst": added_dispense.aggregate(Sum("gst")),
        "grand_total": added_dispense.aggregate(Sum("total_amount")),
        "grand_total_str": grand_total_str,
        "request": request
    }

    invoice_save(context)

    content = render(request, 'pharmacist_templates/sell_slip.html', context)

    response = HttpResponse(content, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename=sell_slip.html'
    # return response
    return render(request, "pharmacist_templates/sell_slip.html", context=context)


def createPatientPharmacist(request):
    form = PatientForm()
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']
            reg_no = form.cleaned_data['reg_no']

            user = CustomUser.objects.create_user(username=username, email=email, password=password,
                                                  last_name=last_name, user_type=5)
            user.patients.address = address
            user.patients.phone_number = phone_number
            user.patients.dob = dob
            user.patients.reg_no = reg_no
            user.patients.first_name = first_name
            user.patients.last_name = last_name
            user.patients.gender = gender

            user.save()
            messages.success(request, username + ' was Successfully Added')

            return redirect('manage_patient_pharmacist')

    context = {
        "form": form,
        "title": "Add Patient"
    }

    return render(request, 'pharmacist_templates/patient_add.html', context)


def invoice_save(context):
    try:
        json_content = {
            "patient_id": context['patients'].id,
            "dispense_ids": [int(dispense.id) for dispense in context['added_dispense']],
            "sub_total": context['sub_total'],
            "all_discount": context['all_discount']['discount__sum'],
            "all_gst": context['all_gst']['gst__sum'],
            "grand_total": context['grand_total']['total_amount__sum'],
            "grand_total_str": context['grand_total_str'],
        }
        SellInvoice.objects.create(patient_id=context['patients'], invoice_detail=json_content)
        dispense_list = Dispense.objects.filter(id__in=json_content['dispense_ids']).update(order_status=True)
        messages.success(context['request'], f"Invoice Created")
        pass
    except Exception as ex:
        messages.error(context['request'],f"Invoice not generate, because {ex}")
        return redirect(f"/manage_disp/{context['patients'].id}/")


def view_invoice_details(request, pk):
    get_invoice = SellInvoice.objects.get(id=int(pk))
    dispense_id = get_invoice.invoice_detail['dispense_ids']
    context = {
        "get_invoice": get_invoice,
        "added_dispense": Dispense.objects.filter(id__in=dispense_id)
    }
    return render(request, "pharmacist_templates/invoice_slip.html", context)