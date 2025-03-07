import random
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from .models import CustomUser, University, OTP, Application, Location
from .forms import SignUpForm, LoginForm, OTPForm, ApplicationForm
from django.core.mail import send_mail
from django.conf import settings


# Function to send OTP using Fast2SMS
def send_otp(number, message):
    url = "https://www.fast2sms.com/dev/bulkV2"
    api = "10EsuPO9dI0E9Wdf00NLLM6GEa6zYJPr5f1YRnZl2eV8pRytmNiFHsTaxgWR"
    querystring = {
        "authorization": api,
        "sender_id": "FSTSMS",
        "message": message, 
        "language": "english",
        "route": "p",
        "numbers": number
    }
    headers = {'cache-control': "no-cache"}
    return requests.request("GET", url, headers=headers, params=querystring)

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print("Form Data Received:", request.POST)  # Debugging
        print("Form Errors:", form.errors)  
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until OTP is verified
            user.save()

            # Generate OTP
            otp_code = random.randint(100000, 999999)
            OTP.objects.create(user=user, otp_code=str(otp_code))

            # Send OTP via SMS
            send_otp(user.phone_number, f"Your OTP for account verification is {otp_code}")

            # Store phone number in session
            request.session["otp_phone_number"] = user.phone_number
            request.session.modified = True  # Ensure session is saved

            messages.success(request, "OTP sent to your phone number. Please verify.")
            return redirect("verify_otp")  # Redirect to OTP verification page

        else:
            print(form.errors)  # Debugging: Print form errors to the console
            messages.error(request, "There was an error in the signup form. Please check your details.")

    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})

# OTP Verification for Signup
def verify_otp(request):
    phone_number = request.session.get("otp_phone_number")

    if not phone_number:
        messages.error(request, "Session expired. Please sign up again.")
        return redirect("signup")

    user = CustomUser.objects.get(phone_number=phone_number)

    if request.method == "POST":
        form = OTPForm(request.POST)
        print("Form Data Received:", request.POST)  # Debugging
        print("Form Errors:", form.errors)  # Debugging
        if form.is_valid():
            otp_code = form.cleaned_data["otp_code"]
            otp_record = OTP.objects.filter(user=user, otp_code=otp_code).last()

            if otp_record and otp_record.is_valid():
                user.is_active = True  # Activate user
                user.save()
                login(request, user)
                messages.success(request, "Account verified successfully!")
                return redirect("login")
            else:
                messages.error(request, "Invalid OTP! Please try again.")
    else:
        form = OTPForm()

    return render(request, "verify_otp.html", {"form": form})


# Login View (Sends OTP)
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            print(f"Trying to authenticate: {email}")  # Debugging
            user = authenticate(request, email=email, password=password)

            if user:
                print(f"Authenticated user: {user}")  # Debugging
                login(request, user)
                return redirect("dashboard")  # Redirect to dashboard after successful login
            else:
                messages.error(request, "Invalid email or password.")
                print("Authentication failed!")  # Debugging

        except Exception as e:
            print(f"Error during authentication: {e}")

    return render(request, "login.html")


# OTP Verification for Login
def login_otp(request):
    user_id = request.session.get("otp_user_id")
    if not user_id:
        return redirect("login")

    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        otp_code = request.POST["otp"]
        stored_otp = cache.get(user.phone_number)

        if not stored_otp or str(stored_otp) != otp_code:
            messages.error(request, "Invalid or expired OTP. Try again!")
            return redirect("login_otp")

        # Login user after OTP verification
        login(request, user)
        del request.session["otp_user_id"]
        messages.success(request, "Login successful!")
        return redirect("dashboard")

    return render(request, "login_otp.html")


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


# Dashboard (Requires Login)
@login_required
def dashboard(request):
    user_type = request.GET.get("user_type")
    return render(request, "dashboard.html", {"user_type": user_type})


# Fetch University Locations
def get_locations(request):
    locations = Location.objects.all().select_related("university")
    data = [
        {
            "id": loc.university.id if loc.university else None,
            "name": loc.name,
            "lat": loc.lat,
            "lon": loc.lon,
            "naac_rating": loc.university.naac_rating if loc.university else None,
            "national_ranking": loc.university.national_ranking if loc.university else None,
            "global_ranking": loc.university.global_ranking if loc.university else None,
            "courses": loc.university.course.split(",") if loc.university and loc.university.course else [],
        }
        for loc in locations
    ]
    return JsonResponse(data, safe=False)


# University Details
def university_detail(request, id):
    university = get_object_or_404(University, id=id)
    return render(request, "university_detail.html", {"university": university})

@login_required
def apply_now(request, university_id):
    university = get_object_or_404(University, id=university_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.university = university
            application.save()

            return redirect('dashboard')  # Redirect after application submission

    else:
        form = ApplicationForm()

    return render(request, 'apply_form.html', {'form': form, 'university': university})


@login_required
def university_dashboard(request):
    if not hasattr(request.user, "university_admin"):
        return render(request, "error.html", {"message": "You are not assigned as an admin for any university."})

    university = request.user.university_admin
    applications = Application.objects.filter(university=university)

    return render(request, "university_dashboard.html", {"university": university, "applications": applications})