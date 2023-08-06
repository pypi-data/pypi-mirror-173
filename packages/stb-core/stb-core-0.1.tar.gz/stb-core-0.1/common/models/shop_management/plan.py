from django.db import models


class ShopPlan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500,unique=True)
    duration = models.IntegerField()
    active = models.BooleanField(null=True,default=True)
    amount = models.IntegerField()
