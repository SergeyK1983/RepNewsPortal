from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):  # объекты всех авторов
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=True)

    def update_rating(self):
        self.rating = 0
        for i in Post.objects.all().values('user_id', 'rating'):
            if self.user_id == i.get('user_id'):
                self.rating += i.get('rating') * 3 if self.rating > 0 else (self.rating + 1) * i.get('rating') * 3

        for i in Comment.objects.all().values('rating', 'post_id', 'user_id'):
            if self.user_id == i.get('user_id'):
                self.rating += i.get('rating')

        return self.rating


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


# Нужно вынести в отдельный файл
NEWS = 'NW'
ARTICLE = 'AR'
TYPE_ARTICLE = [(NEWS, 'Новость'), (ARTICLE, 'Статья')]


class Post(models.Model):  # содержит в себе статьи и новости, которые создают пользователи
    user = models.ForeignKey(Author, on_delete=models.CASCADE)  # Связь с автором
    type_article = models.CharField(max_length=2, choices=TYPE_ARTICLE, default=ARTICLE)  # поле с выбором статья или новость, по умолчанию - статья
    date_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')  # Связь с категориями
    title = models.CharField()  # Заголовок
    article = models.TextField()  # Текст статьи/новости
    rating = models.IntegerField(default=0, null=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        prev = ''
        for i in self.article:
            if len(prev) <= 124:
                prev += i
            else:
                break
        return prev + ' ...'


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
