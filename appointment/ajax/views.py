from django.http.response import JsonResponse
from pharmacy.models import Doctor



def load_doctor_fees(request):
    doctor_id = request.GET.get('doctor_id')
    doctor = Doctor.objects.get(id=doctor_id)
    context = {
        "fees": doctor.fees,
    }
    return JsonResponse(context)
