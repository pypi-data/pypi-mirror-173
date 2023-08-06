from django.db import models
from .order import Order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    # Product related info
    product_name = models.TextField(null=True)
    product_id = models.IntegerField()
    product_sku = models.CharField(max_length=255, null=True)
    quantity = models.IntegerField(db_index=True)
    category_id = models.IntegerField(default=None, null=True)
    
    # Product price info at the time of order placement
    tax_class = models.CharField(null=True, max_length=255)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    subtotal_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True, null=True)
