from datetime import datetime, timedelta

from celery import shared_task
import time

from django.core.mail import send_mass_mail, send_mail
from django_celery_beat.models import PeriodicTask
from .models import *

# Тут пишутся задачи для celery, задачи запускаются во вьюшках.

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


@shared_task
def send_email():
    time.sleep(5)
    q = Post.objects.order_by('date_create').last()  # Получаем созданную публикацию
    lcat = PostCategory.objects.filter(post_id=q.id)  # перечень категорий в этой статье
    us = [Subscription.objects.filter(subscribers=i.category).values('user') for i in lcat]  # Пользователи подписанные на эти категории
    users = set()
    for i in us:
        for j in i:
            users.add(j['user'])  # получаем идентификаторы пользователей

    us_email = [list(User.objects.filter(id=i).values('email'))[0]['email'] for i in users]  # получаем почту пользователей

    send_mail(
        subject='Это мы из таска',
        # message=instance.preview(),
        message=q.preview(),
        from_email='ssp-serg@yandex.ru',
        recipient_list=us_email
    )

    # datatuple = (
    #     'Отправлено тасками',
    #     'У нас что-то новое',
    #     'ssp-serg@yandex.ru',
    #     us_email
    # )
    # send_mass_mail(datatuple=datatuple, fail_silently=False)


@shared_task
def send_email_every_week():
    p = Post.objects.filter(date_create__gt=(datetime.now() - timedelta(seconds=691200)))  # Посты за неделю
    u = Subscription.objects.filter().values('user').distinct()  # пользователи с подпиской

