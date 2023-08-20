from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import PeopleRegistrationForm, TeacherCreateCourse, TeacherCreateWork
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .backends import PeopleAuthenticationBackend  # Import your authentication backend
from .models import People, Course, Assignment
from datetime import date
from django.db.models import Q

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        entered_email = request.POST.get('username')  # Get the email entered in the form
        password = request.POST.get('password')  # Get the password entered in the form
        user = PeopleAuthenticationBackend()
        founduser = user.authenticate(request, username=entered_email, password=password)
        if founduser is not None:
            login(request, founduser)
            if founduser.role == 'Student':
                return redirect('main')
            else:
                return redirect('teacher_main')
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

#@login_required(login_url='/playground/login/')
def main_view(request):
    user = People.objects.get(username="kerybalint@gmail.com")#TODO...
    enrolled_courses = user.courses_enrolled.all()
    assignments = Assignment.objects.filter(course__in=enrolled_courses)
    context = {'name': user.last_name + ' ' + user.first_name, 'enrolled_courses': enrolled_courses, 'assignments' : assignments}
    return render(request, 'student_main.html', context)

#@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

#@login_required
def teacher_main_view(request):
    teacher = People.objects.get(username="tester1@gmail.com")#TODO...
    teacher_courses = Course.objects.filter(teacher=teacher)
    today = date.today()
    future_assignments = Assignment.objects.filter(
        Q(course__in=teacher_courses) & Q(due_date__gte=today)
    )
    context = {'name': teacher.last_name + ' ' + teacher.first_name, 'teacher_courses': teacher_courses, 'assigments': future_assignments}
    return render(request, 'teacher_main.html', context)

#@login_required
def teacher_create_course_view(request):
    teacher = People.objects.get(username="tester1@gmail.com")#TODO...
    created = False
    course_id = None
    print("We got a request! :)")
    if request.method == 'POST':
        form = TeacherCreateCourse(request.POST)
        print("We are experiencing a POST request!")
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            new_course = new_course = Course(title=title, description=description, teacher=teacher)
            new_course.save()
            print("Course created successfully!")
            created = True
            course_id = new_course.course_id
        else:
            print("The form is not valid!")
            print(form.errors)
    else:
        form = TeacherCreateCourse()        
    
    context = {'form' : form, 'name' : teacher.first_name + ' ' + teacher.last_name, 'created' : created, 'course_id' : course_id}
    return render(request, 'teacher_create_course.html', context)

#@login_required
#TODO: THe course's ID needed in the form, not the course's title, the ForgeinKey is an ID!
def teacher_create_work_view(request):
    print("We got a request! :)")
    teacher = People.objects.get(username="tester1@gmail.com")#TODO...
    teacher_courses = Course.objects.filter(teacher=teacher)
    if request.method == "POST":
        print("We are experiencing a POST request!")
        form = TeacherCreateWork(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            due_date = form.cleaned_data["due_date"]
            points = form.cleaned_data["points"]
            course = form.cleaned_data["course"]
            new_assigment = Assignment(course=course, assignment=assignment, points=points, description=description, due_date=due_date)
            new_assigment.save()
            print("Assignment created successfully!")
        else:
            print(form.errors)
            print("The form is not valid!")
    else:
        form = TeacherCreateWork()
        
    context = {'form': form, 'name' : teacher.last_name + ' ' + teacher.first_name, 'courses': teacher_courses}
    return render(request, 'teacher_create_work.html', context)
