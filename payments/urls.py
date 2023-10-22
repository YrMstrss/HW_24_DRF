from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import PaymentListAPIView

app_name = PaymentsConfig.name

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='list-payment'),
]
