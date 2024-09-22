from django.urls import path
from rest_framework.routers import DefaultRouter
from learning.apps import LearningConfig
from learning.views import CourseViewSet, LessonCreateView, LessonListView, LessonRetrieveView, LessonUpdateView, \
    LessonDestroyView

app_name = LearningConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/', LessonListView.as_view(), name='lessons'),
    path('lessons/<int:pk>/', LessonRetrieveView.as_view(), name='lesson'),
    path('lessons/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyView.as_view(), name='lesson_delete')

] + router.urls
