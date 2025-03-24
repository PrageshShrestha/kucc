# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit_application/', views.submit_application, name='submit_application'),
    path('success/', views.success_page, name='success_page'),
]