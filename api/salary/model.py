import uuid
from django.db import models
from decimal import Decimal
from api.Attendance.model import Attendance
from api.YearMaster.model import YearMaster

# Salary calculation and payment tracking
class Salary(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('hold', 'Hold'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attendance = models.ForeignKey(Attendance,on_delete=models.CASCADE,related_name='salary',null=True,blank=True)
    year = models.ForeignKey(YearMaster,on_delete=models.CASCADE,related_name='salary')
    month = models.PositiveSmallIntegerField()
    pf_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)  
    pf_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_working_days = models.IntegerField()
    present_days = models.IntegerField()
    absent_days = models.IntegerField()
    half_days = models.IntegerField()
    deduction = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)  # Final salary after deductions
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='unpaid')
    
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    earned_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    loss_of_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete
    
    class Meta:
        unique_together = ('attendance', 'month', 'year')  # One salary per attendance per month

    def save(self, *args, **kwargs):
        if self.attendance and self.attendance.user:
            user_profile = self.attendance.user.userprofile
            
            # Calculate gross salary
            basic = Decimal(str(user_profile.basic_salary or 0))
            hra = Decimal(str(user_profile.hra or 0))
            allowance = Decimal(str(user_profile.allowance or 0))
            self.gross_salary = basic + hra + allowance
            
            # Calculate per day salary
            per_day_salary = self.gross_salary / Decimal(str(self.total_working_days)) if self.total_working_days > 0 else Decimal('0')
            
            # Calculate actual working days (present + half_days/2)
            actual_days = Decimal(str(self.present_days)) + (Decimal(str(self.half_days)) / Decimal('2'))
            
            # Calculate earned salary
            self.earned_salary = per_day_salary * actual_days
            
            # Calculate loss of pay
            self.loss_of_pay = self.gross_salary - self.earned_salary
            
            # Calculate PF amount
            self.pf_amount = (self.earned_salary * self.pf_percentage) / Decimal('100')
            
            # Calculate total deduction
            self.deduction = self.loss_of_pay + self.pf_amount
            
            # Calculate net salary
            self.net_salary = self.earned_salary - self.pf_amount
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Salary {self.month}/{self.year.year}"
