from rest_framework import serializers

from payments.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = '__all__'


class UserSerializerForOthers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "date_joined",
            "phone",
            "city",
            "avatar",
            "email"
        )
