from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

@login_required
def pathologistsHome(request):
    return render(request,'pathologist_templates/pathologist_home.html')
