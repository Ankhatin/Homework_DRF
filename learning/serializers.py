from rest_framework import serializers

from learning.models import Course, Lesson
from learning.validators import UrlValidator
from users.models import Subscribe


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="video")]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    is_user_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_user_subscribed(self, obj):
        if self.context:
            user = self.context
            subscribe = Subscribe.objects.all().filter(course=obj).filter(user=user)
            if subscribe.exists():
                return 'подписан'
            else:
                return 'не подписан'
        else:
            return

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'owner', 'lessons', 'lessons_count', 'is_user_subscribed']
