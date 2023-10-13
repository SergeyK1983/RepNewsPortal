from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name = 'Новостной портал'  # Название приложения для админ панели, по умолчанию name

    def ready(self):
        # Чтобы работали сигналы в signal.py нужно переопределить этот метод
        import news.signals
