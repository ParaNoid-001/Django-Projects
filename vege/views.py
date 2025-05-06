# Import necessary modules and functions
from .vege_views_imports import *
from .decorators import *

logger = logging.getLogger(__name__)
logger.debug("Debug message")  # Detailed troubleshooting info
logger.info("User logged in")  # Normal operation messages
logger.warning("API response slow")  # Potential issues
logger.error("Payment failed")  # Errors needing investigation
logger.critical("Database down")  # Critical failures



@login_required(login_url='accounts:login')
@permission_required('vege.can_add_recipe', raise_exception=True)
def add_recipe(request):
    if request.method == "POST":
        try:
            # Validate required fields
            recipe_name = request.POST['recipe_name']
            recipe_description = request.POST['recipe_description']
            recipe_image = request.FILES['recipe_image']
            
            # Validate recipe name format
            validate_slug(recipe_name.replace(' ', '-'))
            
            # Create recipe
            Recipe.objects.create(
                Recipe_name=recipe_name,
                Recipe_description=recipe_description,
                Recipe_image=recipe_image,
                created_by=request.user
            )
            
            messages.success(request, "Recipe added successfully!")
            return redirect('vege:recipes')
            
        except KeyError as e:
            messages.error(request, f"Missing required field: {str(e)}")
        except ValidationError:
            messages.error(request, "Recipe name can only contain letters and spaces")
        except Exception as e:
            messages.error(request, f"Error adding recipe: {str(e)}")
    
    return render(request, 'vege/add_recipe.html', {'page': 'Add Recipe'})


def recipes(request):
    recent_recipes = Recipe.objects.all().order_by('-id', '-created_at')[:5]
    context = {
        'page': 'Recipes',
        'recipes': recent_recipes
    }
    return render(request, 'vege/recipe.html', context)

# View to update an existing recipe

def update_recipe(request, id):  # sourcery skip: extract-method
    recipe = get_object_or_404(Recipe, id=id)  # Get the recipe or 404 if not found

    if request.method == "POST":
        # Update recipe fields from form data
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        
         # Update recipe fields
        recipe.Recipe_name = recipe_name
        recipe.Recipe_description = recipe_description
        
        # If a new image is uploaded, update it
        if request.FILES.get('recipe_image'):
            recipe.Recipe_image = request.FILES.get('recipe_image')

        recipe.save()  # Save updated data
        messages.success(request, "Recipe updated successfully!")  # Flash success message
        return redirect('vege:recipe_gallery')
    
    return render(request, 'vege/update_recipe.html', {'page' : 'update recipe', 'recipe': recipe})


def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)# Fetch recipe or show 404 if not found
    if request.method == 'POST':
        recipe.delete()# Delete the recipe from the database
        messages.success(request, "Recipe deleted successfully!")# Flash success message
        return redirect('vege:recipe_dashboard')
    return redirect('vege:recipe_detail', id=id)# Redirect back to recipe list


# View to show all recipes in a gallery format
def recipe_gallery(request):
    
    search_query = request.GET.get('search', '')
        # Filter recipes based on search query (case-insensitive)
    if search_query:
        recipes = Recipe.objects.filter(Recipe_name__icontains=search_query)
    else:
        recipes = Recipe.objects.all()
    #recipes = Recipe.objects.all()  # Get all recipes
    return render(request, 'vege/recipe-gallery.html', {'page' : 'recipe gallery', 'recipes': recipes})


@login_required(login_url='accounts:login')
def recipe_detail(request, id):  # View to show details of a specific recipe
    recipe = get_object_or_404(Recipe, id=id)  # Get one recipe or 404
    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        # Handle missing recipe gracefully
        return render(request, '404.html', status=404)
    
    return render(request, 'vege/recipe-detail.html', {'page' : 'recipe detail','recipe': recipe})


def recipe_dashboard(request): # View function to display the recipe dashboard and handle bulk delete
    # Check if the request is a POST request (usually a form submission)

    if request.method == 'POST':
        # Check if the 'bulk_delete' button was clicked in the form
        if 'bulk_delete' in request.POST:
            # Get the list of recipe IDs selected for deletion from the form data
            recipe_ids = request.POST.getlist('recipe_ids')
            
            # Delete all recipes whose IDs are in the list
            Recipe.objects.filter(id__in=recipe_ids).delete()
            
            # Show a success message indicating how many recipes were deleted
            messages.success(request, f"{len(recipe_ids)} recipes deleted successfully!")
            
            # Redirect the user back to the recipe dashboard after deletion
            return redirect('vege:recipe_dashboard')
    
    # For GET requests (or after deletion), retrieve all recipes ordered by newest first
    recipes = Recipe.objects.all().order_by('-id')
    
    # Render the dashboard template and pass the recipes to the context
    return render(request, 'vege/recipe_dashboard.html', {'page' : 'recipe dashboard','recipes': recipes})

# @AuthenticationForm
# def login_view(request):
#     logger.debug("Login page accessed")
#     logger.info(f"User {request.user} logged in")
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         if not User.objects.filter(username=username).exists():
#             messages.error(request, "Invalid username")
#             return redirect('vege:login')
        
#         user = authenticate(request, username=username, password=password)
        
#         if user is None:
#           messages.error(request, "Invalid username or password")
#           return redirect('vege:login')
#         else:
#             login(request, user)
#             messages.success(request, "Logged in successfully!")
#             return redirect('vege:recipes')  # Redirect to home page after login
        
#     return render(request, 'vege/login.html', {'page' : 'login', 'form': AuthenticationForm()})      
   

# def register_view(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         password = request.POST.get('password1')  # Changed to match form field name
#         email = request.POST.get('email')
        
#         # Check if the username already exists
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect('vege:register')
        
#         # Check if email already exists
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered")
#             return redirect('vege:register')
        
#         try:
#             # Create a new user
#             user = User.objects.create_user(
#                 first_name=first_name, 
#                 last_name=last_name, 
#                 username=username, 
#                 email=email 
#             )
#             user.set_password(password)  # Set the password
#             user.save()
            
            
#             # Send welcome email
#             subject = "Welcome to Our Website!"
#             message = render_to_string('vege/emails/welcome_email.html', {
#                 'user': user,
#                 'domain': request.get_host(),
#             })
            
#             send_mail(
#                 subject=subject,
#                 message='', 
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[user.email],
#                 html_message=message,
#                 fail_silently=False,
#             )
            
#             messages.success(request, "Registration successful! Please check your email for a welcome message.")
#             return redirect('vege:login')
        
#         except Exception as e:
#                 if settings.DEBUG:
#                     print(f"Email sending failed: {str(e)}")
#                 messages.warning(request, "Account created! Welcome email could not be sent.")
        
#         except ValidationError as e:
#             messages.error(request, f"Validation error: {str(e)}")
#             return redirect('vege:register')
        
#         except User.DoesNotExist:
#             messages.error(request, "User creation failed. Please try again.")
#             return redirect('vege:register')
        
#         except User.MultipleObjectsReturned:
#             messages.error(request, "Multiple users found. Please contact support.")
#             return redirect('vege:register')
        
#         except Exception as e:
#             messages.error(request, f"An error occurred during registration: {str(e)}")
#             return redirect('vege:register')
    
#     return render(request, 'vege/register.html', {'page': 'register'})


# def logout_view(request):
    logout(request)  # Log out the user
    messages.success(request, "Logged out successfully!")  # Flash success message
    return redirect('vege:login')  # Redirect to login page after logout






# def test_email(request):
#     try:
#         send_mail(
#             subject="Test Email",
#             message="This is a test email from Django.",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=['your-test-email@gmail.com'],
#             fail_silently=False,
#         )
#         return HttpResponse("Test email sent successfully!")
#     except Exception as e:
#         return HttpResponse(f"Failed to send email: {str(e)}")

