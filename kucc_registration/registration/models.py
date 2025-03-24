# myapp/models.py
from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)  # Combining country_code and phone_number
    gender = models.CharField(max_length=20, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('PreferNotToSay', 'Prefer not to say')
    ])
    faculty = models.CharField(max_length=50)
    batch_year = models.CharField(max_length=4)  # e.g., "2023"
    major = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    why_join = models.TextField()
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    municipality = models.CharField(max_length=100)
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name