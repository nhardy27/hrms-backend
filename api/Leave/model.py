from django.db import models
from django.contrib.auth.models import User
import uuid


class Leave(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # FK to User
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="leaves"
    )

    from_date = models.DateField()
    to_date = models.DateField()

    reason = models.TextField(null=True, blank=True)

    # Leave status
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | {self.from_date} → {self.to_date}"
