from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Add this line for dashboard
    path('signup/', views.signup_view, name='signup'),
    path('locations/', views.get_locations, name='get_locations'),
    path('university/', views.university, name='university'),
    path('dashboard/location/', views.location, name='location'),
]
