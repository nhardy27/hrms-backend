import uuid
from django.db import models
from api.Employee.model import Employee
from api.AttendanceStatus.model import AttendanceStatus
from django.utils import timezone


class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    date = models.DateField()

    attendance_status = models.ForeignKey(
        AttendanceStatus,
        on_delete=models.CASCADE
    )

    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("employee", "date")

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.employee.emp_code} - {self.date}"
