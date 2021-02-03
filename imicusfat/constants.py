# coding=utf-8

"""
constants used in this module
"""

from django.utils.text import slugify

from imicusfat import __version__

VERBOSE_NAME = "ImicusFAT Fleet Activity Tracking for Alliance Auth"
USER_AGENT = "{verbose_name} v{version} {github_url}".format(
    verbose_name=slugify(VERBOSE_NAME, allow_unicode=True),
    version=__version__,
    github_url="https://gitlab.com/evictus.iou/allianceauth-imicusfat",
)
