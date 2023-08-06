from django.db import models
from apps.common.models.product_management.brand import Brand
from apps.common.models.product_management.product import Product
from apps.common.models.product_management.category import Category
from apps.common.utils.enums import ProductStatusChoices


class Variant(models.Model):
    """ Model for a variant product """

    # Make this mandatory if you want a parent and child relationship
    parent = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)    
    name = models.CharField(max_length=500)
    sku  = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=500, unique=True)
    gtin = models.CharField(max_length=255, null=True, default=None, blank=True)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    stock_status   = models.IntegerField(choices=ProductStatusChoices.choices, default=ProductStatusChoices.INSTOCK)
    display_stock_status = models.CharField(max_length=100, default=None)   # for ui
    
    cogs   = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sale_price    = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    stock_quantity = models.IntegerField(default=0, null=True, blank=True)
    gallery        = models.JSONField(default=list, null=True, blank=True)
    
    brand          = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category       = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    featured_image  = models.TextField(null=True, default=None, blank=True)
    thumbnail_image = models.TextField(null=True, default=None, blank=True)
    product_url    = models.TextField(null=True, default=None, blank=True)

    updated_at     =  models.DateTimeField(auto_now=True)
    created_at     =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    # TODO CREATE COMMON METHODS FOR VARIANT
    # TODO: Slug, SKU auto generate, default thumbnail image