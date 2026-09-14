from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),
]
