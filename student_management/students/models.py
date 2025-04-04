from django.db import models
from django.core.validators import EmailValidator

class Student(models.Model):
    roll_number = models.AutoField(primary_key=True)  # Auto-generated roll number
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])  # Unique email
    age = models.PositiveIntegerField()
    course = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.email})"
