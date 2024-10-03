import json

from django.core.management import BaseCommand

from learning.models import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):

    @staticmethod
    def json_read_data():
        with open('payments.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            payments = [item['fields'] for item in data if item['model'] == 'users.payments']
            return payments

    def handle(self, *args, **options):
        payments_for_write = []
        for payment in Command.json_read_data():
            if payment['user']:
                payment['user'] = User.objects.get(pk=payment['user'])
            if payment['course']:
                payment['course'] = Course.objects.get(pk=payment['course'])
            if payment['lesson']:
                payment['lesson'] = Lesson.objects.get(pk=payment['lesson'])
            payments_for_write.append(Payments(**payment))
        Payments.objects.bulk_create(payments_for_write)