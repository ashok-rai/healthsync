from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
def dashboard(request):
    return render(request, 'home.html')
    # if request.user.user_type.lower() == 'patient':
    #     return render(request, 'accounts/patient_dashboard.html')
    # elif request.user.user_type.lower() == 'doctor':
    #     return render(request, 'accounts/doctor_dashboard.html')
    # else:
    #     messages.error(request, "User type is not defined!")
    #     return redirect('home')