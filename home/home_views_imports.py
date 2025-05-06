from django.shortcuts import render, redirect, get_object_or_404 # Import render to render templates, redirect for navigation
from django.contrib import messages  # Import messages for flash messages
from .models import Contact # Import the Recipe model
from django.core.validators import validate_slug
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
#from django.contrib.auth.models import User 
from django.core.mail import send_mail
from django.conf import settings
import logging

from django.urls import reverse  # Import reverse to generate URLs
from django.template.loader import render_to_string  # Import render_to_string for rendering templates to strings




