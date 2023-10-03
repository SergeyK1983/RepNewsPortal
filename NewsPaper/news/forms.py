from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category


class NewsForm(forms.ModelForm):
    # user = forms.ChoiceField(label='Автор', choices='user')
    # category = forms.ChoiceField(label='Категория', choices=Category.CATEGORY)
    # title = forms.C(label='Заголовок')
    # article = forms.Textarea(label='Содержание')

    class Meta:
        model = Post
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-text', 'cols': 150, 'rows': 3}),
            'article': forms.Textarea(attrs={'class': 'form-text', 'cols': 150, 'rows': 10}),
        }
        fields = [
            'user',
            'category',
            'title',
            'article'
        ]

    # хз зачем, в модели эти поля определены, как не могут быть пустыми по умолчанию
    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        if user is None:  # проверка
            raise ValidationError({
                "user": "Должен быть хотя бы один символ"
            })

        # category = cleaned_data.get("category")
        # if category is None:
        #     raise ValidationError({
        #         "category": "Должен быть хотя бы один символ"
        #     })

        title = cleaned_data.get("title")
        if title is None:
            raise ValidationError({
                "title": "Должен быть хотя бы один символ"
            })

        article = cleaned_data.get("article")
        if article is None:
            raise ValidationError({
                "article": "Должен быть хотя бы один символ"
            })
