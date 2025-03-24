import csv
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Student

def submit_application(request):
    if request.method == 'POST':
        errors = {}

        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        student_id = request.POST.get('studentId')
        reg_no = request.POST.get('regNo')
        department = request.POST.get('department')
        location = request.POST.get('location')
        batch_year = request.POST.get('batchYear')
        country_code = request.POST.get('countryCode')
        phone_number = request.POST.get('phoneNumber')
        interests = request.POST.get('interests')

        if not first_name:
            errors['firstName'] = 'First name is required.'
        if not last_name:
            errors['lastName'] = 'Last name is required.'
        if not email:
            errors['email'] = 'Email is required.'
        elif '@' not in email:
            errors['email'] = "Invalid Email."
        if not student_id:
            errors['studentId'] = 'Student ID is required.'
        if not reg_no:
            errors['regNo'] = 'Registration number is required.'
        if not department:
            errors['department'] = 'Department is required.'
        if not location:
            errors['location'] = 'Location is required.'
        if not batch_year:
            errors['batchYear'] = 'Batch year is required.'
        if not country_code:
            errors['countryCode'] = 'Country code is required.'
        if not phone_number:
            errors['phoneNumber'] = 'Phone number is required.'
        if not interests:
            errors['interests'] = 'Interests are required.'

        # Check for duplicate email in database
        if Student.objects.filter(email=email).exists():
            errors['email'] = 'Email already registered.'

        # Check for duplicate email in CSV
        try:
            with open('email_list.csv', 'r') as csvfile:  # Replace with your CSV file path
                reader = csv.reader(csvfile)
                for row in reader:
                    if row and row[0] == email:  # Assuming email is in the first column
                        errors['email'] = 'Email found in existing list.'
                        break
        except FileNotFoundError:
            pass  # If the CSV doesn't exist, skip the check

        if errors:
            return JsonResponse({'errors': errors}, status=400)

        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            student_id=student_id,
            reg_no=reg_no,
            department=department,
            location=location,
            batch_year=batch_year,
            country_code=country_code,
            phone_number=phone_number,
            interests=interests,
        )

        return JsonResponse({'message': 'Application submitted successfully!'}, status=200)

    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)

def success_page(request):
    return render(request, 'success.html')