from datetime import datetime, timedelta

from celery import shared_task
import time

from django.core.mail import send_mass_mail, send_mail
from django.template.loader import render_to_string
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


# Отправка писем подписчикам при публикации новой статьи или новости на любимую категорию
# Задача запускается в signals.py
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


# Отправка подписчикам писем раз в неделю с перечнем публикаций за неделю.
# Задача запускается в celery.py
@shared_task
def send_email_every_week():
    p = Post.objects.filter(date_create__gt=(datetime.now() - timedelta(seconds=691200)))  # Посты за неделю
    u = Subscription.objects.filter().values('user').distinct()  # пользователи с подпиской
    email = [list(User.objects.filter(id=i['user']).values('email'))[0]['email'] for i in u]  # Получаем почту пользователей

    html_content = render_to_string(
        template_name='news/post_for_mailing_to_tasks.html',
        context={
            'post': p,
        }
    )
    # Через цикл для того, чтобы у адресата не было видно кому еще письмо отправлено.
    # т.к. соединение с почтой открывается каждый раз при отправлении, то думаю без разницы отправлять циклом или
    # весь список адресов сразу пихать.
    for i in email:
        send_mail(
            subject='Еженедельная отправка',
            message='тук-тук',
            from_email='ssp-serg@yandex.ru',
            recipient_list=[i, ],
            html_message=html_content,
        )

    # Работает, но адресату при получении письма видно всех кому отправлялись письма
    # message1 = (
    #     'Еженедельная отправка',
    #     'За неделю у нас вышли новые публикации',
    #     'ssp-serg@yandex.ru',
    #     email
    # )
    # send_mass_mail(datatuple=(message1, ), fail_silently=False)
