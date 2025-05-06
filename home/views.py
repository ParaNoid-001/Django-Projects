# from django.shortcuts import render, redirect, get_object_or_404 # Import render to render templates, redirect for navigation
# from django.contrib import messages  # Import messages for flash messages
# from .models import Contact # Import the Recipe model
# from django.core.validators import validate_slug
# from django.core.exceptions import ValidationError
# from django.http import JsonResponse, HttpResponse
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login, authenticate, logout
# #from django.contrib.auth.models import User 
# from django.core.mail import send_mail
# from django.conf import settings
# import logging

# views.py
from .home_views_imports import *

# def home(request):
#     peoples = [
#         {'name': 'Abhijeet Gupta', 'age': 25},
#         {'name': 'Aman Dip', 'age': 20},  # Added a comma here
#         {'name': 'Sohail Khan', 'age': 27},
#         {'name': 'Sree Ram', 'age': 21}
#     ]
    
#     vegetables = ['pumkin', 'tomato', 'potato']
    
    
#     return render(request, "home/index.html", context={'page' : 'Django Tutorial', 'peoples': peoples, 'vegetables':vegetables})


def about(request):
    context = {'page' : 'about'} 
    return render(request, "home/about.html", context)

def success_page(request):
    print("*" * 10)
    return HttpResponse("<h1>Hey, this is a success page</h1>")

# def contact_view(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         message = request.POST.get("message")

#         # Save to database (optional)
#         Contact.objects.create(name=name, email=email, message=message)

#         messages.success(request, "Thank you for contacting us!")
#         return redirect('home:contact_view')

#     return render(request, "home/contact.html")


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Save to database
        Contact.objects.create(name=name, email=email, phone=phone, message=message)
        
        errors = []
        if not name:
            errors.append("Name is required.")
        if not email:
            errors.append("Email is required.")
        elif "@" not in email:  # Very basic email check
            errors.append("Enter a valid email address.")
        if not message:
            errors.append("Message is required.")


        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return redirect('home:contact_view')
        
        # Send email to owner
        subject = f"New Contact Form Submission from {name}"
        full_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:\n{message}"
        send_mail(
            subject,
            full_message,
            email,  # from email (sender)
            [settings.CONTACT_FORM_RECIPIENT],  # recipient list
            fail_silently=False,
        )

        messages.success(request, "Thank you for contacting us!")
        return redirect('home:contact_view')

    return render(request, "home/contact.html", {'page' : 'contact'})

logger = logging.getLogger(__name__)

