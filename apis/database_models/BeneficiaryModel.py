from os import stat
from django.db import models

from datetime import datetime


class BeneficiaryModel(models.Model):
    id = models.AutoField
    full_name = models.CharField(max_length=3000, null=True)
    account_number = models.CharField(max_length=400, null=True)
    ifsc_code = models.CharField(max_length=500, null=True)
    upi_id = models.CharField(max_length=3000, null=True)
    merchant_id = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now())
    deleted_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.CharField(max_length=30, default="merchant")
    deleted_by = models.DateTimeField(default=None, null=True)
    updated_by = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=True)
    bank_name = models.CharField(max_length=45, null=True)
    category = models.CharField(max_length=45, null=True)

    def __str__(self):
        return str(self.id)

    # function to convert the json to class object
    @staticmethod
    def from_json(json_beneficiary):
        beneficiary = BeneficiaryModel()
        beneficiary.full_name = json_beneficiary.get('full_name', None)
        beneficiary.account_number = json_beneficiary.get('account_number', None)
        beneficiary.ifsc_code = json_beneficiary.get('ifsc_code', None)
        beneficiary.upi_id = json_beneficiary.get('upi_id', None)
        beneficiary.merchant_id = json_beneficiary.get('merchant_id', None)
        beneficiary.created_at = datetime.now()
        beneficiary.deleted_at = None
        beneficiary.updated_at = None
        beneficiary.created_by = json_beneficiary.get('created_by', None)
        beneficiary.deleted_by = None
        beneficiary.updated_by = None
        beneficiary.status = json_beneficiary.get('status', None)
        beneficiary.bank_name = json_beneficiary.get('bank_name', None)
        return beneficiary
