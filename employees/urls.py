# payroll/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import *
from employees.views import employee_management, get_employees
from rest_framework.routers import DefaultRouter
from employees.views import EmployeeViewSet

router = DefaultRouter()
router.register(r'api/employees', EmployeeViewSet)

urlpatterns = [
    
    path('', employee_management, name='employee_management'),
    path('get-employees/', get_employees, name='get_employees'),
    path('', include(router.urls)),
]