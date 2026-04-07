"""
Contentstore module generalized definitions.
"""

from functools import lru_cache
from importlib import import_module

from django.conf import settings


@lru_cache(maxsize=1)
def _get_backend():
    """Return the configured contentstore backend module."""
    return import_module(settings.OPENEDX_AI_BADGES_CONTENTSTORE_BACKEND)


def get_static_content():
    """
    Wrapper for `xmodule.contentstore.content.StaticContent` in edx-platform.
    """
    return _get_backend().StaticContent


def update_course_run_asset(*args, **kwargs):
    """
    Wrapper for `cms.djangoapps.contentstore.views.assets.update_course_run_asset`.
    """
    return _get_backend().update_course_run_asset(*args, **kwargs)
