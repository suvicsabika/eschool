from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import PeopleRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render
from .backends import PeopleAuthenticationBackend  # Import your authentication backend
from .models import People

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        entered_email = request.POST.get('username')  # Get the email entered in the form
        password = request.POST.get('password')  # Get the password entered in the form
        user = PeopleAuthenticationBackend()
        founduser = user.authenticate(request, email=entered_email, password=password)
        if founduser is not None:
            login(request, founduser)
            return HttpResponse("Welcome in!")
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'login.html', context)

def register_view(request):
    if request.method == 'POST':
        form = PeopleRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login') + '?registered=True')  # Redirect to a success page
        else:
            print("The form had errors!")
    else:
        form = PeopleRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)

def forgot_view(request):
    if request.method == 'POST':
        student_email = request.POST.get('email')
        token = PeopleAuthenticationBackend.generate_reset_token(student_email)
        try:
            student = People.objects.filter(email=student_email).first()
            if student:
                student.reset_token = token
                forgot_student = PeopleAuthenticationBackend.send_password_reset_email(student)
            else:
                pass
        except People.DoesNotExist:
            pass

    return render(request, 'forgot.html')