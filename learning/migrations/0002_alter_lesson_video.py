# Generated by Django 5.1.1 on 2024-09-22 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на видео'),
        ),
    ]
