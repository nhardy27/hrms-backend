from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from api.AttendanceStatus.model import AttendanceStatus


class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # FK to Django User
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    date = models.DateField()

    # FK to AttendanceStatus
    attendance_status = models.ForeignKey(
        AttendanceStatus,
        on_delete=models.PROTECT,
        related_name="attendances"
    )

    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    # ✅ Total working hours (auto calculated)
    total_hours = models.DurationField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        """
        Automatically calculate total working hours
        """
        if self.check_in and self.check_out:
            check_in_dt = datetime.combine(self.date, self.check_in)
            check_out_dt = datetime.combine(self.date, self.check_out)

            # Safety: prevent negative duration
            if check_out_dt >= check_in_dt:
                self.total_hours = check_out_dt - check_in_dt
            else:
                self.total_hours = None
        else:
            self.total_hours = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
