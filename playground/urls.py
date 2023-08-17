from django.urls import path
from . import views

# URLConf, every app can have it's URLConf
# URLs allways and withan /
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot/', views.forgot_view, name='forgot')
]
