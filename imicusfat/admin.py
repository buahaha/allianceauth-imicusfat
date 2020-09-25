# -*- coding: utf-8 -*-

"""
admin pages configuration
"""

from django.contrib import admin

from .models import IFat, IFatLink, IFatLinkType


# Register your models here.
@admin.register(IFatLink)
class IFatLinkAdmin(admin.ModelAdmin):
    """
    config for fat link model
    """

    list_display = (
        "ifattime",
        "creator",
        "fleet",
        "link_type",
        "is_esilink",
        "hash",
        "deleted_at",
    )
    ordering = ("-ifattime",)


@admin.register(IFat)
class IFatAdmin(admin.ModelAdmin):
    """
    config for fat model
    """

    list_display = ("character", "system", "shiptype", "ifatlink", "deleted_at")
    ordering = ("-character",)


@admin.register(IFatLinkType)
class IFatLinkTypeAdmin(admin.ModelAdmin):
    """
    config for fatlinktype model
    """

    list_display = ("id", "name")
    ordering = ("name",)
