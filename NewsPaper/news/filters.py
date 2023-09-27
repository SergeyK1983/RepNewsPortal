import django_filters
from django.forms import DateTimeInput, DateInput
from django_filters import FilterSet, ModelChoiceFilter, DateFromToRangeFilter, DateFilter
from django_filters.widgets import RangeWidget

from .models import Post, Author


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class NewsFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='user_id',  # 'user_id__user_id__id',
        queryset=Author.objects.select_related('user'),
        label='Автор:',
        empty_label='ничего'
    )
    title = django_filters.CharFilter(label='Заголовок', field_name='title', lookup_expr='icontains')
    # date_create = django_filters.DateTimeFilter(field_name='date_create', widget=DateTimeInput)
    # date_range = DateFromToRangeFilter(field_name='date_create', lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))  # RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))
    # Решение в Пачке подсмотрел, сам мы не допер.
    date_range = DateFilter(
        field_name='date_create',
        label='Не старше чем:',
        lookup_expr='gt',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи
        model = Post
        fields = []  # 'title', 'date_create'
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        # fields = {
        #     # поиск по названию
        #     # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups
        #     'title': ['icontains'],  # соответствует SELECT ... WHERE headline ILIKE '%Lennon%'; (регистр-независимый)
        #     # Имя автора
        #     'user': ['exact'],
        #     'date_create': [
        #         'gt',  # время создания должна быть больше или равна указанной
        #     ],
        # }


