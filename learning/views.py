from datetime import datetime, timedelta

from django.utils import timezone
from django.shortcuts import get_object_or_404

from learning.models import Course, Lesson
from learning.paginators import LearningPaginator
from learning.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModeratorClass, IsOwnerClass

from learning.tasks import send_email


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LearningPaginator
    dict_last_updates = {}

    def list(self, request, *args, **kwargs):
        '''
        Метод выводит список курсов и уроков
        Для авторизованного пользователя выводит все курсы и уроки
        Если пользователь не модератор, передает в сериализатор экземпляр пользователя
        для вывода признака подписки на текущий курс
        '''
        queryset = self.get_queryset()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        if not request.user.groups.filter(name="moders").exists():
            # если текущий ползователь не является модератором передаем в сериализатор текущего пользователя
            CourseSerializer.current_user = request.user
        else:
            CourseSerializer.current_user = None
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        '''
        Метод выводит информацию по запрашиваемому курсу
        Если пользователь не модератор, передает в сериализатор экземпляр пользователя
        для вывода признака подписки на текущий курс
        '''
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **kwargs)
        self.check_object_permissions(request, obj)
        serializer = CourseSerializer(obj)
        if not request.user.groups.filter(name="moders").exists():
            # если текущий ползователь не является модератором передаем в сериализатор текущего пользователя
            CourseSerializer.current_user = request.user
        else:
            CourseSerializer.current_user = None
        return Response(serializer.data)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer, *args, **kwargs):
        course = serializer.save()
        if CourseViewSet.dict_last_updates.get(course):
            last_update = CourseViewSet.dict_last_updates.get(course)
            if datetime.now() - last_update >= timedelta(hours=4):
                send_email.delay(course.pk)
        CourseViewSet.dict_last_updates.update({course: datetime.now()})
        print(CourseViewSet.dict_last_updates[course])

    def get_permissions(self):
        '''
        Метод описывает права доступа на основе текущего действия пользователя
        '''
        if self.action == "create":
            self.permission_classes = [~IsModeratorClass]
        elif self.action == "destroy":
            self.permission_classes = [IsOwnerClass]
        elif self.action == 'list':
            self.permission_classes = [IsModeratorClass | IsAuthenticated]
        elif self.action in ['retrieve', 'update']:
            self.permission_classes = [IsOwnerClass | IsModeratorClass]
        return super().get_permissions()


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModeratorClass]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorClass | IsOwnerClass]
    pagination_class = LearningPaginator

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModeratorClass | IsOwnerClass]


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModeratorClass | IsOwnerClass]


class LessonDestroyView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [~IsModeratorClass | IsOwnerClass]
