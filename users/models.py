from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from learning.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=15, unique=True, verbose_name='Телефон')
    city = models.CharField(max_length=30, verbose_name='Город')
    avatar = models.ImageField(upload_to='media/users/', **NULLABLE, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']


class Payments(models.Model):
    METHODS = (
        ('cash', 'наличные'),
        ('bank transfer', 'перевод на счет')
        ,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь', **NULLABLE)
    date_of_payment = models.DateField(default=timezone.now, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments', verbose_name='Курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='payments', verbose_name='Урок', **NULLABLE)
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма платежа')
    payment_method = models.CharField(max_length=20, choices=METHODS, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.course if self.course else self.lesson} - {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['date_of_payment']


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribes', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscribes', verbose_name='Курс')
    payment_id = models.CharField(max_length=300, verbose_name="ID платежа", **NULLABLE)

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['user']