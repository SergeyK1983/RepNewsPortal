from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):  # объекты всех авторовuse
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=True)

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


# Нужно вынести в отдельный файл
SPOTS = 'SP'
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


class Category(models.Model):  # Категории новостей/статей — темы
    title = models.CharField(max_length=2, choices=CATEGORY, default=OTHER, unique=True)

    def __str__(self):
        return f"{self.title}"


# Нужно вынести в отдельный файл
NEWS = 'NW'
ARTICLE = 'AR'
TYPE_ARTICLE = [(NEWS, 'Новость'), (ARTICLE, 'Статья')]


class Post(models.Model):  # содержит в себе статьи и новости, которые создают пользователи
    user = models.ForeignKey(Author, on_delete=models.CASCADE)  # Связь с автором
    type_article = models.CharField(max_length=2, choices=TYPE_ARTICLE, default=ARTICLE)  # поле с выбором статья или новость, по умолчанию - статья
    date_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')  # Связь с категориями
    title = models.CharField(max_length=200)  # Заголовок
    article = models.TextField()  # Текст статьи/новости
    rating = models.IntegerField(default=0, null=True)

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
        return f'{self.title}: {self.id}'  # : {self.article}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])


class PostCategory(models.Model):  # Промежуточная модель для связи «многие ко многим»
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):  # комментарии к новостям/статьям
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    com_text = models.TextField()  # Текст комментария
    date_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, null=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
