# -*- coding: utf-8 -*-

"""
our app setting
"""

import re

from django.conf import settings

from imicusfat.utils import clean_setting


# set default panels if none are set in local.py
IMICUSFAT_DEFAULT_FATLINK_EXPIRY_TIME = clean_setting(
    "IMICUSFAT_DEFAULT_FATLINK_EXPIRY_TIME", 60
)


def get_site_url():  # regex sso url
    """
    get the site url
    :return: string
    """

    regex = r"^(.+)\/s.+"
    matches = re.finditer(regex, settings.ESI_SSO_CALLBACK_URL, re.MULTILINE)
    url = "http://"

    for match in matches:
        url = match.groups()[0]  # first match

    return url
