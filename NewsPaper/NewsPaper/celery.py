import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object(obj='django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Например, чтобы выполнить какую-то задачу каждый понедельник в 8 утра, необходимо в расписание добавить следующее:
app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.send_email_every_week',
        # crontab позволяет задавать расписание, ориентируясь на точное время, день недели, месяца и т. д. см. док-ю
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'args': (5, ),
    },
}

# Добавим этот код в файл celery.py. Здесь мы каждые 5 секунд вызываем таску printer, которую мы писали ранее.
# У неё есть аргумент (конец счётчика), и мы его передаём в виде аргумента в ключе ‘args’. Перезапускаем Celery и
# наслаждаемся бесконечным счётчиком от 1 до 5, который перезапускается каждые 5 секунд.
# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'news.tasks.printer',
#         'schedule': 5,
#         'args': (5,),
#     },
# }
