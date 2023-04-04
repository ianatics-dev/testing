from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Currency(models.Model):
    name = models.CharField(
        max_length=255
    )
    code = models.CharField(
        max_length=255, unique=True
    )
    created_date = models.DateTimeField(auto_now=True, null=True, blank=True)


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    reference_code = models.CharField(
        max_length=255, unique=True
    )
    amount = models.DecimalField(
        max_digits=19, decimal_places=4, null=True, blank=True
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.DO_NOTHING
    )
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True, null=True, blank=True)