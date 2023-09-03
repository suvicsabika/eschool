from django.db import models
import uuid

# class People(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     dateofbirth = models.DateField()
#     password = models.CharField(max_length=32)
#     username = models.EmailField(max_length=255, unique=True)
#     last_login = models.DateTimeField(auto_now=True)
#     role = models.CharField(max_length=10, choices=[('Student', 'Student'), ('Teacher', 'Teacher')], default='Student')

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} - {self.role}"
    
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create and save a user with the given email and password
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create and save a superuser with the given email and password
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    # Add other fields specific to your application
    role = models.CharField(max_length=10, choices=[('Student', 'Student'), ('Teacher', 'Teacher')], default='Student')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']
    
    
class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    students = models.ManyToManyField(CustomUser, related_name='courses_enrolled')

    def __str__(self):
        return self.title
    
class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    points = models.PositiveIntegerField()
    posted_date = models.DateTimeField(auto_now_add=True)
    file_upload = models.ManyToManyField('AssignmentFile', related_name='assignments')


    def __str__(self):
        return self.title

class AssignmentFile(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file_upload = models.FileField(upload_to='assignment_files/')

    def _str__(self):
        return self.assignment + " files!"
