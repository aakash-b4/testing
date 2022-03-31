from django.db import models
from datetime import datetime

class MerchantAccountDetail(models.Model):
    id = models.AutoField(primary_key=True)
    bank = models.IntegerField(default=0)
    merchantId = models.CharField(max_length=100, blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=12, blank=False, null=False)
    merchantAccountNumber = models.CharField(max_length=100, blank=True, null=True)
    ifscCode = models.CharField(max_length=20, blank=False, null=False)
    upiId = models.CharField(max_length=100, blank=False, null=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.CharField(max_length=100, blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now = True)
    updatedBy = models.CharField(max_length=100, blank=True, null=True)
    deletedAt = models.DateTimeField(default=None,null=True)
    deletedBy = models.CharField(max_length=100, blank=True, null=True)

    # str method to return the object in string format
    def __str__(self):
        return str(self.id)