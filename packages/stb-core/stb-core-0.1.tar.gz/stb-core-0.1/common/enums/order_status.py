from django.db import models
from django.utils.translation import gettext_lazy as _


################# Order Status Enums ##################
class OrderStatus(models.IntegerChoices):
    CONFIRMED = 1, _("confirmed")
    SUCCESS = 2, _("success")
    FAILED = 3, _("failed")
    CANCELLED = 4, _("cancelled")
    PAYMENT_FAILED = 5, _("payment failed")
    PENDING = 6, _("pending")
    PAYMENT_SUCCESSFUL = 7, _("payment successful")
