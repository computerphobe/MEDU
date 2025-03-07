from django.urls import path
from . import views

urlpatterns = [
    # Authentication Routes
    path("signup/", views.signup_view, name="signup"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("login/", views.login_view, name="login"),
    path("login_otp/", views.login_otp, name="login_otp"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard (Protected)
    path("dashboard/", views.dashboard, name="dashboard"),

    # University & Locations
    path("dashboard/get_locations/", views.get_locations, name="get_locations"),
    path("university/<int:id>/", views.university_detail, name="university_detail"),
    path('apply/<int:university_id>/', views.apply_now, name='apply_now'),
    path('university_dashboard/', views.university_dashboard, name='university_dashboard'),
]
