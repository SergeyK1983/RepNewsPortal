from datetime import datetime
from django import template
from django.conf import settings

register = template.Library()
base_url = settings.ROOT_URLCONF


@register.simple_tag
def add_domain(partial_url):  # Херня какая-то, должна была url для ссылок в письмах готовить, вышел бред
    return base_url + partial_url


@register.simple_tag()
def current_time(format_string='%b %d %Y'):
    return datetime.utcnow().strftime(format_string)


# Вот как мы можем поступить — сделать тег, который будет брать текущие параметры запроса и
# по указанному аргументу производить замену, не очищая остальные параметры.
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
