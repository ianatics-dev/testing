from rest_framework import serializers
from .models import Payment, Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()
    username = serializers.CharField(source="user.username",
                                     read_only=True)


    class Meta:
        model = Payment
        fields = ("id", "username", "reference_code", "amount", "currency",
                  "is_paid", "paid_date", "created_date")

    def get_currency(self, instance):
        obj = CurrencySerializer(instance.currency).data
        return obj
