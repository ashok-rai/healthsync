from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

@login_required
def book_appointment(request):
    if request.user.role != 'Patient':
        return HttpResponseForbidden("Only patients can book appointments.")
    return render(request, 'appointments/book.html')