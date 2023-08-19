from django.contrib import admin
from .models import People, Course, Assignment

# Register your models here.
admin.site.register(People)
admin.site.register(Course)
admin.site.register(Assignment)