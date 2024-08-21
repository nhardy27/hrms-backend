from django.db import models
import uuid
class Address(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    address=models.CharField(max_length=200,null=False,blank=False)
    city=models.CharField(max_length=100,null=False,blank=False)
    state=models.CharField(max_length=100,null=False,blank=False)
    pincode=models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.address}"