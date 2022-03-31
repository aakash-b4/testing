from django.db import models
from datetime import datetime

class FeatureModel(models.Model):
    id=models.AutoField
    feature_name=models.CharField(max_length=300)
    slug=models.CharField(max_length=100)
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    created_by=models.DateTimeField(default=None,null=True)
    deleted_by=models.DateTimeField(default=None,null=True)
    updated_by=models.DateTimeField(default=None,null=True)