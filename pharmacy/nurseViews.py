from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

@login_required
def nurseHome(request):
    return render(request,'nurse_templates/nurse_home.html')
