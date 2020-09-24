# -*- coding: utf-8 -*-

"""
utilities
"""

import logging
import os

from django.utils.functional import lazy
from django.utils.html import format_html


# Format for output of datetime for this app
DATETIME_FORMAT = "%Y-%m-%d %H:%M"

format_html_lazy = lazy(format_html, str)


class LoggerAddTag(logging.LoggerAdapter):
    """
    add custom tag to a logger
    """

    def __init__(self, my_logger, prefix):
        super(LoggerAddTag, self).__init__(my_logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        """
        process log items
        :param msg:
        :param kwargs:
        :return:
        """

        return "[%s] %s" % (self.prefix, msg), kwargs


logger = LoggerAddTag(logging.getLogger(__name__), __package__)


def get_swagger_spec_path() -> str:
    """
    returns the path to the current swagger spec file
    """

    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "swagger.json")


def make_logger_prefix(tag: str):
    """
    creates a function to add logger prefix, which returns tag when used empty
    """

    return lambda text="": "{}{}".format(tag, (": " + text) if text else "")
