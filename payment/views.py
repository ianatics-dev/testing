import logging
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from .models import Currency, Payment
from . import serializer
from datetime import date

# Create your views here.
class PaymentViewset(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset =  Payment.objects.all()
    serializer_class = serializer.PaymentSerializer

    def get_object(self):
        queryset = Payment.objects.all()
        try:
            return queryset.get(pk=self.kwargs["pk"])
        except ValidationError:
            raise ValidationError(
                {"details": "The details no longer exists."})

    def list(self, request, *args, **kwargs):
        obj = Payment.objects.filter(user=request.user)
        serializer = self.get_serializer(obj, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj).data
        return Response(serializer, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        currency = data.get("currency")

        amount = 0
        get_obj = Payment.objects.filter(user=request.user,
                                         created_date__gte=date.today())
        if get_obj:
            for i in get_obj:
                amount += i.amount
        amount += data.get("amount")
        if amount >= 5000 or data.get("amount") >= 5000:
            return Response({
                "message": "Amount limit is 5000 per day"
            }, status=status.HTTP_400_BAD_REQUEST)

        currency_obj = Currency(
            name=currency.get("name"),
            code=currency.get("code"),
        )
        currency_obj.save()

        payment_obj = Payment(
            user=request.user,
            reference_code=data.get("reference_code"),
            amount=data.get("amount"),
            currency=currency_obj,
        )
        payment_obj.save()

        serializer = self.get_serializer(payment_obj).data

        return Response(serializer, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        data = request.data

        get_obj = get_object_or_404(Payment, pk=pk)
        currency = Currency.objects.get(pk=get_obj.currency.id)
        logging.info(currency)
        if data.get("currency"):
            currency.name=data.get("currency")["name"]
            currency.code=data.get("currency")["code"]
            currency.save()

        response = super(PaymentViewset, self).update(request, pk, **kwargs)

        return Response(response.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk=None):
        get_obj = get_object_or_404(Payment, pk=pk)

        get_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class IsPaidViewset(APIView):

    def put(self, request, pk=None):
        get_obj = get_object_or_404(Payment, pk=pk)
        get_obj.is_paid = True
        get_obj.paid_date = date.today()

        get_obj.save()

        serialize = serializer.PaymentSerializer(get_obj).data

        return Response(serialize, status=status.HTTP_202_ACCEPTED)