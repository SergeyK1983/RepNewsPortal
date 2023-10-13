from celery import shared_task
from django_celery_beat.models import PeriodicTask

from .models import *


@shared_task(name="mailing_letters")
def mailing_letters():
    print("Отсылается письмо")
