from django.db import models
from api.Department.model import Department 
import uuid

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emp_code = models.CharField(max_length=10,unique=True,editable=False)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null =True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    designation = models.CharField(max_length=30)
    date_of_joining = models.DateField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.emp_code} - {self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.emp_code:
            last_emp = Employee.objects.order_by('-created_at').first()
            if last_emp and last_emp.emp_code:
                last_number = int(last_emp.emp_code.replace('EMP', ''))
                new_number = last_number + 1
            else:
                new_number = 1

            self.emp_code = f"EMP{new_number:04d}"

        super().save(*args, **kwargs)
