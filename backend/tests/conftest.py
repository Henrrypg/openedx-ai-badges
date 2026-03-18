"""
Test configuration and shared fixtures.

Stubs out optional heavy dependencies (openedx_ai_extensions) so that
processor tests can run in environments where the full platform is not
installed.
"""
import sys
from types import ModuleType
from unittest.mock import MagicMock


def _stub_openedx_ai_extensions():
    """Register a minimal stub for openedx_ai_extensions if not installed."""
    if "openedx_ai_extensions" in sys.modules:
        return

    stub = ModuleType("openedx_ai_extensions")
    stub.processors = ModuleType("openedx_ai_extensions.processors")
    stub.processors.LLMProcessor = MagicMock()
    sys.modules["openedx_ai_extensions"] = stub
    sys.modules["openedx_ai_extensions.processors"] = stub.processors


_stub_openedx_ai_extensions()
