from django.db import models
from django.utils.text import slugify


class AttributeValue(models.Model):
    """ Model for attribute values """
    value = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        """ Create a slug and save """
        if not self.slug:
            self.slug = slugify(self.value)
            
        super(AttributeValue, self).save(*args, **kwargs)
