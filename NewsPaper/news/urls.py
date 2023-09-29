from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, PostDetail, SearchNewsList, NewsCreate, ArticlesCreate, NewsUpdate, NewsDelete, \
   ArticlesUpdate, ArticlesDelete


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view(), name='news'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:id>', PostDetail.as_view(), name='post'),
   path('search/', SearchNewsList.as_view(), name='news_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='news_delete'),
]
