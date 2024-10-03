from django.urls import path
from users.apps import UsersConfig
from users.views import PaymentsListView

app_name = UsersConfig.name


urlpatterns = [
    path('payments/', PaymentsListView.as_view(), name='payments'),

]