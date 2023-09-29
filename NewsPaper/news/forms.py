from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class NewsForm(forms.ModelForm):
    # user = forms.CharField(min_length=1)
    # category = forms.CharField(min_length=1)
    # title = forms.CharField(min_length=1)
    # article = forms.CharField(min_length=1)

    class Meta:
        model = Post
        fields = [
            'user',
            'category',
            'title',
            'article'
        ]

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        if user is None:  # проверка
            raise ValidationError({
                "user": "Должен быть хотя бы один символ"
            })

        category = cleaned_data.get("category")
        if category is None:
            raise ValidationError({
                "category": "Должен быть хотя бы один символ"
            })

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
