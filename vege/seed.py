
# def generate_fake_users(num: int) -> List[Dict[str, Any]]:
#     users = []
#     for _ in range(num):
#         user = {
#             'username': fake.user_name(),
#             'email': fake.email(),
#             'password': fake.password(),
#             'first_name': fake.first_name(),
#             'last_name': fake.last_name(),
#             'is_staff': choice([True, False]),
#             'is_active': choice([True, False]),
#         }
#         users.append(user)
#     return users

from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Recipe
import logging

logger = logging.getLogger(__name__)
fake = Faker()

def seed_db(n=10, clear_existing=False):
    """Seed database with recipes, with proper error handling"""
    try:
        User = get_user_model()
        
        if clear_existing:
            Recipe.objects.all().delete()
            logger.info("Cleared existing recipes")
        
        # Ensure at least one user exists
        if not User.objects.exists():
            logger.warning("No users found - creating test user")
            User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
        
        for i in range(1, n+1):
            try:
                recipe = create_recipe(User)
                logger.info(f"Created recipe {i}/{n}: {recipe.Recipe_name}")
            except Exception as e:
                logger.error(f"Failed recipe {i}: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"Seeding failed: {str(e)}")
    finally:
        logger.info(f"Completed seeding {Recipe.objects.count()}/{n} recipes")

def create_recipe(User):
    """Create a single recipe with valid timestamps"""
    # Get random user
    user = User.objects.order_by('?').first()
    
    # Generate valid timestamps
    created_at = fake.date_time_between(
        start_date='-1y', 
        end_date='now',
        tzinfo=timezone.get_current_timezone()
    )
    updated_at = fake.date_time_between(
        start_date=created_at,
        end_date='now',
        tzinfo=timezone.get_current_timezone()
    )
    
    # Create and save recipe
    return Recipe.objects.create(
        Recipe_name=fake.unique.sentence(nb_words=3).rstrip('.'),
        Recipe_description=fake.paragraph(nb_sentences=3),
        Recipe_image=fake.image_url(width=800, height=600),
        created_at=created_at,
        created_by=user,
        updated_at=updated_at
    )

# Example usage:
if __name__ == "__main__":
    import django
    django.setup()
    seed_db(n=20, clear_existing=True)




