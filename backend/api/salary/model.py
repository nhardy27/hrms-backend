import uuid
from django.db import models
from api.Attendance.model import Attendance
from api.YearMaster.model import YearMaster


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
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    allowance = models.DecimalField(max_digits=10, decimal_places=2)
    pf_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)
    pf_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_working_days = models.IntegerField()
    present_days = models.IntegerField()
    absent_days = models.IntegerField()
    half_days = models.IntegerField()
    deduction = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='unpaid')
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('attendance', 'month', 'year')

    def __str__(self):
        return f"Salary {self.month}/{self.year.year}"
