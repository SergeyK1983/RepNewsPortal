from datetime import datetime

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseNotFound
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Post, Subscription, Category, Author
from .filters import NewsFilter
from .forms import NewsForm, CategoryForm
import os
from pathlib import Path
from NewsPaper.settings import LOGIN_URL
from .tasks import hello, printer


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1 align="center"> Ошибка 404 <br> Страница не найдена </h1>')


def user_not_authenticated(request, exception):
    return HttpResponseNotFound('<h1 align="center"> Ошибка 403 <br> Пользователь не авторизирован </h1>')


class ProbaCelery(View):
    def get(self, request):
        printer.delay(10)
        hello.delay()
        return HttpResponse('Hello')


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


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = LOGIN_URL
    permission_required = ('news.add_post', )  # где news - это имя приложения(app), add - это действие(action), а post - это название модели(modelname)

    form_class = NewsForm
    template_name = 'news/news_edit.html'
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_article = 'NW'

        title = post.title  # request.POST['title']
        article = post.article  # self.request.POST['article']
        # category = post.category
        # print(category)
        users = Subscription.objects.filter().values('user__id')
        users_for_email = set([i.get('user__id') for i in users])  # Перечень подписчиков
        # mail = [User.objects.filter(id=i).values('email') for i in a]

        # Рассылка подписчикам при создании новости
        if users_for_email:
            for i in users_for_email:
                u_mail = User.objects.filter(id=i).values('email')
                user_mail = User.objects.filter(id=i).values('username')[0].get('username')
                mail = [u_mail[0].get('email')]

                html_content = render_to_string(
                    template_name='news/post_created_mail.html',
                    context={
                        'title': title,
                        'article': article,
                        'user': user_mail,
                    }
                )

                send_mail(
                    subject='Новостной портал',
                    message='Вы подписаны на рассылку новостей по категории: ',
                    from_email='ssp-serg@yandex.ru',
                    recipient_list=mail,  # ['ksm.serg1983@gmail.com', ],
                    html_message=html_content,
                )

        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
        # msg = EmailMultiAlternatives(
        #     subject='Новостной портал',
        #     body='Вот новая публикация, читай не обляпайся!',
        #     from_email='ssp-serg@yandex.ru',
        #     to=['ksm.serg1983@gmail.com', ]
        # )
        # msg.attach_alternative(html_content, mimetype="text/html")  # добавляем html
        # msg.send()  # отсылаем
        # return redirect('news_create')


class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = LOGIN_URL
    permission_required = ('news.add_post',)

    form_class = NewsForm
    template_name = 'news/articles_edit.html'
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_article = 'AR'
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    raise_exception = False  # если сделать True, то можно использовать user_not_authenticated (написана на верху)
    login_url = LOGIN_URL  # "/accounts/login/"
    redirect_field_name = "redirect_to"

    permission_required = ('news.change_post',)  # Разрешение на редактирование группе которой позволено, https://gadjimuradov.ru/post/django-permissions-upravlenie-pravami-dostupa/

    form_class = NewsForm
    template_name = 'news/news_edit.html'
    model = Post


class ArticlesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    raise_exception = False
    login_url = LOGIN_URL
    redirect_field_name = "redirect_to"

    permission_required = ('news.change_post',)

    form_class = NewsForm
    template_name = 'news/articles_edit.html'
    model = Post


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    raise_exception = False
    login_url = LOGIN_URL

    permission_required = ('news.delete_post',)

    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news')


class ArticlesDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    raise_exception = False
    login_url = LOGIN_URL

    permission_required = ('news.delete_post',)

    model = Post
    template_name = 'news/articles_delete.html'
    success_url = reverse_lazy('news')


# Отправка письма пользователю при подписке на категорию новостей/статей
@login_required
def check_category(request):
    def s_mail(user_m, category: list):

        send_mail(
                subject='Новостной портал',
                message=f'Вы подписаны на рассылку новостей по категории: {", ".join(category)}',
                from_email='ssp-serg@yandex.ru',
                recipient_list=[user_m.email, ]  # ['ksm.serg1983@gmail.com', ]
            )

    form = CategoryForm()
    user = User.objects.get(username=request.user)
    cat_list = dict(request.POST)
    title_l = []
    cat_d = []
    if cat_list:
        sub = list(Subscription.objects.filter(user=user.id).values('subscribers'))
        cat = list(Category.objects.all().values('id', 'title'))

        for i in cat_list['title']:
            for j in cat:
                if int(i) == j['id']:
                    title_l.append(j['title'])  # Отмеченные категории для подписки

        if sub:
            for i in title_l:  # Раз нет, то надо записать, если нет
                if not Subscription.objects.filter(subscribers=i, user=user).exists():  # Записываем, если отсутствует
                    subscribers = Category.objects.get(title=i)
                    subscr = Subscription(user=user, subscribers=subscribers)
                    subscr.save()
                    c = Category.objects.get(title=i)
                    cat_d.append(c.get_title_display())
            if cat_d:
                s_mail(user, cat_d)
        else:  # пользователь ни на что не подписан, точно записываем
            for i in title_l:
                subscribers = Category.objects.get(title=i)
                subscr = Subscription(user=user, subscribers=subscribers)
                subscr.save()
                c = Category.objects.get(title=i)
                cat_d.append(c.get_title_display())
            if cat_d:
                s_mail(user, cat_d)

    title_l.clear()
    context = {'form': form, 'user': user}
    return render(request, template_name='news/category_subscr.html', context=context)

# class CheckCategory(LoginRequiredMixin, ListView):  Что-то не получилось!!!
#     login_url = LOGIN_URL
#
#     model = Category
#     template_name = 'news/category_subscr.html'
#     context_object_name = 'check_category'
#
#     form_class = CategoryForm

