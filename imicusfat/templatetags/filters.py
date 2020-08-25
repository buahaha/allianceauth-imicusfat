from django.template.defaulttags import register
import calendar


@register.filter
def month(value):
    value = int(value)
    return calendar.month_name[value]
