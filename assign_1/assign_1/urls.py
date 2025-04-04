from django.contrib import admin
from django.urls import path
from assign_1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",uppercase_converter,name="uppercse_converter")
]