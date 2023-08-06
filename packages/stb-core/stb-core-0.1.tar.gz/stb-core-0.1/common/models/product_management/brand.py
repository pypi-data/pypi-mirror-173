from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=1000, unique=True)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.slug
