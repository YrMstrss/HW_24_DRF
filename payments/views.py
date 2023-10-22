from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('course', 'lesson', 'payment_method')

