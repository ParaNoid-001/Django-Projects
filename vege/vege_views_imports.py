from django.shortcuts import render, redirect, get_object_or_404 # Import render to render templates, redirect for navigation
from django.contrib import messages  # Import messages for flash messages
import logging

from .models import Recipe # Import the Recipe model
from django.urls import reverse_lazy  # Import reverse_lazy for URL redirection
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # Import class-based views

from django.core.validators import validate_slug
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User  # Import User model for user-related functionalities
from django.core.mail import send_mail  # Import send_mail for sending emails
from django.template.loader import render_to_string  # Import render_to_string for rendering templates to strings
from django.utils.html import strip_tags  # Import strip_tags to remove HTML tags from strings
from django.conf import settings  # Import settings to access email configuration
from django.urls import reverse  # Import reverse to generate URLs
import os
from django.core.mail import EmailMessage
import smtplib 
from django.template.exceptions import TemplateDoesNotExist
from django.contrib.auth.decorators import login_required  # Import login_required to protect views

import json
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings  # Import settings to access Google Client ID
