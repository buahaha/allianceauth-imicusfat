# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import IFat, IFatLink, IFatLinkType


# Register your models here.
admin.site.register(IFatLink)
admin.site.register(IFat)
admin.site.register(IFatLinkType)
