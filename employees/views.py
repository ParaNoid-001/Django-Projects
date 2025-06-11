# employees/views.py
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from django.template.loader import render_to_string

def employee_management(request):
    return render(request, 'employees/management.html')

def get_employees(request):
    designation = request.GET.get('designation', None)
    employees = Employee.objects.all()
    
    
    if designation:
        employees = employees.filter(designation=designation)
        
    

    employees_html = render_to_string('employees/includes/employee_table.html', {'employees': employees})
    return JsonResponse({'employees_html': employees_html})


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer