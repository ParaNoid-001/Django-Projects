from django.shortcuts import render, redirect, get_object_or_404 # Import render to render templates, redirect for navigation

from django.forms import Form
from .forms import ProfileUpdateForm, UserUpdateForm  #UserRegistrationForm, UserLoginForm, PasswordResetForm, SetPasswordForm, EmailChangeForm, EmailVerificationForm
from .models import *
from django.urls import reverse  # Import reverse to generate URL
from django.urls import reverse_lazy  # Import reverse_lazy for URL redirection

from django.core.validators import validate_slug , validate_email
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.mail import send_mail  # Import send_mail for sending emails
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives  # Import EmailMultiAlternatives for sending HTML emails

from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string  # Import render_to_string for rendering templates to strings

from django.utils.html import strip_tags  # Import strip_tags to remove HTML tags from strings
from django.conf import settings  # Import settings to access email configuration
from django.http import JsonResponse
import os
import smtplib 
import json

from google.oauth2 import id_token
from google.auth.transport import requests
#.views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # Import class-based views
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")  # Detailed troubleshooting info
logger.info("User logged in")  # Normal operation messages
logger.warning("API response slow")  # Potential issues
logger.error("Payment failed")  # Errors needing investigation
logger.critical("Database down")  # Critical failures

from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin 
from django.contrib import messages
User = get_user_model()

from django.contrib import messages, auth










