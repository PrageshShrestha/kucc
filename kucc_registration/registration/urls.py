# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("" , views.membership_form),
    path('submit_application/', views.submit_application, name='submit_application'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('success/', views.success_page, name='success'),
]