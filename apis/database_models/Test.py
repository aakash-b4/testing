from django.db import models
from datetime import datetime
class TestModel(models.Model):
    id = models.AutoField
    created_at = models.DateTimeField(default=datetime.now())
    updated_at=models.DateTimeField(null=True)
    def __str__(self):
        return str(self.id)