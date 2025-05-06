from django.contrib import admin

# Register your models here.
from .models import Contact
from django.utils.html import format_html

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email')

    def message_preview(self, obj):
        return format_html(
            '<span style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{}</span>', obj.message)
    message_preview.short_description = 'Message Preview'
    
admin.site.register(Contact, ContactAdmin)