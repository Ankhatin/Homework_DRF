from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Payments, User
from users.permissions import IsModeratorClass, IsOwnerClass, IsOwnerProfile
from users.serializers import PaymentsSerializer, UserSerializer, SimpleTokenObtainPairSerializer, \
    UserOnlyReadSerializer


class UserListView(generics.ListAPIView):
    serializer_class = UserOnlyReadSerializer
    queryset = User.objects.all()
    permission_classes = [IsModeratorClass | IsAuthenticated]


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserOnlyReadSerializer
    queryset = User.objects.all()
    permission_classes = [IsModeratorClass | IsAuthenticated]

    def get_serializer_class(self):
        user_pk = self.kwargs.get('pk')
        if User.objects.get(pk=user_pk) == self.request.user:
            return UserSerializer
        return UserOnlyReadSerializer


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerProfile]


class UserDestroyView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerProfile]


class PaymentsListView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['date_of_payment']


class SimpleTokenObtainPairView(TokenObtainPairView):
    serializer_class = SimpleTokenObtainPairSerializer
