from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import PeopleRegistrationForm, TeacherCreateCourse, TeacherCreateWork, AssignmentFileForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import CustomUser, Course, Assignment, AssignmentFile
# from .models import People, Course, Assignment, AssignmentFile
from datetime import date
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms import modelformset_factory
from django.contrib.auth.hashers import check_password
from .decorators import teacher_required
from .backends import EmailBackend

def login_view(request):
    if request.method == 'POST':
        print("We are experiencing a POST request!")
        form = LoginForm(request.POST)
        if form.is_valid():
            print("The form is valid! :)")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email, password)
            founduser = authenticate(request, username=email, password=password)
            print(founduser)
            if founduser is not None:
                print("Successfully authenticated")
                login(request, founduser)
                if founduser.role == 'Student':
                    return redirect('main')
                else:
                    return redirect('teacher_main')
            else:
                print("We didn't find the user!")
        else:
            print("The form had errors!")
            print(form.errors)
    else:
        print("We are experiencing a GET request!")
        form = LoginForm()

    context = {'form' : form}
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

@login_required()
def main_view(request):
    logged_in_user = request.user
    enrolled_courses = logged_in_user.courses_enrolled.all()
    assignments = Assignment.objects.filter(course__in=enrolled_courses)
    context = {'name': logged_in_user.last_name + ' ' + logged_in_user.first_name, 'enrolled_courses': enrolled_courses, 'assignments' : assignments}
    return render(request, 'student_main.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@teacher_required
def teacher_main_view(request):
    logged_in_user = request.user
    teacher_courses = Course.objects.filter(teacher=logged_in_user)
    today = date.today()
    future_assignments = Assignment.objects.filter(
        Q(course__in=teacher_courses) & Q(due_date__gte=today)
    )
    context = {'name': logged_in_user.last_name + ' ' + logged_in_user.first_name, 'teacher_courses': teacher_courses, 'assigments': future_assignments}
    return render(request, 'teacher_main.html', context)

@login_required
@teacher_required
def teacher_create_course_view(request):
    logged_in_user = request.user
    created = False
    course_id = None
    print("We got a request! :)")
    if request.method == 'POST':
        form = TeacherCreateCourse(request.POST)
        print("We are experiencing a POST request!")
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            new_course = new_course = Course(title=title, description=description, teacher=logged_in_user)
            new_course.save()
            print("Course created successfully!")
            created = True
            course_id = new_course.course_id
        else:
            print("The form is not valid!")
            print(form.errors)
    else:
        form = TeacherCreateCourse()        
    
    context = {'form' : form, 'name' : logged_in_user.first_name + ' ' + logged_in_user.last_name, 'created' : created, 'course_id' : course_id}
    return render(request, 'teacher_create_course.html', context)

from django.forms import modelformset_factory

@login_required
@teacher_required
def teacher_create_work_view(request):
    logged_in_user = request.user
    teacher_courses = Course.objects.filter(teacher=logged_in_user)
    
    AssignmentFileFormSet = modelformset_factory(AssignmentFile, form=AssignmentFileForm, extra=5)

    if request.method == "POST":
        form = TeacherCreateWork(request.POST)
        file_formset = AssignmentFileFormSet(request.POST, request.FILES, prefix='files')
        
        if form.is_valid() and file_formset.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = logged_in_user
            assignment.save()
            
            for file_form in file_formset:
                if file_form.cleaned_data.get('file_upload'):
                    AssignmentFile.objects.create(assignment=assignment, file_upload=file_form.cleaned_data['file_upload'])
            
            print("Assignment created successfully!")
            #return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = TeacherCreateWork()
        file_formset = AssignmentFileFormSet(queryset=AssignmentFile.objects.none(), prefix='files')

    context = {'form': form, 'file_formset': file_formset, 'name' : logged_in_user.first_name + ' ' + logged_in_user.last_name, 'courses': teacher_courses}
    return render(request, 'teacher_create_work.html', context)



def delete_course(request, course_id):
    if request.method == 'DELETE':
        course = get_object_or_404(Course, pk=course_id)
        course.delete()
        return JsonResponse({'message': 'Course deleted successfully.'}, status=204)
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)


@login_required
def join_course_view(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    logged_in_user = request.user

    # Check if the student is already enrolled in the course
    if logged_in_user in course.students.all():
        return JsonResponse({'success': False})

    # Enroll the student in the course
    course.students.add(logged_in_user)
    return JsonResponse({'success': True})

@login_required
def access_denied(request):
    return render(request, 'access_denied.html')