from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from learning.models import Course
from users.models import User

# from django_celery_beat.models import CrontabSchedule, PeriodicTask
#
#
# schedule, _ = CrontabSchedule.objects.get_or_create(
#     minute='45',
#     hour='*',
#     day_of_week='*',
#     day_of_month='*',
#     month_of_year='*',
# )
#
# PeriodicTask.objects.create(
#     crontab=schedule,
#     name='Disable inactive users',
#     task='proj.tasks.check_user_on_active',
# )


@shared_task
def send_email(course_id):
    course = Course.objects.get(pk=course_id)
    subscribes = course.subscribes.all()
    recipient_list = [subscribe.user.email for subscribe in subscribes]
    send_mail('Обновление курса',
              f'Курс {course.name} обновлен. Посетите наш сайт для более подробной информации',
              EMAIL_HOST_USER,
              recipient_list,
              fail_silently=False)


@shared_task
def check_user_on_active():
    user_set = User.objects.all()
    for user in user_set:
        print(user.email)
        if user.last_login:
            print(f'current {timezone.now()}')
            print(f'now {user.last_login}')
            if (timezone.now() - user.last_login) >= timedelta(hours=12):
                user.is_active = True
                user.save()
