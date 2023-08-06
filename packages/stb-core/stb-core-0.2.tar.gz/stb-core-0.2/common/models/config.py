from django.db import models

class Configuration(models.Model):
    name = models.CharField(max_length=255, blank=True)
    value = models.CharField(max_length=1000, blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)