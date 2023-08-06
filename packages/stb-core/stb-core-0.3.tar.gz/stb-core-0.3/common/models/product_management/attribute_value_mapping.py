from django.db import models

from apps.common.models.product_management.attribute import Attribute
from apps.common.models.product_management.attribute_value import \
    AttributeValue


class AttributeValueMapping(models.Model):
    """ Model for an Attribute of a product """
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value     = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

