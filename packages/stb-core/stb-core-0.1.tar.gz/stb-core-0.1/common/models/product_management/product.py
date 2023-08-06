from django.db import models
from apps.common.models.product_management.category import Category
from apps.common.models.product_management.brand import Brand
from apps.common.utils.enums import ProductStatusChoices, ProductTypeChoices
from .brand import Brand

class Product(models.Model):
    """ Model for a parent product """

    name = models.CharField(max_length=500)
    sku  = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=500, unique=True)

    display_type           = models.CharField(max_length=100, default=None, null=True)       # for ui
    display_stock_status   = models.CharField(max_length=100, default=None, null=True)       # for ui

    type           = models.IntegerField(choices=ProductTypeChoices.choices , default=ProductTypeChoices.SIMPLE)   
    stock_status   = models.IntegerField(choices=ProductStatusChoices.choices, default=ProductStatusChoices.INSTOCK)
    product_url    = models.TextField(null=True, default=None)
    
    variant_id     = models.JSONField(default=list)
    variants_count = models.IntegerField(default=0)
    description    = models.TextField(null=True, default=None)

    featured_image  = models.TextField(null=True, default=None)
    thumbnail_image = models.TextField(null=True, default=None)

    gallery        = models.JSONField(default=list)
    brand          = models.ForeignKey(Brand,on_delete=models.SET_NULL, null=True, default=None)
    
    category       = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    updated_at     =  models.DateTimeField(auto_now=True)
    created_at     =  models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return str(self.name)
        
    # TODO CREATE COMMON METHODS FOR PRODUCT