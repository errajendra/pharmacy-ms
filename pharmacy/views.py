from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
from .decorators import *
from django.conf.global_settings import AUTH_USER_MODEL as User
from django.shortcuts import get_object_or_404

# Create your views here.

# @unautheticated_user
def loginPage(request):
    print("siukghgjhgjhg")
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == 'AdminHOD':
                return redirect('admin_dashboard')
                
            elif user_type == 'Pharmacist':
                return redirect('pharmacist_home')

            elif user_type == 'Doctor':
                return redirect('doctor_home')
            elif user_type == 'PharmacyClerk':
                return redirect('clerk_home')
            elif user_type == 'Patients':
                return redirect('patient_home')
                
           
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')
    
    return render(request,'login.html')



def logoutUser(request):
    logout(request)
    return redirect('login')
