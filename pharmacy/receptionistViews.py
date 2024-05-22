from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

@login_required
def receptionistHome(request):
    return render(request,'receptionist_templates/receptionist_home.html')
