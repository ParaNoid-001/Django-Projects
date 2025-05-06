from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(
        default='profile_pics/default-profile-pic.jpg',
        upload_to='profile_pics'
    )
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Update timestamp on every save
        if self.pk:
            self.date_updated = timezone.now()
        super().save(*args, **kwargs)
        
        # Only process image if it's not the default
        if self.profile_pic and self.profile_pic.name != 'profile_pics/default.jpg':
            try:
                img = Image.open(self.profile_pic.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_pic.path)
            except Exception as e:
                # Handle potential image processing errors
                print(f"Error processing image: {e}")

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Profile.objects.get_or_create(user=instance)
        instance.profile.save()
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error in profile signal: {e}")