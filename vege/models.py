from django.db import models  # Import Django's models module
from django.utils import timezone
from django.contrib.auth.models import User  # Import User model for user-related functionalities
from django.core.validators import FileExtensionValidator

# Recipe Model to store recipes in the database
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to link each recipe to a user # This field creates a many-to-one relationship with the User model. If a user is deleted, all their recipes will also be deleted.

    Recipe_name = models.CharField(max_length=255)  # Field to store the recipe name (max 255 characters)
    Recipe_description = models.TextField(
        verbose_name="Description",help_text="Detailed recipe description")  # Field to store the recipe description (unlimited text)
    
    Recipe_image = models.ImageField(upload_to="recipes/", validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name="Image",
        help_text="Upload recipe image (JPEG or PNG)")  # Field to upload and store images inside "public/static/recipes/"
    serial_number = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='recipes_created')  # Foreign key to link each recipe to the user who created it
    updated_at = models.DateTimeField(auto_now=True)  # Field to store the last updated time of the recipe
    catagory = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)  # Foreign key to link each recipe to a category


    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ['-created_at']
        permissions = [
            ("can_add_recipe", "Can add recipes through web interface"),
            ("can_edit_recipe", "Can edit existing recipes"),
            ("can_delete_recipe", "Can delete recipes"),
        ]

    def __str__(self):
        return self.Recipe_name

    def clean(self):
        
        from django.core.exceptions import ValidationError
        if not self.Recipe_name.replace(' ', '').isalpha():
            raise ValidationError({
                'Recipe_name': "Recipe name should only contain letters and spaces"
            })
            
    def save(self, *args, **kwargs):
        if not self.serial_number:  # only assign serial_number when it's not set
            last_sn = Recipe.objects.all().order_by('-serial_number').first()
            self.serial_number = last_sn.serial_number + 1 if last_sn else 1
        super().save(*args, **kwargs)
        

# Category Model to categorize recipes
class Category(models.Model):
    name = models.CharField(max_length=100)  # Field to store the category name (max 100 characters)
    created_at = models.DateTimeField(auto_now_add=True)  # Field to store the creation time of the category

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name