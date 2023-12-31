"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import index  # Выбрана рабочая папка NewsPaper в меню папки: "Mark Directory as"
from news.views import page_not_found, user_not_authenticated
from accounts.views import IndexView

# Для кэширования
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('', cache_page(60)(index), name="home"),  # Добавлено кэширование главной страницы, 1 мин
    path('protect/', IndexView.as_view(), name="login_redirect_url"),
    path('accounts/', include('accounts.urls')),
    path('account/', include('allauth.urls')),  # это при помощи pip install django-allauth
    # path('', Index.as_view(), name="home"),
]

handler404 = page_not_found  # Теперь при ошибке 404 будет наша запись, а не стандартная, есть handler для др. ошибок
handler403 = user_not_authenticated
