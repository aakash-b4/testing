from django.db import models
from datetime import date, datetime


class MercahantModeModel(models.Model):
    id=models.AutoField
    merchant_id=models.IntegerField()
    bank_partner_id=models.IntegerField()
    mode_id=models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now())
    deleted_at = models.DateTimeField(default=None,null=True)
    updated_at = models.DateTimeField(default=None,null=True)
    created_by = models.CharField(max_length=100,null=True)
    updated_by = models.CharField(max_length=100,null=True)
    deleted_by = models.CharField(max_length=100,null=True)
    status = models.BooleanField(null=True,default=True)
