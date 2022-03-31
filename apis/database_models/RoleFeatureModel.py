from django.db import models
from datetime import datetime

class RoleFeatureModel(models.Model):
    id=models.AutoField
    role_id=models.IntegerField()
    feature_id=models.IntegerField()
    custom_json = models.CharField(max_length=300,default=None,null=True)
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    created_by=models.DateTimeField(default=None,null=True)
    deleted_by=models.DateTimeField(default=None,null=True)
    updated_by=models.DateTimeField(default=None,null=True)
    def __str__(self):
        return str(self.id)