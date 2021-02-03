# -*- coding: utf-8 -*-

"""
providers
"""

from esi.clients import EsiClientProvider

from imicusfat import __title__
from imicusfat.constants import USER_AGENT
from imicusfat.utils import LoggerAddTag, get_swagger_spec_path

from allianceauth.services.hooks import get_extension_logger


logger = LoggerAddTag(get_extension_logger(__name__), __title__)

esi = EsiClientProvider(spec_file=get_swagger_spec_path(), app_info_text=USER_AGENT)
