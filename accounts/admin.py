from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# If using custom User model
from .models import *

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
# admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio_short', 'location')
    list_select_related = ('user',)
    
    def bio_short(self, obj):
        return obj.bio[:50] + '...' if len(obj.bio) > 50 else obj.bio
    bio_short.short_description = 'Bio'