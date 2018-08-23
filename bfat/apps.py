from django.apps import AppConfig
from django.template.defaulttags import register


class BfatConfig(AppConfig):
    name = 'bfat'


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
