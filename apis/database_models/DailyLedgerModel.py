from django.db import models




class DailyLedgerModel(models.Model):
    id=models.AutoField
    merchant_id=models.IntegerField()
    date=models.DateField()
    opening_balance=models.FloatField(null=True)
    closing_balance=models.FloatField(null=True)
    opening_credit=models.FloatField(null=True)
    closing_credit=models.FloatField(null=True)
    opening_debit=models.FloatField(null=True)
    closing_debit=models.FloatField(null=True)
    today_charges=models.FloatField(null=True)
    created_at=models.DateTimeField()
    updated_at=models.DateTimeField(null=True)
    deleted_at=models.DateTimeField(null=True) 
    created_by=models.CharField(max_length=3000)
    updated_by=models.CharField(max_length=3000,null=True)
    deleted_by=models.CharField(max_length=3000,null=True)
    def __str__(self):
        return str(self.id)
    