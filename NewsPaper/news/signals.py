from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail
from .models import *  # все модели
from .tasks import send_email

# Тут обрабатываются сигналы происходящих событий и выполняются некоторые действия.
# Чтобы работало, нужно переопределить метод ready в apps.py


@receiver(m2m_changed, sender=PostCategory)
def create_post(sender, instance, **kwargs):  # created был после instance
    # Для массовой рассылки надо использовать send_mass_mail() https://djangodoc.ru/3.2/topics/email/
    q = Post.objects.order_by('date_create').last()  # Получаем созданную публикацию
    lcat = PostCategory.objects.filter(post_id=q.id)  # перечень категорий в этой статье
    us = [Subscription.objects.filter(subscribers=i.category).values('user') for i in lcat]  # Пользователи подписанные на эти категории
    users = set()
    for i in us:
        for j in i:
            users.add(j['user'])  # получаем идентификаторы пользователей

    us_email = [list(User.objects.filter(id=i).values('email'))[0]['email'] for i in users]  # получаем почту пользователей

    # send_mail(
    #     subject='Это мы',
    #     # message=instance.preview(),
    #     message=q.preview(),
    #     from_email='ssp-serg@yandex.ru',
    #     recipient_list=us_email,  # ['ksm.serg1983@gmail.com', ],
    # )


@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):  # created был после instance
    send_email.delay()

