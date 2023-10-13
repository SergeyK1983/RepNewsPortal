from django.contrib import admin
from .models import Post, Category, Author, PostCategory, Comment, Subscription


# Вспомогательный класс для админ панели
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type_article', 'title', 'date_create', 'rating')
    list_display_links = ('id',)
    search_fields = ('title',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating')
    list_display_links = ('id', 'user')
    search_fields = ('rating',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id',)


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'category')
    list_display_links = ('id', 'post')
    search_fields = ('post', 'category')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'com_text', 'date_create', 'rating')
    list_display_links = ('id', 'post', 'user')
    search_fields = ('post', 'user', 'com_text')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subscribers')
    list_display_links = ('id', 'user', 'subscribers')
    search_fields = ('user', 'subscribers')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
