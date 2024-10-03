from django.urls import path
from users.apps import UsersConfig
from users.views import PaymentsListView, UserListView, UserCreateView, UserRetrieveView, UserUpdateView, \
    UserDestroyView

app_name = UsersConfig.name


urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='lesson_create'),
    path('<int:pk>/', UserRetrieveView.as_view(), name='lesson'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='lesson_update'),
    path('delete/<int:pk>/', UserDestroyView.as_view(), name='lesson_delete'),
    path('payments/', PaymentsListView.as_view(), name='payments'),

]