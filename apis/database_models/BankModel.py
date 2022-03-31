from django.db import models
from datetime import datetime


class BankPartnerModel(models.Model):
    id = models.AutoField
    bank_name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=100)
    nodal_account_number = models.CharField(max_length=300)
    nodal_ifsc = models.CharField(max_length=300)
    nodal_account_name = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=datetime.now())
    deleted_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.CharField(max_length=100, null=True)
    deleted_by = models.CharField(max_length=100, null=True)
    updated_by = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
