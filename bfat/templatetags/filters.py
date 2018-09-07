from django.template.defaulttags import register
import datetime.datetime


@register.filter
def month(value):
    value = int(value)
    return datetime.date(month=value).strftime("%B")
