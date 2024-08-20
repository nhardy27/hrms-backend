from django.db import models
import uuid
class Test(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name}"