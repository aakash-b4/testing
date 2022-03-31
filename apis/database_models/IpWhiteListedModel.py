from django.db import models
from datetime import datetime

class IpWhiteListedModel(models.Model):
    id=models.AutoField
    merchant_id=models.IntegerField()
    ip_address=models.CharField(max_length=300)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    created_by = models.CharField(default=None,null=True,max_length=50)
    deleted_by = models.CharField(default=None,null=True,max_length=50)
    updated_by = models.CharField(default=None,null=True,max_length=50)
    def __str__(self):
        return str(self.id)
