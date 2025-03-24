from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    student_id = models.CharField(max_length=20)
    reg_no = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    batch_year = models.IntegerField()
    country_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=20)
    interests = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
