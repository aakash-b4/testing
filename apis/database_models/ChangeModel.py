from django.db import models

from datetime import datetime
class ChargeModel(models.Model):
    id=models.AutoField
    # client=models.IntegerField()
    mode_id=models.IntegerField()
    min_amount=models.FloatField()
    max_amount=models.FloatField()
    charge_percentage_or_fix=models.CharField(max_length=300)
    charge=models.FloatField()
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    merchant_id=models.IntegerField()
    charge_type=models.CharField(max_length=300,null=True)
    partner_id=models.IntegerField(null=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return str(self.id)
    
    