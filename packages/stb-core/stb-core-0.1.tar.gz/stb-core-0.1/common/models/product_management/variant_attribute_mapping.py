from django.db import models

from apps.common.models.product_management.attribute import Attribute
from apps.common.models.product_management.attribute_value import \
    AttributeValue
from apps.common.models.product_management.variant import Variant


class VariantAttributeMapping(models.Model):
    """ Model for an Variant & Attribute mapping of a product """
    
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value     = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    variant   = models.ForeignKey(Variant, on_delete=models.CASCADE)

    def __str__(self):
        return self.variant.slug
