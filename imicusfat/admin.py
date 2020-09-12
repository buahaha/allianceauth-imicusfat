# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import IFat, IFatLink, IFatLinkType


# Register your models here.
@admin.register(IFatLink)
class IFatLinkAdmin(admin.ModelAdmin):
    list_display = ("ifattime", "creator", "fleet", "link_type", "hash", "deleted_at")
    ordering = ("-ifattime",)


@admin.register(IFat)
class IFatAdmin(admin.ModelAdmin):
    list_display = ("character", "system", "shiptype", "ifatlink", "deleted_at")
    ordering = ("-character",)


@admin.register(IFatLinkType)
class IFatLinkTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    ordering = ("name",)
