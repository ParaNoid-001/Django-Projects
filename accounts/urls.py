# from django.urls import path
# from .import views
# from .views import *
# from accounts import views
# from .decorators import *
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views

# app_name =  'accounts'  # This creates a namespace for app's URLs

# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('register/', views.register_view, name='register'),
#     #path('logout/', views.logout_view, name='logout'),  # Will be /accounts/logout/
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('profile/', views.profile_view, name='profile'),  # Will be /accounts/profile/
#     path('profile/edit_profile/', views.edit_profile, name='edit_profile'),  # Will be /accounts/profile/edit_profile/
#     path('account/', views.account_management, name='account_management'),
    
#     path('accounts/delete/', AccountDeleteView.as_view(), name='delete_account'),
# #     path('accounts/delete/', 
# #          login_required(views.AccountDeleteView.as_view()), 
# #          name='delete_account'),
    
#     # Password change
#     path('password-change/',
#          login_required(
#              csrf_protect(
#                  sensitive_post_parameters()(
#                      views.CustomPasswordChangeView.as_view()
#                  )
#              )
#          ), name='password_change'),
    
#     path('password-change/done/', 
#          login_required(views.CustomPasswordChangeDoneView.as_view()), 
#          name='password_change_done'),
    
#     # Password reset
#     path('password-reset/',
#          csrf_protect(views.CustomPasswordResetView.as_view()), 
#          name='password_reset'),
    
#     path('password-reset/done/',
#          views.CustomPasswordResetDoneView.as_view(), 
#          name='password_reset_done'),
    
#     path('password-reset-confirm/<uidb64>/<token>/',
#          csrf_protect(
#              sensitive_post_parameters()(
#                  views.CustomPasswordResetConfirmView.as_view()
#              )
#          ), name='password_reset_confirm'),
    
#     path('password-reset-complete/',
#          views.CustomPasswordResetCompleteView.as_view(), 
#          name='password_reset_complete'),
    
#     # Account Deletion URL
#     #path('account/delete/', views.delete_account, name='delete_account'),
    
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# # Only add static files URL pattern in development
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from .views import (
    login_view, 
    register_view, 
    LogoutView, 
    profile_view, 
    edit_profile,
    account_management,
    AccountDeleteView,
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Profile URLs
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('account/', account_management, name='account_management'),
    
    # Account Deletion URL (updated with proper decorators)
    path('delete/',
         login_required(
             csrf_protect(
                 sensitive_post_parameters()(
                     AccountDeleteView.as_view()
                 )
             )
         ), name='delete_account'),
    
    # Password Change URLs
    path('password-change/',
         login_required(
             csrf_protect(
                 sensitive_post_parameters()(
                     CustomPasswordChangeView.as_view()
                 )
             )
         ), name='password_change'),
    
    path('password-change/done/',
         login_required(CustomPasswordChangeDoneView.as_view()),
         name='password_change_done'),
    
    # Password Reset URLs
    path('password-reset/',
         csrf_protect(CustomPasswordResetView.as_view()),
         name='password_reset'),
    
    path('password-reset/done/',
         CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         csrf_protect(
             sensitive_post_parameters()(
                 CustomPasswordResetConfirmView.as_view()
             )
         ), name='password_reset_confirm'),
    
    path('password-reset-complete/',
         CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    
]

# Static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)