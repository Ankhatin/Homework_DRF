# Generated by Django 5.1.1 on 2024-10-03 08:51

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0003_alter_course_preview_alter_lesson_preview'),
        ('users', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_payment', models.DateField(default=django.utils.timezone.now, verbose_name='Дата оплаты')),
                ('payment_amount', models.PositiveIntegerField(verbose_name='Сумма платежа')),
                ('payment_method', models.CharField(choices=[('cash', 'наличные'), ('bank transfer', 'перевод на счет')], max_length=20, verbose_name='Способ оплаты')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='learning.course', verbose_name='Курс')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='learning.lesson', verbose_name='Урок')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
                'ordering': ['date_of_payment'],
            },
        ),
    ]
