from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Application

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'})
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

class OTPForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter OTP'})
    )

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['course', 'statement_of_purpose']
