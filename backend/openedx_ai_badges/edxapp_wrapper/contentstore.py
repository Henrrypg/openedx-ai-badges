"""
Contentstore module generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def get_static_content():
    """
    Wrapper for `xmodule.contentstore.content.StaticContent` in edx-platform.
    """
    backend = import_module(settings.OPENEDX_AI_BADGES_CONTENTSTORE_BACKEND)
    return backend.StaticContent


def update_course_run_asset(*args, **kwargs):
    """
    Wrapper for `cms.djangoapps.contentstore.views.assets.update_course_run_asset`.
    """
    backend = import_module(settings.OPENEDX_AI_BADGES_CONTENTSTORE_BACKEND)
    return backend.update_course_run_asset(*args, **kwargs)
