from django.db import models
from datetime import datetime


class WebhookRequestModel(models.Model):
    id=models.AutoField
    payout_trans_id=models.CharField(max_length=3000)
    hit_init_time=models.DateTimeField(null=True)
    trans_complete_time=models.DateTimeField(null=True)
    status=models.BooleanField()
    response_from_merchant=models.TextField()
    created_on=models.DateTimeField()
    deleted_on=models.DateTimeField(null=True)
    updated_on=models.DateTimeField(null=True)
    