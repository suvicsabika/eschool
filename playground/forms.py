from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from .models import People
from django.contrib.auth.hashers import make_password

class PeopleRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = People
        fields = ['first_name', 'last_name', 'dateofbirth', 'email', 'password', 'password_again']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')

        if password and password_again and password != password_again:
            raise ValidationError("Passwords do not match. Please enter the same password in both fields.")
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get('password')
        instance.password = make_password(password)  # Hash the password
        if commit:
            instance.save()
        return instance