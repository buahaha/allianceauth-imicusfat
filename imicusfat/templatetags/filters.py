# coding=utf-8

import calendar

from django.template.defaulttags import register


@register.filter
def month(value):
    value = int(value)
    return calendar.month_name[value]
