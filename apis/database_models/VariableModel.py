from django.db import models


class VariableModel(models.Model):
    id=models.AutoField
    variable_name=models.CharField(max_length=300)
    variable_value=models.CharField(max_length=300)
    