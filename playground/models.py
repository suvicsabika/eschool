from django.db import models

# Create your models here.
class People(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dateofbirth = models.DateField()
    password = models.CharField(max_length=32)
    email = models.EmailField(max_length=255, unique=True)
    last_login = models.DateTimeField(auto_now=True)  # Add last_login field
    role = models.CharField(max_length=10, choices=[('Student', 'Student'), ('Teacher', 'Teacher')], default='Student')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"