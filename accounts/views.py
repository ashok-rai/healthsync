from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import CustomUserCreationForm
from django.contrib.auth import views as auth_views  # Authentication views


class UserLoginView(auth_views.LoginView):
    """
    Display the login form and handle the login action.
    """
    template_name = "accounts/login.html"

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirect based on user type
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            elif user.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                # In case user_type is somehow unset
                messages.error(request, "User type is not defined!")
                return redirect('login')
        else:
            messages.error(request, "Invalid credentials!")
    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})




@login_required
def dashboard(request):
    if request.user.user_type.lower() == 'patient':
        return render(request, 'accounts/patient_dashboard.html')
    elif request.user.user_type.lower() == 'doctor':
        return render(request, 'accounts/doctor_dashboard.html')
    else:
        messages.error(request, "User type is not defined!")
        return redirect('home')

def doctor_dashboard(request):
    context = {'user': request.user}
    return render(request, 'accounts/doctor_dashboard.html', context=context)

def patient_dashboard(request):
    context = {'user': request.user}
    return render(request, 'accounts/patient_dashboard.html', context=context)
