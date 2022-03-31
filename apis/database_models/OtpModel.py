from django.db import models
from datetime import datetime


class OtpModel(models.Model):
    id=models.AutoField
    user_id=models.IntegerField()
    user_type=models.CharField(max_length=1000)
    verification_token=models.CharField(max_length=60)
    mobile=models.CharField(max_length=12,null=True)
    email=models.EmailField(max_length=1000)
    otp=models.BigIntegerField()
    expire_datetime=models.DateTimeField()
    otp_status = models.CharField(max_length=300)
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    created_by=models.CharField(default=None,null=True,max_length=400)
    deleted_by=models.CharField(default=None,null=True,max_length=400)
    updated_by=models.CharField(default=None,null=True,max_length=400)
    type=models.CharField(default=None,null=True,max_length=300)
    def __str__(self):
        return str(self.id)
    




