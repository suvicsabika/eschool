from django.contrib import admin
# from .models import People, Course, Assignment
from .models import CustomUser, Course, Assignment, AssignmentFile
# Register your models here.
# admin.site.register(People)
admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(AssignmentFile)