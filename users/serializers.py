from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from users.models import Payments, User, Subscribe


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ["email", "phone", "city", "password", "payments"]


class UserOnlyReadSerializer(serializers.ModelSerializer):
    '''
    Класс сериализатора для просмотра профилей любых пользователей
    '''
    class Meta:
        model = User
        fields = ["email", "phone", "city"]


class SimpleTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        token["email"] = user.email
        return token


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = "__all__"



