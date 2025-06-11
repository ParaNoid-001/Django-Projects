# employees/models.py
from django.db import models
from django.core.validators import MinValueValidator

class Employee(models.Model):
    DESIGNATION_CHOICES = [
        ('Junior Designer', 'Junior Designer'),
        ('Designer', 'Designer'),
        ('Senior Designer', 'Senior Designer'),
        ('Junior Developer', 'Junior Developer'),
        ('Developer', 'Developer'),
        ('Senior Developer', 'Senior Developer'),
        ('Tester', 'Tester'),
        ('QA Engineer', 'QA Engineer'),
        ('Junior Manager', 'Junior Manager'),
        ('Manager', 'Manager'),
        ('Senior Manager', 'Senior Manager'),
    ]
    
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES)
    Monthly_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_designation_display()} (ID: {self.employee_id})"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['designation']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(Monthly_salary__gte=0),
                name="non_negative_salary"
            )
        ]
        
    def annual_salary(self):
        """Calculate the annual salary based on the monthly salary."""
        return self.Monthly_salary * 12
    
    def promotion(self, new_designation, salary_increase):
        """
        Promote the employee to a new designation with a salary increase.
        Validates the new designation and salary increase before applying.
        """
        if new_designation not in dict(self.DESIGNATION_CHOICES):
            raise ValueError(f"Invalid designation: {new_designation}. Must be one of {list(dict(self.DESIGNATION_CHOICES).keys())}")
        if salary_increase < 0:
            raise ValueError("Salary increase cannot be negative.")
        
        self.designation = new_designation
        self.Monthly_salary += salary_increase
        self.save()
        
    def get_salary_grade(self):
        """
        Returns a salary grade based on monthly salary:
        - 'A': >= 150,000
        - 'B': 100,000 - 149,999
        - 'C': 50,000 - 99,999
        - 'D': < 50,000
        """
        if self.Monthly_salary >= 150000:
            return 'A'
        elif self.Monthly_salary >= 100000:
            return 'B'
        elif self.Monthly_salary >= 50000:
            return 'C'
        else:
            return 'D'