from django.shortcuts import render
from django.shortcuts import get_object_or_404

from learning.models import Course, Lesson
from learning.paginators import LearningPaginator
from learning.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics
from rest_framework.response import Response

from users.permissions import IsModeratorClass, IsOwnerClass


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LearningPaginator

    def list(self, request, *args, **kwargs):
        '''
        Метод выводит список курсов и уроков
        Для авторизованного пользователя выводит объекты, владельцем которых является
        Для модераторов выводит весь список
        '''
        if request.user.groups.filter(name="moders").exists():
            queryset = self.get_queryset()
            paginated_queryset = self.paginate_queryset(queryset)
            serializer = CourseSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            queryset = self.get_queryset()
            paginated_queryset = self.paginate_queryset(queryset)
            serializer = CourseSerializer(paginated_queryset, many=True, context=request.user)
            return self.get_paginated_response(serializer.data)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModeratorClass]
        elif self.action == "destroy":
            self.permission_classes = [~IsModeratorClass, IsOwnerClass]
        else:
            self.permission_classes = [IsModeratorClass | IsOwnerClass]
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


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
