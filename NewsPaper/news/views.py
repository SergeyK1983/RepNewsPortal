from datetime import datetime

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseNotFound
from .models import Post
from .filters import NewsFilter
from .forms import NewsForm
import os
from pathlib import Path


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1 align="center"> Ошибка 404 <br> Страница не найдена </h1>')


def user_not_authenticated(request, exception):
    return HttpResponseNotFound('<h1 align="center"> Ошибка 403 <br> Пользователь не авторизирован </h1>')


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news/news.html'
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
    template_name = 'news/post.html'
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
    template_name = 'news/search.html'
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


class NewsCreate(CreateView):
    form_class = NewsForm
    template_name = 'news/news_edit.html'
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_article = 'NW'
        return super().form_valid(form)


class ArticlesCreate(CreateView):
    form_class = NewsForm
    template_name = 'news/articles_edit.html'
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_article = 'AR'
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    # login_url = "/login/"
    redirect_field_name = "redirect_to"
    form_class = NewsForm
    template_name = 'news/news_edit.html'
    model = Post


class ArticlesUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    # login_url = "/login/"
    redirect_field_name = "redirect_to"
    form_class = NewsForm
    template_name = 'news/articles_edit.html'
    model = Post


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news')


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'news/articles_delete.html'
    success_url = reverse_lazy('news')
