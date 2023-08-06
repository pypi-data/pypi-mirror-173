"""."""

# Note that no third party dependency imports are allowed in this module as it will break setup.py in the project root. If it is
# absolutely necessary, change setup.py to use exec() method of loading constants inside __version__.py, thus allowing any imports
# in this module.

# Refer to PyPA documentation for details on imports:
# https://packaging.python.org/guides/single-sourcing-package-version
from powershell.__version__ import (
    __project_name__,
    __package_name__,
    __description__,
    __version__,
    __docs_url__,
    __source_url__,
    __home_url__,
    __author__,
    __author_email__,
    __copyright__,
    __license__
)

__all__ = [
    '__project_name__',
    '__package_name__',
    '__description__',
    '__version__',
    '__docs_url__',
    '__source_url__',
    '__home_url__',
    '__author__',
    '__author_email__',
    '__copyright__',
    '__license__'
]
