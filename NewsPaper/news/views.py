from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseNotFound
from .models import Post
from .filters import NewsFilter
import os
from pathlib import Path


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
    paginate_by = 10

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
        return context


class SearchNewsList(ListView):
    model = Post
    ordering = '-date_create'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации.
        return context

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
