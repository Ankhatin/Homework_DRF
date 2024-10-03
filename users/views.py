from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsListView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['date_of_payment']
