from django.db import models

from config.settings import MEDIA_ROOT

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to=f'{MEDIA_ROOT}/learning/', **NULLABLE, verbose_name='Изображение')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name']


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to=f'{MEDIA_ROOT}/learning/', **NULLABLE, verbose_name='Изображение')
    video = models.URLField(max_length=200, **NULLABLE, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name']
