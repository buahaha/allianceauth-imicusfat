# -*- coding: utf-8 -*-

"""
app config
"""

from django.utils.text import slugify

default_app_config: str = "imicusfat.apps.ImicusfatConfig"

__title__ = "ImicusFAT"
__version__ = "1.3.1"
__verbose_name__ = "ImicusFAT Fleet Activity Tracking for Alliance Auth"
__user_agent__ = "{verbose_name} v{version} {github_url}".format(
    verbose_name=slugify(__verbose_name__, allow_unicode=True),
    version=__version__,
    github_url="https://gitlab.com/evictus.iou/allianceauth-imicusfat",
)
