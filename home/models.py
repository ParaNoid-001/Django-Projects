from django.db import models  # Import Django's models module
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import validate_email

# class Student(models.Model):
#     #id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     email = models.EmailField(null=True, blank=True)
#     address = models.TextField(null=True, blank=True)
#     image = models.ImageField(null=True, blank=True)
#     file = models.FileField(null=True, blank=True)
    

    
    
# class Car(models.Model):
#     car_name = models.CharField(max_length=100)
#     speed = models.IntegerField(default=50)
    
#     def __str__(self) -> str:
#         return self.car_name
    


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)

    email = models.EmailField(validators=[validate_email])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['created_at']

    def __str__(self):
        return self.name
