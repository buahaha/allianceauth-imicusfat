# -*- coding: utf-8 -*-

"""
app config
"""

default_app_config: str = "imicusfat.apps.ImicusfatConfig"

__title__ = "ImicusFAT"
__version__ = "1.4.0"
__verbose_name__ = "ImicusFAT Fleet Activity Tracking for Alliance Auth"
__user_agent__name__ = "ImicusFAT-Fleet-Activity-Tracking-for-Alliance-Auth"
__user_agent__ = "{verbose_name} v{version} {github_url}".format(
    verbose_name=__user_agent__name__,
    version=__version__,
    github_url="https://gitlab.com/evictus.iou/allianceauth-imicusfat",
)
