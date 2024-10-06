from rest_framework.permissions import BasePermission

from learning.models import Course, Lesson


class IsModeratorClass(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwnerClass(BasePermission):

    def has_permission(self, request, view):
        '''
        Метод проверяет является ли пользователь владельцем хотя бы одного курса или урока
        для отображения списка курсов и уроков
        Если явялется: return True
        '''
        return Course.objects.filter(owner=request.user) or Lesson.objects.filter(owner=request.user)

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj
