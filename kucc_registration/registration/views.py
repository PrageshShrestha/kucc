# myapp/views.py
import csv
import random
import smtplib
from email.mime.text import MIMEText
from django.shortcuts import render
from django.http import JsonResponse
from .models import Student
from .locations import nepal_locations
from django.core.cache import cache

def membership_form(request):
    # Render the registration form HTML
    return render(request, 'test2.html')

def submit_application(request):
    if request.method == 'POST':
        errors = {}
        # ... (rest of your existing submit_application POST logic remains unchanged)
        full_name = request.POST.get('full_name')
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        faculty = request.POST.get('faculty')
        batch_year = request.POST.get('batch_year')
        major = request.POST.get('major')
        skills = request.POST.get('skills')
        why_join = request.POST.get('why_join')
        province = request.POST.get('province')
        district = request.POST.get('district')
        municipality = request.POST.get('municipality')
        consent = request.POST.get('consent') == 'on'

        if not full_name:
            errors['full_name'] = 'Full name is required.'
        # ... (other validations)
        
        if Student.objects.filter(email=email).exists():
            errors['email'] = 'Email already registered.'
        if Student.objects.filter(student_id=student_id).exists():
            errors['student_id'] = 'Student ID already registered.'
        if Student.objects.filter(phone=phone).exists():
            errors['phone'] = 'Phone number already registered.'

        try:
            with open('email_list.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row and row[0] == email:
                        errors['email'] = 'Email found in existing list.'
                        break
        except FileNotFoundError:
            pass

        if errors:
            return JsonResponse({'errors': errors}, status=400)

        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        cache.set(f'otp_{email}', otp, timeout=300)
        sender_email = 'binormus007@gmail.com'
        sender_password = "gzmljziqphfqnflw"
       
        subject = "Your OTP for Club Membership Verification"
        body = f"Dear {full_name},\n\nYour One-Time Password (OTP) for joining the Computer Club is: **{otp}**. Please enter this code on the verification page to complete your registration. This OTP is valid for 5 minutes.\n\nRegards,\nComputer Club Team"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = email

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
        except Exception as e:
            return JsonResponse({'errors': {'email': f'Failed to send OTP: {str(e)}'}}, status=500)

        request.session['form_data'] = request.POST.dict()
        return JsonResponse({'message': 'OTP sent to your email.', 'redirect': '/verify_otp/'}, status=200)

    elif request.method == 'GET':
        province = request.GET.get('province')
        district = request.GET.get('district')

        if province and district:
            return JsonResponse({province: {district: nepal_locations[province][district]}})
        elif province:
            return JsonResponse({province: nepal_locations[province]})
        else:
            return JsonResponse(nepal_locations)

    return JsonResponse({'message': 'Invalid request.'}, status=400)

def verify_otp(request):
    # ... (unchanged verify_otp logic)
    if request.method == 'POST':
        email = request.session.get('form_data', {}).get('email')
        user_otp = request.POST.get('otp')
        stored_otp = cache.get(f'otp_{email}')

        if not stored_otp:
            return JsonResponse({'errors': {'otp': 'OTP expired or invalid. Please try again.'}, 'redirect': '/membership/'}, status=400)

        if user_otp == stored_otp:
            form_data = request.session.get('form_data', {})
            Student.objects.create(
                full_name=form_data['full_name'],
                student_id=form_data['student_id'],
                email=form_data['email'],
                phone=form_data['phone'],
                gender=form_data['gender'],
                faculty=form_data['faculty'],
                batch_year=form_data['batch_year'],
                major=form_data['major'],
                skills=form_data['skills'],
                why_join=form_data['why_join'],
                province=form_data['province'],
                district=form_data['district'],
                municipality=form_data['municipality'],
                consent=form_data['consent'] == 'on'
            )
            cache.delete(f'otp_{email}')
            del request.session['form_data']
            return JsonResponse({'message': 'OTP verified successfully!', 'redirect': '/success/'}, status=200)
        else:
            return JsonResponse({'errors': {'otp': 'Incorrect OTP. Please try again.'}, 'redirect': ''}, status=400)

    return render(request, 'verify_otp.html')

def success_page(request):
    return render(request, 'success.html')