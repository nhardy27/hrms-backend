from django.db import models
import uuid
from api.Address.model import Address

class Test(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    address=models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_test_FK')
    
    def __str__(self):
        return f"{self.name}"