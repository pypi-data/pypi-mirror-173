from django.db import models


class TokenBlacklist(models.Model):
    token  = models.TextField(null=True, default=None)
    reason = models.CharField(max_length=100, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
