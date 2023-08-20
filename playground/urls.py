from django.urls import path
from . import views

# app_name = 'playground'

# URLConf, every app can have it's URLConf
# URLs allways and withan /
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot/', views.forgot_view, name='forgot'),
    path('main/', views.main_view, name='main'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher_main/', views.teacher_main_view, name='teacher_main'),
    path('teacher_create_course/', views.teacher_create_course_view, name='teacher_create_course'),
    path('teacher_create_work/', views.teacher_create_work_view, name='teacher_create_work')
]
