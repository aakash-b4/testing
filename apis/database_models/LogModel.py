from django.db import models
from datetime import date, datetime

class LogModel(models.Model):
    id=models.AutoField
    log_type=models.CharField(max_length=300)
    client_ip_address = models.CharField(max_length=100)
    server_ip_address = models.CharField(max_length=100)
    table_primary_id = models.IntegerField(null=True)
    table_name=models.CharField(max_length=100,null=True)
    remarks = models.CharField(max_length=100,null=True)
    
    full_request = models.TextField(null=True)
    full_response= models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now())
    deleted_at = models.DateTimeField(default=None,null=True)
    updated_at = models.DateTimeField(default=None,null=True)
    created_by = models.CharField(max_length=100,null=True)
    updated_by = models.CharField(max_length=100,null=True)
    deleted_by = models.CharField(max_length=100,null=True)
    json=models.TextField(null=True)
