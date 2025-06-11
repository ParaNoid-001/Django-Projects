from django.contrib import admin
from django import forms
from .models import Employee
from django.shortcuts import render
from django.utils.html import format_html



class SalaryRangeFilter(admin.SimpleListFilter):
    title = 'Monthly Salary Range'
    parameter_name = 'Monthly_salary'

    def lookups(self, request, model_admin):
        return (
            ('0-50000', 'Grade D: < ₹50,000'),
            ('50000-100000', 'Grade C: ₹50,000 to ₹100,000'),
            ('100000-150000', 'Grade B: ₹100,000 to ₹150,000'),
            ('150000+', 'Grade A: ₹150,000+'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0-50000':
            return queryset.filter(Monthly_salary__lt=50000)
        if self.value() == '50000-100000':
            return queryset.filter(Monthly_salary__gte=50000, Monthly_salary__lt=100000)
        if self.value() == '100000-150000':
            return queryset.filter(Monthly_salary__gte=100000, Monthly_salary__lt=150000)
        if self.value() == '150000+':
            return queryset.filter(Monthly_salary__gte=150000)

class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        designation = cleaned_data.get('designation')
        salary = cleaned_data.get('Monthly_salary')
        
        # Add any custom validation logic here
        return cleaned_data

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm
    list_display = ('name', 'employee_id', 'designation', 'Monthly_salary', 
                   'annual_salary_display', 'salary_grade', 'created_at')
    search_fields = ('name', 'employee_id', 'designation')
    list_filter = ('designation', 'created_at', SalaryRangeFilter)
    actions = ['apply_salary_increase', 'promote_employees']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'employee_id')
        }),
        ('Employment Details', {
            'fields': ('designation', 'Monthly_salary'),
            'description': 'Use promotion action for bulk designation changes with salary adjustments'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'salary_grade')
    date_hierarchy = 'created_at'
    list_per_page = 25
    ordering = ('-created_at',)
    list_select_related = True

    def annual_salary_display(self, obj):
        """Display formatted annual salary"""
        return f"₹{obj.annual_salary():,.2f}"
    annual_salary_display.short_description = 'Annual Salary'
    annual_salary_display.admin_order_field = 'Monthly_salary'

    def salary_grade(self, obj):
        """Display salary grade with color coding"""
        grade = obj.get_salary_grade()
        colors = {'A': 'green', 'B': 'blue', 'C': 'orange', 'D': 'red'}
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(grade, 'black'),
            grade
        )
    salary_grade.short_description = 'Grade'

    def apply_salary_increase(self, request, queryset):
        """Admin action to apply percentage salary increase with confirmation"""
        if 'apply' in request.POST:
            percentage = float(request.POST.get('percentage', 10))
            updated_count = 0
            for employee in queryset:
                employee.Monthly_salary *= (1 + percentage/100)
                employee.save()
                updated_count += 1
            
            self.message_user(
                request,
                f"Successfully updated salary for {updated_count} employee(s) with {percentage}% increase"
            )
            return
            
        return render(
            request,
            'admin/salary_increase_confirmation.html',
            context={'employees': queryset}
        )
    apply_salary_increase.short_description = "Apply salary percentage increase"

    def promote_employees(self, request, queryset):
        """Admin action to promote multiple employees with salary adjustment"""
        if 'apply' in request.POST:
            new_designation = request.POST.get('new_designation')
            salary_increase = float(request.POST.get('salary_increase', 0))
            
            updated_count = 0
            for employee in queryset:
                try:
                    employee.promotion(new_designation, salary_increase)
                    updated_count += 1
                except ValueError as e:
                    self.message_user(request, f"Error promoting {employee.name}: {str(e)}", level='error')
            
            self.message_user(
                request,
                f"Successfully promoted {updated_count} employee(s) to {new_designation} with ₹{salary_increase:,.2f} increase"
            )
            return
            
        return render(
            request,
            'admin/promotion_confirmation.html',
            context={
                'employees': queryset,
                'designation_choices': Employee.DESIGNATION_CHOICES
            }
        )
    promote_employees.short_description = "Promote selected employees"

admin.site.register(Employee, EmployeeAdmin)