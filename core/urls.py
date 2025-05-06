from django.contrib import admin
from django.urls import path, include

from home.views import * #about, contact_view, success_page
from vege.views import * #recipes, recipe_dashboard, delete_recipe, update_recipe, recipe_gallery, recipe_detail
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(('home.urls', 'home'), namespace='home')), # Include home app URLs
    path('', include('vege.urls', namespace='vege')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),  # Include accounts app URLs under /accounts/
    #path('accounts/', include('accounts.urls', namespace='accounts')),  # Include all accounts app URLs under /accounts/
    #path('recipes/', include('vege.urls', namespace='vege')),  # Include all vege app URLs under /recipes/
    
]

# Add media URL serving correctly
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
urlpatterns += staticfiles_urlpatterns()

