from django.db import models
from datetime import datetime


class MerchantModel(models.Model):
    id = models.AutoField
    role_id = models.IntegerField(null=True)
    client_id = models.IntegerField()
    client_code = models.CharField(max_length=60)
    auth_key = models.CharField(max_length=60)
    auth_iv = models.CharField(max_length=60)
    bank_id = models.IntegerField()
    client_username = models.CharField(max_length=100)
    client_password = models.CharField(max_length=100)
    is_payout = models.BooleanField(null=True)
    is_merchant = models.BooleanField(null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now())
    deleted_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    user_id = models.IntegerField()
    created_by = models.CharField(max_length=300)
    updated_by = models.CharField(max_length=300)
    deleted_by = models.CharField(max_length=300)
    is_ip_checking = models.BooleanField(default=True)
    email = models.EmailField(default=None, null=True)
    phone = models.CharField(default=None, null=True, max_length=300)
    is_charge = models.BooleanField(default=True)
    is_encrypt = models.BooleanField(default=True)
    encrypted_password = models.CharField(default="", max_length=300)
    is_tax_inclusive = models.BooleanField(default=False, null=True)
    client_name = models.CharField(max_length=3000, null=True)
    is_transactable = models.BooleanField(null=True, default=True)
    default_account = models.CharField(max_length=50, null=True)
    account_number = models.CharField(max_length=50, null=True)
    upi_id = models.CharField(max_length=50, null=True)

    # status=models.BooleanField(default=True)
    def __str__(self):
        return str(self.id)
