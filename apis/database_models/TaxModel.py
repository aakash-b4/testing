from django.db import models

from datetime import datetime,date

class TaxModel(models.Model):
    id=models.AutoField
    tax=models.IntegerField()
    start_date = models.DateField()
    end_date=models.DateField(null=True)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=datetime.now())
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=300,null=True)
    deleted_by = models.CharField(max_length=300,null=True)
    updated_by=models.CharField(max_length=300,null=True)