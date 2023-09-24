from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseNotFound
from .models import Post
import os
from pathlib import Path


def index(request):  # HttpRequest
    index_dir = os.path.join(Path(__file__).resolve().parent.parent, 'templates')
    now = datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now   # os.path.join(index_dir, 'index.html')
    return HttpResponse("/news")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1 align="center"> Страница не найдена </h1>')


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Вызываем метод из родительского класса MultipleObjectMixin
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()  # utcnow()
        # Добавим ещё одну пустую переменную, чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None  # Если написать None, то сработает это: <h3> {{ next_sale|default_if_none:"Чуть позже сообщим о распродаже!" }} </h3>
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context
