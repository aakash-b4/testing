from django.db import models

from datetime import datetime


class UserActiveModel(models.Model):
    id=models.AutoField
    merchant_id=models.IntegerField()
    tab_token=models.CharField(max_length=300)
    active_status=models.CharField(max_length=300)
    login_status=models.CharField(max_length=300)
    client_ip_address=models.CharField(max_length=300)
    tab_token_expire_time=models.DateTimeField(null=True)
    geo_location=models.CharField(max_length=3000)
    login_time=models.DateTimeField()
    login_expire_time=models.DateTimeField(null=True)
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    created_by=models.DateTimeField(default=None,null=True)
    deleted_by=models.DateTimeField(default=None,null=True)
    updated_by=models.DateTimeField(default=None,null=True)
    login_token=models.CharField(max_length=300,null=True)
    def __str__(self) -> str:
        return str(self.id)



