from django.db import models
from apps.common.models.order_management.order import Order


class OrderAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # Address related info
    house_flat_number = models.CharField(max_length=500, null=True)
    street = models.CharField(max_length=500, null=True)
    area = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    type = models.CharField(max_length=50, null=True)
    pin = models.IntegerField()

    # Address priority
    is_shipping = models.BooleanField(default=True)

    # Customer related info
    phone = models.CharField(max_length=12, null=True)
    alternate_contact = models.CharField(max_length=12, null=True,blank=True)
    customer_name = models.CharField(max_length=100, null=True, default=None)

