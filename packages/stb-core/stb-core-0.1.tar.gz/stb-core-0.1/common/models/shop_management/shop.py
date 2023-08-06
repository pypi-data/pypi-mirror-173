from django.db import models

from apps.common.models.address import Address
from apps.common.models.product_management.category import Category
from apps.common.models.shop_management.plan import ShopPlan
from apps.common.models.shop_management.template import Template


class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500,unique=True)
    description = models.CharField(max_length=500)
    slug = models.CharField(max_length=500, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address , on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey(ShopPlan, on_delete=models.SET_NULL, null=True)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)

    # TODO CREATE COMMON METHODS FOR THE SHOP