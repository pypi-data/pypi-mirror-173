from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """ Model for a category """

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    parent = models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True)
    left  = models.IntegerField(default=0)
    right = models.IntegerField(default=0)

    display = models.CharField(max_length=100, null=True, default=None)
    image   = models.TextField(null=True)
    count   = models.IntegerField(default=0)
    header  = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        """ Create a slug and save """
        if not self.slug:
            self.slug = slugify(self.name)
            
        super(Category, self).save(*args, **kwargs)

    # TODO CREATE COMMON METHODS FOR CATEGORY
