from django.db import models

class IpHittingRecordModel(models.Model):
    id=models.AutoField
    ip_address=models.CharField(max_length=300)
    hitting_time=models.DateTimeField()
    ip_type=models.CharField(max_length=300)
    def __str__(self):
        return str(self.id)