import uuid
from django.db import models

class AttendanceStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=20,
        unique=True
    )  # present, absent, half_day

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
