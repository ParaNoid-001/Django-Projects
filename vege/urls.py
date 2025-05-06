from django.urls import path
from .import views

app_name = 'vege'  # This creates a namespace for app's URLs

urlpatterns = [
    
    # Home/Add Recipe
    path('', views.recipes, name='recipes'),  # Will be /recipes/
    path('add/', views.add_recipe, name='add_recipe'),
    
    # Dashboard
    path('recipe_dashboard/', views.recipe_dashboard, name='recipe_dashboard'),  # Will be /recipes/dashboard/
    
    # Recipe Operations
    path('delete-recipe/<int:id>/', views.delete_recipe, name='delete_recipe'),
    path('update-recipe/<int:id>/', views.update_recipe, name='update_recipe'),
    #path('bulk-delete/', views.bulk_delete_recipes, name='bulk_delete'),
    
    # Recipe Views
    path('recipe-gallery/', views.recipe_gallery, name='recipe_gallery'),
    path('recipe-detail/<int:id>/', views.recipe_detail, name='recipe_detail'),
    
    # path('login/', views.login_view, name='login'),  # Will be /recipes/login/
    # path('logout/', views.logout_view, name='logout'),  # Will be /recipes/logout/
    # path('register/', views.register_view, name='register'),  # Will be /recipes/register/  
    #path('auth/google/', views.google_auth, name='google_auth'),
    
    #path('test-email/', views.test_email, name='test-email'),
    
    
    
    
    
    
    
    
     
]
