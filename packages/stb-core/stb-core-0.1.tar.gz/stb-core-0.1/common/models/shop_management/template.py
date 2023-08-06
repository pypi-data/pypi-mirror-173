from django.db import models


class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500,unique=True)
    active = models.BooleanField(null=True,default=True)
    custom = models.BooleanField(null=True,default=True)
    theme = models.JSONField(default=list)