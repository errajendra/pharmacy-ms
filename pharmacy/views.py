from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
from .decorators import *
from django.conf.global_settings import AUTH_USER_MODEL as User
from .models import CustomUser

# Create your views here.

# @unautheticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('logout')
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        # user=authenticate(request,username=username,password=password)
        try:
            user = CustomUser.objects.get(username=username)
            # user.set_password(password)
            # user.save()
            print(user)
            if not user.check_password(password):
                user = None
                print(user)
        except:
            user = None
        if user:
            login(request, user)
            user_type = user.user_type
            if user_type == 'AdminHOD':
                return redirect('admin_dashboard')
                
            elif user_type == 'Pharmacist':
                return redirect('pharmacist_home')

            elif user_type == 'Doctor':
                return redirect('doctor_home')
            elif user_type == 'Pathologist':
                return redirect('pathologist_home')
            elif user_type == 'Patients':
                return redirect('patient_home')
            elif user_type == 'Reception':
                return redirect('receptionist_home')
            elif user_type == 'Nurse':
                return redirect('nurse_home')
                
           
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
