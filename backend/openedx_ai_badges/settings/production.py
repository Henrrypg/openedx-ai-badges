"""
Production settings for the openedx_ai_extensions application.
"""

from openedx_ai_badges.settings.common import plugin_settings as common_settings


def plugin_settings(settings):
    """
    Set up production-specific settings.

    Args:
        settings (dict): Django settings object
    """
    # Apply common settings
    common_settings(settings)

    # -------------------------
    # MIT DCC Badge API
    # -------------------------
    if hasattr(settings, "ENV_TOKENS"):
        settings.MIT_DCC_BADGE_API_URL = settings.ENV_TOKENS.get(
            "MIT_DCC_BADGE_API_URL", settings.MIT_DCC_BADGE_API_URL
        )
