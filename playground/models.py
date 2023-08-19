from django.db import models
import uuid

# Create your models here.
class People(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dateofbirth = models.DateField()
    password = models.CharField(max_length=32)
    username = models.EmailField(max_length=255, unique=True)
    last_login = models.DateTimeField(auto_now=True)  # Add last_login field
    role = models.CharField(max_length=10, choices=[('Student', 'Student'), ('Teacher', 'Teacher')], default='Student')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"
    
class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(People, on_delete=models.CASCADE)
    students = models.ManyToManyField(People, related_name='courses_enrolled')

    def __str__(self):
        return self.title
    
class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    points = models.PositiveIntegerField()
    posted_date = models.DateTimeField(auto_now_add=True)  # Add the posted_date field

    def __str__(self):
        return self.title
