from django.db import models
from datetime import datetime

class ChargeBreakingModel(models.Model):
    id=models.AutoField
    charge_amount=models.FloatField()
    charge_id=models.IntegerField()
    transaction_id=models.IntegerField()
    payout_transaction_id=models.CharField(max_length=3000)
    tax_amount=models.FloatField()
    charge_type=models.CharField(max_length=3000)
    created_on=models.DateTimeField()
    deleted_on=models.DateTimeField(null=True)
    updated_on=models.DateTimeField(null=True)
    created_by=models.CharField(max_length=3000)
    deleted_by=models.CharField(max_length=3000,null=True)
    updated_by=models.CharField(max_length=3000,null=True)
    def __str__(self):
        return str(self.id)
