from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

from learning.models import Course
from users.models import Payments, User, Subscribe
from users.permissions import IsModeratorClass, IsOwnerClass, IsOwnerProfile
from users.serializers import PaymentsSerializer, UserSerializer, SimpleTokenObtainPairSerializer, \
    UserOnlyReadSerializer, SubscribeSerializer


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


class SubscribeView(generics.GenericAPIView):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()

    def post(self, *args, **kwargs):
        user = self.request.user
        user_id = int(kwargs.get('user_id'))
        requested_user = get_object_or_404(User, pk=user_id)
        if requested_user != user:
            return Response({"message": 'Управление подписками запрашиваемого пользователя Вам недоступно'})
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscribe.objects.all().filter(user=user).filter(course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscribe.objects.create(user=user,
                                     course=course_item)
            message = "подписка добавлена"
        return Response({"message": message})
