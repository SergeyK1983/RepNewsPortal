from django import template

register = template.Library()


@register.filter()
def censor(value):
    pass
