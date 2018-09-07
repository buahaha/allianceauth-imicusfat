from django.template.defaulttags import register
from datetime import datetime

@register.filter
def month(value):
    value = int(value)
    return datetime.date(month=value).strftime("%B")
