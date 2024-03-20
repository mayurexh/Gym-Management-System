from django import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = models.Enquiry
        fields = ('full_name','email','details')

class SignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name","last_name", "email", "username" ,"password1", "password2")

class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name","last_name", "email", "username")
