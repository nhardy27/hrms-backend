from django.db import models
import uuid


class AttendanceStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    present = models.BooleanField(default=False)
    absent = models.BooleanField(default=False)
    halfday = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.present:
            return "Present"
        elif self.absent:
            return "Absent"
        elif self.halfday:
            return "Half Day"
        return "Not Marked"
