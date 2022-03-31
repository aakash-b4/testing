from django.db import models

from datetime import datetime

class RoleModel(models.Model):
    id=models.AutoField
    role_name=models.CharField(max_length=300)
    permited_apis=models.CharField(max_length=5000,null=True)
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    created_by=models.CharField(null=True,max_length=500)
    deleted_by=models.CharField(null=True,max_length=500)
    updated_by=models.CharField(null=True,max_length=500)
    status = models.BooleanField(null=True,default=True)
    def __str__(self):
        return str(self.id)