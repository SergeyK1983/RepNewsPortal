# Generated by Django 4.2.5 on 2023-10-03 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0007_alter_post_options_alter_post_date_create_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['id', 'user_id'], 'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['id', 'post_id', 'user_id', 'date_create'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['id', 'user'], 'verbose_name': 'Публикация', 'verbose_name_plural': 'Публикации'},
        ),
        migrations.AlterModelOptions(
            name='postcategory',
            options={'ordering': ['id', 'post_id', 'category_id'], 'verbose_name': 'Категория публикации', 'verbose_name_plural': 'Категории публикаций'},
        ),
        migrations.AlterField(
            model_name='author',
            name='rating',
            field=models.IntegerField(default=0, null=True, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(choices=[('SP', 'Спорт'), ('PO', 'Политика'), ('ED', 'Образование'), ('TE', 'Техника'), ('SC', 'Наука'), ('NA', 'Природа'), ('IN', 'Интернет'), ('OT', 'Прочее')], default='OT', max_length=2, unique=True, verbose_name='Категории'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='com_text',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(default=0, null=True, verbose_name='Рейтинг'),
        ),
    ]
