from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import AllowAny
from django.urls import path
from users.apps import UsersConfig
from users.views import PaymentsListView, UserListView, UserCreateView, UserRetrieveView, UserUpdateView, \
    UserDestroyView, SimpleTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('login/', SimpleTokenObtainPairView.as_view(permission_classes=[AllowAny]), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', UserRetrieveView.as_view(), name='user'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDestroyView.as_view(), name='user_delete'),
    path('payments/', PaymentsListView.as_view(), name='payments'),

]
