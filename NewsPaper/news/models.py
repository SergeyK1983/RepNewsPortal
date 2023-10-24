from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache  # Для кэширования


class Author(models.Model):  # объекты всех авторовuse
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, verbose_name='Автор')
    rating = models.IntegerField(default=0, null=True, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['id', 'user_id']

    def update_rating(self):
        self.rating = 0
        for i in Post.objects.all().values('user_id', 'rating'):
            if self.user_id == i.get('user_id'):
                self.rating += i.get('rating') * 3 if self.rating > 0 else (self.rating + 1) * i.get('rating') * 3

        for i in Comment.objects.all().values('rating', 'user_id'):
            if self.user_id == i.get('user_id'):
                self.rating += i.get('rating')

        post_user = Post.objects.filter(user_id=self.user_id).values("id")
        # Сдается, что это можно было сделать изящней
        for i in Comment.objects.all().values('rating', 'post_id'):
            for j in post_user:
                if j.get('id') == i.get('post_id'):
                    self.rating += i.get('rating')

        self.save()

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):  # Категории новостей/статей — темы
    SPOTS = 'SP'  # определяются внутри класса
    POLICY = 'PO'
    EDUCATION = 'ED'
    TECHNIQUE = 'TE'
    SCIENCE = 'SC'
    NATURE = 'NA'
    INTERNET = 'IN'
    OTHER = 'OT'

    CATEGORY = [
        (SPOTS, 'Спорт'),
        (POLICY, 'Политика'),
        (EDUCATION, 'Образование'),
        (TECHNIQUE, 'Техника'),
        (SCIENCE, 'Наука'),
        (NATURE, 'Природа'),
        (INTERNET, 'Интернет'),
        (OTHER, 'Прочее')
    ]

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    title = models.CharField(max_length=2, choices=CATEGORY, default=OTHER, unique=True, verbose_name='Категории')

    def __str__(self):
        return f"{self.title}"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usersabscr', verbose_name='Пользователь')
    subscribers = models.ForeignKey(Category, to_field='title', on_delete=models.CASCADE, related_name='categories', verbose_name='Подписка', null=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['user']

    def __str__(self):
        return f'{self.user}: {self.subscribers}'


# Нужно вынести в отдельный файл
NEWS = 'NW'
ARTICLE = 'AR'
TYPE_ARTICLE = [(NEWS, 'Новость'), (ARTICLE, 'Статья')]


class Post(models.Model):  # содержит в себе статьи и новости, которые создают пользователи
    user = models.ForeignKey(Author, to_field='user_id', on_delete=models.CASCADE, verbose_name='Автор')  # Связь с автором
    type_article = models.CharField(max_length=2, choices=TYPE_ARTICLE, default=ARTICLE, verbose_name='Тип')  # поле с выбором статья или новость, по умолчанию - статья
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    category = models.ManyToManyField(Category, through='PostCategory')  # Связь с категориями
    title = models.CharField(max_length=200, verbose_name='заголовок')  # Заголовок
    article = models.TextField()  # Текст статьи/новости
    rating = models.IntegerField(default=0, null=True, verbose_name='рейтинг')

    class Meta:
        verbose_name = 'Публикация'  # Название модели для админ панели
        verbose_name_plural = 'Публикации'  # Тоже самое для множественного числа
        ordering = ['id', 'user']  # Сортировка в админ панели по id и user, в список можно добавить еще параметры

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        pr = self.article[:124]
        return pr + ' ...'

    def __str__(self):
        return f'{self.title[:15]}: {self.id}'  # : {self.article}'

    def get_absolute_url(self):
        return reverse(viewname='post', args=[str(self.id)])

    # Для кэширования на странице с новостью.
    # Установили реакцию на редактирование объекта. Когда объект меняется его надо удалять из кэша,
    # чтобы ключ сбрасывался и больше не находился.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'news-{self.id}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):  # Промежуточная модель для связи «многие ко многим»
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория публикации'
        verbose_name_plural = 'Категории публикаций'
        ordering = ['id', 'post_id', 'category_id']


class Comment(models.Model):  # комментарии к новостям/статьям
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    com_text = models.TextField(verbose_name='Содержание')  # Текст комментария
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    rating = models.IntegerField(default=0, null=True, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['id', 'post_id', 'user_id', 'date_create']

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
