
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random
# views.py
from .forms import SignUpForm

from django.http import JsonResponse
from .models import Location

from django.shortcuts import render
from .models import University

def university(request):
    universities = University.objects.all()
    return render(request, 'accounts/university.html', {'universities': universities})


def get_locations(request):
    locations = Location.objects.all()
    data = [
        {
            "name": location.name,
            "lat": location.lat,
            "lon": location.lon
        }
        for location in locations
    ]
    return JsonResponse(data, safe=False)




def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful signup
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))  # Redirect to a home page
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')


@login_required
def home_view(request):
    if request.method == "POST":
        # Capture the form data from POST request
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        address = request.POST.get('address')
        dropdown = request.POST.get('dropdown')

        # You can store the collected data or process it as needed
        # For demonstration, you can print it or save it to the database

        print("Name:", name)
        print("Contact:", contact)
        print("Email:", email)
        print("Address:", address)
        print("Dropdown selection:", dropdown)

        # Redirect to the same page after form submission (or another page if needed)
        return HttpResponseRedirect(reverse('dashboard'))

    return render(request, 'accounts/home.html')
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

def location(request):
    return render(request, 'accounts/location.html')
