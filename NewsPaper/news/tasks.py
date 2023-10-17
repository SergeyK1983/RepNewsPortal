from celery import shared_task
import time
from django_celery_beat.models import PeriodicTask
from .models import *


# @shared_task(name="mailing_letters")
# def mailing_letters():
#     print("Отсылается письмо")


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)
