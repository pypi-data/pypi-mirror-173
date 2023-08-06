from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.managers import CustomUserManager

user_status_choices = [('Active','Active'),('Inactive','Inactive')]
class CustomUser(AbstractUser):
    username = models.CharField(max_length=60, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=60, default=None, blank=True, null=True)
    email = models.EmailField(unique=True)
    user_id = models.AutoField(primary_key=True)
    first_login = models.BooleanField(default=True)
    recovery_email = models.CharField(max_length=100, blank=True)
    email_verified = models.BooleanField(default=False)
    phone = models.CharField(blank=True,null=True,max_length=20)
    status = models.CharField(max_length=10, choices=user_status_choices, default='Active')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, blank=True)
    modified_date = models.DateTimeField(null=True,auto_now=True, blank=True)
    modified_by = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

