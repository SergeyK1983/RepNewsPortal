from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from news.models import *


# Создаем периодическую задачу
class Command(BaseCommand):

    def handle(self, *args, **options):
        PeriodicTask.objects.create(
            name='Task',
            task='mailing_letters',
            interval=IntervalSchedule.objects.get(every=10, period='seconds')
        )

