# -*- coding: utf-8 -*-
from django.apps import AppConfig

from . import __version__


class ImicusfatConfig(AppConfig):
    name = "imicusfat"
    label = "imicusfat"
    verbose_name = f"ImicusFAT v{__version__}"
