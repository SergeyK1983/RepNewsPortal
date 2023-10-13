from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail
from .models import *  # все модели

# Тут обрабатываются сигналы происходящих событий и выполняются некоторые действия.
# Чтобы работало, нужно переопределить метод ready в apps.py


@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
    # Для массовой рассылки надо использовать send_mass_mail() https://djangodoc.ru/3.2/topics/email/
    send_mail(
        subject='Это мы',
        message=instance.preview(),
        from_email='ssp-serg@yandex.ru',
        recipient_list=['ksm.serg1983@gmail.com', ],
    )
