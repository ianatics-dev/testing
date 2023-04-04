from django.contrib import admin
from .models import Payment, Currency
# Register your models here.

admin.site.register(Payment)
admin.site.register(Currency)