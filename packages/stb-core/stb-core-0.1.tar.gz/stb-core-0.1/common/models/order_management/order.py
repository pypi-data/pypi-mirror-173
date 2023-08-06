""" This script consists of a class that defines the schema of Order """
from django.db import models
import uuid


class Order(models.Model):
    # Order status
    id =  models.UUIDField(primary_key=True,default=uuid.uuid4)
    status = models.IntegerField(db_index=True)
    display_status = models.CharField(max_length=30)

    # Discount Prices
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Shipping Prices
    shipping_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Order core info
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    total_items = models.IntegerField(default=0, db_index=True)

    # Order payment related info
    payment_paid = models.BooleanField(default=False, db_index=True)
    payment_method = models.CharField(max_length=200, db_index=True, null=True) 
    transaction_id = models.CharField(max_length=100, default=None, null=True)
    currency_code = models.CharField(max_length=5, default='INR')

    # Meta data
    meta_data = models.JSONField(default=list)
    cancelled_reason = models.CharField(max_length=400, default=None, null=True)

    # Customer related details
    customer_id = models.CharField(max_length=100,db_index=True)
    customer_name = models.CharField(max_length=255, null=True, default=None)
    customer_email = models.EmailField(max_length=100, null=True, default=None)

    # Timestamps
    payment_date = models.DateTimeField(null=True, default=None)
    order_complete_date = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
