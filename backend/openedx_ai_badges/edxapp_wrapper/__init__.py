"""
Wrappers for Open edX platform (edx-platform) functions.

These wrappers delegate to a configurable backend module so that cms.djangoapps
and xmodule are never imported at module load time, keeping CI and test
environments functional without a full edx-platform install.
"""
