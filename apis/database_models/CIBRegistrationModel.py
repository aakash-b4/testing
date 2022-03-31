from enum import auto
from django.db import models
from datetime import datetime
from apis.database_models.BankModel import BankPartnerModel
import uuid


class CIBRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    bank = models.ForeignKey(
        BankPartnerModel, on_delete=models.CASCADE, default=1)
    merchantId = models.CharField(max_length=100, blank=True, null=True)
    aggrName = models.CharField(max_length=100, blank=True, null=True)
    aggrId = models.CharField(max_length=100, blank=True, null=True)
    corpId = models.CharField(max_length=100, blank=True, null=True)
    userId = models.CharField(max_length=100, blank=True, null=True)
    aliasId = models.CharField(max_length=100, blank=True, null=True)
    urn = models.CharField(null=False, max_length=50, default=uuid.uuid4)
    errorMessage = models.CharField(max_length=100, blank=True, null=True)
    response = models.CharField(max_length=100, blank=True, null=True)
    success = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=100, null=True)
    errorCode = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.bank.bank_name)

    # function to convert object to json

    def to_json(self):
        return {
            'id': self.id,
            'aggrName': self.aggrName,
            'merchantId': self.merchantId,
            'aggrId': self.aggrId,
            'corpId': self.corpId,
            'userId': self.userId,
            'aliasId': self.aliasId,
            'urn': self.urn,
            'errorMessage': self.errorMessage,
            'response': self.response,
            'success': self.success,
            'status': self.status,
            'message': self.message,
            'errorCode': self.errorCode,
            'created_at': self.created_at,
            'deleted_at': self.deleted_at,
            'updated_at': self.updated_at,
        }
