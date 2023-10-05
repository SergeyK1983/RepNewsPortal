from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

# для регистрации пользователей, это если делать с помощью встроенных инструментов django
# class BaseRegisterView(CreateView):
#     model = User  # модель формы, которую реализует данный дженерик
#     form_class = BaseRegisterForm  # форма, которая будет заполняться пользователем
#     success_url = '/'  # URL, на который нужно направить пользователя после успешного ввода данных в форму


# Для перехода на страницу зарегистрированного пользователя
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):  # переопределили метод получения контекста
        context = super().get_context_data(**kwargs)  # Сначала мы получили весь контекст из класса-родителя
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()  # после чего добавили новую контекстную переменную is_not_authors
        return context
# Чтобы ответить на вопрос, есть ли пользователь в группе, мы заходим в переменную запроса self.request.
# Из этой переменной мы можем вытащить текущего пользователя. В поле groups хранятся все группы, в которых он состоит.
# Далее мы применяем фильтр к этим группам и ищем ту самую, имя которой authors. После чего проверяем, есть ли
# какие-то значения в отфильтрованном списке. Метод exists() вернёт True, если группа premium в списке групп
# пользователя найдена, иначе — False. А нам нужно получить наоборот — True, если пользователь не находится в этой
# группе, поэтому добавляем отрицание not, и возвращаем контекст обратно.


# Апгрейд до аккаунта "Стать автором"
@login_required
def upgrade_me(request):
    user = request.user  # получили объект текущего пользователя из переменной запроса
    authors_group = Group.objects.get(name='authors')  # Вытащили authors-группу из модели Group
    if not request.user.groups.filter(name='authors').exists():  # Дальше мы проверяем, находится ли пользователь в этой группе
        authors_group.user_set.add(user)  # если нет, то добавляем
    return redirect('/')  # на главную
