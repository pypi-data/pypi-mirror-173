"""
This module consists of a schema/model for creating a cart
"""
from django.db import models
from apps.common.models.user import CustomUser


class Cart(models.Model):
    # customer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=255, unique=True)
    customer_email = models.CharField(max_length=255,null=True, blank=True)
    customer_name = models.CharField(max_length=255,null=True, blank=True)
    cart_hash  = models.CharField(max_length=255, null=True, blank=True, default=None)
    cart_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=None)


class CartItem(models.Model):
    #TODO: cart_id and product_id should be unique
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_id = models.IntegerField()
    quantity   = models.IntegerField()
    is_freebie = models.BooleanField(default=False)
