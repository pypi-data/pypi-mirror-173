from django.db import models


class Address(models.Model):
    id = models.AutoField(primary_key=True)

    # Address related info
    house_flat_number = models.CharField(max_length=500, null=True)
    street = models.CharField(max_length=500, null=True)
    area = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    type = models.CharField(max_length=50)
    pin = models.IntegerField()

    # Address priority
    primary = models.BooleanField(default=False)
    is_shipping = models.BooleanField(default=True)

    # Customer related info
    phone = models.CharField(max_length=12, null=True)
    alternate_contact = models.CharField(max_length=12, null=True,blank=True)

    customer_name = models.CharField(max_length=100, null=True, default=None)
    user_id = models.CharField(max_length=255)
