from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status
from django.urls import reverse

from learning.models import Lesson, Course
from users.models import User


class LessonListTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create(email='test@test', phone='test', city='test')
        self.course = Course.objects.create(name="Develop",
                                       description="real")
        self.lesson = Lesson.objects.create(name="Java",
                              description="good",
                              course=self.course,
                              owner=user
                              )
        Lesson.objects.create(name="Python",
                              description="great",
                              course=self.course,
                              owner=user
                              )

        self.client.force_authenticate(user=user)

    def test_get_list(self):
        url = reverse('learning:lessons')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lesson(self):
        url = reverse('learning:lesson', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Java')

    def test_create_lesson(self):
        self.data = {'name': 'Databases', 'description': 'Базы данных', 'course': 1, 'owner': 1}
        url = reverse('learning:lesson_create')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson(self):
        url = reverse('learning:lesson_update', kwargs={'pk': self.lesson.pk})
        self.data = {"name": "C++"}
        response = self.client.patch(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        url = reverse("learning:lesson_delete", kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Exception):
            Lesson.objects.get(pk=self.lesson.pk)


