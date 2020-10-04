# -*- coding: utf-8 -*-

"""
app config
"""

from django.apps import AppConfig

from imicusfat import __version__


class ImicusfatConfig(AppConfig):
    """
    general config
    """

    name = "imicusfat"
    label = "imicusfat"
    verbose_name = f"ImicusFAT v{__version__}"
