from django.db import models


class ProductTypeChoices(models.IntegerChoices):
    SIMPLE   = 1
    VARIABLE = 2
    

class ProductStatusChoices(models.IntegerChoices):
    INSTOCK = 1
    OUTOFSTOCK = 2
