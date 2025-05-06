from .accounts_views_imports import *
from .decorators import *


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('vege:recipes')  # Redirect to home page after login
        else:
            # Return error message
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'accounts/login.html')



@csrf_exempt
@never_cache
def register_view(request):
    if request.method == 'POST':
        
        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, "Username already exists")
            return redirect('accounts:register')
        
        if User.objects.filter(email=request.POST.get('email')).exists():
            messages.error(request, "Email already registered")
            return redirect('accounts:register')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=request.POST.get('password1'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
            )

            # Update the auto-created profile
            profile = user.profile
            profile.bio = request.POST.get('bio', '')
            profile.location = request.POST.get('location', '')
            profile.birth_date = request.POST.get('birth_date')
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            # Send welcome email
            try:
                subject = "Welcome to Our Website!"
                message = render_to_string('accounts/welcome_email.html', {
                    'user': user,
                    'domain': request.get_host(),
                })
                
                send_mail(
                    subject=subject,
                    message='',  # Plain text fallback (empty as we're using html_message)
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=message,
                    fail_silently=False,
                )
                messages.success(request, "Registration successful! Please check your email for a welcome message.")
            except Exception as e:
                logger.error(f"Email error: {e}")
                messages.warning(request, "Account created but welcome email failed")

            return redirect('accounts:login')

        except Exception as e:
            logger.error(f"Registration error: {e}")
            messages.error(request, f"Registration failed: {e}")
            return redirect('accounts:register')

    return render(request, 'accounts/register.html')

# @csrf_exempt
# @never_cache
# def register_view(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         password = request.POST.get('password1')
#         email = request.POST.get('email')
#         location = request.POST.get('location')
#         bio = request.POST.get('bio')
#         birth_date = request.POST.get('birth_date')
#         profile_pic = request.FILES.get('profile_pic')
        
#         # Check if username exists
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect('accounts:register')
        
#         # Check if email exists
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered")
#             return redirect('accounts:register')
        
#         try:
#             # Create user
#             user = User.objects.create_user(
#                 first_name=first_name,
#                 last_name=last_name,
#                 username=username,
#                 email=email,
#                 location=location,
#                 bio=bio,
#                 birth_date=birth_date,
#                 profile_pic=profile_pic
                
#             )
#             user.set_password(password)
#             user.save()
            
#             # Try to send email in a separate try-except block
#             try:
#                 subject = "Welcome to Our Website!"
#                 message = render_to_string('accounts/welcome_email.html', {
#                     'user': user,
#                     'domain': request.get_host(),
#                 })
                
#                 send_mail(
#                     subject=subject,
#                     message='',  # Plain text fallback (empty as we're using html_message)
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=[user.email],
#                     html_message=message,
#                     fail_silently=False,
#                 )
#                 messages.success(request, "Registration successful! Please check your email for a welcome message.")
#             except Exception as e:
#                 # Log the error for debugging
#                 logger.error(
#                     "Failed to send welcome email to %s. Error: %s",
#                     user.email,
#                     str(e),
#                     exc_info=True  # Includes stack trace
#                 )
                
#                 messages.warning(request, "Account created! Welcome email could not be sent.")
            
#             return redirect('accounts:register')
            
#         except ValidationError as e:
#             messages.error(request, f"Validation error: {str(e)}")
#             return redirect('accounts:register')
            
#         except Exception as e:
#             logger.critical(
#                 "Registration failed for %s: %s", 
#                 request.POST.get('email', 'no-email'),
#                 str(e),
#                 exc_info=True
#             )
#             messages.error(request, f"An error occurred during registration: {str(e)}")
#             return redirect('accounts:register')
    
#     return render(request, 'accounts/register.html', {'page': 'register'})



class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/logout.html'
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')


@login_required
def account_management(request):
    return render(request, 'accounts/account_management.html')


@login_required
def profile_view(request):
    """View for displaying the user's profile"""
    return render(request, 'accounts/profile.html', {'user': request.user, 'page': 'profile'})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
        else:
            # Forms are invalid - you might want to see errors
            print(user_form.errors, profile_form.errors)
            
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/edit_profile.html', context)


# @login_required
# def delete_account(request):
#     if request.method == 'POST':
#         # Send confirmation email
#         subject = 'Your account has been deleted'
#         html_message = render_to_string('accounts/account_deleted_email.html', {
#             'user': request.user,
#         })
#         plain_message = strip_tags(html_message)
#         from_email = settings.DEFAULT_FROM_EMAIL
#         to_email = request.user.email
        
#         # Delete user account
#         user = request.user
#         logout(request)
#         user.delete()
        
#         # Send email (use try-except in production)
#         send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
        
#         messages.success(request, 'Your account has been permanently deleted.')
#         return redirect('home')  # Replace 'home' with your homepage URL
    
#     return render(request, 'accounts/delete_account.html')


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/account_delete.html'
    success_url = reverse_lazy('accounts:login')
    form_class = Form
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user_email = user.email
        
        # Verify password
        password = request.POST.get('password')
        if password and not user.check_password(password):
            messages.error(request, "Incorrect password. Account not deleted.")
            return redirect('accounts:delete_account')
        
        try:
            # Send email before deletion
            self.send_deletion_email(user, user_email)
        except Exception as e:
            logger.error(f"Failed to send deletion email: {str(e)}")
            # Continue with deletion even if email fails
        
        # Logout user
        from django.contrib.auth import logout
        logout(request)
        
        # Perform deletion
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Your account has been deleted successfully.")
        return response
    
    def send_deletion_email(self, user, user_email):
        subject = "Account Deletion Confirmation"
        message = render_to_string('accounts/account_deletion_email.html', {
            'user': user,
            'domain': get_current_site(self.request).domain,
        })
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send account deletion email: {str(e)}")


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password/password_change_done.html'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password/password_reset.html'
    email_template_name = 'accounts/password/password_reset_email.html'
    subject_template_name = 'accounts/password/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    token_generator = default_token_generator
    
    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': 'accounts/password/password_reset_email.html',
            'extra_email_context': {
                'domain': get_current_site(self.request).domain,
                'protocol': 'https' if self.request.is_secure() else 'http',
            }
        }
        form.save(**opts)
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password/password_reset_complete.html'
