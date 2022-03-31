from django.db import models
from datetime import datetime


class ModeModel(models.Model):
    id = models.AutoField
    mode = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=datetime.now())
    deleted_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return str(self.id)
