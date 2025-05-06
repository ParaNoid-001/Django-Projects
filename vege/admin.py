
from django.contrib import admin
from .models import Recipe, Category
from django.utils.html import format_html

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'Recipe_name', 'truncated_description', 'image_preview', 'created_at', 'created_by', 'updated_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('Recipe_name',)
    readonly_fields = ('image_preview',)  # Makes the image display in edit view
    
    def truncated_description(self, obj):
        return obj.Recipe_description[:50] + '...' if len(obj.Recipe_description) > 50 else obj.Recipe_description
    truncated_description.short_description = 'Description'
    
    def image_preview(self, obj):
        if obj.Recipe_image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;"/>', obj.Recipe_image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

admin.site.register(Recipe, RecipeAdmin)

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )
    
