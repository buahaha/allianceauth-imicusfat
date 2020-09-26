# -*- coding: utf-8 -*-

"""
admin pages configuration
"""

from django.contrib import admin

from .models import IFat, IFatLink, IFatLinkType


def custom_filter_title(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title

            return instance

    return Wrapper


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
        "_link_type",
        "is_esilink",
        "hash",
        "deleted_at",
    )

    list_filter = (
        "is_esilink",
        ("link_type__name", custom_filter_title("fleet type")),
    )

    ordering = ("-ifattime",)

    def _link_type(self, obj):
        if obj.link_type:
            return obj.link_type.name
        else:
            return "-"

    _link_type.short_description = "Fleet Type"
    _link_type.admin_order_field = "link_type__name"


@admin.register(IFat)
class IFatAdmin(admin.ModelAdmin):
    """
    config for fat model
    """

    list_display = ("character", "system", "shiptype", "ifatlink", "deleted_at")

    list_filter = ("character", "system", "shiptype")

    ordering = ("-character",)


@admin.register(IFatLinkType)
class IFatLinkTypeAdmin(admin.ModelAdmin):
    """
    config for fatlinktype model
    """

    list_display = ("id", "name")
    ordering = ("name",)
