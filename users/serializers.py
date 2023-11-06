from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from payments.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)

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


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    def create(self, validated_data):
        # validated_data['username'] = 'test'
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('email', 'password')
