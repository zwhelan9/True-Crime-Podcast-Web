from atexit import register
from django.urls import path
from . import views
from .views import register

urlpatterns = [
    path('profile/', views.profile, name='profile'),
     path('register/', register, name='register'),
]