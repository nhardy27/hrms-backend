from django.db import models
from django.contrib.auth.models import User
import uuid


class ChatMessage(models.Model):
    ROOM_TYPES = (
        ('private', 'Private'),
        ('department', 'Department'),
        ('designation', 'Designation'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    room_id = models.CharField(max_length=100)  # user_id, department_id, or designation_id
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} [{self.room_type}:{self.room_id}] - {self.message[:30]}"
