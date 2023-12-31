from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
# from .models import People, Course, Assignment, AssignmentFile
from .models import CustomUser, Course, Assignment, AssignmentFile
from django.contrib.auth.hashers import make_password


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class PeopleRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'password', 'password_again']
        
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
    
class TeacherCreateCourse(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField()

    class Meta:
        model = Course
        fields = ['title', 'description']
        
        
class TeacherCreateWork(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    course = forms.Select()
    due_date = forms.DateField()
    points = forms.NumberInput()
    file_upload = forms.FileField(allow_empty_file=True, required=False)
    
    class Meta:
        model = Assignment
        fields = ['course', 'due_date', 'points', 'title', 'description', 'file_upload']
        
class AssignmentFileForm(forms.ModelForm):
    class Meta:
        model = AssignmentFile
        fields = ['file_upload']
